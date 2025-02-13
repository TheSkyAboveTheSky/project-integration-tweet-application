"""
Configuration for Tweet API.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Elasticsearch configuration
ES_HOST = os.getenv("ES_HOST", "elasticsearch:9200")
ES_INDEX = os.getenv("ES_INDEX", "tweets")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# CORS settings - Allow all origins in container environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Caching settings
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "False").lower() in ("true", "1", "t")
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", "300"))  # 5 minutes

# Print configuration when module is loaded (useful for debugging containers)
if __name__ == "__main__":
    print(f"Elasticsearch: {ES_HOST} (Index: {ES_INDEX})")
    print(f"API: {API_HOST}:{API_PORT} (Workers: {API_WORKERS})")
    print(f"CORS: {CORS_ORIGINS}")
    print(f"Cache: {'Enabled' if ENABLE_CACHE else 'Disabled'} (Expiry: {CACHE_EXPIRY}s)")
