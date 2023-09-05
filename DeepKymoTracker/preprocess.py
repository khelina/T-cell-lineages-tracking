from keras.models import model_from_json
from keras.optimizers import Adam
import os
import re
import cv2
################################################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##################################################
def load_images_both(folder_dir):
 print("loading images...")
 fluor_files=[]
 bright_files=[]
 fluor_compressed=[]
 fluor_names=[]
 bright_names=[]
 
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith("ch00.tif"):
        full_name=os.path.join(folder_dir, filename)
        fluor_names.append(full_name)
        raw=cv2.imread(full_name,0)
        raw2=raw.copy()
        raw1_compressed = cv2.resize(raw2, (100, 100), interpolation = cv2.INTER_LANCZOS4)       
        fluor_compressed.append(raw1_compressed)
        raw3=raw.copy()
        fluor_files.append(raw3) 
      if filename.endswith("ch02.tif"):
        full_name=os.path.join(folder_dir, filename)
        bright_names.append(full_name)
        bright0=cv2.imread(full_name,0)
        bright=bright0.copy()        
        bright_files.append(bright)
 print("loading finished")
 return fluor_compressed,fluor_files,bright_files,fluor_names,bright_names
########################################################
#######################################
def load_one_well_images(folder_dir):
 print("loading images...")
 fluor_files=[]
 bright_files=[]
 fluor_compressed=[]
 fluor_names=[]
 bright_names=[]
 
 for filename in os.listdir(folder_dir):
     if filename[4:6]=="FI":
        full_name=os.path.join(folder_dir, filename)
        fluor_names.append(full_name)        
        raw=cv2.imread(full_name,-1)
        raw2=raw.copy()
        raw1_compressed = cv2.resize(raw2, (100, 100), interpolation = cv2.INTER_LANCZOS4)       
        fluor_compressed.append(raw1_compressed)
        raw3=raw.copy()
        fluor_files.append(raw3) 
     if filename[4:6]=="BF":
        full_name=os.path.join(folder_dir, filename)
        bright_names.append(full_name)
        bright0=cv2.imread(full_name,-1)
        bright=bright0.copy()        
        bright_files.append(bright)
 print("loading finished")
 return fluor_compressed,fluor_files,bright_files,fluor_names,bright_names
#####################################################
def load_images(folder_dir):
 print("loading images...")
 fluor_files=[]
 bright_files=[]
 fluor_compressed=[]
 fluor_names=[]
 bright_names=[]
 
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith("ch00.tif"):
        full_name=os.path.join(folder_dir, filename)
        fluor_names.append(full_name)
        raw=cv2.imread(full_name,0)
        raw2=raw.copy()
        raw1_compressed = cv2.resize(raw2, (100, 100), interpolation = cv2.INTER_LANCZOS4)       
        fluor_compressed.append(raw1_compressed)
        raw3=raw.copy()
        fluor_files.append(raw3) 
      if filename.endswith("ch02.tif"):
        full_name=os.path.join(folder_dir, filename)
        bright_names.append(full_name)
        bright0=cv2.imread(full_name,0)
        bright=bright0.copy()        
        bright_files.append(bright)
 print("loading finished")
 return fluor_compressed,fluor_files,bright_files,fluor_names,bright_names
########################################################
def create_output_folders(outpath):
   subfolders=[]
   subfolder_names=["TRACKED",
                 "TEMPORARY_FOR_MOVIE",             
                 "PATCHES_FROM_SEGMENTOR",
                 "TRACKED_PLUS_CONTOURS",
                 "CELLS_INFO",
                 "TEMPORARY_FOLDER",
                 "PATCHES_FROM_REFINER",
                 "PATCHES_FROM_ENSEMBLE",
                 "CLEANED_PATCHES"]              
   for i in range(len(subfolder_names)):
       destination=os.path.join(outpath,subfolder_names[i])
       if not os.path.exists(destination):
           os.mkdir(destination)
       subfolders.append(destination)
   return subfolders
#######################################################
def load_models(directory):
    os.chdir(directory)
    model_names=["Tracker-1","Tracker-2","Tracker-3",
              "Segmentor", "Refiner"]  
    models=[]
    for name in model_names:
      full_name=os.path.join(directory,name)
      json_file=open(full_name +"-model.json","r")  
      model_read=json_file.read()
      json_file.close()
      model = model_from_json(model_read)
      model.load_weights(full_name + "-weights.h5")
      model.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
      models.append(model)
    print("models loaded")
    return models
############################################################
