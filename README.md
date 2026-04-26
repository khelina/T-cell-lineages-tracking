# DeepKymoTracker

An end-to-end deep learning pipeline for automated tracking, segmentation,
and lineage reconstruction of highly motile cells in time-lapse microscopy.

**Published in PLOS ONE (2025):**
https://doi.org/10.1371/journal.pone.0315947

---

## Quick Links

- [Output demo video](https://youtu.be/9nSulQDEles)
- [5-minute conference presentation](https://www.youtube.com/watch?v=NebOgh1q0kc)
- [Video tutorial series](https://youtube.com/playlist?list=PLF7yuSFLLabDfAgING0tK6rLZitfkkXcJ&si=KFzx-8Sb8rjMEmVg)
- [PLOS ONE paper](https://doi.org/10.1371/journal.pone.0315947)
- [User Guide PDF](User_Guide/YOUR_GUIDE_FILENAME.pdf)
- [Docker Hub](https://hub.docker.com/r/khelinafedorchuk/deepkymotracker)

---

## What DeepKymoTracker Does

DeepKymoTracker automatically tracks and segments T lymphocytes across
thousands of microscopy frames, constructing complete cell lineage trees
with minimal manual intervention. For each tracked cell in each frame,
it extracts centroid coordinates, area, perimeter, circularity, and
average fluorescent intensity across all imaging channels.

Central to the pipeline is a novel 3D CNN architecture — to the best of
our knowledge the first application of 3D CNNs to cell tracking — that
integrates detection and association into a single unified step,
eliminating the error-prone two-step tracking-by-detection paradigm
used by conventional tools.

**Benchmarking results (Cell Tracking Challenge methodology):**
Outperformed CellPose, DeepCell, Ilastik, and Weka+TrackMate on
tracking, detection, and segmentation metrics — while running ten
times faster than CellPose.

---

## Which Version Should I Use?

| Version | Folder | Purpose |
|---|---|---|
| **Full version** | `DeepKymoTracker_full` | Use this for analysing your own data |
| **Paper version** | `DeepKymoTracker_paper` | Use this to reproduce PLOS ONE results |

**If you are new to DeepKymoTracker, start with `DeepKymoTracker_full`.**

---

## Pipeline Overview

DeepKymoTracker processes cell movies in five sequential steps:

| Step | Name | Description |
|---|---|---|
| 1 | Extract Movie | Extracts and reformats a chosen movie from a folder of acquisitions |
| 2 | Cut Well | Crops a single well from each frame for analysis |
| 3 | Track & Correct | Automated tracking, segmentation, and division detection with real-time manual correction |
| 4 | Correct Segmentation | Manual correction of segmentation errors after tracking |
| 5 | Visualise Results | Dynamic frame-by-frame visualisation of cell properties and lineage |

**Note:** Use the EXIT button to move between steps rather than the
Back/Next buttons, to avoid out-of-memory errors.

For detailed instructions see the
[User Guide PDF](User_Guide/YOUR_GUIDE_FILENAME.pdf) or the
[video tutorial series](https://youtube.com/playlist?list=PLF7yuSFLLabDfAgING0tK6rLZitfkkXcJ&si=KFzx-8Sb8rjMEmVg).

---

## Installation

### Option 1 — Docker (Linux only)

Docker eliminates all installation complexity on Linux systems.
The entire environment — Python, TensorFlow, all dependencies —
is pre-configured inside the container.

> **Note:** Docker support is currently available for Linux only.
> Mac and Windows Docker support is under development.
> Mac and Windows users please use Option 2 (manual installation).

**Prerequisites:**
1. Install [Docker](https://docs.docker.com/engine/install/)
2. Download trained model files from
   [Zenodo](https://doi.org/10.5281/zenodo.11540886) (1.7 GB)
   and place them in a folder on your computer
3. Have your raw microscope movies accessible in a folder
4. Create an empty folder for processed output movies

**Pull the container (one time only):**
```bash
docker pull khelinafedorchuk/deepkymotracker:latest
```

**Run using the launcher script:**

Download `launchers/run_deepkymotracker.sh` from this repository.

Make it executable:
```bash
chmod +x run_deepkymotracker.sh
```

Run it:
```bash
./run_deepkymotracker.sh
```

The script will ask you for three folder paths:
- **Raw movies folder** — your large folder of raw microscope acquisitions
- **Trained models folder** — where you placed the Zenodo model files
- **Working movies folder** — where processed output will be saved

DeepKymoTracker will then launch automatically.

---

### Option 2 — Manual Installation (All platforms)

**Minimum requirements:**
Python = 3.6.13
TensorFlow = 1.15.0 (or tensorflow-gpu = 1.14.0 if you have a GPU)
Keras = 2.3.1
OpenCV = 3.3.1
h5py = 2.10.0
xlsxwriter = 3.0.3
tifffile = 2020.9.3
pillow (any version)
matplotlib (any version)
imagecodecs
A complete list of conda installation commands is provided in
`Instructions_for_anaconda_packages.txt` inside each folder.

After installation:
1. Download trained model files from
   [Zenodo](https://doi.org/10.5281/zenodo.11540886) (1.7 GB)
2. Place model files in the `TRAINED MODELS` folder
3. Run `GUI_launch.py`

---

## Quick Start (Docker — Linux)

1. Install Docker
2. Pull the container: `docker pull khelinafedorchuk/deepkymotracker:latest`
3. Download model files from [Zenodo](https://doi.org/10.5281/zenodo.11540886)
4. Download the launcher script from `launchers/run_deepkymotracker.sh`
5. Make it executable: `chmod +x run_deepkymotracker.sh`
6. Run it: `./run_deepkymotracker.sh`
7. Follow the prompts

## Quick Start (Manual — All platforms)

1. Install dependencies (see Option 2 above)
2. Download model files from [Zenodo](https://doi.org/10.5281/zenodo.11540886)
3. Place model files in the `TRAINED MODELS` folder
4. Run `GUI_launch.py`

---

## Frequently Asked Questions

**Can DeepKymoTracker handle more than one cell in the first frame?**
Yes. In Step 3 you will be asked to manually assign the starting
positions of each cell by clicking on them.

**Can I track only a subset of cells in a movie?**
Yes. Click only the cells you are interested in when assigning
starting positions in the first frame.

**Can I track only a section of a movie rather than the whole thing?**
Yes. You can extract any consecutive sequence of frames and apply
DeepKymoTracker to that section.

**Can I interrupt tracking and resume later?**
Yes. Press PAUSE then EXIT — results are saved automatically.
When you relaunch, the interface will ask if you want to continue
from where you left off.

**Can I interrupt manual segmentation correction and resume later?**
Yes. Step 4 is designed to be used across multiple sessions.

**Do I need to monitor tracking in real time?**
It is the most efficient approach. If you leave the algorithm running
unattended and discover an error in Frame 1000 after 3000 frames have
been processed, the algorithm must retrack from Frame 1000 onwards.
If you cannot monitor continuously, use PAUSE and EXIT to save your
progress and resume later.

**Where do I find the tracked output movie?**
Three options are available:
- Frame-by-frame: folders TRACKED_BRIGHTFIELD_CHANNEL,
  TRACKED_GREEN_FL_CHANNEL, TRACKED_RED_FL_CHANNEL
- As a movie: `lineage_movie.avi` (brightfield + lineage tree)
- In the interface: reload the movie in Step 3 to scroll through
  tracked frames

**Where are my results saved?**
All output folders, Excel files, and movies are saved inside your
Working Movies Folder — the folder you specified when launching
the script. They remain on your computer after Docker closes.

---

## Known Limitations & Data Requirements

DeepKymoTracker was trained on high-quality fluorescence microscopy
data from an Olympus IX71 inverted microscope with EM-CCD camera.
Performance is best on data with similar characteristics:

- **Image quality:** Performance degrades on lower resolution or
  higher background noise images. Retraining the segmentation network
  on representative images is recommended for new microscope data.
- **Cell density:** Currently validated on movies with up to 5 cells
  per frame. Higher density environments are under active development.
- **Occlusions:** Occlusion detection is automated but occlusion
  segmentation requires manual correction in Step 4.
- **Cell death and new cell emergence:** Currently require manual
  correction using the REMOVE CELL and ADD CELL buttons in Step 3.
- **Docker:** Currently supported on Linux only. Mac and Windows
  Docker support is under development.

---

## Repository Structure
DeepKymoTracker/
│
├── Dockerfile                      Container definition (Linux)
├── DeepKymoTracker_full/           Main source code for your own data
├── DeepKymoTracker_paper/          Paper-specific version
├── MODELS/                         Training code and data samples
├── User_Guide/                     PDF user guide
└── launchers/
├── run_deepkymotracker.sh      Linux launcher (Docker)
├── run_deepkymotracker_mac.sh  Mac — Docker coming soon
└── run_deepkymotracker.bat     Windows — Docker coming soon
---

## Algorithm Overview

DeepKymoTracker uses three neural network modules in sequence:

**Tracking** — A 3D CNN processes 4-frame clips, treating the temporal
dimension equivalently to spatial dimensions. A seed channel transmits
cell identity between clips, preventing identity swaps at transitions.

**Segmentation** — A two-network ensemble (Segmentor + Refiner), both
based on U-Net architecture, segments patches centred on tracked
centroids. The ensemble approach improved segmentation IoU from 82%
to 94%.

**Division Detection** — Classical computer vision detects pre- and
post-division cell shapes, triggering automatic tracker switching.

For full technical details see the
[PLOS ONE paper](https://doi.org/10.1371/journal.pone.0315947).

---

## Contact

Khelina Fedorchuk, PhD
khelina.fedorchuk@gmail.com
[LinkedIn](YOUR LINKEDIN URL)

Found a bug or need help? Open a GitHub Issue or email directly.

 




