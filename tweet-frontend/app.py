from flask import Flask, render_template, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration - Use container hostname
API_URL = os.environ.get('API_URL', 'http://tweet-api:8000')

# Add current datetime and API URL to all templates
@app.context_processor
def inject_globals():
    return {
        'now': datetime.now(),
        'api_url': API_URL
    }

@app.route('/')
def index():
    """Render the dashboard page."""
    return render_template('dashboard.html')

@app.route('/tweets')
def tweets():
    """Render the tweets page."""
    return render_template('tweets.html')

@app.route('/map')
def map_view():
    """Render the map page."""
    return render_template('map.html')

@app.route('/api/trends')
def get_trends():
    """Fetch trending hashtags from the API."""
    try:
        response = requests.get(f"{API_URL}/trends")
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error fetching trends: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sentiment')
def get_sentiment():
    """Fetch sentiment summary from the API."""
    try:
        response = requests.get(f"{API_URL}/sentiment")
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error fetching sentiment: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/regions')
def get_regions():
    """Fetch region data from the API."""
    try:
        response = requests.get(f"{API_URL}/regions")
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error fetching regions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tweets')
def get_tweets():
    """Fetch tweets from the API with optional filtering."""
    try:
        # Forward query parameters
        params = {k: v for k, v in request.args.items()}
        response = requests.get(f"{API_URL}/tweets", params=params)
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error fetching tweets: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/map-data')
def get_map_data():
    """Fetch geo data for map visualization."""
    try:
        # Forward query parameters
        params = {k: v for k, v in request.args.items()}
        response = requests.get(f"{API_URL}/map-data", params=params)
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error fetching map data: {e}")
        return jsonify({"error": str(e)}), 500

@app.template_filter('format_date')
def format_date(value):
    """Format ISO date to readable format."""
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return value

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
