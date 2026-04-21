#!/bin/bash

echo "========================================"
echo "       DeepKymoTracker Launcher"
echo "       Linux version"
echo "========================================"
echo ""
echo "This script will launch DeepKymoTracker inside a Docker container."
echo "You will need to provide paths to three folders."
echo ""

# ── Step 1 — Trained Models Folder ───────────────────────────────────────────
echo "Step 1 of 3: Trained Models Folder"
echo "This is the folder containing the model files downloaded from Zenodo."
echo "Download models from: https://doi.org/10.5281/zenodo.11540886"
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

# ── Step 2 — Raw Microscope Movies Folder ────────────────────────────────────
echo "Step 2 of 3: Raw Microscope Movies Folder"
echo "This is the folder containing your raw microscope movie acquisitions."
echo "DeepKymoTracker Step 1 will extract movies from here."
echo "Example: /home/username/RAW_MICROSCOPE_MOVIES"
echo ""
read -p "Raw microscope movies folder path: " raw_path

if [ ! -d "$raw_path" ]; then
    echo ""
    echo "Folder not found: $raw_path"
    echo "Shall we create it for you? (y/n)"
    read -p "" create_raw
    if [ "$create_raw" = "y" ] || [ "$create_raw" = "Y" ]; then
        mkdir -p "$raw_path"
        echo "Folder created: $raw_path"
        echo "Please place your raw microscope movie folders inside:"
        echo "$raw_path"
        echo "Then relaunch this script."
        exit 0
    else
        echo "Please create the folder and try again."
        exit 1
    fi
fi

echo ""

# ── Step 3 — Working Movies Folder ───────────────────────────────────────────
echo "Step 3 of 3: Working Movies Folder"
echo "This is where DeepKymoTracker will save all processed movies and results."
echo "Output folders and Excel files will appear here after tracking."
echo "Example: /home/username/MOVIES"
echo ""
read -p "Working movies folder path: " movies_path

if [ ! -d "$movies_path" ]; then
    echo ""
    echo "Folder not found: $movies_path"
    echo "Shall we create it for you? (y/n)"
    read -p "" create_movies
    if [ "$create_movies" = "y" ] || [ "$create_movies" = "Y" ]; then
        mkdir -p "$movies_path"
        echo "Folder created: $movies_path"
    else
        echo "Please create the folder and try again."
        exit 1
    fi
fi

echo ""

# ── Summary before launch ─────────────────────────────────────────────────────
echo "========================================"
echo "Ready to launch DeepKymoTracker with:"
echo "========================================"
echo ""
echo "Trained models:          $models_path"
echo "Raw microscope movies:   $raw_path"
echo "Working movies folder:   $movies_path"
echo ""

# ── Check models are present ──────────────────────────────────────────────────
if [ -z "$(ls -A "$models_path")" ]; then
    echo "WARNING: Your trained models folder appears to be empty."
    echo "DeepKymoTracker will launch but will remind you to download"
    echo "model files from: https://doi.org/10.5281/zenodo.11540886"
    echo ""
fi

# ── Enable display ────────────────────────────────────────────────────────────
xhost +local:docker 2>/dev/null

# ── Launch container ──────────────────────────────────────────────────────────
echo "Starting DeepKymoTracker..."
echo ""

docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "$models_path":/app/"TRAINED MODELS" \
           -v "$raw_path":/app/RAW_MICROSCOPE_MOVIES \
           -v "$movies_path":/app/MOVIES \
           khelinafedorchuk/deepkymotracker:latest

echo ""
echo "========================================"
echo "DeepKymoTracker has closed."
echo "Your results are saved in:"
echo "$movies_path"
echo "========================================"
