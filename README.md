# Tweet Analytics Platform

A real-time tweet analysis platform with collection, processing, visualization, and Kubernetes deployment capabilities.

## Architecture

This project implements a complete data pipeline for tweet analytics:

1. **Tweet Collector**: Collects tweets from a mock API and sends them to Kafka
2. **Tweet Processor**: Processes tweets with sentiment analysis and feature extraction
3. **Tweet API**: REST API serving processed tweet data from Elasticsearch
4. **Tweet Frontend**: Web dashboard for visualizing tweet analytics

## Components

Each component is designed to run as a standalone containerized microservice and is configured to work together in a Kubernetes cluster.

## Local Development

For local development, a docker-compose setup is provided to quickly spin up all necessary services.
