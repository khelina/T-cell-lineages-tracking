# 1. T-cell-tracking-and-segmentation: the main idea and the pipeline
This is my ML project on tracking T cell lineages in microscope movies.A 5-minute poster presentation at ABACBS-2020 Virtual Conference outlining the main idea of the algorithm can be viewed here: https://www.youtube.com/watch?v=NebOgh1q0kc&ab_channel=HelinaFedorchuk.

An example of applying this algorithm to a test movie:
https://www.youtube.com/watch?v=pHPd5FArgYU&ab_channel=HelinaFedorchuk

The purpose of this algorithm is to segment and track T cells in microscope movies, with the ultimate goal of buidling T cell lineages. Currently, this has been achieved for small pedigrees up to 5 cells, without occlusions and dying cells - the issues which are going to be tackled in the near future.
To acieve both segmentation and tracking, a series of deep comnvolutional neaural networks have been trained: 5 CNNs for tracking (Tracker-1,..., Tracker-5) each specialising in a fixed number of cells, according to their names,  and 2 U-Net based deep learning models named Segmentor and Refiner for segmenteing small patches with a tracked cell in the centre cut out of each frame after tracking.

The main innovation of this algorithm is that tracking has been done with 3D CNNs where the inputs are short clips of T cell movies rather than separate frames. The second unconventional is that segmentation is done after tracking.So, the trackers were traned on fluorescent images and as a result, after the centroids of the cells are calculated by a tracker, segmentation neural networks take over and segment small patches described above.
The flow of the algortihm is shown in the picure below:
![image](https://user-images.githubusercontent.com/17193930/188294823-f0d75314-a2fa-4fec-bb47-82150116d443.png) 
Figure-1:
1. The top row: an input cell movie consisting of images with both fluorescent and bright field channels (the size of each image is 382 x 382 pixels).
2. The first clip of 4 frames (fluorescent channel only) is passed through Tracker-1. As a result, we know the centroids of the cell in every frame of the clip now.
 3. Patches of size 96 x 96 (both channels this time) with the tracked cells in the centre are cropped out and fed into the Segmentation Ensemble. The outputs are segmented cells which are binary images of the same size 96 x 96. 
4. Each segmented patch is passed through the Division Detector. It a division is detected then the switch to Tracker-2 occurs.
5. Finally, the segmented patches are pasted into empty black images 382 x 382 according to their locations obtained from Tracker-1. As a result, we obtain the first clip of the output movie (the bottom row).
 6. Go to the next clip and repeat the whole procedure again.
 


# 2. THE CONTENTS OF THIS REPOSITORY
In this repository, you will find 2 folders: EXECUTION and MODELS. 

The EXECUTION folder contains the code for executing  sections of T cell movies containing 4 cells only, without occlusions. The reason why only one section is given is that the files with the weights of the rest of the trackers (Tracker-1, Tracker-2, Tracker-3 and Tracker-5) take up too much memory to be stored somewhere (Tracker-4 weights file is already 1.15 GB).

 The MODELS folder includes 3 files which I used for training Tracker-4, Segmentor and Refiner.

# 3. HOW TO RUN THE ALGORITHM

**Step-1.** Download folder EXECUTION from this repository. It contains 4 python files:

            •	execute-4.py
            •	functions.py
            •	plot.py
            •	postprocess.py


**Step-2.** Download folder DATA from Dropbox: https://www.dropbox.com/scl/fo/ra8a630gxm1ucnm9x7cg3/h?dl=0&rlkey=oxzo3dyj02kd6zt4nq4mxynnx   which contains 2 subfolders: INPUT-T-CELL-MOVIE (132 MB, 796 frames) and TRAINED MODELS (1.38 GB).

**Step-3.** Place DATA folder inside EXECUTION folder.

**Step-4.**  Make sure you adjust paths for folders (essentially, change my name kfedorchuk for your directory ) in the following files:

        •	execute-4.py: lines 7,32,40,70 and 72.
        •	poostprocess.py: line 5
        •	functions.py: line 8

**Step-5.** Run file execute-4.py.
**Step-6.** Observe the results in folder RESULTS. It containes a number of subfolders where the outputs are given in different forms.

**3 subfolders** are designated for the final results, i.e. segmented and tracked version of the input movie.

     •	TRACKED_PLUS_SEGMENTED_CARTOON. In this folder, you will get the most beautiful result where each frame is a RGB image and each cell has its own color.
     •	TRACKED_PLUS_CONTOURS. This is another variant of visualizing the output: segmentation and tracking results are plotted as contours of cells on top of    fluorescent images. Very useful as it clearly gives you the idea of the segmentation quality. Different cells are assigned different colors just like in the previous   case.
      •	SEGMENTEDS_BLACK_AND_WHITE. In this folder, as can be concluded from the name, you will see binary segmentation. It is essentially semantic segmentation unlike in the two previous folders. 

**2 folders** with fluorescent images where tracking results (centroids of cells) are plotted as proxy bounding boxes around the cells. Why 2 folders? To be able visually assess the effect of “tracking-segmentation-correction” approach on tracking results.

    •	TRACKED. Here are the tracking results before correction.
    •	TRACKED CORRECTED. After correction.

**4 folders** for segmented patches. The purpose is to visually compare the quality of segmentation from Segmentor, Refiner, Ensemble and after postprocessing by Cleaner-1 and Cleaner-2.

           •	PATCHES FROM SEGMENTOR
           •	PATCHES FROM REFINER
           •	PATCHES FROM ENSEMBLE
           •	CLEANED PATCHES








 




