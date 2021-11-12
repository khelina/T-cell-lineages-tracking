# T-cell-lineages-tracking
This is my ML project on tracking T cell lineages in microscopic movies. Here is the description of the contents of this repository:
1. TRACK-4.py. This is a 3D CNN for tracking sections of a movie containing 4 cells. The inputs are 4-frame clips of fluorescent 382 x 382 images.The labels are lists of the centroids of all the cells present in this clip.
2. SEGMENTOR.py. This is a U-Net for segmentation. The inputs are 96 x 96 images comprising 3 channels: fluorescent, bright field and artificial. Tha artificial channel is a binary image containing a marker (40 x 40 square) which points to the cell of interest )in the fluorescent and bright field channels) by having the largest overlap with it. The labels (outputs) are binary i96 x 96 images where the cell of interest is segmented only - ohter cells, or their fragemnets are ignored by SEGMENTOR.  
3. DIVISION DETECTOR.py
4. EXECUTION.py
5. An example of a training sample for TRACK-4.py
6. An example of a training sample for SEGMENTOR.py
7. An example of the result of applying thos algorithm to a test movie.
