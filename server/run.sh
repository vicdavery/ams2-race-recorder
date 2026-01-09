#!/bin/bash

# Run script for AMS2 Race Results Web Server

# Parse command line arguments
PORT=5000
HOST="0.0.0.0"
DATABASE=""
DEBUG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        -db|--database)
            DATABASE="--database $2"
            shift 2
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        -h|--help)
            echo "Usage: run.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -p, --port PORT        Port to run server on (default: 5000)"
            echo "  --host HOST            Host address to bind to (default: 0.0.0.0)"
            echo "  -db, --database FILE   Database file path"
            echo "  --debug                Run in debug mode"
            echo "  -h, --help             Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./run.sh                               # Run on port 5000"
            echo "  ./run.sh --port 8000                   # Run on port 8000"
            echo "  ./run.sh -db sample_races.db           # Use sample database"
            echo "  ./run.sh -p 3000 -db races.db --debug  # Custom DB and debug"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh first..."
    bash setup.sh
fi

source venv/bin/activate

# Run the Flask app
echo ""
python3 app.py --port "$PORT" --host "$HOST" $DATABASE $DEBUG
