#!/bin/bash

echo "========================================"
echo "       DeepKymoTracker Launcher"
echo "========================================"
echo ""

# Check XQuartz is running
if ! pgrep -x "Xquartz" > /dev/null; then
    echo "XQuartz is not running. Please:"
    echo "1. Install XQuartz from https://www.xquartz.org"
    echo "2. Open XQuartz"
    echo "3. Run this script again"
    exit 1
fi

echo "Step 1 of 2: Trained Models Folder"
echo "This is where you placed the model files"
echo "downloaded from Zenodo."
echo "Example: /Users/username/TRAINED_MODELS"
echo ""
read -p "Trained models folder path: " models_path

if [ ! -d "$models_path" ]; then
    echo ""
    echo "ERROR: Folder not found: $models_path"
    echo "Please check the path and try again."
    exit 1
fi

echo ""
echo "Step 2 of 2: Movies Folder"
echo "This is where your cell movie files are stored."
echo "Example: /Users/username/MOVIES"
echo ""
read -p "Movies folder path: " movies_path

if [ ! -d "$movies_path" ]; then
    echo ""
    echo "ERROR: Folder not found: $movies_path"
    echo "Please check the path and try again."
    exit 1
fi

echo ""
echo "Starting DeepKymoTracker..."
xhost + 127.0.0.1

docker run -e DISPLAY=host.docker.internal:0 \
           -v "$models_path":/app/"TRAINED MODELS" \
           -v "$movies_path":/app/MOVIES \
           khelinafedorchuk/deepkymotracker:latest
