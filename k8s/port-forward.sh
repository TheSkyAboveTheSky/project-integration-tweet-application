#!/bin/bash

echo "🌐 Starting port forwarding for all services..."
echo "   Press Ctrl+C to stop"

# Make sure we're using the tweet-analytics namespace
if ! kubectl get namespace tweet-analytics &>/dev/null; then
    echo "❌ Error: tweet-analytics namespace doesn't exist."
    echo "   Have you deployed the application? Try:"
    echo "   ./k8s/deploy.sh"
    exit 1
fi

# Start port forwarding for our main services
echo "🔗 Setting up port forwarding for tweet-frontend (http://localhost:5000)"
kubectl port-forward -n tweet-analytics svc/tweet-frontend 5000:80 &
FRONTEND_PID=$!

echo "🔗 Setting up port forwarding for tweet-api (http://localhost:8000)"
kubectl port-forward -n tweet-analytics svc/tweet-api 8000:8000 &
API_PID=$!

echo "🔗 Setting up port forwarding for Kibana (http://localhost:5601)"
kubectl port-forward -n tweet-analytics svc/kibana 5601:5601 &
KIBANA_PID=$!

# Show access URLs
echo ""
echo "✅ All services are now available locally at:"
echo "   - Frontend: http://localhost:5000"
echo "   - API: http://localhost:8000"
echo "   - Kibana: http://localhost:5601"
echo ""
echo "🔍 Port forwarding is active. Press Ctrl+C to stop all port forwards."

# Make sure we cleanup on exit
function cleanup {
    echo ""
    echo "🛑 Stopping all port forwarding..."
    kill $FRONTEND_PID $API_PID $KIBANA_PID 2>/dev/null
    echo "✅ Port forwarding stopped."
}

trap cleanup EXIT

# Wait until the user presses Ctrl+C
wait
