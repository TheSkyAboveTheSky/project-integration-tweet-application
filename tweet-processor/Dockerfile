FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .
COPY config.ini .

# Copy application code
COPY src/ ./src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for Elasticsearch interactions
RUN apt-get update && apt-get install -y curl && apt-get clean

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ES_HOST=elasticsearch:9200
ENV ES_INDEX=tweets
ENV CONTINUOUS_MODE=true
ENV PROCESSING_INTERVAL=60

# Run the processor with the new path
CMD ["python", "src/main.py"]
