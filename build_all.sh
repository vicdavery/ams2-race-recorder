#!/bin/bash

# Build script for entire AMS2 project (recorder + server)

echo "Building AMS2 Race Recorder System..."
echo "======================================"
echo ""

# Build C++ recorder
echo "1. Building C++ Race Recorder..."
cd recorder
bash build.sh

if [ $? -ne 0 ]; then
    echo "Failed to build recorder!"
    exit 1
fi

cd ..
echo ""

# Setup Python server
echo "2. Setting up Python Web Server..."
cd server
bash setup.sh

if [ $? -ne 0 ]; then
    echo "Failed to setup server!"
    exit 1
fi

cd ..
echo ""
echo "======================================"
echo "Build complete!"
echo ""
echo "Next steps:"
echo "1. Start the recorder:"
echo "   cd recorder && ../build/bin/ams2_recorder"
echo ""
echo "2. In another terminal, start the web server:"
echo "   cd server && bash run.sh"
echo ""
echo "3. Open http://localhost:5000 in your browser"
