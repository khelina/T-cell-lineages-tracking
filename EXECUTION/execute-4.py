import cv2 
import numpy as np 
import os
from keras.optimizers import Adam
from keras.models import model_from_json
##################################################
os.chdir("C:\\Users\\kfedorchuk\\Documents\\EXECUTE")# this is the directory of the folder EXECUTION`
#######################################################
from functions import (load_images, rename_file,
                       recalculate_centres,
                       predict_tracking,segment_frame,
                       create_output_folders,draw_exact_pixel_markers)  
from postprocess import Cleaner_2                               
from plot import plot_frame 
 ##################################################################################  
def  initialize_variables(): 
 Colors=[[0,0,255,255],[0,128,255,255],[0,255,0,255],[255,0,0,255],[255,128,0,255]]
 Bordersize=int(96/2)+5+6
 return Colors, Bordersize
#####################################################################
def disaster(coords,first_frame_of_clip):#disaster is when calculated centroids in the 1st frame are too far away
### from the centroids in the last frame of the previous clip. When this happens, the function disaster output verdict"Disaster!"
# and the execution algorithm goes 1 frame back and tries the clip beginning with that frame.
    fr=first_frame_of_clip   
    distances=[(coords[i][0]-fr[i][0])**2+(coords[i][1]-fr[i][1])**2 for i in range(4)]
    if all (x < 1600 for x in distances)==True:
        verdict="All good"
    else:
        verdict="Disaster!"
    return verdict
##################### Load input movie ############
source="C:\\Users\\kfedorchuk\\Documents\\EXECUTE\\DATA\\INPUT-T_CELL-MOVIE"# that is where your original movie is
inputs=load_images(source)
fluor_images_compressed=inputs[0]
fluor_images=inputs[1]
bright_images=inputs[2]
fluor_names=inputs[3]
bright_names=inputs[4]
######################### Load trained models ##################
os.chdir("C:\\Users\\kfedorchuk\\Documents\\EXECUTE\\DATA\\TRAINED MODELS")
######################################
Models=[]

json_file_track_4=open("Tracker-4-model.json","r")
model_track_4=json_file_track_4.read()
json_file_track_4.close()
Model_track_4 = model_from_json(model_track_4)
Model_track_4.load_weights("Tracker-4-weights.h5")
Model_track_4.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
Models.append(Model_track_4)
##########################################################
json_file_segm=open("Segmentor-model.json","r")
model_segm=json_file_segm.read()
json_file_segm.close()
Model_segm = model_from_json(model_segm)
Model_segm.load_weights("Segmentor-weights.h5")
Model_segm.compile(Adam(lr=0.003), loss='mse',metrics=["mae"])
Models.append(Model_segm)
##############################################################
json_file_refiner=open("Refiner-model.json","r")
model_refiner=json_file_refiner.read()
json_file_refiner.close()
Model_refiner = model_from_json(model_refiner)
Model_refiner.load_weights("Refiner-weights.h5")
Model_refiner.compile(Adam(lr=0.003), loss='mse',metrics=["mae"])
Models.append(Model_refiner)
##########################################################################
###############################################################################
############################# Create output folders ###############
os.chdir("C:\\Users\\kfedorchuk\\Documents\\EXECUTE")
##############################################################
destination="C:\\Users\\kfedorchuk\\Documents\\EXECUTE\\RESULTS"# the results will be plotted here
os.mkdir(destination)
destinations=create_output_folders(destination)
print(destinations)
########################## Initialize variables ###############
N_cells=4
Coeff=382.0/100.0
coords=np.array([316.,349.,355.,289.,353.,324.,351.,358.])# Pos0302f
coords=coords.reshape((N_cells,2))
texts=["1","2","3","4"]
if N_cells!=1:
  markers_empty = np.zeros((382,382), np.uint8)
  markers=draw_exact_pixel_markers(markers_empty,coords)
Colors, Bordersize=initialize_variables()
centroids_raw=[]
centroids_corrected=[]
lineage=[]
k=0  
kk=0
p=0
n=795
################################### Execute ############
while k<n:# k=number of the 1st frame inside each clip     
   print("entering a new clip beginning with frame number ",k)    
   clip_centr=predict_tracking(coords,fluor_images,fluor_images_compressed,fluor_names,k,destinations[0], Models)      
   centroids_raw+=clip_centr   
   verdict=disaster(coords,clip_centr[0]) 
   if verdict=="Disaster!":               
       print("Disaster in frame=",k)
       print("Going back to the previous frame")          
       k-=1     
       coords=centroids_corrected[k]
       lineage.pop()       
       centroids_corrected.pop()      
       continue 
   for kk in range(4):# kk is the  number of a frame inside clip           
       print("entering frame number ",k+kk)        
       cells =segment_frame(fluor_images,bright_images,clip_centr,coords,k,kk, Models)                 
       cells=Cleaner_2(cells)      
       cells=recalculate_centres(cells)                        
       lineage.append(cells)          
       coords=plot_frame(texts,cells,clip_centr,k,kk,fluor_images,destinations,coords,fluor_names,p+kk)           
       centroids_corrected.append(coords)                                            
   k+=4
   p+=4
np.savez(os.path.join(destinations[0],"centroids_raw.npz"), new_centr=centroids_raw)          
######################   plot corrected tracking ###############
z=centroids_corrected
for i in range(len(z)):
    img=fluor_images[i]
    im1 = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    x=np.round(z[i])    
    x=x.astype(int)
    nn=len(z[i]) 
    name=names[i]               
    cv2.rectangle(im1,(x[0][0]-20,x[0][1]-20),(x[0][0]+20,x[0][1]+20),Colors[0],1)
    cv2.rectangle(im1,(x[1][0]-20,x[1][1]-20),(x[1][0]+20,x[1][1]+20),Colors[1],1)
    if nn>2:
        cv2.rectangle(im1,(x[2][0]-20,x[2][1]-20),(x[2][0]+20,x[2][1]+20),Colors[2],1)
    if nn>3:
        cv2.rectangle(im1,(x[3][0]-20,x[3][1]-20),(x[3][0]+20,x[3][1]+20),Colors[3],1)
    if nn>4:  
        cv2.rectangle(im1,(x[4][0]-20,x[4][1]-20),(x[4][0]+20,x[4][1]+20),Colors[4],1)          
    newname = rename_file(destinations[5],name)   
    cv2.imwrite(newname,im1)
  
np.savez(os.path.join(destinations[5],"centroids_corrected.npz"), new_centr=centroids_corrected)       
#################################################################################
