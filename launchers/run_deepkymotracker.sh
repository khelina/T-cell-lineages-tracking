#!/bin/bash

echo "========================================"
echo "       DeepKymoTracker Launcher"
echo "========================================"
echo ""
echo "Step 1 of 2: Trained Models Folder"
echo "This is where you placed the model files"
echo "downloaded from Zenodo."
echo "Example: /home/username/TRAINED_MODELS"
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
echo "Example: /home/username/MOVIES"
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
xhost +local:docker

docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "$models_path":/app/"TRAINED MODELS" \
           -v "$movies_path":/app/MOVIES \
           khelinafedorchuk/deepkymotracker:latest
