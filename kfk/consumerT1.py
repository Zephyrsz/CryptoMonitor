from kafka import KafkaConsumer
from kafka import TopicPartition
from typing import Optional
'''
ref:
https://www.cnblogs.com/wxzhe/p/10186452.html
'''

import re
def ip_match(str):
    return re.search( r'(.*)[0-9]{3}\.[0-9]{3}\.[0-9]{3}.*', str, re.M|re.I)

####手动指定topic ， partition
def consumer1():
    consumer = KafkaConsumer(group_id= 'groupt1', bootstrap_servers= ['localhost:9192'])
    consumer.assign([TopicPartition(topic= 'Logs', partition= 0)])
    for msg in consumer:
        print(msg)


#### 自动分配partition
def consumer2():
    consumer = KafkaConsumer("testa1", bootstrap_servers=["localhost:9192"], auto_offset_reset='earliest')
    for msg in consumer:
        # key = msg.key.decode(encoding="utf-8")
        value = msg.value.decode(encoding="utf-8")
        key = msg.key
        if msg.key != None:
            key = msg.key.decode(encoding="utf-8")
        else:
            key = "null"
        # value = msg.value
        print("%s-%d-%d key=%s value=%s" % (msg.topic, msg.partition, msg.offset, key, value))
        # if(ip_match(value)):
        #     print(value)


import time
###使用poll方式手动拉取


def consumer_poll():
    consumer = KafkaConsumer("Logs", bootstrap_servers=['localhost:9192'],auto_offset_reset='earliest')
    while True:
        msg = consumer.poll(timeout_ms=5)
        print(msg)
        time.sleep(2)


consumer2()