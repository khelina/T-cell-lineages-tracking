# 1. T-cell-tracking-and-segmentation: the main idea and the pipeline
This is my ML project on tracking T cell lineages in microscope movies.A 5-minute poster presentation at ABACBS-2020 Virtual Conference outlining the main idea of the algorithm can be viewed here: https://www.youtube.com/watch?v=NebOgh1q0kc&ab_channel=HelinaFedorchuk.

An example of applying this algorithm to a test movie:
https://www.youtube.com/watch?v=pHPd5FArgYU&ab_channel=HelinaFedorchuk

The purpose of this algorithm is to segment and track T cells in microscope movies, with the ultimate goal of buidling T cell lineages. Currently, this has been achieved for small pedigrees up to 5 cells, without occlusions and dying cells - the issues which are going to be tackled in the near future.
To acieve both segmentation and tracking, a series of deep comnvolutional neaural networks have been trained: 5 CNNs for tracking (Tracker-1,..., Tracker-5) each specialisinfg in a fixed number of cells, according to their names,  and 2 U-Net based deep learning models named Segmentor and Refiner for segmenteing small patches with a tracked cell in the centre cut out of each frame after tracking.

The main innovation of this algorithm is that tracking has been done with 3D CNNs where the inputs are short clips of T cell movies rather than separate frames. The second unconventional is that segmentation is done after tracking.So, the trackers were traned on fluorescent images and as a result, after the centroids of the cells are calculated by a tracker, segmentation neural networks take over and segment small patches described above.
The flow of the algortihm is shown in the picure below:


![image](https://user-images.githubusercontent.com/17193930/188291538-0cbf1844-94a0-42c5-afab-66e54c02b722.png)


2. Contens of this repository.



4.How to run the algorithm.


 




