# Tweet Analytics Platform

A real-time tweet analysis platform with collection, processing, visualization, and Kubernetes deployment capabilities.

## Architecture

This project implements a complete data pipeline for tweet analytics:

1. **Tweet Collector**: Collects tweets from a mock API and sends them to Kafka
2. **Tweet Processor**: Processes tweets with sentiment analysis and feature extraction
3. **Tweet API**: REST API serving processed tweet data from Elasticsearch
4. **Tweet Frontend**: Web dashboard for visualizing tweet analytics

## Components

- **tweet-collector**: Python service collecting tweets from JSON server
- **tweet-processor**: Processing pipeline for tweet analysis
- **tweet-api**: FastAPI service for accessing analyzed tweets
- **tweet-frontend**: Flask web application with visualization dashboards
- **k8s**: Kubernetes deployment manifests for all components

## Technologies

- **Messaging**: Kafka for real-time data streaming
- **Storage**: Elasticsearch for tweet indexing and search
- **Backend**: Python with FastAPI
- **Frontend**: Flask with Bootstrap, Chart.js, and Leaflet
- **Containers**: Docker for containerization
- **Orchestration**: Kubernetes for deployment and scaling

## Getting Started

### Local Development with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Access the dashboard
open http://localhost:5000# Tweet Analytics Platform

A real-time tweet analysis platform with collection, processing, visualization, and Kubernetes deployment capabilities.

## Architecture

This project implements a complete data pipeline for tweet analytics:

1. **Tweet Collector**: Collects tweets from a mock API and sends them to Kafka
2. **Tweet Processor**: Processes tweets with sentiment analysis and feature extraction
3. **Tweet API**: REST API serving processed tweet data from Elasticsearch
4. **Tweet Frontend**: Web dashboard for visualizing tweet analytics

## Components

- **tweet-collector**: Python service collecting tweets from JSON server
- **tweet-processor**: Processing pipeline for tweet analysis
- **tweet-api**: FastAPI service for accessing analyzed tweets
- **tweet-frontend**: Flask web application with visualization dashboards
- **k8s**: Kubernetes deployment manifests for all components

## Technologies

- **Messaging**: Kafka for real-time data streaming
- **Storage**: Elasticsearch for tweet indexing and search
- **Backend**: Python with FastAPI
- **Frontend**: Flask with Bootstrap, Chart.js, and Leaflet
- **Containers**: Docker for containerization
- **Orchestration**: Kubernetes for deployment and scaling

## Getting Started

### Local Development with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Access the dashboard
open http://localhost:5000