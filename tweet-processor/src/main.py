import json
import logging
import os
import sys
import time
import configparser
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
from elasticsearch import Elasticsearch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import processors
try:
    from processors.hashtag_processor import process_hashtags
    from processors.location_processor import normalize_locations
    from processors.sentiment_processor import analyze_sentiment
    PROCESSORS_AVAILABLE = True
    logger.info("Using advanced processors")
except ImportError as e:
    logger.warning(f"Could not import processors: {e}. Using simplified versions.")
    PROCESSORS_AVAILABLE = False

# Simplified processors if imports fail
def simple_process_hashtags(tweet):
    if 'text' in tweet and 'hashtags' not in tweet:
        # Extract hashtags using simple regex
        import re
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, tweet.get('text', ''))
        tweet['hashtags'] = [tag.lower() for tag in hashtags]
    return tweet

def simple_normalize_locations(tweet):
    if 'location' in tweet and isinstance(tweet['location'], dict):
        if 'lat' in tweet['location'] and 'lon' in tweet['location']:
            # Convert to float to ensure proper format for Elasticsearch
            try:
                lat = float(tweet['location']['lat'])
                lon = float(tweet['location']['lon'])
                
                # Add geo field in Elasticsearch format
                tweet['geo'] = {
                    'lat': lat,
                    'lon': lon
                }
                
                # Simple region classification
                if lon < -30:
                    if lat > 30:
                        tweet['region'] = 'North America'
                    else:
                        tweet['region'] = 'South America'
                elif lon < 60:
                    if lat > 30:
                        tweet['region'] = 'Europe'
                    else:
                        tweet['region'] = 'Africa'
                else:
                    if lat > 30:
                        tweet['region'] = 'Asia'
                    else:
                        tweet['region'] = 'Oceania'
            except (ValueError, TypeError):
                # Handle case where lat/lon can't be converted to float
                logger.warning(f"Could not convert location coordinates to float for tweet {tweet.get('id', 'unknown')}")
    return tweet

def simple_analyze_sentiment(tweet):
    if 'sentiment' not in tweet and 'text' in tweet:
        # Very basic sentiment using keywords
        text = tweet.get('text', '').lower()
        positive_words = ['good', 'great', 'nice', 'happy', 'love']
        negative_words = ['bad', 'awful', 'hate', 'sad', 'terrible']
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            sentiment = 'positive'
        elif neg_count > pos_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
            
        tweet['sentiment'] = {'label': sentiment}
    return tweet

def process_tweet(tweet):
    """Process a single tweet."""
    try:
        # Make a copy to avoid modifying the original
        if isinstance(tweet, str):
            processed = json.loads(tweet)
        else:
            processed = tweet.copy()
        
        # Apply processors
        if PROCESSORS_AVAILABLE:
            processed = process_hashtags(processed)
            processed = normalize_locations(processed)
            processed = analyze_sentiment(processed)
        else:
            processed = simple_process_hashtags(processed)
            processed = simple_normalize_locations(processed)
            processed = simple_analyze_sentiment(processed)
        
        # Add processing metadata
        processed['processed'] = True
        processed['processed_at'] = datetime.now().isoformat()
        
        return processed
    except Exception as e:
        logger.error(f"Error processing tweet: {e}")
        if isinstance(tweet, str):
            return json.loads(tweet)
        return tweet

def load_config():
    """Load configuration from config.ini."""
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    
    if os.path.exists(config_file):
        config.read(config_file)
        logger.info(f"Loaded configuration from {config_file}")
        return config
    else:
        logger.warning(f"Config file {config_file} not found, using defaults")
        return None

def create_elasticsearch_client(config):
    """Create and return an Elasticsearch client."""
    # Use environment variables or config file
    if config and 'elasticsearch' in config:
        es_hosts = config['elasticsearch'].get('hosts', 'elasticsearch:9200')
    else:
        es_hosts = os.environ.get('ES_HOST', 'elasticsearch:9200')
    
    logger.info(f"Connecting to Elasticsearch at {es_hosts}")
    
    # Create client
    if ',' in es_hosts:
        hosts = [host.strip() for host in es_hosts.split(',')]
    else:
        hosts = [es_hosts]
    
    return Elasticsearch(hosts)

def create_kafka_consumer(config):
    """Create and return a Kafka consumer."""
    import time
    
    # Use environment variables or config file
    if config and 'kafka' in config:
        bootstrap_servers = config['kafka'].get('bootstrap_servers', 'kafka:9092')
        topic = config['kafka'].get('input_topic', 'raw-tweets')
        # Use a unique group ID each time to force reading from the beginning
        unique_suffix = str(int(time.time()))
        group_id = f"tweet-processor-{unique_suffix}"
    else:
        bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        topic = os.environ.get('KAFKA_INPUT_TOPIC', 'raw-tweets')
        unique_suffix = str(int(time.time()))
        group_id = f"tweet-processor-{unique_suffix}"
    
    logger.info(f"Creating Kafka consumer for {topic} at {bootstrap_servers} with group {group_id}")
    
    # Create consumer with explicit settings to force reading from beginning
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',  # Always start from the beginning
        enable_auto_commit=True,
        group_id=group_id,  # Use unique group ID
        value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )

