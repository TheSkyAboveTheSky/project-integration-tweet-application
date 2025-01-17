"""
Module for processing hashtags in tweets.
"""
import re
import logging
from collections import Counter

logger = logging.getLogger(__name__)

def extract_hashtags(text):
    """
    Extract hashtags from tweet text.
    
    Args:
        text (str): Tweet text
        
    Returns:
        list: List of hashtags found in the text
    """
    # Match hashtags using regex
    hashtag_pattern = r'#(\w+)'
    hashtags = re.findall(hashtag_pattern, text)
    
    # Convert to lowercase for standardization
    hashtags = [tag.lower() for tag in hashtags]
    
    return hashtags

def count_hashtags(hashtags):
    """
    Count frequency of hashtags.
    
    Args:
        hashtags (list): List of hashtags
        
    Returns:
        dict: Dictionary mapping hashtags to their counts
    """
    counter = Counter(hashtags)
    return dict(counter)

def process_hashtags(tweet):
    """
    Process hashtags in a tweet.
    
    Args:
        tweet (dict): Tweet data
        
    Returns:
        dict: Tweet with processed hashtag information
    """
    try:
        # Extract hashtags from text if not already present
        if 'hashtags' not in tweet or not tweet['hashtags']:
            tweet['hashtags'] = extract_hashtags(tweet['text'])
        
        # Ensure all hashtags are lowercase
        tweet['hashtags'] = [tag.lower() for tag in tweet['hashtags']]
        
        # Add hashtag count
        tweet['hashtag_count'] = len(tweet['hashtags'])
        
        # Add hashtag frequency
        tweet['hashtag_frequency'] = count_hashtags(tweet['hashtags'])
        
        return tweet
    except Exception as e:
        logger.error(f"Error processing hashtags for tweet {tweet.get('id')}: {e}")
        # Return the original tweet if processing fails
        return tweet
