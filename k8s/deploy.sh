#!/bin/bash
set -e

echo "🚀 Deploying Tweet Analytics platform to Kubernetes..."

# Make sure Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "❌ Error: Minikube is not running. Please run:"
    echo "   ./k8s/setup-local.sh"
    exit 1
fi

# Create namespace if it doesn't exist
kubectl apply -f namespace.yaml

# Deploy infrastructure components first
echo "🏗️ Deploying infrastructure components..."
echo "   - Zookeeper (for Kafka)"
kubectl apply -f zookeeper.yaml

echo "   - Kafka (message broker)"
kubectl apply -f kafka.yaml

echo "   - Elasticsearch (data storage)"
kubectl apply -f elasticsearch.yaml

echo "   - Kibana (data visualization)"
kubectl apply -f kibana.yaml

echo "   - JSON Server (mock data)"
kubectl apply -f json-server.yaml

# Give some time for infrastructure to initialize
echo ""
echo "⏳ Waiting for infrastructure to initialize (30 seconds)..."
sleep 30

# Deploy application components
echo ""
echo "🏗️ Deploying application components..."
echo "   - Tweet API"
kubectl apply -f tweet-api.yaml

echo "   - Tweet Frontend"
kubectl apply -f tweet-frontend.yaml

echo "   - Tweet Collector"
kubectl apply -f tweet-collector.yaml

echo "   - Tweet Processor"
kubectl apply -f tweet-processor.yaml

# Show the current status
echo ""
echo "✅ Deployment complete! Here's what's running:"
kubectl get pods -n tweet-analytics

# Display access information
MINIKUBE_IP=$(minikube ip)
echo ""
echo "🌐 To access the services, run:"
echo "   ./k8s/port-forward.sh"
echo ""
echo "📋 This will make the services available at:"
echo "   - Frontend: http://localhost:5000"
echo "   - API: http://localhost:8000"
echo "   - Kibana: http://localhost:5601"
