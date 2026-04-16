---

## Algorithm Overview

DeepKymoTracker uses three neural network modules in sequence:

**Tracking** — A 3D CNN processes 4-frame clips, treating the temporal
dimension equivalently to spatial dimensions. A seed channel transmits
cell identity between clips, preventing identity swaps at transitions.

**Segmentation** — A two-network ensemble (Segmentor + Refiner), both
based on U-Net architecture, segments patches centred on tracked
centroids. The ensemble approach improved the segmentation IoU from 82%
to 94%.

**Division Detection** — Classical computer vision detects pre- and
post-division cell shapes, triggering automatic tracker switching.

For full technical details, see the
[PLOS ONE paper](https://doi.org/10.1371/journal.pone.0315947).

---

## Contact

Khelina Fedorchuk, PhD
khelina.fedorchuk@gmail.com
[LinkedIn](YOUR LINKEDIN URL)

Found a bug or need help? Open a GitHub Issue or email directly.










 




