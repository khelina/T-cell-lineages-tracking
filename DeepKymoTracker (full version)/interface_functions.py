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
from threading import Thread
#####################################
def drag_start(event):
        """Begining drag of an object"""
        # record the item`s location
        global x,y
        x = event.x
        y = event.y
####################################
class CustomThread(Thread):
    def _init_(self,group=None,target=None,name=None,args=(), kwargs={},Verbose=None):
        Thread._init_(self,group,name,args,kwargs)
        self._return=None
        
    def run(self):
        if self._target is not None:
            self._return=self._target(*self._args,**self._kwargs)
            
    def join(self):
        Thread.join(self)
        return self._return
######################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
########################################################
def turn_image_into_tkinter(image, window_size): # if image is open in cv2
  if image.dtype=="uint16":
      image_norm=(image/image.max())*255.  
      image_copy=np.uint8(image_norm)      
  else:
     image_copy=np.uint8(image)
  ###################################
  #print("image_copy.shape=",image_copy.shape)
  #print("windoe_size=", window_size)
  
  if image_copy.shape[0]!=image_copy.shape[1]:# for lineage_image
     num_frames=image_copy.shape[0]
     image_resized=np.zeros(image_copy.shape, np.uint8)
     basic_part=image_copy[:,:num_frames]
     added_part=image_copy[:, num_frames:]
     #print("basic_part.shape=", basic_part.shape)
     #print("added_part.shape=", added_part.shape)
     #coefficient=image_copy.shape[0]/window_size
     basic_resized=cv2.resize(basic_part, (window_size,window_size), interpolation = cv2.INTER_AREA)
     added_resized=cv2.resize(added_part, (80,window_size), interpolation = cv2.INTER_AREA)
     #added_resized=resize_image_aspect_ratio(added_part, window_size)
     #print("added_resized.shape=", added_resized.shape)
     image_resized= np.concatenate((basic_resized,added_resized), axis=1)
  else:
  
     image_resized=cv2.resize(image_copy, (window_size,window_size), interpolation = cv2.INTER_AREA)
  #####################################################
  if len(image.shape)==2:
       image_rgb=cv2.cvtColor(image_resized,cv2.COLOR_GRAY2RGB)
  elif image.shape[2]==3:
         image_rgb=cv2.cvtColor(image_resized,cv2.COLOR_BGR2RGB)
  elif image.shape[2]==4:
         image_rgb=cv2.cvtColor(image_resized,cv2.COLOR_BGRA2RGB)
  else:
         image_rgb=image_resized
  photo_image=Image.fromarray(image_rgb)
  photo_image =ImageTk.PhotoImage(photo_image)
  return  photo_image 
###############################################
######### Page-5(Correct segmentaion); for sliding frames
def show_2_canvases(canvas_bright,canvas_fluor,photo_filled_brights,photo_filled_fluors,image_number, window_size):
    canvas_bright.delete('all')
    canvas_fluor.delete('all')
   
    canvas_bright.create_image(0, 0, anchor=NW, image=photo_filled_brights[image_number-1])    
    canvas_fluor.create_image(0, 0, anchor=NW, image=photo_filled_fluors[image_number-1])
    
########### Page-5(Correct segmentaion); for correcting one current frame
def display_both_channels(filled_fluor,filled_bright,canvas_fluor,canvas_bright,target_size,image_origin_x,image_origin_y):      
      photo_fluor=turn_image_into_tkinter(filled_fluor, target_size) 
      photo_bright=turn_image_into_tkinter(filled_bright, target_size)
      canvas_fluor.create_image(image_origin_x,image_origin_y, anchor=NW, image=photo_fluor)      
      canvas_bright.create_image(image_origin_x,image_origin_y, anchor=NW, image=photo_bright)
      return canvas_bright,canvas_fluor, photo_fluor, photo_bright
