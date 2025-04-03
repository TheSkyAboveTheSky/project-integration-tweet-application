#!/bin/bash
set -e

echo "🏗️ Building Docker images for our Tweet Analytics platform..."

# Make sure Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "❌ Error: Minikube is not running. Please start it first with:"
    echo "   ./k8s/setup-local.sh"
    exit 1
fi

# Set Docker to use Minikube's Docker daemon (keeps images inside Minikube)
echo "🔄 Configuring Docker to use Minikube's daemon..."
eval $(minikube docker-env)

# Build all our application images
echo "🔨 Building tweet-collector image..."
docker build -t tweet-collector:latest -f ../tweet-collector/Dockerfile ../tweet-collector

echo "🔨 Building tweet-processor image..."
docker build -t tweet-processor:latest -f ../tweet-processor/Dockerfile ../tweet-processor

echo "🔨 Building tweet-api image..."
docker build -t tweet-api:latest -f ../tweet-api/Dockerfile ../tweet-api

echo "🔨 Building tweet-frontend image..."
docker build -t tweet-frontend:latest -f ../tweet-frontend/Dockerfile ../tweet-frontend

# Show what we've built
echo ""
echo "✅ Build complete! Here are the new images:"
docker images | grep -E 'tweet-(collector|processor|api|frontend)'

echo ""
echo "📋 Next step: Deploy to Kubernetes with ./k8s/deploy.sh"
