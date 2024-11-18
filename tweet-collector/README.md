# Tweet Collector

Python-based tweet collector that reads from a database (mock initially) and pushes data to Kafka.

## Features

- Connects to a mock database (JSON Server) expandable to other sources
- Collects tweet data in a configurable format
- Pushes tweets to Kafka topics with fallback to local file storage
- Configurable polling intervals

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the infrastructure:
   ```bash
   cd ..  # Navigate to project root
   docker-compose up -d
   ```

3. Run the collector:
   ```bash
   python src/main.py
   ```

## Configuration

The collector is configured via environment variables or a .env file:

- DB_URL: URL to the JSON Server or database
- KAFKA_BOOTSTRAP_SERVERS: Kafka broker addresses
- KAFKA_TOPIC: Topic to publish tweets to
- BATCH_SIZE: Number of tweets to process in each batch
