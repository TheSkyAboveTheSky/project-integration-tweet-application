#!/bin/bash

echo "🚀 Opening Kubernetes Dashboard..."

# Make sure Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "❌ Error: Minikube is not running."
    echo "   Please start it with: ./k8s/setup-local.sh"
    exit 1
fi

# Make sure the dashboard addon is enabled
if ! minikube addons list | grep dashboard | grep -q enabled; then
    echo "🔧 Enabling Kubernetes Dashboard..."
    minikube addons enable dashboard
fi

# Create an admin user for better access
if ! kubectl get serviceaccount admin-user -n kube-system &>/dev/null; then
    echo "👤 Creating admin service account..."
    kubectl create serviceaccount admin-user -n kube-system
    kubectl create clusterrolebinding admin-user --clusterrole=cluster-admin --serviceaccount=kube-system:admin-user
fi

# Create a token for authentication
echo "🔑 Creating dashboard access token..."
TOKEN=$(kubectl create token admin-user -n kube-system --duration=24h)

echo ""
echo "🎫 Here's your token for dashboard login (copy this):"
echo "------------------------------------------------------"
echo "$TOKEN"
echo "------------------------------------------------------"
echo ""

# Open the dashboard
echo "🌐 Opening the Kubernetes Dashboard in your browser..."
minikube dashboard
