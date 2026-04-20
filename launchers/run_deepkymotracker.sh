#!/bin/bash

echo "========================================"
echo "       DeepKymoTracker Launcher"
echo "       Linux version"
echo "========================================"
echo ""
echo "This script will launch DeepKymoTracker inside a Docker container."
echo "You will need to provide paths to three folders."
echo ""

# ── Step 1 — Raw Movies Folder ────────────────────────────────────────────────
echo "Step 1 of 3: Raw Movies Folder"
echo "This is the large folder containing your raw microscope movies."
echo "DeepKymoTracker Step 1 will extract movies from here."
echo "Example: /home/username/microscope_data"
echo ""
read -p "Raw movies folder path: " raw_movies_path

if [ ! -d "$raw_movies_path" ]; then
    echo ""
    echo "ERROR: Folder not found: $raw_movies_path"
    echo "Please check the path and try again."
    exit 1
fi

echo ""

# ── Step 2 — Trained Models Folder ───────────────────────────────────────────
echo "Step 2 of 3: Trained Models Folder"
echo "This is the folder containing the model files downloaded from Zenodo."
echo "Download models from: https://doi.org/10.5281/zenodo.11540886"
echo "Example: /home/username/deepkymotracker_models"
echo ""
read -p "Trained models folder path: " models_path

if [ ! -d "$models_path" ]; then
    echo ""
    echo "ERROR: Folder not found: $models_path"
    echo "Please check the path and try again."
    exit 1
fi

echo ""

# ── Step 3 — Working Movies Folder ───────────────────────────────────────────
echo "Step 3 of 3: Working Movies Folder"
echo "This is where DeepKymoTracker will save processed movies and results."
echo "Output folders and Excel files will appear here after tracking."
echo "Example: /home/username/deepkymotracker_output"
echo ""
read -p "Working movies folder path: " movies_path

if [ ! -d "$movies_path" ]; then
    echo ""
    echo "ERROR: Folder not found: $movies_path"
    echo "Shall we create it for you? (y/n)"
    read -p "" create_folder
    if [ "$create_folder" = "y" ] || [ "$create_folder" = "Y" ]; then
        mkdir -p "$movies_path"
        echo "Folder created: $movies_path"
    else
        echo "Please create the folder and try again."
        exit 1
    fi
fi

echo ""

# ── Launch ────────────────────────────────────────────────────────────────────
echo "========================================"
echo "Starting DeepKymoTracker..."
echo "========================================"
echo ""
echo "Raw movies:     $raw_movies_path"
echo "Trained models: $models_path"
echo "Working folder: $movies_path"
echo ""

xhost +local:docker 2>/dev/null

docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "$raw_movies_path":/app/RAW_MOVIES \
           -v "$models_path":/app/"TRAINED MODELS" \
           -v "$movies_path":/app/MOVIES \
           khelinafedorchuk/deepkymotracker:latest

echo ""
echo "DeepKymoTracker has closed."
echo "Your results are saved in: $movies_path"
