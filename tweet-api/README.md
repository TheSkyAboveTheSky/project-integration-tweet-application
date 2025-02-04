# Tweet API

Python-based RESTful API for querying tweets from Elasticsearch.

## Features

- RESTful endpoints for tweet data retrieval
- Elasticsearch integration for efficient queries
- Filtering and search capabilities
- Aggregation for trend analysis
- Geo data for map visualizations

## Technology Stack

- FastAPI: Modern, high-performance web framework
- Elasticsearch-py: Elasticsearch client
- Pydantic: Data validation and settings management
- Uvicorn: ASGI server

## Setup

### Prerequisites
- Python 3.8+
- Elasticsearch running with indexed tweets
- Docker (optional, for containerized deployment)

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API documentation at http://localhost:8000/docs

## API Endpoints

- GET /tweets - List tweets with filtering options
- GET /tweets/{id} - Get a specific tweet by ID
- GET /trends - Get trending hashtags
- GET /sentiment - Get sentiment distribution
- GET /map-data - Get geo data for mapping