def create_kafka_producer(config):
    """Create and return a Kafka producer."""
    # Use environment variables or config file
    if config and 'kafka' in config:
        bootstrap_servers = config['kafka'].get('bootstrap_servers', 'kafka:9092')
    else:
        bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    
    logger.info(f"Creating Kafka producer at {bootstrap_servers}")
    
    # Create producer
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8') if x else None
    )

def ensure_elasticsearch_index(es_client, config):
    """Ensure the Elasticsearch index exists with proper mappings."""
    # Get index name from config or environment
    if config and 'elasticsearch' in config:
        index_name = config['elasticsearch'].get('index', 'tweets')
    else:
        index_name = os.environ.get('ES_INDEX', 'tweets')
    
    logger.info(f"Ensuring Elasticsearch index {index_name} exists")
    
    # Delete existing index to ensure clean mapping
    if es_client.indices.exists(index=index_name):
        logger.info(f"Deleting existing index {index_name}")
        try:
            es_client.indices.delete(index=index_name)
        except Exception as e:
            logger.warning(f"Error deleting index {index_name}: {e}")
    else:
        logger.info(f"Index {index_name} does not exist, creating new one")
    
    # Define mapping with geo_point
    mapping = {
        "mappings": {
            "properties": {
                "geo": {"type": "geo_point"},
                "created_at": {"type": "date"},
                "processed_at": {"type": "date"},
                "sentiment": {
                    "properties": {
                        "label": {"type": "keyword"},
                        "polarity": {"type": "float"},
                        "subjectivity": {"type": "float"}
                    }
                },
                "hashtags": {"type": "keyword"},
                "region": {"type": "keyword"}
            }
        }
    }
    
    # Create index with mapping
    try:
        es_client.indices.create(index=index_name, body=mapping)
        logger.info(f"Created Elasticsearch index {index_name} with mapping")
    except Exception as e:
        logger.error(f"Error creating index {index_name}: {e}")
    
    return index_name

def process_tweets_from_kafka(config):
    """Process tweets from Kafka and store in Elasticsearch."""
    # Create Elasticsearch client
    es_client = create_elasticsearch_client(config)
    
    # Create Kafka consumer and producer
    consumer = create_kafka_consumer(config)
    producer = create_kafka_producer(config)
    
    # Ensure index exists
    index_name = ensure_elasticsearch_index(es_client, config)
    
    # Get output topic
    if config and 'kafka' in config:
        output_topic = config['kafka'].get('output_topic', 'processed-tweets')
    else:
        output_topic = os.environ.get('KAFKA_OUTPUT_TOPIC', 'processed-tweets')
    
    # Process messages
    logger.info(f"Starting to process messages from Kafka")
    processed_count = 0
    
    # Check if the consumer is connected
    if not consumer.bootstrap_connected():
        logger.error("Failed to connect to Kafka. Check your configuration.")
        return False
    
    try:
        for message in consumer:
            if message is None or message.value is None:
                continue
            
            # Process tweet
            raw_tweet = message.value
            processed_tweet = process_tweet(raw_tweet)
            
            # Send to output Kafka topic
            producer.send(output_topic, processed_tweet)
            
            # Index in Elasticsearch
            try:
                es_client.index(index=index_name, body=processed_tweet)
            except Exception as e:
                logger.error(f"Error indexing tweet in Elasticsearch: {e}")
            
            processed_count += 1
            if processed_count % 10 == 0:
                logger.info(f"Processed {processed_count} tweets")
            
    except KeyboardInterrupt:
        logger.info("Interrupted, stopping...")
    except Exception as e:
        logger.error(f"Error processing tweets from Kafka: {e}")
        return False
    
    return True

def main():
    """Main function to process tweets."""
    logger.info("Starting tweet processor")
    
    # Load configuration
    config = load_config()
    
    # Determine if running in continuous mode
    continuous_mode = os.environ.get('CONTINUOUS_MODE', 'false').lower() == 'true'
    if config and 'processing' in config:
        interval = int(config['processing'].get('slide_interval', '60'))
    else:
        interval = int(os.environ.get('PROCESSING_INTERVAL', '60'))
    
    if continuous_mode:
        logger.info(f"Running in continuous mode with {interval}s interval")
        while True:
            success = process_tweets_from_kafka(config)
            if not success:
                logger.warning("Failed to process tweets")
            
            logger.info(f"Waiting {interval} seconds before next processing cycle...")
            time.sleep(interval)
    else:
        process_tweets_from_kafka(config)

if __name__ == "__main__":
    main()