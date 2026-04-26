# ── Base image ────────────────────────────────────────────────────────────────
# Python 3.6.13 slim — matches your development environment exactly
FROM python:3.6.13-slim

# ── Metadata ──────────────────────────────────────────────────────────────────
LABEL maintainer="Khelina Fedorchuk <khelina.fedorchuk@gmail.com>"
LABEL description="DeepKymoTracker: automated T cell tracking and segmentation"
LABEL paper="https://doi.org/10.1371/journal.pone.0315947"
LABEL github="https://github.com/khelina/T-cell-lineages-tracking"

# ── System dependencies ───────────────────────────────────────────────────────
# libglib2.0-0, libsm6, libxext6, libxrender1: required for OpenCV and display
# libgomp1: required for TensorFlow parallel processing
# tk, python3-tk: required for Tkinter GUI
# libgl1: required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    tk \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ───────────────────────────────────────────────────────
# Install in specific order — numpy first as everything depends on it
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir \
    numpy==1.16.4

RUN pip install --no-cache-dir \
    tensorflow==1.15.0

RUN pip install --no-cache-dir \
    keras==2.3.1 \
    h5py==2.10.0

RUN pip install --no-cache-dir \
    opencv-python-headless==3.4.18.65

RUN pip install --no-cache-dir \
    xlsxwriter==3.0.3 \
    tifffile==2020.10.1 \
    pillow \
    matplotlib \
    imagecodecs

# ── Application structure ─────────────────────────────────────────────────────
# Create the main application folder — this is software_folder
WORKDIR /app

# Copy SOURCE_CODE folder with all Python files
COPY SOURCE_CODE/ /app/SOURCE_CODE/

# Create empty TRAINED MODELS and MOVIES folders
# Note: folder name has a space — use quotes
RUN mkdir -p "/app/TRAINED MODELS"
RUN mkdir -p "/app/MOVIES"

# ── Display environment ───────────────────────────────────────────────────────
ENV DISPLAY=:0

# ── Default command ───────────────────────────────────────────────────────────
# Run from SOURCE_CODE folder so relative imports work correctly
WORKDIR /app/SOURCE_CODE
CMD ["python", "GUI_launch.py"]
