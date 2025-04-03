#!/bin/bash

# Check if the user provided a component name
if [ -z "$1" ]; then
    echo "📋 Usage: $0 <component-name> [number-of-lines]"
    echo ""
    echo "   Examples:"
    echo "     ./k8s/logs.sh tweet-processor     (shows last 50 lines by default)"
    echo "     ./k8s/logs.sh tweet-api 100       (shows last 100 lines)"
    echo ""
    echo "   Available components:"
    echo "     tweet-api, tweet-frontend, tweet-collector, tweet-processor,"
    echo "     elasticsearch, kafka, zookeeper, json-server, kibana"
    exit 1
fi

COMPONENT=$1
LINES=${2:-50}  # Default to 50 lines if not specified

# Find the pod for the specified component
POD=$(kubectl get pods -n tweet-analytics | grep "$COMPONENT" | awk '{print $1}' | head -n 1)

if [ -z "$POD" ]; then
    echo "❌ Error: No pod found for component '$COMPONENT'"
    echo ""
    echo "📋 Available pods:"
    kubectl get pods -n tweet-analytics
    exit 1
fi

echo "🔍 Showing logs for pod: $POD (last $LINES lines)"
echo "   Press Ctrl+C to exit"
echo "------------------------------------------------------"

# Show the logs with follow mode enabled
kubectl logs -f --tail="$LINES" -n tweet-analytics "$POD"
