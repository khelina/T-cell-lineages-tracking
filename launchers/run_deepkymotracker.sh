#!/bin/bash

echo "========================================"
echo "       DeepKymoTracker Launcher"
echo "       Linux version"
echo "========================================"
echo ""

# ── Create standard data folder structure automatically ───────────────────────
DATA_DIR="$HOME/DeepKymoTracker_data"
MODELS_DIR="$DATA_DIR/TRAINED MODELS"
RAW_DIR="$DATA_DIR/RAW_MICROSCOPE_MOVIES"
MOVIES_DIR="$DATA_DIR/MOVIES"

mkdir -p "$MODELS_DIR"
mkdir -p "$RAW_DIR"
mkdir -p "$MOVIES_DIR"

echo "Your DeepKymoTracker data folder:"
echo "$DATA_DIR"
echo ""
echo "It contains three subfolders:"
echo "  TRAINED MODELS       — place model files from Zenodo here"
echo "  RAW_MICROSCOPE_MOVIES — place your raw movie folders here"
echo "  MOVIES               — processed results will appear here"
echo ""

# ── Check models are present ──────────────────────────────────────────────────
if [ -z "$(ls -A "$MODELS_DIR")" ]; then
    echo "WARNING: TRAINED MODELS folder is empty."
    echo "Please download model files from Zenodo:"
    echo "https://doi.org/10.5281/zenodo.11540886"
    echo "and place them in:"
    echo "$MODELS_DIR"
    echo ""
    read -p "Press Enter to launch anyway or Ctrl+C to exit: "
fi

# ── Check raw movies are present ──────────────────────────────────────────────
if [ -z "$(ls -A "$RAW_DIR")" ] && [ -z "$(ls -A "$MOVIES_DIR")" ]; then
    echo "NOTE: No movies found yet."
    echo "Place your raw microscope movie folders in:"
    echo "$RAW_DIR"
    echo ""
    read -p "Press Enter to launch anyway or Ctrl+C to exit: "
fi

# ── Enable display ────────────────────────────────────────────────────────────
xhost +local:docker 2>/dev/null

# ── Launch container ──────────────────────────────────────────────────────────
echo ""
echo "Starting DeepKymoTracker..."
echo ""

docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "$MODELS_DIR":/app/"TRAINED MODELS" \
           -v "$RAW_DIR":/app/RAW_MICROSCOPE_MOVIES \
           -v "$MOVIES_DIR":/app/MOVIES \
           khelinafedorchuk/deepkymotracker:latest

echo ""
echo "========================================"
echo "DeepKymoTracker has closed."
echo "Your results are saved in:"
echo "$MOVIES_DIR"
echo "========================================"
