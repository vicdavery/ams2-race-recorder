#!/bin/bash

# Setup script for AMS2 Race Results Web Server

echo "Setting up AMS2 Race Results Web Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To start the server, run:"
echo "  ./run.sh"
