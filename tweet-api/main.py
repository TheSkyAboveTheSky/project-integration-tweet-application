"""
FastAPI server for querying tweets from Elasticsearch.
"""
import os
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch, NotFoundError, RequestError
from pydantic import BaseModel, Field
from datetime import datetime

# Import configuration
from config import ES_HOST, ES_INDEX, CORS_ORIGINS, ENABLE_CACHE, CACHE_EXPIRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tweet API",
    description="API for querying processed tweets from Elasticsearch",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Elasticsearch client
logger.info(f"Connecting to Elasticsearch at {ES_HOST}")
es = Elasticsearch([ES_HOST])

# Check if Elasticsearch is available
if not es.ping():
    logger.error(f"Cannot connect to Elasticsearch at {ES_HOST}")
else:
    logger.info(f"Connected to Elasticsearch at {ES_HOST}")

# Pydantic models for requests and responses
class Location(BaseModel):
    lat: float
    lon: float

class User(BaseModel):
    id: int
    screen_name: str
    followers_count: int

class Sentiment(BaseModel):
    polarity: float
    subjectivity: float
    label: str

class Tweet(BaseModel):
    id: str
    text: str
    user: User
    created_at: datetime
    location: Optional[Location] = None
    hashtags: List[str] = []
    retweet_count: int = 0
    favorite_count: int = 0
    sentiment: Optional[Sentiment] = None
    region: Optional[str] = None

class TweetResponse(BaseModel):
    total: int
    tweets: List[Tweet]

class TrendingHashtag(BaseModel):
    tag: str
    count: int

class TrendsResponse(BaseModel):
    hashtags: List[TrendingHashtag]
    total_analyzed: int

class RegionCount(BaseModel):
    region: str
    count: int

class RegionsResponse(BaseModel):
    regions: List[RegionCount]
    total_analyzed: int

class SentimentSummary(BaseModel):
    positive: int
    negative: int
    neutral: int
    total_analyzed: int

@app.get("/")
def read_root():
    """API health check endpoint."""
    return {"status": "ok", "service": "Tweet API"}

