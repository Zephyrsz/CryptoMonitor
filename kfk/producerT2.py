from kafka import KafkaConsumer, KafkaProducer, TopicPartition

import gc
import platform
import time
import threading
topic = "cmc"
producer = KafkaProducer(bootstrap_servers="localhost:9192",
                         retries=5,
                         max_block_ms=30000,
                         compression_type=None)


future = producer.send(
    topic,
    value=b"Simple value", key=b"Simple key", timestamp_ms=None,
    partition=0)
record = future.get(timeout=5)