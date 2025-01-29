#!/bin/bash
# Simple script to run the tweet processor locally

echo "Starting tweet processor..."

# Check for virtual environment and activate if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment"
fi

# Run the processor with the new path
python src/main.py

# Deactivate venv when done
if [ -d "venv" ]; then
    deactivate
fi