@app.get("/tweets", response_model=TweetResponse)
async def get_tweets(
    q: Optional[str] = Query(None, description="Search term in tweet text"),
    hashtag: Optional[str] = Query(None, description="Filter by hashtag"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment (positive, negative, neutral)"),
    region: Optional[str] = Query(None, description="Filter by geographic region"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
):
    """
    Get tweets with optional filtering.
    """
    # Build query
    query = {"bool": {"must": []}}
    
    # Add text search if provided
    if q:
        query["bool"]["must"].append({"match": {"text": q}})
    
    # Add hashtag filter if provided
    if hashtag:
        query["bool"]["must"].append({"term": {"hashtags": hashtag.lower()}})
    
    # Add sentiment filter if provided
    if sentiment:
        query["bool"]["must"].append({"term": {"sentiment.label": sentiment.lower()}})
    
    # Add region filter if provided
    if region:
        query["bool"]["must"].append({"term": {"region": region}})
    
    # If no filters, use match_all query
    if not query["bool"]["must"]:
        query = {"match_all": {}}
    
    try:
        # Execute search
        result = es.search(
            index=ES_INDEX,
            body={
                "query": query,
                "sort": [{"created_at": {"order": "desc"}}],
                "from": offset,
                "size": limit
            }
        )
        
        # Process results
        hits = result["hits"]["hits"]
        total = result["hits"]["total"]["value"]
        
        # Convert Elasticsearch results to Tweet objects
        tweets = []
        for hit in hits:
            source = hit["_source"]
            # Convert the source to a Tweet model with proper field mapping
            try:
                tweets.append(Tweet(**source))
            except Exception as e:
                logger.error(f"Error converting tweet: {e}")
                # Skip invalid tweets
                continue
        
        return TweetResponse(total=total, tweets=tweets)
    
    except RequestError as e:
        logger.error(f"Elasticsearch request error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching tweets: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tweets/{tweet_id}", response_model=Tweet)
async def get_tweet(tweet_id: str):
    """
    Get a specific tweet by ID.
    """
    try:
        result = es.get(index=ES_INDEX, id=tweet_id)
        return Tweet(**result["_source"])
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Tweet {tweet_id} not found")
    except Exception as e:
        logger.error(f"Error fetching tweet {tweet_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/trends", response_model=TrendsResponse)
async def get_trends(
    limit: int = Query(10, ge=1, le=50, description="Number of top hashtags to return"),
    q: Optional[str] = Query(None, description="Filter trends by tweet text"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
):
    """
    Get trending hashtags based on frequency.
    """
    try:
        # Build query
        query = {"bool": {"must": []}}
        
        # Add text search if provided
        if q:
            query["bool"]["must"].append({"match": {"text": q}})
        
        # Add sentiment filter if provided
        if sentiment:
            query["bool"]["must"].append({"term": {"sentiment.label": sentiment.lower()}})
        
        # If no filters, use match_all query
        if not query["bool"]["must"]:
            query = {"match_all": {}}
        
        # Execute aggregation
        result = es.search(
            index=ES_INDEX,
            body={
                "query": query,
                "size": 0,  # We only need aggregations, not results
                "aggs": {
                    "hashtags": {
                        "terms": {
                            "field": "hashtags",
                            "size": limit
                        }
                    }
                }
            }
        )
        
        # Extract hashtag counts
        buckets = result["aggregations"]["hashtags"]["buckets"]
        total = result["hits"]["total"]["value"]
        
        hashtags = [
            TrendingHashtag(tag=bucket["key"], count=bucket["doc_count"])
            for bucket in buckets
        ]
        
        return TrendsResponse(hashtags=hashtags, total_analyzed=total)
    
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/regions", response_model=RegionsResponse)
async def get_regions():
    """
    Get tweet counts by geographic region.
    """
    try:
        result = es.search(
            index=ES_INDEX,
            body={
                "size": 0,
                "aggs": {
                    "regions": {
                        "terms": {
                            "field": "region",
                            "size": 10  # Should cover all continents/regions
                        }
                    }
                }
            }
        )
        
        # Extract region counts
        buckets = result["aggregations"]["regions"]["buckets"]
        total = result["hits"]["total"]["value"]
        
        regions = [
            RegionCount(region=bucket["key"], count=bucket["doc_count"])
            for bucket in buckets
        ]
        
        return RegionsResponse(regions=regions, total_analyzed=total)
    
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/sentiment", response_model=SentimentSummary)
async def get_sentiment_summary():
    """
    Get sentiment distribution summary.
    """
    try:
        result = es.search(
            index=ES_INDEX,
            body={
                "size": 0,
                "aggs": {
                    "sentiment": {
                        "terms": {
                            "field": "sentiment.label",
                            "size": 3  # positive, negative, neutral
                        }
                    }
                }
            }
        )
        
        # Extract sentiment counts
        buckets = result["aggregations"]["sentiment"]["buckets"]
        total = result["hits"]["total"]["value"]
        
        # Initialize counts
        positive = 0
        negative = 0
        neutral = 0
        
        # Map bucket key to count
        for bucket in buckets:
            if bucket["key"] == "positive":
                positive = bucket["doc_count"]
            elif bucket["key"] == "negative":
                negative = bucket["doc_count"]
            elif bucket["key"] == "neutral":
                neutral = bucket["doc_count"]
        
        return SentimentSummary(
            positive=positive,
            negative=negative,
            neutral=neutral,
            total_analyzed=total
        )
    
    except Exception as e:
        logger.error(f"Error fetching sentiment summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/map-data")
async def get_map_data(
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    hashtag: Optional[str] = Query(None, description="Filter by hashtag"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum number of points to return"),
):
    """
    Get geo data for map visualization.
    """
    try:
        # Build query
        query = {"bool": {"must": [{"exists": {"field": "geo"}}]}}
        
        # Add hashtag filter if provided
        if hashtag:
            query["bool"]["must"].append({"term": {"hashtags": hashtag.lower()}})
        
        # Add sentiment filter if provided
        if sentiment:
            query["bool"]["must"].append({"term": {"sentiment.label": sentiment.lower()}})
        
        # Execute search
        result = es.search(
            index=ES_INDEX,
            body={
                "query": query,
                "size": limit,
                "_source": ["id", "geo", "text", "sentiment.label", "hashtags"]
            }
        )
        
        # Extract geo data
        hits = result["hits"]["hits"]
        total = result["hits"]["total"]["value"]
        
        geo_data = [
            {
                "id": hit["_source"]["id"],
                "geo": hit["_source"]["geo"],
                "text": hit["_source"]["text"],
                "sentiment": hit["_source"].get("sentiment", {}).get("label", "neutral"),
                "hashtags": hit["_source"].get("hashtags", [])
            }
            for hit in hits
            if "geo" in hit["_source"]
        ]
        
        return {"total": total, "points": geo_data}
    
    except Exception as e:
        logger.error(f"Error fetching map data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
