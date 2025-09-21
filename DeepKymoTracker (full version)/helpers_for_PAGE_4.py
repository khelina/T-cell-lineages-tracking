import numpy as np
import cv2
import math
import os
from keras.optimizers import Adam
from keras.models import model_from_json
import re

from functions import segment_patch
from print_excel import extract_lineage
#Bordersize=100
#########################################

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
#######################################################

def load_tracked_movie_p5(input_dir,output_dir):    
    path_filled_brights, path_filled_fluors, path_filled_reds,path_masks=[],[],[],[]
    

    empty_fluors, empty_brights, empty_reds,filled_fluors, filled_brights,filled_reds, masks=[],[],[],[],[],[],[]
    
    for filename in sorted_aphanumeric(os.listdir(input_dir)):
        if filename.endswith("ch02.tif"):
           im_bright=cv2.imread(os.path.join(input_dir, filename),0)
           #image_bright=cv2.cvtColor(im_bright,cv2.COLOR_GRAY2BGRA)
           empty_brights.append(im_bright)
        if filename.endswith("ch00.tif"):
           im_fluor=cv2.imread(os.path.join(input_dir, filename),0)
           #image_fluor=cv2.cvtColor(im_fluor,cv2.COLOR_GRAY2BGRA)
           empty_fluors.append(im_fluor)
        if filename.endswith("ch01.tif"):
           im_red=cv2.imread(os.path.join(input_dir, filename),0)
           #image_fluor=cv2.cvtColor(im_fluor,cv2.COLOR_GRAY2BGRA)
           empty_reds.append(im_red)
           
    print("loaded empty images")       
    dir_bright=os.path.join(output_dir,"TRACKED_BRIGHTFIELD_CHANNEL")
    for filename in sorted_aphanumeric(os.listdir(dir_bright)):
           path_im_bright=os.path.join(dir_bright, filename)
           im_bright_filled=cv2.imread(path_im_bright ,-1)
           path_filled_brights.append(path_im_bright)
           filled_brights.append(im_bright_filled)
        
    print("loaded bright filled  images")        
    dir_fluor=os.path.join(output_dir,"TRACKED_GREEN_FL_CHANNEL")
    for filename in sorted_aphanumeric(os.listdir(dir_fluor)):
           path_im_fluor=os.path.join(dir_fluor, filename)
           im_fluor_filled=cv2.imread(path_im_fluor ,-1)
           path_filled_fluors.append(path_im_fluor)
           filled_fluors.append(im_fluor_filled)
           
    dir_red=os.path.join(output_dir,"TRACKED_RED_FL_CHANNEL")
    for filename in sorted_aphanumeric(os.listdir(dir_red)):
           path_im_red=os.path.join(dir_red, filename)
           im_red_filled=cv2.imread(path_im_red ,-1)
           path_filled_reds.append(path_im_red)
           filled_reds.append(im_red_filled)
          
    print("loaded fluor filled  images")        
    dir_masks=os.path.join(output_dir, "HELPER_FOLDERS_(NOT FOR USER)","MASKS")
    for filename in sorted_aphanumeric(os.listdir(dir_masks)):
           path_im_mask=os.path.join(dir_masks, filename)
           im_mask=cv2.imread(path_im_mask ,-1)
           
           #scaled_mask=scaled_mask.astype(np.float16)
           #print("im_mask.dtype=",im_mask.dtype)
           #print("np.max(im_mask)=",np.max(im_mask))
           path_masks.append(path_im_mask)
           masks.append(im_mask)
           del im_mask
           
    print("loaded masks")        
           
    helper_dir_p5=os.path.join(output_dir,"HELPER_FOLDERS_(NOT FOR USER)")         
    lineage_per_frame=extract_lineage(helper_dir_p5)
    print("loaded lineage_per_frame") 
    
    return path_filled_brights,path_filled_fluors,path_filled_reds,path_masks, empty_fluors, empty_brights,empty_reds, filled_fluors, filled_brights,filled_reds, masks, lineage_per_frame
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
################# works for colorues text as well - removes it
def delete_contour_with_specific_colour(filled_image, empty_image,color):
    lower_thresh = np.array(color, dtype = "uint8")
    upper_thresh= np.array(color, dtype = "uint8")
    color_mask = cv2.inRange(filled_image, lower_thresh, upper_thresh)
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask.tif", color_mask)
    empty_image = cv2.cvtColor(empty_image,cv2.COLOR_GRAY2BGRA)
    filled_image[color_mask==255]=empty_image[color_mask==255]
    return filled_image
######################## for step-4 (segmentation correctiob)
def make_contour_red(filled_image, empty_image,color):
    lower_thresh = np.array(color, dtype = "uint8")
    upper_thresh= np.array(color, dtype = "uint8")
    color_mask = cv2.inRange(filled_image, lower_thresh, upper_thresh)
    cv2.imwrite("C:\\Users\\helina\\Desktop\\color_mask.tif", color_mask)
    #empty_image = cv2.cvtColor(empty_image,cv2.COLOR_GRAY2BGRA)
    filled_image=delete_contour_with_specific_colour(filled_image, empty_image,color)
    filled_image[color_mask==255]=[0,0,255,255]
    cv2.imwrite("C:\\Users\\helina\\Desktop\\red_contor.tif", filled_image)
    return filled_image
