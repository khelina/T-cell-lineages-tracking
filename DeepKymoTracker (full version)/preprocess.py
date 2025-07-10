import keras
from keras.models import model_from_json, Model
from keras.optimizers import Adam
import os
import re
import cv2
from PIL import Image
import numpy as np
import re    
##############################################################
def removeLeadingZeros(string):   
        regex = "^0+(?!$)"    
        cleaned_string = re.sub(regex, "", string) 
        return cleaned_string    
##################################################
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
  #first_frame_in_name=int(first)-1
  first_frame_in_name=int(first)
  return full_core_name, n_digits, first_frame_in_name
###################################################
def load_clip(first_number_in_clip,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number,full_core_red_name): 
  fluor_names, bright_names, red_names =[],[],[]   
  fluor_images,fluor_images_compressed,bright_images, red_images=[],[],[],[]  
  last_frame_number=num_frames+first_frame_number-1  
  for kk in range(4):  
   if first_number_in_clip+kk <= last_frame_number:
    fluor_name=full_core_fluor_name+str(first_number_in_clip+kk).zfill(n_digits)+"_ch00.tif"   
    fluor_names.append(fluor_name)
    ################################    
    fl_pillow = Image.open(fluor_name)
    raw = np.array(fl_pillow, dtype=np.uint8)  
    fluor_images.append(raw)
    #####################################
    raw2 = raw.copy()
    fluor_compressed = cv2.resize(raw2, (100, 100), interpolation=cv2.INTER_AREA)   
    fluor_images_compressed.append(fluor_compressed)
    ######################################    
    bright_name=full_core_bright_name+str(first_number_in_clip+kk).zfill(n_digits)+"_ch02.tif"
    bright_names.append(bright_name)
    #########################################
    br_pillow = Image.open(bright_name)
    bright = np.array(br_pillow, dtype=np.uint8)   
    bright_images.append(bright)
    ################################################
    red_name=full_core_red_name+str(first_number_in_clip+kk).zfill(n_digits)+"_ch01.tif"
    red_names.append(bright_name)
    #########################################
    red_pillow = Image.open(red_name)
    red = np.array(red_pillow, dtype=np.uint8)   
    red_images.append(red)
    #############################################
  return  fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names, red_names, red_images    
############################################
def create_output_folders(outpath):# creates only names if folders already exost. It is importnat when retrieving
   subfolders=[]
   ################################
   subfolder_names=["BRIGHT_MOVIE_RESULTS",
                    "FLUORESCENT_MOVIE_RESULTS",
                    "RED_MOVIE_RESULTS",
                    "PER_CELL_RESULTS",
                    "HELPERS_(NOT_FOR_USER)", "FLUOR_BOREDRS"]
   ##########################################################                 
   for i in range(len(subfolder_names)):
       destination=os.path.join(outpath,subfolder_names[i])
       if not os.path.exists(destination):
           os.mkdir(destination)
       subfolders.append(destination)
   ######################################
   helper_subfolders=[ "CLEANED_PATCHES", "LINEAGE_IMAGES", "MASKS","IMAGES_FOR_FINAL_MOVIE"]
   for helper_subfolder in helper_subfolders:
       destinn=os.path.join(outpath,"HELPERS_(NOT_FOR_USER)",helper_subfolder)
       if not os.path.exists(destinn):
           os.mkdir(destinn)
   ###########################################
   """
   visualize_helper_folder=os.path.join(outpath,"HELPERS_(NOT_FOR_USER)","VISUALISATION_HELPERS")
   #################################
   visualize_helper_subfolders=["PLOTS","RED_LINEAGE_PATCHES","PATCHES_FOR_RESULTS"]
   for vis_subfolder in visualize_helper_subfolders:
       destin=os.path.join(visualize_helper_folder,vis_subfolder)
       if not os.path.exists(destin):
           os.mkdir(destin)
   """
   return subfolders
#############
def create_models(software_folder):    
    os.chdir(software_folder)        
    models_directory = os.path.join(software_folder, "TRAINED MODELS")
    model_names = ["Tracker-6","Segmentor", "Refiner"]    
    models = []
    for name in model_names:                
        full_name = os.path.join(models_directory, name)
        #print("full_name=", full_name)
        json_file = open(full_name + "-model.json", "r")
        model_read = json_file.read()
        json_file.close()        
        models.append((model_read, full_name)) 
    return models,models_directory
#############################
def load_weights(models):    
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
##################################################
#this is the teatx for feedback window (execytion step)
def update_feedback_text_p4(feedback_dict_p4):
    text="Input movie :  "+feedback_dict_p4["movie name"]+\
         "\nFrame size :  "+feedback_dict_p4["frame size"]+\
         "                  Cell diameter : "+feedback_dict_p4["cell diameter"]+\
         "                  Patch size : "+feedback_dict_p4["patch size"]+\
         "\nNumber of cells in Frame 1 : "+feedback_dict_p4["number in frame 1"]+\
         "                  Maximum number of cells : "+feedback_dict_p4["max number"]+\
         "\nFluorescent frames :  "+feedback_dict_p4["fluor frames"]+"    Brightfield frames :  "+feedback_dict_p4["bright frames"]+"    Red frames :  "+feedback_dict_p4["red frames"]+\
         "\nNumber of processed frames :  "+ feedback_dict_p4["number of processed"]
         
    return text
################# 
def update_feedback_text(feedback_dict):
    text="Source :"+feedback_dict["s"]+\
         "\nDestination :"+feedback_dict["dest"]+\
         "\nNumber of fluorescent frames : "+feedback_dict["fl"]+\
         "            Number of bright frames : "+feedback_dict["br"]+\
         "            Number of red frames : "+feedback_dict["red"]+\
         "\nFrame size : "+feedback_dict["im"]+\
         "\nWell size : "+feedback_dict["w"]
         
    return text
############################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
####################################
def load_full_raw_movie(my_dir):# load raw movie for preview
    print("inside load_full_raw_movie")
    all_names_fluor,all_names_bright,all_names_red=[],[],[]     
    for filename in sorted_aphanumeric(os.listdir(my_dir)):   
        if filename.endswith("ch00.tif"):
            full_name_fluor = os.path.join(my_dir, filename)
            all_names_fluor.append(full_name_fluor)
        if filename.endswith("ch02.tif"):
            full_name_bright = os.path.join(my_dir, filename)
            all_names_bright.append(full_name_bright)
        if filename.endswith("ch01.tif"):
            full_name_red = os.path.join(my_dir, filename)
            all_names_red.append(full_name_red)
    return all_names_fluor, all_names_bright,all_names_red