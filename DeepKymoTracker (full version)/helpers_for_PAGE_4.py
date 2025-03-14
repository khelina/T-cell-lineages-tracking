import numpy as np
import cv2
import math
import os
from keras.optimizers import Adam
from keras.models import model_from_json
import re

from functions import segment_patch
from extract_lineage_for_Lorenzo import extract_lineage
Bordersize=100
#########################################

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
#######################################################

def load_tracked_movie(input_dir,output_dir):    
    path_filled_brights, path_filled_fluors, path_masks=[],[],[]
    

    empty_fluors, empty_brights, filled_fluors, filled_brights, masks=[],[],[],[],[]
    
    for filename in sorted_aphanumeric(os.listdir(input_dir)):
        if filename.endswith("ch02.tif"):
           im_bright=cv2.imread(os.path.join(input_dir, filename),0)
           #image_bright=cv2.cvtColor(im_bright,cv2.COLOR_GRAY2BGRA)
           empty_brights.append(im_bright)
        if filename.endswith("ch00.tif"):
           im_fluor=cv2.imread(os.path.join(input_dir, filename),0)
           #image_fluor=cv2.cvtColor(im_fluor,cv2.COLOR_GRAY2BGRA)
           empty_fluors.append(im_fluor)
           
    print("loaded empty images")       
    dir_bright=os.path.join(output_dir,"BRIGHT_MOVIE_RESULTS")
    for filename in sorted_aphanumeric(os.listdir(dir_bright)):
           path_im_bright=os.path.join(dir_bright, filename)
           im_bright_filled=cv2.imread(path_im_bright ,-1)
           path_filled_brights.append(path_im_bright)
           filled_brights.append(im_bright_filled)
        
    print("loaded bright filled  images")        
    dir_fluor=os.path.join(output_dir,"FLUORESCENT_MOVIE_RESULTS")
    for filename in sorted_aphanumeric(os.listdir(dir_fluor)):
           path_im_fluor=os.path.join(dir_fluor, filename)
           im_fluor_filled=cv2.imread(path_im_fluor ,-1)
           path_filled_fluors.append(path_im_fluor)
           filled_fluors.append(im_fluor_filled)
          
    print("loaded fluor filled  images")        
    dir_masks=os.path.join(output_dir, "HELPERS_(NOT_FOR_USER)","MASKS")
    for filename in sorted_aphanumeric(os.listdir(dir_masks)):
           path_im_mask=os.path.join(dir_masks, filename)
           im_mask=cv2.imread(path_im_mask ,-1)
           path_masks.append(path_im_mask)
           masks.append(im_mask)
           
    print("loaded masks")        
           
             
    lineage_per_frame=extract_lineage(output_dir)
    print("loaded lineage_per_frame") 
    
    return path_filled_brights,path_filled_fluors,path_masks, empty_fluors, empty_brights, filled_fluors, filled_brights, masks, lineage_per_frame
###############################################


def load_models_p5(software_folder):
   directory = os.path.join(software_folder, "TRAINED MODELS")
   model_names = ["Segmentor", "Refiner"]
   models = []
   for name in model_names:        
        full_name = os.path.join(directory, name)
        json_file = open(full_name + "-model.json", "r")
        model_read = json_file.read()
        json_file.close()        
        models.append((model_read, full_name)) 
   #global segmentor,refiner  
   segmentor = model_from_json(models[0][0])
   segmentor.load_weights(models[0][1] + "-weights.h5")   
   segmentor.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
   refiner = model_from_json(models[1][0])
   refiner.load_weights(models[1][1] + "-weights.h5")   
   refiner.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
   return segmentor, refiner
#########################################
def create_models_for_segmentation_correction(models):    
    segmentor = model_from_json(models[6][0])
    segmentor.load_weights(models[6][1] + "-weights.h5")   
    segmentor.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
    refiner = model_from_json(models[7][0])
    refiner.load_weights(models[7][1] + "-weights.h5")   
    refiner.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
    return segmentor, refiner
############################################
  
#############################################

##########################################################
def delete_contour_with_specific_colour(filled_image, empty_image,color):
    lower_thresh = np.array(color, dtype = "uint8")
    upper_thresh= np.array(color, dtype = "uint8")
    color_mask = cv2.inRange(filled_image, lower_thresh, upper_thresh)
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask.tif", color_mask)
    empty_image = cv2.cvtColor(empty_image,cv2.COLOR_GRAY2BGRA)
    filled_image[color_mask==255]=empty_image[color_mask==255]
    return filled_image
   