###############################################################
def extract_output_images(output_fluor_path,lineage_path, window_size, output_images, output_names):# extract fluor and linage images for display
    #it is very essential (it is not a mistake) that output_names and output_images are not empty lists!
    lineage_images, lineage_images_cv2=[],[]
    for filename in sorted_aphanumeric(os.listdir(output_fluor_path)):
        #output_name=os.path.join(fluor_path,filename)
        output_name=filename
        full_output_name=os.path.join(output_fluor_path,output_name)
        output_names.append(output_name)
        fluor_tracked=cv2.imread(full_output_name, -1)
        photo_fluor_tracked=turn_image_into_tkinter(fluor_tracked, window_size)     
        output_images.append(photo_fluor_tracked)
    for filename in sorted_aphanumeric(os.listdir(lineage_path)):
        lineage_image_cv2_name=os.path.join(lineage_path,filename)
        print(" lineage_image_cv2_name=", lineage_image_cv2_name)
        lineage_cv2=cv2.imread(os.path.join(lineage_path,filename), -1)
        lineage_images_cv2.append(lineage_cv2)
        photo_lineage=turn_image_into_tkinter(lineage_cv2, window_size)     
        lineage_images.append(photo_lineage)
    return output_images,lineage_images, output_names, lineage_images_cv2
##################################################    
def flash(colors_combinations, buttons,flashers_names, win, flashers):  
  for k in range(len(colors_combinations)):        
          for kk in range(len(buttons)):                        
             flashers[flashers_names[kk]]  = win.after(300*k, lambda k=k, kk=kk:buttons[kk].configure(background = colors_combinations[k][kk])) 
  flashers[flashers_names[kk+1]] = win.after(300*(k+1), lambda:flash(colors_combinations, buttons,flashers_names, win, flashers))
  return flashers      
###############################
def show_3_channels(canvas_left,canvas_mid,canvas_right,left_names,mid_names,right_names,window_size,image_number):
    canvas_left.delete('all')
    canvas_mid.delete('all')    
    canvas_right.delete('all')
      
    left_cv_image=cv2.imread(left_names[image_number-1],0)
    mid_cv_image=cv2.imread(mid_names[image_number-1],0)
    right_cv_image=cv2.imread(right_names[image_number-1],0)
    global left_tk_image,mid_tk_image,right_tk_image
    left_tk_image=turn_image_into_tkinter(left_cv_image, window_size)
    mid_tk_image=turn_image_into_tkinter(mid_cv_image, window_size)
    right_tk_image=turn_image_into_tkinter(right_cv_image, window_size)
    
    canvas_left.create_image(0, 0, anchor=NW, image= left_tk_image) 
    canvas_mid.create_image(0, 0, anchor=NW, image= mid_tk_image)
    canvas_right.create_image(0, 0, anchor=NW, image= right_tk_image)    
########## show tracking dynamically during execution
def show_3_canvases(canvas_previous,canvas_current,canvas_lineage_exec,output_images,lineage_images_tk,image_number, first_frame_number):
  canvas_previous.delete('all')
  canvas_current.delete('all')    
  canvas_lineage_exec.delete('all')  
  internal_image_number=image_number-first_frame_number+1 
  if internal_image_number<len(output_images):
   canvas_current.create_image(0, 0, anchor=NW, image=output_images[internal_image_number])
   canvas_previous.create_image(0, 0, anchor=NW, image=output_images[internal_image_number-1])
   canvas_lineage_exec.create_image(0, 0, anchor=NW, image=lineage_images_tk[internal_image_number-1])   
#######################################################
def create_name_dictionary_p4(filenames):# available frame names (some might be missing)
  name_dictionary={}
  for i in range(len(filenames)):
     filename=filenames[i]    
     index_t=filename.find("_t")
     internal_number=filename[index_t+2:-9]
     name_dictionary[internal_number]=filename
  return  name_dictionary 
