#!/bin/bash

# Build script for AMS2 Race Recorder

echo "Building AMS2 Race Recorder..."

# Create build directory if it doesn't exist
if [ ! -d "../build" ]; then
    mkdir ../build
fi

cd ../build

# Run CMake configuration
cmake ../recorder -DCMAKE_BUILD_TYPE=Release

# Build the project
cmake --build . --config Release

if [ $? -eq 0 ]; then
    echo "Build completed successfully!"
    echo "Executable: $(pwd)/bin/ams2_recorder"
else
    echo "Build failed!"
    exit 1
fi
