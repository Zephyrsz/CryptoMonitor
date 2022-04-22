#base
import platform
import logging
import pandas as pd
import datetime as dt
import json
import os

#flask
from flask import Flask
from flask import request

#kafka
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient
from kafka.structs import TopicPartition,OffsetAndMetadata

from db_conn import DatabaseConnect

app = Flask(__name__)
from logging.handlers import TimedRotatingFileHandler

# 代表kafka offset 需要回退的时间 单位为分钟

global logger
def get_logger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = TimedRotatingFileHandler(filename, when="midnight", interval=1, backupCount=3650)
        handler.suffix = "%Y-%m-%d"  # or anything else that strftime("%Y-%m-%d") will allow
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(process)d %(filename)s:%(lineno)d %(message)s',
                                      datefmt='[%Y-%m-%d %H:%M:%S]')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
mysql_read = {
    "drivername": "mysql+pymysql",
    "host": "data_analysis_m.db.xiaoying.io",
    "port": 3306,
    "database": "monitor",
    "username": "data",
    "password": "xL8sG4NtiJZKRU",
    "query": {"charset": "utf8"}
}
# mysql_read = {
#     "drivername": "mysql+pymysql",
#     "host": "127.0.0.1",
#     "port": 3306,
#     "database": "monitor",
#     "username": "root",
#     "password": "root",
#     "query": {"charset": "utf8"}
# }
conn = DatabaseConnect(mysql_read).get_conn()

@app.route('/pieline_rollback_base_kafka',methods=['POST'])
def pieline_rollback_base_kafka():
    params = json.loads(request.get_data())
    delta = params.get('delta') if  params.get('delta') != None else 60  # 选填，默认回退到前一小时
    batch_num = params.get('batch_num')  if  params.get('batch_num') != None else 1000  # 选填，默认回退batch_num=1000
    pipline_id = params.get('pipline_id') #必填
    pipline_status = params.get('pipline_status') #必填
    topic = params.get('topic')  #必填
    consumer = params.get('consumer') #必填
    mode = params.get('mode') if  params.get('mode') in ("time","batch") else "time" #选填，默认为 time 模式 , mode = time（根据回退时间回退）、mode = batch（根据回退记录条数进行回退）


    # 判断输入参数的正确性
    if pipline_id and isinstance(pipline_id, str) == True :
        logger.info('<pipline_id>:%s',pipline_id)
    else:
        return {"code":-1,"msg":"<pipline_id> can't be empty and must be string"}
    if pipline_status and isinstance(pipline_status, str) == True:
        logger.info('<pipline_status>:%s', pipline_status)
    else:
        return {"code": -1, "msg": "<pipline_status> can't be empty and must be string"}
    if topic and isinstance(topic, str) == True :
        logger.info('<topic>:%s', topic)
    else:
        return {"code": -1, "msg": "<topic> can't be empty  and must be string"}
    if consumer and isinstance(topic, str) == True :
        logger.info('<consumer>:%s', topic)
    else:
        return {"code": -1, "msg": "<consumer> can't be empty and must be string"}
    if delta and isinstance(delta,int)==False:
        return {"code": -1, "msg": "<delta> must be int"}
    else:
        logger.info('<delta>:%s', delta)
    if batch_num and isinstance(batch_num, int) == False:
        return {"code": -1, "msg": "<batch_num>must be int"}
    else:
        logger.info('<batch_num>:%s', batch_num)

    if mode and isinstance(mode, str) == True:
        logger.info('<mode>:%s', mode)
    else:
        return {"code": -1, "msg": "<mode>must be string"}
    #计算出回滚的时间点
    rollback_time = (dt.datetime.now() + dt.timedelta(minutes=-delta)).strftime("%Y-%m-%d %H:%M:%S")
    kafka_consumer = KafkaConsumer(group_id= consumer,
                                   bootstrap_servers=['10.0.122.8:9092','10.0.122.10:9092','10.0.122.15:9092','10.0.122.16:9092','10.0.122.3:9092'])

    adminClient = KafkaAdminClient(
        bootstrap_servers='10.0.122.8:9092,10.0.122.10:9092,10.0.122.15:9092,10.0.122.16:9092,10.0.122.3:9092')

    #获取分区
    partitions = kafka_consumer.partitions_for_topic(topic)
    if partitions == None:
        result =  {"code": -1, "msg": "topic:{}不存在".format(topic)}
        print(result)
        return result

    if consumer not in map(lambda c:c[0],adminClient.list_consumer_groups()):
        result = {"code": -1, "msg": "consumer:{}不存在".format(consumer)}
        print(result)
        return {"code": -1, "msg": "consumer:{}不存在".format(consumer)}

    if pipline_status != 'RUNNING_ERROR':
        logger.info('pipline<%s> 不是异常（RUNNING_ERROR）终止，不需要补偿数据,pipline状态为:%s',pipline_id,pipline_status)
        return {"code": -1, "msg": "pipline属于正常终止，不需要补偿数据"}


    logger.info('pipline<%s> 开始补偿数据',pipline_id)


    #遍历分区重置offset, partion字段需要mysql关键字，写sql的时候注意加上反引号
    for partition in partitions:
        # topicPartition = TopicPartition(topic=topic, partition=partition)
        topicPartition = TopicPartition(topic=topic, partition=partition)
        kafka_consumer.assign([topicPartition])
        position = kafka_consumer.position(topicPartition)

        sql = "select * from kafka_offset_record where " \
              " topic = '{}' and consumer = '{}' and `partition` = {} and create_time >='{}' " \
              "order by create_time asc limit 1".format(topic,consumer,partition,rollback_time)
        # logger.info(sql)
        df = pd.read_sql_query(sql,conn)

        if df.size == 0:
            new_position = position
        else:
            new_position= df['offset'][0]

        #如果回退的postion 比当前 所处的position要大，或者mode=batch，则按照批次条数回退
        if position-new_position <= 0 or mode =='batch':
            new_position = position - batch_num

        #重置offset
        kafka_consumer.commit({topicPartition: OffsetAndMetadata(offset=new_position, metadata=None)})

        logger.info('消费组：%s-%s, 当前位置为：%s, 回滚到到位置为：%s,一共回滚条数为: %s',consumer,partition,position,new_position,position-new_position)



    return {"code":0,"msg":"kafka的offset重置了{}条messege".format(position-new_position)}

@app.route('/kafka_report/<string:msg>')
def kafka_report(msg):
    logger.info(msg)

@app.route('/test/<string:topic>/<string:consumer>')
def test(topic,consumer):
    kafka_consumer = KafkaConsumer(group_id=consumer,
                                   bootstrap_servers=['10.0.122.8:9092', '10.0.122.10:9092', '10.0.122.15:9092',
                                                      '10.0.122.16:9092', '10.0.122.3:9092'])

    adminClient = KafkaAdminClient(
        bootstrap_servers='10.0.122.8:9092,10.0.122.10:9092,10.0.122.15:9092,10.0.122.16:9092,10.0.122.3:9092')

    partitions = kafka_consumer.partitions_for_topic(topic)




    print(partitions)
    print('---------------------')

    consumer_list = adminClient.list_consumer_groups()
    for consumer in consumer_list:
        print(consumer)

    return 'OK'
if __name__ == '__main__':
    os.makedirs("./logs/",exist_ok=True)
    logger = get_logger("./logs/server.log")
    app.run(host='0.0.0.0', port=37778)
    logger.info("数据补偿服务启动成功........")
