import re
import time
import paramiko
import pandas as pd
from szdata.utils.xyutil import fn_timer

import host_config as config

from influxdb import InfluxDBClient

client = InfluxDBClient(host='10.0.4.35', port=8086, username='', password='', database='cluster_monitor')


def kudu_status_handle(sshRes=[]):
    status = 'unknown'
    for msg in sshRes:
        if 'running[  OK  ]' in msg:
            status = 'health'
        if 'running[FAILED]' in msg:
            status = 'bad'
    return status


def presto_status_handle(sshRes=[]):
    status = 'unknown'
    for msg in sshRes:
        if 'Running as' in msg:
            status = 'health'
        if 'Not running' in msg:
            status = 'bad'
    return status

def kafka_status_handle(self, sshRes=[]):
    print(sshRes)
    status = 'bad'
    for msg in sshRes:
        if 'Kafka' in msg:
            status = 'health'
    return status

class MonitorServer:
    '''
    创建 ssh 连接函数
    hostname, port, username, password,访问linux的ip，端口，用户名以及密码
    '''
    def sshConnect(self, host):
        # print('host:{}'.form
        paramiko.util.log_to_file('paramiko_log')
        try:
            private_key = paramiko.RSAKey.from_private_key_file('/home/xyhadoop/monitor/collect_data/test')

            # 创建SSH对象
            sshClient = paramiko.SSHClient()

            # 允许连接不在know_hosts文件中的主机
            sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接服务器
            ret = sshClient.connect(hostname=host, port=36000, username='user_00', pkey=private_key, timeout=1)
        except:
            # print("SSH链接失败：[host:%s]" %(host))
            return None

        return sshClient

    def sshConnect2(self, host,username,private_key_path):
        # print('host:{}'.format(host))
        paramiko.util.log_to_file('paramiko_log')
        try:
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

            # 创建SSH对象
            sshClient = paramiko.SSHClient()

            # 允许连接不在know_hosts文件中的主机
            sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接服务器
            ret = sshClient.connect(hostname=host, port=36000, username=username, pkey=private_key, timeout=1)
        except:
            # print("SSH链接失败：[host:%s]" %(host))
            return None

        return sshClient

    '''
    创建命令执行函数
    command 传入linux运行指令
    '''
    def sshExecCmd(self,sshClient,command):

        stdin, stdout, stderr = sshClient.exec_command(command)
        filesystem_usage = stdout.readlines()
        return filesystem_usage
    '''
    关闭ssh
    '''
    def sshClose(self,sshClient):
        sshClient.close()

    def swap_rate(self, row):
        if int(row['SwapTotal']) == 0:
            return '0.00%'
        rate = 100 - 100 * int(row['SwapFree']) / float(row['SwapTotal'])
        rate = str("%.2f" % rate) + "%"
        return rate

    def mem_rate(self, row):
        free = int(row['MemFree']) + int(row['Buffers']) + int(row['Cached'])
        used = int(row['MemTotal']) - free
        rate = 100 * used / float(row['MemTotal'])
        rate = str("%.2f" % rate) + "%"
        return rate

    '''内存监控'''
    @fn_timer
    def cpu_info(self, hostList):
        try:
            dfList = []
            command = 'top -b -n1'
            columns = ['us', 'sy', 'ni', 'id', 'wa', 'hi', 'si', 'st']
            for host in hostList:#遍历所有服务器并去监控内存
                sshClient = self.sshConnect(host=host)
                if sshClient == None:
                    print("{} connect fail，获取cpu信息失败".format(host))
                    continue
                sshRes = self.sshExecCmd(sshClient, command)
                for line in sshRes:
                    if 'Cpu(s)' in line:
                        line = line.strip() + ','
                        # print(line)
                        keys = re.findall(r' (\w+),', line)
                        values = re.findall(r'(\d+.\d+) ', line)
                        values = [value + '%' for value in values]
                        df = pd.DataFrame([dict(zip(keys, values))])
                        df['Host'] = host
                        dfList.append(df)
                        break
                self.sshClose(sshClient)

            result = pd.concat(dfList)
            result['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            result.to_sql(name="cpuinfo", con=config.db_conn, if_exists='append', index=False)

            # 插入到influxdb
            for index,row in result.iterrows():
                insert_values = []
                insert_value = {'measurement': 'cpuinfo'}

                tags = {'host': row['Host']}
                insert_value['tags'] = tags

                fields = {}
                fields['us'] = row['us']
                fields['sy'] = row['sy']
                fields['ni'] = row['ni']
                fields['id'] = row['id']
                fields['wa'] = row['wa']
                fields['hi'] = row['hi']
                fields['si'] = row['si']
                fields['st'] = row['st']
                fields['create_time'] = row['create_time']
                insert_value['fields'] = fields
                insert_values.append(insert_value)
                ret = client.write_points(insert_values)
        except Exception as e:
            print(e)

    '''内存监控'''
    @fn_timer
    def mem_info(self, hostList):
        try:
            dfList = []
            command = 'cat /proc/meminfo'
            columns = ['MemTotal', 'MemFree', 'Buffers', 'Cached', 'SwapCached', 'SwapFree', 'SwapTotal']
            for host in hostList:#遍历所有服务器并去监控内存
                sshClient = self.sshConnect(host=host)
                if sshClient == None:
                    print("{} connect fail，获取内存失败".format(host))
                    continue
                sshRes = self.sshExecCmd(sshClient,command)
                sshRes = ','.join(sshRes)
                mem_keys = re.findall(r'(\w+\(*\w+\)*):', sshRes)
                mem_values = re.findall("(\d+)\ kB", sshRes)

                mem_dict = dict(zip(mem_keys, mem_values))
                # print(mem_dict)
                for key in list(mem_dict.keys()):
                    if key not in columns:
                        del mem_dict[key]

                df = pd.DataFrame([mem_dict])

                df['SwapRate'] = df.apply(self.swap_rate, axis=1)
                df['MemRate'] = df.apply(self.mem_rate, axis=1)
                df["Host"] = host
                dfList.append(df)
                self.sshClose(sshClient)

            result = pd.concat(dfList)
            result['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # print(result)
            result.to_sql(name="meminfo", con=config.db_conn, if_exists='append', index=False)

            # 插入到influxdb
            for index, row in result.iterrows():
                insert_values = []
                insert_value = {'measurement': 'meminfo'}

                tags = {'host': row['Host']}
                insert_value['tags'] = tags

                fields = {}
                fields['MemTotal'] = int(row['MemTotal'])
                fields['MemFree'] = int(row['MemFree'])
                fields['Buffers'] = int(row['Buffers'])
                fields['Cached'] = int(row['Cached'])
                fields['SwapCached'] = int(row['SwapCached'])
                fields['SwapFree'] = int(row['SwapFree'])
                fields['SwapTotal'] = int(row['SwapTotal'])
                fields['create_time'] = row['create_time']
                insert_value['fields'] = fields
                insert_values.append(insert_value)
                ret = client.write_points(insert_values)
        except Exception as e:
            print(e)



    """ 
    磁盘空间监控
    """
    @fn_timer
    def disk_stat(self, hostList):
        try:
            command = 'df -h'
            columns = ['Filesystem', 'Size', 'Used', 'Avail', 'UseRate', 'MountedOn']
            dfList = []
            for host in hostList:
                # print(host)
                sshClient = self.sshConnect(host=host)
                if sshClient == None:
                    print("{} connect fail， 获取磁盘信息失败".format(host))
                    continue

                # print("{} connect succ".format(host))
                sshRes = self.sshExecCmd(sshClient, command)
                hostDisk  = []
                for i in range(len(sshRes)):
                    temp = re.sub(' +', ',', sshRes[i])
                    temp = temp.replace('\n', '')
                    temp = temp.split(',')
                    # print(temp)
                    if temp[0] == 'Filesystem':
                        continue

                    hostDisk.append(temp)
                df = pd.DataFrame([dict(zip(columns, value)) for value in hostDisk])
                df['Host'] = host
                dfList.append(df)
                self.sshClose(sshClient)
            result = pd.concat(dfList)
            timestamp = time.time()
            result['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))
            result.to_sql(name="diskinfo", con=config.db_conn, if_exists='append', index=False)

            # 插入到influxdb
            for index, row in result.iterrows():
                insert_values = []
                insert_value = {'measurement': 'diskinfo'}

                tags = {'host': row['Host']}
                insert_value['tags'] = tags

                fields = {}
                fields['Filesystem'] = row['Filesystem']
                fields['Size'] = row['Size']
                fields['Used'] = row['Used']
                fields['Avail'] = row['Avail']
                fields['UseRate'] = row['UseRate']
                fields['MountedOn'] = row['MountedOn']
                fields['create_time'] = int(timestamp)
                insert_value['fields'] = fields
                insert_values.append(insert_value)
                ret = client.write_points(insert_values)
        except Exception as e:
            print(e)

    """ 
    端口监控

    """
    def get_Com_Str(self, hostList):
        command = 'netstat -tpln'
        for host in hostList:
            sshClient = self.sshConnect(host)
            sshRes = self.sshExecCmd(sshClient, command)
            sshResStr = ''.join(sshRes)
            sshResList = sshResStr.strip().split('\n')
            sshResLists = []
            for sshCom in sshResList[2:]:
                sshResLists.append(sshCom.strip().split())
            print('******************************端口监控，对应主机[name:%s]*********************************'%host)

            print("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
            for temp in sshResLists:
                print("\t Proto:",temp[0])
                print("\t Recv-Q:", temp[1])
                print("\t Send-Q:", temp[2])
                print("\t Local Address:", temp[3])
                print("\t  Foreign Address:", temp[4])
                print("\t State:", temp[5])
                print("\t PID/Program name:", temp[6])
                print("****************************************")
        self.sshClose(sshClient)


    """
    各组件监控
    """
    @fn_timer
    def component_stat(self,component_type):
        sql = """SELECT
        a.id AS instance_id,
        b.*,
        c.ip,
        c.username,
        c.private_key,
        d.name as component_name
         FROM
        xy_ops.`instance` a
        JOIN xy_ops.`service` b ON a.service_id = b.id
        JOIN xy_ops.`host` c ON a.host_id = c.id
        JOIN xy_ops.`component` d ON b.component_id = d.id
        where d.type = '{}'""".format(component_type)
        df = pd.read_sql(sql, config.ops_db_conn)
        for index, row in df.iterrows():
            try:
                host = row['ip']
                component_name = row['component_name']
                instance_id = row['instance_id']
                status_script = row['status_script']
                username = row['username']
                service= row['name']
                private_key_path = row['private_key']
                sshClient = self.sshConnect2(host,username,private_key_path)
                status_script = "bash --login -c '{}'".format(status_script)
                print(status_script)
                sshRes = self.sshExecCmd(sshClient, status_script)
                if sshClient == None:
                    print("{} connect fail，组件状态失败".format(host))
                    continue
                insert_values = []
                if component_type == 'kudu':
                    insert_value = {'measurement': 'kuduinfo'}
                    status = kudu_status_handle(self,sshRes)

                if component_type == 'presto':
                    insert_value = {'measurement': 'prestoinfo'}
                    status = presto_status_handle(self,sshRes)

                if component_type == 'kafka':
                    print(sshRes)
                    insert_value = {'measurement': 'kafkainfo'}
                    status = kafka_status_handle(self,sshRes)

                tags = {'host': host, 'component_name': component_name}
                insert_value['tags'] = tags
                fields = {}
                fields['service'] = service
                fields['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                fields['status'] = status
                insert_value['fields'] = fields

                insert_values.append(insert_value)
                ret = client.write_points(insert_values)
                self.sshClose(sshClient)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    obj = MonitorServer()
    obj.sshConnect('xybase04')