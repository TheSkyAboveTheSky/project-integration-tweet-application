#!/bin/bash
set -e

echo "🚀 Setting up local Kubernetes environment with Minikube..."

# First, check if the required tools are installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Error: minikube is not installed. Please install it first."
    echo "   Visit: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl is not installed. Please install it first."
    echo "   Visit: https://kubernetes.io/docs/tasks/tools/install-kubectl/"
    exit 1
fi

# Start Minikube if it's not already running
if ! minikube status | grep -q "Running"; then
    echo "🔄 Starting Minikube with 2 CPUs and 4GB RAM..."
    minikube start --cpus=2 --memory=4096 --driver=docker
else
    echo "✅ Minikube is already running."
fi

# Enable the Kubernetes dashboard for easier management
echo "🔧 Enabling Kubernetes dashboard..."
minikube addons enable dashboard

# Create the namespace for our application
echo "🏗️ Creating tweet-analytics namespace..."
kubectl apply -f namespace.yaml

# Show the Minikube IP for hosts file setup
MINIKUBE_IP=$(minikube ip)
echo ""
echo "✅ Setup complete! Minikube is running at IP: ${MINIKUBE_IP}"
echo ""
echo "📝 For local development with port-forwarding, no hosts file changes are needed."
echo "   Use ./k8s/port-forward.sh to access services."
echo ""
echo "🔍 To check Minikube status, run: minikube status"
