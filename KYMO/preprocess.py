import keras
from keras.models import model_from_json, Model
from keras.optimizers import Adam
import os
import re
import cv2
from PIL import Image
import numpy as np    
##############################################################
def extract_red_frame_numbers(red_frame_names):
    list_of_frame_numbers =[]
    for i in range(len(red_frame_names)):
        filename=red_frame_names[i]
        full_core_name, n_digits, first_frame_in_name=extract_file_name(filename)
        list_of_frame_numbers.append(first_frame_in_name)
    return  list_of_frame_numbers 
#########################################################
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
def load_clip(k,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number): 
  fluor_names, bright_names =[],[]   
  fluor_images,fluor_images_compressed,bright_images=[],[],[]
  print("n_digits=", n_digits)  
  for kk in range(4):
   if k+kk<num_frames:
    fluor_name=full_core_fluor_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch00.tif"  
    fluor_names.append(fluor_name)
    #raw = cv2.imread(fluor_name, -1)
    ##########
    fl_pillow = Image.open(fluor_name)
    raw = np.array(fl_pillow, dtype=np.uint8)
    ###########
    fluor_images.append(raw)
    raw2 = raw.copy()
    fluor_compressed = cv2.resize(raw2, (100, 100), interpolation=cv2.INTER_AREA)
    fluor_images_compressed.append(fluor_compressed)
    
    bright_name=full_core_bright_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch02.tif"
    bright_names.append(bright_name)
    br_pillow = Image.open(bright_name)
    bright = np.array(br_pillow, dtype=np.uint8)
    #bright= cv2.imread(bright_name, -1) # was 0   
    bright_images.append(bright)
    #print("bright_name=",bright_name)
  print("fluor_names=",fluor_names)
  print("len(fluor_images_compressed)=",len(fluor_images_compressed))
  print("bright_names=",bright_names)
  print("len(bright_images)=",len(bright_images))
  print("len(fluor_images)=",len(fluor_images))
  return  fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names    
############################################
def create_output_folders(outpath):
   subfolders=[]
   subfolder_names=["MASKS",
                 "IMAGES_FOR_FINAL_MOVIE",             
                 "RED_LINEAGE_PATCHES",
                 "RESULT_FLUORESCENT",
                 "CELLS_INFO_EXCEL",
                 "LINEAGE_IMAGES",
                 "PLOTS",
                 "PATCHES_FOR_RESULTS",
                 "CLEANED_PATCHES", "RESULT_BRIGHT"]              
   for i in range(len(subfolder_names)):
       destination=os.path.join(outpath,subfolder_names[i])
       if not os.path.exists(destination):
           os.mkdir(destination)
       subfolders.append(destination)
   return subfolders
############# upload only one tracker at a time (to save memory)
def create_models(models):    
    segmentor = model_from_json(models[1][0])
    segmentor.load_weights(models[1][1] + "-weights.h5")   
    segmentor.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
    print("segmentor is ready")
    
    refiner = model_from_json(models[2][0])
    refiner.load_weights(models[2][1] + "-weights.h5")   
    refiner.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])   
    print("refiner is ready")
    
    tracker = model_from_json(models[0][0])
    tracker.load_weights(models[0][1] + "-weights.h5")   
    tracker.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
    print("tracker is ready")
         
    return tracker, segmentor, refiner
############################################################
def characters(x): # in most cases it is [-13:-9] (for names like t0001_ch02.tif)
    return(x[-14:-9])# if it is t00001_ch02.tif it should be changed to [-14:-9]
                     # if t001_ch02.tif it is [-12:-9]
def load_image_names(source):
 #global bright_names_sorted,fluor_names_sorted
 bright_names,fluor_names, red_names=[], [], []
 for filename in os.listdir(source):
    if filename.endswith("ch02.tif"):
     full_name=os.path.join(source, filename)
     bright_names.append(full_name)
    if filename.endswith("ch00.tif"):
     full_name=os.path.join(source, filename)
     fluor_names.append(full_name)
    if filename.endswith("ch01.tif"):
     full_name=os.path.join(source, filename)
     red_names.append(full_name)   
 bright_names_sorted=sorted(bright_names,key=characters) 
 fluor_names_sorted=sorted(fluor_names,key=characters)
 red_names_sorted =sorted(red_names,key=characters)
 print("len(bright_names_sorted INSIDE)=",len(bright_names_sorted))
 return bright_names_sorted,fluor_names_sorted, red_names_sorted