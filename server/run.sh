#!/bin/bash

# Run script for AMS2 Race Results Web Server

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh first..."
    bash setup.sh
fi

source venv/bin/activate

# Run the Flask app
echo "Starting AMS2 Race Results Web Server..."
echo "Open http://localhost:5000 in your browser"
echo ""

python3 app.py
