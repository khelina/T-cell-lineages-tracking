import keras
from keras.models import model_from_json
from keras.optimizers import Adam
import os
import re
import cv2    
##############################################################
def extract_file_name(full_image_name):
  base =os.path.basename(full_image_name)
  name =os.path.splitext(base)[0] 
  dirr=os.path.dirname(full_image_name)
  core_name = name
  while True:
    if core_name[-1]!="t":
        core_name=core_name[:-1]        
    else:
        break   
  n_digits = len(name[:-5])-len(core_name)
  digits_string=name[len(core_name):-5] 
  first=digits_string
  while True:
    if first[0] =="0":
        first =first[1:]
    else:
        break
  full_core_name =os.path.join(dirr,core_name) 
  first_frame_in_name=int(first)-1
  return full_core_name, n_digits, first_frame_in_name
###################################################
def load_clip(k,full_core_name,n_digits, num_frames, first_frame_number): 
  fluor_names, bright_names =[],[]   
  fluor_images,fluor_images_compressed,bright_images=[],[],[]  
  for kk in range(4):
   if k+kk<num_frames:
    fluor_name=full_core_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch00.tif"  
    fluor_names.append(fluor_name)
    raw = cv2.imread(fluor_name, -1) 
    fluor_images.append(raw)
    raw2 = raw.copy()
    fluor_compressed = cv2.resize(raw2, (100, 100), interpolation=cv2.INTER_AREA)
    fluor_images_compressed.append(fluor_compressed)
    
    bright_name=full_core_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch02.tif"
    bright_names.append(bright_name)
    bright= cv2.imread(bright_name, -1) # was 0   
    bright_images.append(bright)
  return  fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names    
############################################
def create_output_folders(outpath):
   subfolders=[]
   subfolder_names=["MASKS",
                 "IMAGES_FOR_FINAL_MOVIE",             
                 #"RED_LINEAGE_PATCHES",
                 "RESULT_FLUORESCENT",
                 #"CELLS_INFO_EXCEL",
                 "LINEAGE_IMAGES",
                 #"PLOTS",
                 #"PATCHES_FOR_RESULTS",
                 "CLEANED_PATCHES", "RESULT_BRIGHT"]              
   for i in range(len(subfolder_names)):
       destination=os.path.join(outpath,subfolder_names[i])
       if not os.path.exists(destination):
           os.mkdir(destination)
       subfolders.append(destination)
   return subfolders
############# upload only one tracker at a time (to save memory)
def create_models(N_cells, models):    
    segmentor = model_from_json(models[6][0])
    segmentor.load_weights(models[6][1] + "-weights.h5")   
    segmentor.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
    refiner = model_from_json(models[7][0])
    refiner.load_weights(models[7][1] + "-weights.h5")   
    refiner.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
  
    trackers=[]
    
    if N_cells==1:
        trackers_template=[0, None, None, None, None]
    elif N_cells==2:
        trackers_template=[None, 1, None, None, None]       
    elif N_cells==3:
      trackers_template=[None, None, 2, None, None]
    elif N_cells==4:
      trackers_template=[None, None, None, 3, None]
    else:
        trackers_template=[None, None, None, None, 4]  
       
    for i in range(5):# 5 is the number of trackers available
         item=trackers_template[i]
         if item!=None:                  
            model_track_read=models[i]
            model_track = model_from_json(model_track_read[0])
            model_track.load_weights(model_track_read[1] + "-weights.h5")   
            model_track.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
            print("Tracker-%s is created" %(i+1))
         else:
             model_track=None
         trackers.append(model_track)
    return trackers, segmentor, refiner
############################################################
