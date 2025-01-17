"""
Module for processing and normalizing location data in tweets.
"""
import logging

logger = logging.getLogger(__name__)

# Map of common city names to their coordinates
CITY_COORDINATES = {
    'new york': {'lat': 40.7128, 'lon': -74.0060},
    'los angeles': {'lat': 34.0522, 'lon': -118.2437},
    'chicago': {'lat': 41.8781, 'lon': -87.6298},
    'london': {'lat': 51.5074, 'lon': -0.1278},
    'paris': {'lat': 48.8566, 'lon': 2.3522},
    'tokyo': {'lat': 35.6762, 'lon': 139.6503},
    'sydney': {'lat': -33.8688, 'lon': 151.2093},
    'mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'beijing': {'lat': 39.9042, 'lon': 116.4074},
    'cairo': {'lat': 30.0444, 'lon': 31.2357}
}

def normalize_locations(tweet):
    """
    Normalize location data in a tweet.
    
    Args:
        tweet (dict): Tweet data
        
    Returns:
        dict: Tweet with normalized location information
    """
    try:
        # Check if location data exists
        if 'location' not in tweet or not tweet['location']:
            # Try to extract location from text or user profile
            if 'user' in tweet and 'location' in tweet['user']:
                user_location = tweet['user']['location'].lower()
                for city, coords in CITY_COORDINATES.items():
                    if city in user_location:
                        tweet['location'] = coords
                        break
            
            # If still no location, skip further processing
            if 'location' not in tweet or not tweet['location']:
                tweet['location_normalized'] = False
                return tweet
        
        # Ensure location has correct format
        if 'lat' not in tweet['location'] or 'lon' not in tweet['location']:
            tweet['location_normalized'] = False
            return tweet
        
        # Convert coordinates to float
        try:
            lat = float(tweet['location']['lat'])
            lon = float(tweet['location']['lon'])
        except (ValueError, TypeError):
            logger.warning(f"Could not convert location coordinates to float for tweet {tweet.get('id', 'unknown')}")
            tweet['location_normalized'] = False
            return tweet
            
        # Add Elasticsearch geo format
        tweet['geo'] = {
            'lat': lat,
            'lon': lon
        }
        
        # Add continent/region based on coordinates
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
        
        tweet['location_normalized'] = True
        return tweet
    except Exception as e:
        logger.error(f"Error normalizing location for tweet {tweet.get('id')}: {e}")
        tweet['location_normalized'] = False
        return tweet
