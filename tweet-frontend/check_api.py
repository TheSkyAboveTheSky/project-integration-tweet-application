#!/usr/bin/env python3
"""
Script to check tweet-api connection.
"""
import requests
import os
import sys
import time

API_URL = os.environ.get('API_URL', 'http://tweet-api:8000')

def check_api_connection():
    """Try to connect to the API and report status."""
    print(f"Checking connection to API at {API_URL}...")
    
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        
        print(f"✓ API is available - Status code: {response.status_code}")
        print(f"API response: {response.json()}")
        
        try:
            # Try to get tweets
            tweets_response = requests.get(f"{API_URL}/tweets?limit=1", timeout=5)
            tweets_response.raise_for_status()
            tweets_data = tweets_response.json()
            
            print(f"✓ API can fetch tweets - Found {tweets_data.get('total', 0)} tweets")
            
            # Try to get trends
            trends_response = requests.get(f"{API_URL}/trends", timeout=5)
            trends_response.raise_for_status()
            trends_data = trends_response.json()
            
            print(f"✓ API can fetch trends - Found {len(trends_data.get('hashtags', []))} trending hashtags")
            
            return True
        except Exception as e:
            print(f"✗ API endpoint test failed: {e}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API at {API_URL}")
        print("  Check if the API service is running and reachable")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Connection to API timed out")
        print("  The API service might be overloaded or not responding")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Main function with retry logic."""
    max_retries = 5
    retry_delay = 3
    
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}/{max_retries}")
        
        if check_api_connection():
            print("API connection check successful!")
            return 0
        
        if attempt < max_retries:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print("API connection check failed after multiple attempts.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