################################################
def update_frame_dictionary_after_manual_segm_correction(mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,frame_size, patch_size, bordersize):    
    keys=list(frame_dictionary.keys())
    modified_cells=list(modified_cell_IDs.keys())
    #print("keys=", keys)
    for cell_ID in modified_cells:
       #cell_ID=modified_cell_IDs[i]
       print("cell_ID=",cell_ID)
       cell_name=frame_dictionary[ "cell_%s" % cell_ID][11]
       print("cell_name=",cell_name)

       ######################################
       binary_image_with_one_cell=modified_cell_IDs[cell_ID][0]
       cv2.imwrite(r"C:\Users\helina\Desktop\binary_image_with_one_cell.tif",binary_image_with_one_cell)
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
       new_base=cv2.copyMakeBorder(binary_image_with_one_cell , top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )
       a_new,b_new,c_new,d_new=int(round(new_cX))+bordersize-patch_size,int(round(new_cX))+bordersize+ patch_size,int(round(new_cY))+bordersize-patch_size,int(round(new_cY))+bordersize+patch_size           
       new_patch = new_base[c_new:d_new, a_new:b_new]
       cv2.imwrite(r"C:\Users\helina\Desktop\new_patch.tif",new_patch)
       #########################################
       new_mask=modified_cell_IDs[cell_ID][1]
       #old_path=os.path.join(path,"cell_%s.tif" %(cell_name))
       #old_patch=frame_dictionary[ "cell_%s" % cell_ID][3]
       #new_path=os.path.join(path,"new_cell_%s.tif" %(cell_name))
       #cv2.imwrite(old_path,old_patch)
       #cv2.imwrite(new_path, new_patch )
       colour=frame_dictionary[ "cell_%s" % cell_ID][15][0]
       cv2.putText(filled_fluor,cell_name,(int(new_cX)-10,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,1,colour,1)
       cv2.putText(filled_bright,cell_name,(int(new_cX)-10,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,1,colour,1)
       
       #old_area=frame_dictionary[ "cell_%s" % cell_ID][18]
       #old_perimeter=frame_dictionary[ "cell_%s" % cell_ID][19]
       #old_circularity=frame_dictionary[ "cell_%s" % cell_ID][20]
      
       ######## update frame_dictionary
       frame_dictionary["cell_%s" % cell_ID][3]=new_patch
       frame_dictionary["cell_%s" % cell_ID][6]=[new_cX,new_cY]
       frame_dictionary["cell_%s" % cell_ID][7]=a_new
       frame_dictionary["cell_%s" % cell_ID][8]=b_new
       frame_dictionary["cell_%s" % cell_ID][9]=c_new
       frame_dictionary["cell_%s" % cell_ID][10]=d_new
       frame_dictionary["cell_%s" % cell_ID][13]=new_mask
       frame_dictionary["cell_%s" % cell_ID][18]=new_area
       frame_dictionary["cell_%s" % cell_ID][19]=new_perimeter
       frame_dictionary["cell_%s" % cell_ID][20]=new_circularity
       final_patch= frame_dictionary["cell_%s" % cell_ID][3]
       cv2.imwrite(r"C:\Users\helina\Desktop\final_patch.tif",final_patch)
    return frame_dictionary  
###########################################
def update_cheatsheet(cheatsheets,mode,bg_color,label_color):
    if mode=="neutral":
        for k in range(8):
            cheatsheets[k].config(text=" ", bg=bg_color)
    else:
        cheatsheets[0].config(text="Choose cell:",bg=label_color, fg="black")
        cheatsheets[1].config(text="Right-click",bg=label_color, fg="red")
        cheatsheets[2].config(text="CREATE contour:",bg=label_color, fg="black")
       
        cheatsheets[4].config(text="SAVE contour:",bg=label_color, fg="black")
        cheatsheets[5].config(text="Right-click\ninside magenta circle",bg=label_color, fg="red")
        cheatsheets[6].config(text="DELETE contour:",bg=label_color, fg="black")
        cheatsheets[7].config(text="Right-click\nanywhere on background",bg=label_color, fg="red")
        if mode=="fast":
            cheatsheets[3].config(text="Left-click",bg=label_color, fg="red")
            cheatsheets[6].config(text=" ",bg=bg_color, fg="black")
            cheatsheets[7].config(text=" ",bg=bg_color, fg="black")
        else:
            cheatsheets[3].config(text="Draw with mouse",bg=label_color, fg="red")
            cheatsheets[6].config(text="DELETE contour:",bg=label_color, fg="black")
            cheatsheets[7].config(text="Right-click\nanywhere on background",bg=label_color, fg="red")