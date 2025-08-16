import os
import re
import time
#import tifffile as tiff
import numpy as np
import cv2
from PIL import Image


#####################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##############################################
def process_tif(tif_image_path):
    tif_image = Image.open(tif_image_path)
    n_slices=tif_image.n_frames
    if n_slices>1:
        multi_np_image=np.zeros((tif_image.size[0],tif_image.size[1],n_slices), np.uint16)
        for i in range(tif_image.n_frames):
            #print("i=", i)
            tif_image.seek(i)
            numpy_array = np.array(tif_image)
            #print("numpy_array.shape=",numpy_array.shape)
            multi_np_image[:,:,i]=numpy_array
        result_max=np.max(multi_np_image, axis=2)        
    else:
        result_max=np.array(tif_image)
    #print("result_max.shape=", result_max.shape)    
    normalised=(result_max/result_max.max())*255.    
    final_max_tif=np.uint8(normalised)
    return final_max_tif, n_slices
###########################################

##############################
def display_image_p2_fix_missing(slide_frame_number, channel_names_dictionary, channel_code,n_digits,canvas_size_p2):
    channel_keys=list(channel_names_dictionary.keys())
    if slide_frame_number in channel_keys:
        old_name=channel_names_dictionary[slide_frame_number][0]
        new_name=create_new_name(old_name,channel_code,n_digits)
        image_for_display=channel_names_dictionary[slide_frame_number][1]        
    else:
         image_for_display=np.zeros((canvas_size_p2, canvas_size_p2,3), dtype=np.uint8)
         cv2.putText(image_for_display,"NO IMAGE",((canvas_size_p2-200)//2,canvas_size_p2//2),cv2.FONT_HERSHEY_PLAIN,3.0,(238,238,0),2) 
         old_name= "No image available"
         new_name="               " 
    return  image_for_display, old_name, new_name
##########################
def create_new_name(old_name,channel_code,n_digits):
    name =os.path.splitext(old_name)[0]
    index_t =name.find("_t")    
    old_number =name[index_t+2:]
    new_number =str(old_number).zfill(n_digits)    
    new_name =name[:index_t+2]+new_number+"_"+channel_code+".tif" 
    return new_name
############################################################
def extract_movie_name(name):# name is a filename
  fluor, bright,s,t="FITC", "BF", "_s","_t"
  index_s,index_t=name.find(s),name.find(t)
  if fluor in name:
      index_channel =name.find(fluor)    
  elif bright in name:
      index_channel=name.find(bright)     
  core =name[:index_channel-1]# before FITC or BF
  movie_name =name[index_s+1:index_t]  
  return movie_name, core
###########################################
def create_name_dictionary(filenames, images):# available frame names (some might be missing)
  name_dictionary={}
  for i in range(len(filenames)):
     filename=filenames[i]
     image=images[i]
     index_t=filename.find("_t")
     internal_number=filename[index_t+2:-4]
     name_dictionary[internal_number]=(filename, image)
  return  name_dictionary  
########################################
def save_images_page2(movie_name,feedback_var_p2,bright_names,fluor_names, red_names,bright_images, fluor_images, red_images, instruct_var_p2):       
    software_folder =os. getcwd() 
    destination=os.path.join(software_folder, movie_name)
    print("destination=", destination)
    n_digits=calculate_n_digits_in_name(fluor_names[-1])
    
    if not os.path.exists(destination):  
            os.makedirs(destination)
            print("The new directory is created!", destination)
    if len(bright_names)!=0:       
           zfill_file_name("ch02",bright_names,bright_images, n_digits, destination)
    else:
           print("no bright channel discovered")
    if len(fluor_names)!=0:
           zfill_file_name("ch00",fluor_names,fluor_images, n_digits, destination)
    else:
           print("no fluor channel discovered")
    if len(red_names)!=0:
          zfill_file_name("ch01",red_names,red_images, n_digits, destination)
    else:
           print("no red channel discovered")
    
    feedback_var_p2.set(feedback_var_p2.get()+"\nProcessed movie saved as  "+destination)
    instruct_var_p2.set("Movie has been saved.\n\n Now you can either go to the next page or exit.")
    print("Finished saving channels")
##########################################
def calculate_n_digits_in_name(base_image_name):    
    #base =os.path.basename(last_fluor_name)
    name =os.path.splitext(base_image_name)[0]
    index_t =name.find("_t")
    n_digits = len(name)-index_t-2
    return n_digits
###################################


def zfill_file_name(channel_name,list_of_base_image_names,list_of_images, n_digits, destination):
    for i in range(len(list_of_base_image_names)):
        base_image_name=list_of_base_image_names[i]
        name =os.path.splitext(base_image_name)[0]
        index_t =name.find("_t")    
        old_number =name[index_t+2:]
        new_number =str(old_number).zfill(n_digits)
        new_base_name =name[:index_t+2]+new_number
        new_full_name =os.path.join(destination, new_base_name)
        new_full_name=new_full_name+"_"+channel_name+".tif"             
        cv2.imwrite(new_full_name, list_of_images[i])
####################################################
