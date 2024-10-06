import os
import re
import time
import tifffile as tiff
import numpy as np
import cv2


#####################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##############################################
def process_tif(tif_image): # add stacks of tiff image together  
    sh = tif_image.shape
    if len(sh)==3:
           processed_tif =np.zeros((sh[1], sh[2]), dtype=np.uint16)
           for ii in range(sh[0]):
              processed_tif+=tif_image[ii,:,:]           
    else:
          processed_tif=tif_image
    normalised=(processed_tif/processed_tif.max())*255.    
    final=np.uint8(normalised)
    
    return final
##########################################



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
