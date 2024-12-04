import json
import logging
import os
import time
import requests
from kafka_producer import TweetKafkaProducer

logger = logging.getLogger(__name__)

class TweetCollector:
    def __init__(self):
        self.db_url = os.environ.get('DB_URL', 'http://json-server/tweets')
        self.producer = TweetKafkaProducer()
        self.last_id = 0
        
    def get_tweets(self):
        try:
            logger.info(f"Fetching tweets from {self.db_url}")
            response = requests.get(self.db_url)
            if response.status_code == 200:
                tweets = response.json()
                logger.info(f"Successfully fetched {len(tweets)} tweets")
                return tweets
            else:
                logger.error(f"Failed to fetch tweets: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            return []
            
    def collect_and_send(self):
        tweets = self.get_tweets()
        new_count = 0
        
        for tweet in tweets:
            try:
                tweet_id = int(tweet['id'])
                if tweet_id > self.last_id:
                    if self.producer.send_tweet(tweet):
                        self.last_id = tweet_id
                        new_count += 1
            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid tweet format: {e}")
                
        logger.info(f"Collected and sent {new_count} new tweets")
        return new_count
        
    def run(self, polling_interval=30):
        logger.info("Starting tweet collector...")
        while True:
            try:
                self.collect_and_send()
                time.sleep(polling_interval)
            except KeyboardInterrupt:
                logger.info("Stopping tweet collector...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(polling_interval)
