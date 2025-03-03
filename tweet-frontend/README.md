# Tweet Frontend

Flask-based web application for visualizing tweet analytics.

## Features

- Real-time dashboard with charts for hashtag trends, sentiment analysis, and geographic distribution
- Interactive tweet browser with filtering capabilities
- Geographic visualization of tweets on a map
- Responsive design for desktop and mobile devices

## Technology Stack

- Flask: Python web framework
- Chart.js: JavaScript charting library
- Leaflet.js: Interactive mapping library
- Bootstrap 5: UI framework

## Setup

### Prerequisites
- Python 3.8+
- Tweet API running and accessible

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run --host=0.0.0.0 --port=5000
   ```

3. Access the application at http://localhost:5000

## Application Views

- Dashboard: Overview of tweet analytics with charts and statistics
- Tweets: Browse and search through the collected tweets
- Map: Visualize tweet locations on an interactive map
