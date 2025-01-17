"""
Module for analyzing sentiment in tweets.
"""
import logging

logger = logging.getLogger(__name__)

# Try to import TextBlob with a fallback mechanism
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    logger.warning("TextBlob not available. Will use simplified sentiment analysis.")
    TEXTBLOB_AVAILABLE = False

def analyze_sentiment(tweet):
    """
    Analyze sentiment of a tweet text.
    
    Args:
        tweet (dict): Tweet data
        
    Returns:
        dict: Tweet with added sentiment information
    """
    try:
        if 'text' not in tweet or not tweet['text']:
            # Skip sentiment analysis if no text
            tweet['sentiment'] = {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'label': 'neutral'
            }
            return tweet
        
        if TEXTBLOB_AVAILABLE:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(tweet['text'])
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        else:
            # Simplified sentiment using keyword approach
            text = tweet['text'].lower()
            positive_words = ['good', 'great', 'awesome', 'excellent', 'happy', 'love', 'amazing']
            negative_words = ['bad', 'terrible', 'awful', 'sad', 'hate', 'disappointing', 'poor']
            
            # Count positive and negative words
            pos_count = sum(1 for word in positive_words if word in text)
            neg_count = sum(1 for word in negative_words if word in text)
            
            # Calculate polarity based on counts
            total = pos_count + neg_count
            polarity = 0.0 if total == 0 else (pos_count - neg_count) / total
            subjectivity = 0.5 if total == 0 else min(1.0, total / 10)
        
        # Assign sentiment label based on polarity
        if polarity > 0.1:
            sentiment_label = 'positive'
        elif polarity < -0.1:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        # Add sentiment data to tweet
        tweet['sentiment'] = {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'label': sentiment_label
        }
        
        return tweet
    except Exception as e:
        logger.error(f"Error analyzing sentiment for tweet {tweet.get('id', 'unknown')}: {e}")
        # Add neutral sentiment if analysis fails
        tweet['sentiment'] = {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'label': 'neutral'
        }
        return tweet
