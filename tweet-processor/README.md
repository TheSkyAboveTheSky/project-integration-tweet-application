# Tweet Processor

A containerized service for processing tweets, extracting insights, and storing data in Elasticsearch.

## Features

- Extracts hashtags from tweet content
- Performs sentiment analysis on tweet text
- Normalizes geo data for mapping visualizations
- Indexes processed tweets into Elasticsearch

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the processor:
   ```bash
   python src/main.py
   ```

## Environment Variables

- ES_HOST: Elasticsearch host (default: localhost:9200)
- ES_INDEX: Elasticsearch index name (default: tweets)
- CONTINUOUS_MODE: Set to "true" for continuous processing (default: false)
- PROCESSING_INTERVAL: Seconds between processing cycles (default: 60)
- KAFKA_BOOTSTRAP_SERVERS: Kafka broker addresses
- KAFKA_INPUT_TOPIC: Topic to consume raw tweets from
- KAFKA_OUTPUT_TOPIC: Topic to publish processed tweets to
