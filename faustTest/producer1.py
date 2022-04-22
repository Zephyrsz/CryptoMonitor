import gc
import platform
import time
import threading

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.producer.buffer import SimpleBufferPool

topic="pytest1"
kafka_broker = {
    'host': '10.80.75.67',
    'port': 9092
}
# [None, 'gzip', 'snappy', 'lz4', 'zstd']
connect_str = ':'.join([kafka_broker.get('host'), str(kafka_broker.get('port'))])
producer = KafkaProducer(
                         # bootstrap_servers=connect_str,
                         # bootstrap_servers='10.80.75.67:9092',
                         bootstrap_servers='127.0.0.1:9092',
                         retries=5,
                         max_block_ms=30000,
                         compression_type=None,
                         value_serializer=str.encode
)

messages = 100
futures = []
for i in range(messages):
    futures.append(producer.send(topic, 'msg %d' % i))
print(futures)
producer.close()