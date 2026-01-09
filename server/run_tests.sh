#!/bin/bash

# Test runner for AMS2 web server

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup.sh first..."
    bash setup.sh
fi

source venv/bin/activate

echo "Running AMS2 Web Server Tests..."
echo "================================"
echo ""

# Run pytest with verbose output
pytest -v

# Capture exit code
exit_code=$?

echo ""
echo "================================"
if [ $exit_code -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed (exit code: $exit_code)"
fi

exit $exit_code
