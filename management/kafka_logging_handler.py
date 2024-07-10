# kafka_logging_handler.py
from kafka import KafkaProducer
import logging


class KafkaLoggingHandler(logging.Handler):
    def __init__(self, kafka_url, topic):
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(bootstrap_servers=kafka_url)
        self.topic = topic

    def emit(self, record):
        log_entry = self.format(record)
        self.producer.send(self.topic, log_entry.encode("utf-8"))

    def close(self):
        self.producer.close()
        super().close()
