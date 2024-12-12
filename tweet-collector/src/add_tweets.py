#!/usr/bin/env python3
"""Script to add mock tweets to the JSON Server database."""
import json, random, requests, time, logging, os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get DB_URL from environment variable, fall back to default if not available
DB_URL = os.getenv('DB_URL', 'http://localhost:3000/tweets')

# Sample data for tweet generation
LOCATIONS = [
    (40.7128, -74.0060),  # New York
    (34.0522, -118.2437), # Los Angeles
    (51.5074, -0.1278),   # London
    (48.8566, 2.3522),    # Paris
    (35.6762, 139.6503),  # Tokyo
    (19.0760, 72.8777),   # Mumbai
    (55.7558, 37.6173),   # Moscow
    (-33.8688, 151.2093), # Sydney
]

HASHTAGS = [
    "tech", "AI", "machinelearning", "python", "java", 
    "programming", "data", "cloud", "serverless", "bigdata",
    "blockchain", "cybersecurity", "IoT", "analytics", "docker",
    "kubernetes", "devops", "frontend", "backend", "fullstack"
]

def generate_tweet(tweet_id):
    """Generate a random tweet with specified ID."""
    lat, lon = random.choice(LOCATIONS)
    lat += random.uniform(-0.1, 0.1)  # Add some randomness
    lon += random.uniform(-0.1, 0.1)
    
    tweet_hashtags = random.sample(HASHTAGS, random.randint(1, 3))
    
    return {
        "id": tweet_id,
        "text": f"New trending topic on #{' #'.join(tweet_hashtags)} - what do you think?",
        "user": {
            "id": random.randint(1000, 9999),
            "screen_name": f"user_{random.randint(1000, 9999)}",
            "followers_count": random.randint(1, 10000)
        },
        "created_at": datetime.now().isoformat(),
        "location": {"lat": lat, "lon": lon},
        "hashtags": tweet_hashtags,
        "retweet_count": random.randint(0, 100),
        "favorite_count": random.randint(0, 200)
    }

def add_tweets(url=None, num_tweets=5):
    """Add new tweets to JSON Server with properly incremented IDs."""
    if url is None:
        url = DB_URL
        
    try:
        logger.info(f"Connecting to {url} to add tweets")
        # Get current tweets to find highest ID
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning(f"Could not fetch tweets: HTTP {response.status_code}. Starting with ID 1000.")
            next_id = 1000
            return
            
        current_tweets = response.json()
        
        # Find highest ID (handle both string and int IDs)
        highest_id = 0
        for tweet in current_tweets:
            try:
                tweet_id = int(tweet['id'])
                if tweet_id > highest_id:
                    highest_id = tweet_id
            except (ValueError, TypeError):
                pass
        
        next_id = highest_id + 1 if highest_id > 0 else 1000
        logger.info(f"Found highest ID: {highest_id}, next ID will be: {next_id}")
        
        # Generate and add new tweets
        added = 0
        for i in range(num_tweets):
            tweet = generate_tweet(next_id + i)
            response = requests.post(url, json=tweet)
            if response.status_code == 201:
                logger.info(f"Added tweet with ID {tweet['id']}")
                added += 1
            else:
                logger.error(f"Failed to add tweet: HTTP {response.status_code}")
        
        return added
    except Exception as e:
        logger.error(f"Error adding tweets: {e}")
        return 0

def main():
    """Run tweet generator periodically."""
    logger.info(f"Starting tweet generator using DB_URL: {DB_URL}")
    
    try:
        while True:
            num_tweets = random.randint(1, 3)
            added = add_tweets(num_tweets=num_tweets)
            logger.info(f"Added {added} new tweets")
            
            wait_time = random.randint(20, 60)
            logger.info(f"Waiting {wait_time} seconds before adding more tweets...")
            time.sleep(wait_time)
    except KeyboardInterrupt:
        logger.info("Stopping tweet generator...")

if __name__ == "__main__":
    main()
