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
###########################################
def load_and_process_page2(path,number_of_frames,progressbar,frame, movie_name):
  print("entering new function")
  global fluor_images,bright_images
  fluor_images=[]
  fluor_names=[]
  bright_images=[]
  bright_names=[]
  i=0
  for filename in sorted_aphanumeric(os.listdir(path)):
   if "thumb" not in filename and filename.endswith(".TIF"):
     index_s,index_t=filename.find("_s"),filename.find("_t")
     exact_name =filename[index_s+1:index_t]     
     if exact_name==movie_name:
        i+=1
        print("i=", i)
        progressbar["value"]=(i+1)/(number_of_frames)*100
        time.sleep(0.02)
        frame.update_idletasks()
        #print("FILE NAME= ", filename)
        if "_w1BF_" in filename:
          bright_names.append(filename)
          old_name=os.path.join(path,filename)
          #print("bright_file_name=", filename)
          a = tiff.imread(old_name)
          c=process_tif(a)
          #new_name =os.path.join(destination, filename[:-4])
          #new_name+="_ch02.tif"             
          #cv2.imwrite(new_name, a)
          bright_images.append(c)
        elif ("_w2FITC_" in filename) or ("_w2Multi-" in filename):
          fluor_names.append(filename)
          old_name=os.path.join(path,filename)
          #print("fluor_file_name=", filename)
          b = tiff.imread(old_name)
          #new_name =os.path.join(destination, filename[:-4])              
          #new_name+="_ch00.tif"
          b=process_tif(b)
          #cv2.imwrite(new_name, a)
          fluor_images.append(b)
       
  #page2.update_idletasks()
  #threading.current_thread().return_value = [fluor_images,bright_images]    
  return fluor_images,bright_images, fluor_names, bright_names
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
def save_images_page2(movie_name,l_feedback,bright_names,fluor_names, bright_images, fluor_images):       
    software_folder =os. getcwd() 
    destination=os.path.join(software_folder, movie_name)
    print("destination=", destination)
    if not os.path.exists(destination):  
            os.makedirs(destination)
            print("The new directory is created!", destination)
            
    for i in range(len(bright_names)):
           filename=bright_names[i]
           new_name =os.path.join(destination, filename[:-4])
           new_name+="_ch02.tif"             
           cv2.imwrite(new_name, bright_images[i])
    for k in range(len(fluor_names)):
          filename=fluor_names[k]
          new_name =os.path.join(destination, filename[:-4])
          new_name+="_ch00.tif"             
          cv2.imwrite(new_name, fluor_images[k])          
    l_feedback.configure(text="Saved images ", fg="#00FFFF", bg="black") 