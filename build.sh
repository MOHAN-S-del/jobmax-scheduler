#!/bin/bash

# Build script for C++ scheduler

if ! command -v cmake &> /dev/null; then
    echo "❌ CMake not found. Installing..."
    brew install cmake
fi

echo "🔨 Building scheduler..."
mkdir -p build
cd build
cmake ..
make

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📍 Executable: ./build/scheduler"
    chmod +x scheduler
else
    echo "❌ Build failed!"
    exit 1
fi
