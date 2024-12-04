import json
import logging
import os
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

class TweetKafkaProducer:
    def __init__(self):
        self.bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        self.topic = 'raw-tweets'
        self._producer = None
        self._connect()
        
    def _connect(self):
        try:
            logger.info(f"Connecting to Kafka at {self.bootstrap_servers}")
            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 10)
            )
            logger.info("Successfully connected to Kafka")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
            
    def send_tweet(self, tweet):
        try:
            logger.info(f"Sending tweet ID {tweet['id']} to Kafka topic {self.topic}")
            self._producer.send(self.topic, tweet)
            self._producer.flush()
            logger.info(f"Tweet ID {tweet['id']} sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending tweet to Kafka: {e}")
            return False
