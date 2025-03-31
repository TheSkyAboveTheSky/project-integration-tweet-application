"""
Cache implementation for API endpoints to improve performance.
"""
from functools import wraps
import time

# Simple in-memory cache
cache = {}
cache_expiry = {}
DEFAULT_CACHE_EXPIRY = 300  # 5 minutes

def cached(expiry=None):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Get current time
            now = time.time()
            
            # If key exists in cache and hasn't expired, return cached value
            if key in cache and cache_expiry.get(key, 0) > now:
                return cache[key]
            
            # Otherwise, call the function and cache the result
            result = await func(*args, **kwargs)
            cache[key] = result
            cache_expiry[key] = now + (expiry or DEFAULT_CACHE_EXPIRY)
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear the entire cache."""
    cache.clear()
    cache_expiry.clear()

def clean_expired():
    """Remove expired cache entries."""
    now = time.time()
    expired_keys = [k for k, exp in cache_expiry.items() if exp <= now]
    for key in expired_keys:
        cache.pop(key, None)
        cache_expiry.pop(key, None)
