FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p static/css templates

# Copy application files
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Environment variables - Set default to container service name
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV API_URL=http://tweet-api:8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
