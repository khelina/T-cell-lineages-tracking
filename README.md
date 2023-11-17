# DeepKymoTracker: A tool for the accurate construction of cell lineage trees for highly motile cells
This is my ML project on tracking T-cell lineages in microscope movies. A 5-minute poster presentation at the ABACBS-2020 Virtual Conference outlining the main idea of the algorithm can be viewed here: https://www.youtube.com/watch?v=NebOgh1q0kc&ab_channel=HelinaFedorchuk.

An example of applying this algorithm to a test movie:
https://youtu.be/9nSulQDEles

The purpose of this algorithm is to segment and track T cells in microscope movies, with the ultimate goal of building T cell lineages. Currently, this has been achieved for small pedigrees up to 5 cells, without occlusions and dying cells - the issues that are going to be tackled in the near future.
To achieve both segmentation and tracking, a series of deep convolutional neural networks have been trained: 5 CNNs for tracking (Tracker-1,..., Tracker-5) each specializing in a fixed number of cells, according to their names,  and 2 U-Net-based deep learning models named Segmentor and Refiner for segmenting small patches with a tracked cell in the center cut out of each frame after tracking.

The main innovation of this algorithm is that tracking has been done with 3D CNNs where the inputs are short clips of T-cell movies rather than separate frames. The second unconventional is that segmentation is done after tracking. So, the trackers were trained on fluorescent images and as a result, after the centroids of the cells are calculated by a tracker, segmentation neural networks take over and segment small patches described above.
The flow of the algorithm is shown in the picture below (**Figure-1**):
![image](https://user-images.githubusercontent.com/17193930/188294823-f0d75314-a2fa-4fec-bb47-82150116d443.png) 

**Figure-1:** 1. The top row: an input cell movie consisting of images with both fluorescent and bright field channels (the size of each image is 382 x 382 pixels).
2. The first clip of 4 frames (fluorescent channel only) is passed through Tracker-1. As a result, we know the centroids of the cell in every frame of the clip now.
3. Patches of size 96 x 96 (both channels this time) with the tracked cells in the center are cropped out and fed into the Segmentation Ensemble. The outputs are segmented cells which are binary images of the same size 96 x 96. 
4. Each segmented patch is passed through the Division Detector. If a division is detected then the switch to Tracker-2 occurs.
5. Finally, the segmented patches are pasted into empty black images 382 x 382 according to their locations obtained from Tracker-1. As a result, we obtain the first clip of the output movie (the bottom row).
6. Go to the next clip and repeat the whole procedure again.
 


## 2. THE CONTENTS OF THIS REPOSITORY
In this repository, you will find the DeepKymoTracker folder. 

The folder contains the code for building lineage trees for T-cell movies containing from 1 to 5 cells in each frame. The main file is GUI_execute.py, and the remaining files contain helper functions.

## 3. HOW TO RUN THE ALGORITHM

**Step-1.** You need to install the following:
+ Python=3.6.13
+ Tensorflow= 1.15.0
+ Keras = 2.3.1
+ Spyder = 5.0.0
+ OpenCV = 3.3.1
+ Matplotlib = 3.3.4
+ Xlsxwriter = 3.0.8
+ H5py = 2.10.0



**Step-2.** Download folders TRAINED MODELS (5 GB) and INPUT MOVIE  from https://zenodo.org/deposit/7747438.

**Step-3.** Place these folders inside the DeepKymoTracker folder.

**Step-4.** Run file GUI_execute.py. You will see the following interface:
![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/de784a17-07b1-4b42-8066-4df4334f9111)





**Step-5.** Follow the prompts in the interface, it is easy to do that as all buttons are enumerated. You need to take steps 1,2,3 ( where the last button is **3. Execute**). You can monitor the progress in the **Current Frame** window. If an error occurs push the button **3a. Pause** and then **4. Display results**. After that, you will be able to correct the error. There can be 2 types of tracking errors during execution: lost cells and ID swappings. To manually correct them, you need to use buttons **5a.EDIT IDs** and **5b.Edit division**. After finishing editing, go back to button **4. Execute**.
For this particular movie, you will have to manually correct 2 missed divisions (in Frame 1910 and Frame 1972) and 2 wrong ID assignments due to big jumps (Frame 2017 and Frame 3119).

1. Let us see in more detail how to manually correct  the missed division in Frame 1910. After pushing **4. Display results** and positioning Frame 1910 in the Current Frame window by sliding the sliding bar, push **5b.Edit division**. You are now in editing mode. Click on the mother cell (the green one) in Previous Frame (the green one), then click on both daughter cells ( try to click as close to their centroids as possible!). Finally, push **6a. Save division edits**. You should get the following picture: 
![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/e8f34a07-f333-4ebc-9784-4338c4d9c5d4)

After that, push **4. Execute**. Note: a division correction can only be done once, i.e. 1 division per frame. 

2. How to correct IDs in Frame 2017. After positioning Frame 2017 in the Current Frame window, push **5a.Edit IDs**. Then, click on the cell to be corrected ( the magenta one, for instance) in Previous Frame window. Now, you have an ID of that cell. After that, click on the desired cell in Current Frame. This will give you the desired position of the magenta cell, so try to click as close to its centroid as possible. Repeat the process for the blue and cyan cells. For safety, you can also do it for the red cell, even though it is not absolutely necessary.  Remember to close the editing mode by pushing **5a. Save ID edits**. You should get the following picture:
![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/d26c59fb-0a0f-4cc8-aeda-e3d64c4f1832)

After that, push **4. Execute**.


**TRACKED_PLUS_CONTOURS** folder is designated for the final results, i.e. segmented and tracked version of the input movie. Segmentation and tracking results are plotted as contours of cells on top of    fluorescent images which clearly gives you the idea of the segmentation quality. Different cells are assigned different colors 
      








 