#################### this function is used for displaying all 3 types of images
########### especially if red channel is missing - in this case image is zero
def display_image_p4(slide_frame_number, channel_names_dictionary, channel_code,canvas_size_p4):
    channel_keys=list(channel_names_dictionary.keys())
    if slide_frame_number in channel_keys:
        file_name=channel_names_dictionary[slide_frame_number]
        name_for_display=os.path.basename(file_name)
        image=cv2.imread(file_name,0)
       
    else:
         image=np.zeros((canvas_size_p4, canvas_size_p4,3), dtype=np.uint8)
         cv2.putText(image,"NO IMAGE",((canvas_size_p4-200)//2,canvas_size_p4//2),cv2.FONT_HERSHEY_PLAIN,3.0,(238,238,0),2) 
         #name= "No image available"
         name_for_display="               "
    image_for_display=turn_image_into_tkinter(image, canvas_size_p4)         
    return  image_for_display, name_for_display
###############################################
def calculate_angle(rect):
    box = cv2.boxPoints(rect)     
    box = np.int0(np.round(box))
    x0,y0,x1,y1,x3,y3=box[0][0],box[0][1],box[1][0],box[1][1],box[3][0],box[3][1]
    angle_1, angle_2=abs(y3-y0)/abs(x3-x0),abs(y1-y0)/abs(x1-x0)

    if angle_1>angle_2:        
       #first_x0=first_box[0][0]
       angle=rect[2]+90.
    else:
       #first_x0=first_box[0][0] 
       angle=rect[2]
    return angle, box
################################################
def cut_well_from_image(im_bright,seed,well_size, first_x0,delta_x, delta_y, first_rect):
 mask=None
 rot_indicator="no"# shows if you need to rotate final image or not
 ww=[]
 hh=[]
 low =np.min(im_bright)
 high =np.max(im_bright)
 #####
 rect=first_rect      
 #box = cv2.boxPoints(rect)     
 #box = np.int0(np.round(box))      
 
 ########   
 for i in range(low,high+1,1):
   ret,thresh = cv2.threshold(im_bright,low+i,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold (it is now from 130 to 255)   
   thresh[thresh!=0]=255 
   
   im_thr=thresh.copy()
   fill_image=cv2.floodFill(im_thr, mask, seed, 255,flags=8)# here you define the centre of the well (there are 4 in total)
   fill_image = thresh | im_thr
   fill_image-=thresh   
   closing = cv2.morphologyEx(fill_image, cv2.MORPH_CLOSE, (5,5))    
   _,contours, hierarchy = cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)     
   #print("len(contours) in cut_well_from_image=", len(contours))
   if len(contours)==1:       
       cnt=contours[0]
       rect_temp = cv2.minAreaRect(cnt)             
       box_temp = cv2.boxPoints(rect_temp)    
       box_temp = np.int0(np.round(box_temp))
       w,h=rect_temp[1][0],rect_temp[1][1]       
       if (well_size-40<=w<=well_size+40 and well_size-40<=h<=well_size+40) :
          rect = rect_temp        
          break
       
 angle, box=calculate_angle(rect)   
 rows,cols = im_bright.shape 
 M = cv2.getRotationMatrix2D((int(round(cols/2)),int(round(rows/2))),angle,1)
######3 3  rotate  it horisontal 
 temp=np.zeros(im_bright.shape, np.uint8)
 cv2.drawContours(temp,[box],0,255,-1)
 dst = cv2.warpAffine(temp,M,(cols,rows))
####################  4. calculate its borders   
 _,contours_new, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt_new=contours_new[0]
 rect_new = cv2.minAreaRect(cnt_new)             
 box_final = cv2.boxPoints(rect_new)    
 box_final = np.int0(np.round(box_final))
 #print("box_final=", box_final)
 xs=[box_final[k][0] for k in range(4)]
 ys=[box_final[k][1] for k in range(4)]
 #index=ys.index(min(ys))
 global x_min, y_min
 
 x_min, y_min=min(xs),min(ys)
 print(" x_min before, y_min before=", x_min," , ", y_min)
 print("delta_x, delta_y=",delta_x, delta_y)
 #x_min, y_min=box_final[1][0],box_final[1][1] 
 x_min=x_min+delta_x
 y_min=y_min+delta_y
 print(" x_min after, y_min after=", x_min," , ", y_min)
 #print(" x_min after, y_min after=", x_min," , ", y_min)
############################################# 
 #width=x_max-x_min
 #height=y_max-y_min
 #side=max(width,height)
 #side=well_size
 
####### 5. apply 
 rot_bright = cv2.warpAffine(im_bright,M,(cols,rows))
 #rot_bright = cv2.rotate(rot_bright_init, cv2.ROTATE_90_COUNTERCLOCKWISE)
 cut_bright_init=rot_bright[y_min:y_min+well_size,x_min:x_min+well_size]
 final_bright=cut_bright_init
 #cut_bright = cv2.rotate(cut_bright_init, cv2.ROTATE_90_COUNTERCLOCKWISE)
 
 current_x0=box[0][0]
 if abs(current_x0-first_x0)>=well_size-40:
    print("rotation problem detected")
    rot_indicator="yes"
    final_bright = cv2.rotate(cut_bright_init, cv2.ROTATE_90_COUNTERCLOCKWISE)
 else:
    final_bright=cut_bright_init
 #final_bright=rot_bright[y_min-Margin:y_max+1+Margin,x_min-Margin:x_max+1+Margin]
 #rot_fluor = cv2.warpAffine(im_fluor,M,(cols,rows))
 #final_fluor=rot_fluor[y_min-Margin:y_max+1+Margin,x_min-Margin:x_max+1+Margin]
  
 #final_name=os.path.join(destin_folder,"final_%s_width_%s.tif" % (i,w))
 #cv2.imwrite(final_name, final)
 
 return final_bright,M,x_min,y_min, rows, cols, rot_indicator, rot_bright
##################################################################
############### this is for Step 1
def cut_all(file_names,progressbar,tk_frame,label,M, cols,rows,Margin, x_min,x_max,y_min,y_max, destin, window_size):
  new_names=[]
  rotated_images=[]
  #print("len(file_names)=", len(file_names))
  for i in range(len(file_names)):     
    progressbar["value"]=((i+1)/len(file_names))*100
    label.config(text="Frame " + str(i+1))     
    time.sleep(0.02)
    tk_frame.update_idletasks()
    file_name= file_names[i]
    #print("file_name=", file_name)                   
    img=cv2.imread(file_name,-1)  
    ###################################################
    
    angle=rect[2]      
    rows,cols = im.shape
    M = cv2.getRotationMatrix2D((cols//2,rows//2),angle,1)
   
    #########################################################
    #global  x_min, x_max,y_min, y_max, temp 
    temp=np.zeros(im.shape, np.uint8)
    cv2.drawContours(temp,[box],0,255,-1)
    dst = cv2.warpAffine(temp,M,(cols,rows))
 
    _,contours, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt=contours[0]
    rect_new = cv2.minAreaRect(cnt)             
    box_final = cv2.boxPoints(rect_new)    
    box_final = np.int0(np.round(box_final))

    xs=[box_final[k][0] for k in range(4)]
    ys=[box_final[k][1] for k in range(4)]
    x_min, x_max=min(xs), max(xs)
    y_min, y_max =min(ys), max(ys)
    
    fl_rot = cv2.warpAffine(img,M,(cols,rows))
    final=fl_rot[y_min-Margin:y_max+1+Margin, x_min-Margin:x_max+1+Margin]
    #final=dst[cy-length-Margin:cy+length+Margin,cx-length-Margin:cx+length+Margin]
    final_squeezed=cv2.resize(final, (382,382), interpolation = cv2.INTER_AREA)
    head, tail=os.path.split(file_name)
    new_name=os.path.join(destin,tail)
    #print("new_name=", new_name)
    cv2.imwrite(new_name, final_squeezed)
    new_names.append(new_name)
    if i==0:       
        first=final_squeezed
        first_tk=turn_image_into_tkinter(first, window_size)
              
  return first_tk, new_names  
###########################################################
def move(event):    
    global x_img,y_img, points, x_last,y_last,dx,dy
    x, y = event.x, event.y   
    points.append([x,y])       
    if len(points)>1:
         dx, dy=x-x_img,y-y_img
         canvas.move(imageFinal, dx,dy)
         canvas.update()
         x_last-=dx
         y_last-=dy                
    x_img = x
    y_img = y
def record_last_position(event):
    global points
    points=[]
def cut_and_save():      
      patch=im[y_last:y_last+382, x_last:x_last+382]
      cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\patch.tif", patch)
