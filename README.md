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
6. Go to the next clip and repeat the whole procedure.
 


## 2. THE CONTENTS OF THIS REPOSITORY
In this repository, you will find 2 folders: DeepKymoTracker and MODELS. 
In the **MODEL**S folder, you will find the Python code that was used for training deep learning models utilized in DeepKymoTracker and samples of training data for each neural network. 
The **DeepKymoTracker** folder contains the code for building lineage trees for T-cell movies containing from 1 to 5 cells in each frame. The main file is GUI_execute.py, and the remaining files contain helper functions.

## 3. HOW TO RUN THE ALGORITHM

**Step-1.** You need to install the following:
+ Python=3.6.13 (The best way to do it is via Anaconda as it contains all the classical libraries such as numpy, os, etc.)
+ Tensorflow= 1.15.0
+ Keras = 2.3.1
+ OpenCV = 3.3.1
+ H5py = 2.10.0


**Step-2.** Download DeepKymoTracker folder from this repository, then download folders TRAINED MODELS.zip (5 GB) and INPUT_MOVIE_EXAMPLE.zip (426 MB)  from https://doi.org/10.5281/zenodo.10720117, unzip them and place both unzipped folders inside DeepKymoTracker folder. If you would like to use the full version of DeepKymoTracker, download models from https://zenodo.org/records/11540886?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjViZTI2ZTJlLWQ1YjItNGQ0Mi05MDU1LTVhMzFlOGUwZDg0ZiIsImRhdGEiOnt9LCJyYW5kb20iOiIyZjhlYjY1OTNhNmNlNDg0ZGRkMmE1MWQ0NzdlY2M1MyJ9.-W9uEoTsIxg2NqFYkxPawWd4-F7gjrem9aBEKLXTmHZl0dEBcEKN_QFjj3gKSdhEbm1fm2Ldez0Nf4Jt-0Ilhg.

**Step-3.** Run file GUI_execute.py. You will see the following interface:

![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/d6c00888-c0e3-4de6-a9f8-293c72ef8d74)



**Step-4.** Follow the prompts (flashing buttons) in the interface, it is easy to do that as all the instructions and the feedback are given in the black window on the top of the screen (yellow font). When answering the question "2. How many cells are there in Frame 1?" you can choose any option, they both work for this particular movie (the difference being in the case of "1 cell" the position of the cell will be calculated automatically whereas for the "More than 1 cell" option you will have to assign that position manually in the popup window).
You can monitor the progress in the **Current Frame**. If an error occurs push the button **3a. Pause** and then **4. Display results**. After that, you will be able to correct the error. There can be 2 types of tracking errors during execution: ID swappings and missed divisions. To manually correct them, you need to use buttons **5. Start editing IDs** or **6. Start editing division**. After pushing one of these buttons, more detailed instructions for editing will appear in the black window just below them. Read them carefully and follow the prompts. 

For this particular movie, you will have to manually correct 2 missed divisions (in Frame 1910 and Frame 1973) and 2 wrong ID assignments due to big jumps (Frame 2017 and Frame 3119).

**a.** Let us see in more detail how to manually correct  the missed division in Frame 1910. After pushing **4. Display results** and fixing Frame 1910 in the Current Frame window by sliding the sliding bar, push **6. Start editing division**. You are now in the editing mode. Click on the mother cell (the green one) in the Previous Frame, then click on both daughter cells ( try to click as close to their centroids as possible!). Finally, push **6a. Save division edits**. You should get the following picture:
 
![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/e2bb433f-be2d-4d3a-8cf4-61277f760a62)


After that, push **4. Execute**. **Note:** A division correction can only be done once, i.e. 1 division per frame.

**b.** Similarly, you edit another missed division in Frame 1973. That is what it looks like as a result:
   
   ![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/84252667-a5cf-4630-92ad-adf1e9968d33)
 

**c.** How to correct IDs in Frame 2017. After positioning Frame 2017 in the Current Frame window, push **5. Start editing IDs**. Then, click on the cell to be corrected ( the magenta one, for instance) in the Previous Frame window. Now, you have an ID of that cell. After that, click on the desired cell in the Current Frame. This will give you the desired position of the magenta cell, so try to click as close to its centroid as possible. Repeat the process for the blue and cyan cells. For safety, you can also do it for the red cell, even though it is not absolutely necessary.  Remember to close the editing mode by pushing **5a. Save ID edits**. You should get the following picture:

 ![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/6c607765-9401-4f31-bbf5-0697cc1aeb7b)


After that, push **4. Execute**.

**d.** The ID correction in Frame 3119 is conducted similarly:
![image](https://github.com/khelina/T-cell-lineages-tracking/assets/17193930/60294618-b563-49f0-8c25-181aeea7fd39)

**Step-5.** Finally, push button **7. Create final movie**. This movie will be saved inside OUTPUT_INPUT_MOVIE_EXAMPLE as avi. file. Also, several folders and files with different output information will be created inside that folder.

**Note:** In this example, we corrected manually only the most obvious tracking errors, we did not bother about the ones occurring during cell occlusions. If you wish you are welcome to correct them as well using **6. Start editing division**.  

      








 