################################################
def update_lineage_after_manual_segm_correction(mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,cells_in_current_frame_sorted,frame_size, p_size):
    
    
    keys=list(frame_dictionary.keys())
    #print("keys=", keys)
    for i in range(len(modified_cell_IDs)):
       cell_ID=modified_cell_IDs[i]
       #print("cell_ID=",cell_ID)
       cell_name=frame_dictionary[ "cell_%s" % cell_ID][11]
       #print("cell_name=",cell_name)
       binary_image_with_one_cell =np.zeros((frame_size,frame_size),dtype="uint8")     
       binary_image_with_one_cell[mask==cell_ID+1] = 255
      
       im2, contours, hierarchy = cv2.findContours(binary_image_with_one_cell,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
       cell_contour=contours[0]                          
       new_area=np.round(cv2.contourArea(cell_contour),2)
       new_perimeter=np.round(cv2.arcLength(cell_contour,True),2)
       new_circularity=np.round(4*math.pi*new_area/new_perimeter**2,2)     
       M = cv2.moments(cell_contour) 
       if M["m00"]==0.:
          M["m00"]=0.001
       new_cX = np.round(M["m10"] / M["m00"],2)
       new_cY = np.round(M["m01"] / M["m00"],2)
       ##########################################
       new_base=cv2.copyMakeBorder(binary_image_with_one_cell , top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )
       a,b,c,d=int(round(new_cX))+Bordersize-p_size,int(round(new_cX))+Bordersize+ p_size,int(round(new_cY))+Bordersize-p_size,int(round(new_cY))+Bordersize+p_size           
       new_patch = new_base[c:d, a:b]  
       #########################################
      
       #old_path=os.path.join(path,"cell_%s.tif" %(cell_name))
       old_patch=frame_dictionary[ "cell_%s" % cell_ID][3]
       #new_path=os.path.join(path,"new_cell_%s.tif" %(cell_name))
       #cv2.imwrite(old_path,old_patch)
       #cv2.imwrite(new_path, new_patch )
       colour=frame_dictionary[ "cell_%s" % cell_ID][15]
       cv2.putText(filled_fluor,cell_name,(int(new_cX)-10,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,1,colour,1)
       cv2.putText(filled_bright,cell_name,(int(new_cX)-10,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,1,colour,1)
       
       old_area=frame_dictionary[ "cell_%s" % cell_ID][18]
       old_perimeter=frame_dictionary[ "cell_%s" % cell_ID][19]
       old_circularity=frame_dictionary[ "cell_%s" % cell_ID][20]
      
       ######## update frame_dictionary
       frame_dictionary["cell_%s" % cell_ID][3]=new_patch
       frame_dictionary["cell_%s" % cell_ID][6]=[new_cX,new_cY]
       frame_dictionary["cell_%s" % cell_ID][7]=a
       frame_dictionary["cell_%s" % cell_ID][8]=b
       frame_dictionary["cell_%s" % cell_ID][9]=c
       frame_dictionary["cell_%s" % cell_ID][10]=d
       frame_dictionary["cell_%s" % cell_ID][18]=new_area
       frame_dictionary["cell_%s" % cell_ID][19]=new_perimeter
       frame_dictionary["cell_%s" % cell_ID][20]=new_circularity
       
###########################################
"""
def begin_with_one_cell():# after pushing button "1 cell"
    stop_flash("radio", page4, flashers)
    feedback_label.configure(text="Calculating position of cell in Frame 1 ...")
    R1.configure(bg="red")
    R2.configure(bg=button_color)
    global coords, coords_very_first
    
           
    full_name = os.path.join(directory, "Tracker-1")
    print("full_name=", full_name)
    json_file = open(full_name + "-model.json", "r")
    model_read = json_file.read()
    json_file.close()        
        
    tracker_1 = model_from_json(model_read)
    tracker_1.load_weights(full_name + "-weights.h5")   
    tracker_1.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
       
    coords = predict_first_frame(fluor_images_compressed, tracker_1)  
    coords_very_first= coords.tolist()
    print("coords=", coords)    
    global colours, template_names, prev_frame
    colours, template_names = create_color_dictionary(
        max_number_of_cells, coords.shape[0])# 10 =maximum number of cells
    global xs
    xs=create_dictionary_of_xs( template_names, coords_very_first, num_frames)
  
    global text
    text = template_names[:coords.shape[0]]
    
    R2.configure(bg=button_color, fg="black")
    R1.configure(bg="black", fg="#00FFFF")
    
    start_flash([button_execute], "exec", page4, flashers)
    feedback_label.config(text="The centroids of the cell in Frame 1 has been calculated.\n\nTo start execution, press Button 3.")    
####################################   
"""       
       
       
       
       
       
 