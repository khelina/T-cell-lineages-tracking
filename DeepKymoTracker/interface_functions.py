import tkinter as tk
import copy
import cv2
import numpy as np
from PIL import ImageTk, Image
import time 
import os
import re
#from tkinter import filedialog
#from tkinter import ttk
#from tkinter import *
from tkinter import NW
#####################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
########################################################
def turn_image_into_tkinter(image): 
  if image.dtype=="uint16":
      image_norm=(image/image.max())*255.  
      image_copy=np.uint8(image_norm)      
  else:
     image_copy=np.uint8(image)
  image_resized=cv2.resize(image_copy, (382,382), interpolation = cv2.INTER_AREA)
  if len(image.shape)==3:
         image_rgb=cv2.cvtColor(image_resized,cv2.COLOR_BGR2RGB)
  else:
         image_rgb=image_resized
  photo_image=Image.fromarray(image_rgb)
  photo_image =ImageTk.PhotoImage(photo_image)
  return  photo_image 
#################################################
def start_flash(buttons,idd, frame, flashers):
    colors_combinations, buttons,flashers_names= prepare_for_flash(buttons,idd)
    flash(colors_combinations, buttons,flashers_names, frame, flashers)
#####################################################        
def prepare_for_flash(buttons,idd):   
    flashers_names =[]
    for i in range(len(buttons)):
        button_name = str(buttons[i])
        flasher_name ="flasher%s_" % (i+1) + idd
        flashers_names.append(flasher_name)         
    flasher_name ="flasher%s_" % (len(buttons)+1) + idd
    flashers_names.append(flasher_name)      
    colors =['#9ACD32' for k in range(len(buttons)+1)]    
    colors_combinations =[]
    for iii in range(len(colors)):
        colors_copy =copy.deepcopy(colors)
        old =colors_copy
        old[iii]="red"
        colors_combinations.append(old)      
    return colors_combinations, buttons,flashers_names
##################################################    
def flash(colors_combinations, buttons,flashers_names, frame, flashers):  
  for k in range(len(colors_combinations)):        
          for kk in range(len(buttons)):                        
             flashers[flashers_names[kk]]  = frame.after(300*k, lambda k=k, kk=kk:buttons[kk].configure(background = colors_combinations[k][kk])) 
  flashers[flashers_names[kk+1]] = frame.after(300*(k+1), lambda:flash(colors_combinations, buttons,flashers_names, frame, flashers))      
###############################
global stop_flash   
def stop_flash(idd, frame, flashers):
    for key in flashers.keys():
        if key[9:]==idd:
            frame.after_cancel(flashers[key])
           # page4.after_cancel(fl_1)
###############################################

def show_3_canvases(canvas_previous,canvas_current,canvas_lineage,output_images,lineage_images,image_number):
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    #print("len(output_images)=",len(output_images)) 
    #print("len(lineage_images)=",len(lineage_images))   
    canvas_current.create_image(0, 0, anchor=NW, image=output_images[image_number])
    canvas_previous.create_image(0, 0, anchor=NW, image=output_images[image_number-1])
    photo_image_lin=lineage_images[image_number-1]   
    canvas_lineage.create_image(
        0, 0, anchor=NW, image=photo_image_lin)
   