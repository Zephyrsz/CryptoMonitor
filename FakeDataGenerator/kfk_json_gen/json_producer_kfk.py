import sys
import time
import json

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

KAFAKA_HOST = "127.0.0.1"
KAFAKA_PORT = 9192
KAFAKA_TOPIC = "testa2"
offset = "earliest"

class Kafka_producer():
    ''''' 生产模块：根据不同的key，区分消息 '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, key):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.key = key
        print("producer:h,p,t,k", kafkahost, kafkaport, kafkatopic, key)
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
        )
        print("boot svr:", bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers
                                      )

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params, ensure_ascii=False)
            producer = self.producer
            print(parmas_message)
            v = parmas_message.encode('utf-8')
            k = key.encode('utf-8')
            print("send msg:(k,v)", k, v)
            producer.send(self.kafkatopic, key=k, value=v)
            producer.flush()
        except KafkaError as e:
            print(e)


class Kafka_consumer():
    ''''' 消费模块: 通过不同groupid消费topic里面的消息 '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.key = key
        self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort)
                                      ,auto_offset_reset="earliest")

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)


def main(xtype, group, key):
    ''''' 测试consumer和producer '''
    if xtype == "p":
        # 生产模块
        producer = Kafka_producer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, key)
        print("===========> producer:", producer)
        for _id in range(100):
            # params = '{"消息" : "%s"}' % str(_id)
            params=[{"消息0":_id}]
            # 这种方式会将引号都打上\, 可以直接用python对象params=[{"消息0":_id},{"消息1" :_id}]
            producer.sendjsondata(params)
            time.sleep(1)

    if xtype == 'c':
        # 消费模块
        consumer = Kafka_consumer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, group)
        print("===========> consumer:", consumer)
        message = consumer.consume_data()
        for msg in message:
            print('msg---------------->k,v', msg.key.decode(encoding="utf-8"), msg.value.decode(encoding="utf-8"))
            # print('msg---------------->k,v', msg.key, msg.value)
            print('offset---------------->', msg.offset)


if __name__ == '__main__':
    xtype = sys.argv[1]
    group = sys.argv[2]
    key = sys.argv[3]
    main(xtype, group, key)



'''
ref:
http://abloz.com/tech/2017/07/22/python-kafka-producer-consumer/

脚本运行方法：
生产消息
python json_producer_kfk.py p g k
消费消息
python json_producer_kfk.py c g k
'''