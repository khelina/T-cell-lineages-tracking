import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import xlsxwriter
import os
import pickle
import re 
from PIL import ImageTk, Image
import tkinter
#############################################################
Bordersize=100
##############################################################
def create_pedigree(lineage_per_frame,outpath):
  a=[(lineage_per_frame[i].keys(),i) for i in range(len(lineage_per_frame))] 
  names=[]
  for k in range(len(lineage_per_frame)):
    item =lineage_per_frame[k]
    keys =list(item.keys())
    names+=[item[key][11] for key in keys]
  cell_names =list(set(names))
 
  pedigree ={}
  centroids_per_cell_dict={}
  for name in cell_names:
    pedigree["cell-%s" % name]=[]
    centroids_per_cell_dict["cell-%s" % name]=[]
  for i in range(len(lineage_per_frame)):   
     item =lineage_per_frame[i]
     keys =list(item.keys())
     for key in keys:
        cell_name=item[key][11]
        frame=item[key][12]
        cX,cY=item[key][6][0],item[key][6][1]
        a,b,c,d=item[key][7],item[key][8],item[key][9],item[key][10]       
        patch_before=item[key][3]     
        base=np.zeros((382+2*Bordersize,382+2*Bordersize),dtype="uint8")
        base[c:d,a:b]=patch_before
        patch_after=base[int(cY)-48+Bordersize:int(cY)+48+Bordersize,int(cX)-48+Bordersize:int(cX)+48+Bordersize]       
        im2, contours, hierarchy = cv2.findContours(patch_after,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                         
        area=np.round(cv2.contourArea(contours[0]),2)
        perimeter=np.round(cv2.arcLength(contours[0],True),2)
        circularity=np.round(4*math.pi*area/perimeter**2,2)
        patch_color=np.zeros((patch_after.shape[0], patch_after.shape[1],3), np.uint8)           
        coll=item[key][15][:-1]
        patch_color[patch_after==255]=coll        
        add=[cell_name,frame,patch_color,[cX,cY],area,perimeter,circularity, coll]
        add_fed=[frame,[cX,cY]] 
        pedigree["cell-%s" % item[key][11]].append(add)
        centroids_per_cell_dict["cell-%s" % item[key][11]].append(add_fed)
      
  pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
  with open(pedigree_path, 'wb') as f:
         pickle.dump(pedigree, f)  
  return pedigree
####################################################################
def create_dictionary_of_xs( template, coords_very_first, num_frames):    
  first_text=template[:len(coords_very_first)]  
  numbers =[len(item) for item in template]
  max_number =max(numbers)
  if len(coords_very_first)==1:
    xs ={"1":int(num_frames/2)}
  else:
    xs={}
    for i  in range(len(first_text)):
        xs[first_text[i]]=int((num_frames/(len(first_text)+1))*(i+1))
  for k in range(len(template)):
       cell_name =template[k]        
       kk=len(cell_name)
       if kk<max_number:
         item_1=xs[cell_name]-num_frames/(2**(kk+1))
         item_2=xs[cell_name]+num_frames/(2**(kk+1))            
         xs[cell_name+"0"]=int(item_1)
         xs[cell_name+"1"]=int(item_2)              
  return xs
#################################################
def create_lineage_image_one_frame(out_folders,cells, previous_lineage_image, xs, frame):
 temp_path=out_folders[3]#  "LINEAGE_IMAGES",was [5]
 ###### prepare points for lineage images ######
 rrad=10# radius of plotted point in lineage image
 size=previous_lineage_image.shape[0]
 points=[]# points for plotting animated lineage
 keys=cells.keys()
 for key in keys:
   item=cells[key]   
   cell_name=item[11]
   x=xs[cell_name]
   y = item[12]# y=frame_number
   colour=item[15][:-1]   
   if size <=382:    
       rrad=1      
   points.append(((x,y),colour)) 
   # more points for the  case of division (horizontal lines drawing)  
   if item[16]=="daughter-1":
          start=cell_name[:-1]                
          more_points=[((xx,y),colour) for xx in range(xs[start+"0"],xs[start],1)]    
          points+=more_points 
   if item[16]=="daughter-2":      
          start=cell_name[:-1]                   
          more_points=[((xx,y),colour) for xx in range(xs[start],xs[start+"1"],1)]    
          points+=more_points        
   ######### create lineage image at last                    
 for p in range(len(points)):
      cv2.circle(previous_lineage_image, points[p][0], rrad, points[p][1], -1)
 current_lineage_image= previous_lineage_image      
 dest =os.path.join(temp_path,"tree_%s.tif" % (frame))
 cv2.imwrite(dest, current_lineage_image) 
 still_lineage=current_lineage_image
 cv2.imwrite(os.path.join( os.path.dirname(temp_path),"still_lineage.tif"), still_lineage)
 return current_lineage_image    
##########################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
#################################################
def load_files(folder_dir):# load linegae images and segmented images to create final movie
 images=[]
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith(".tif"):
        full_name=os.path.join(folder_dir, filename)      
        image=cv2.imread(full_name,1)
        images.append(image)       
 return images
############ prepare images for movie
def create_output_movie(outpath,out_folders, frame_size):
 print("Creating images for movie and saving in TEMPORARY_FOR_MOVIE folder")
 images_out_path=os.path.join(outpath,out_folders[1])
 images_seg=load_files(out_folders[5])# was [9]
 print("len(images_seg)=", len(images_seg)) 
 images_lin=load_files(out_folders[3])# was [5]
 print("len(images_lin)=", len(images_lin))
 images=[]
 for i in range(len(images_lin)):
    img=np.zeros((frame_size,frame_size*2,3))
    im_seg_resized =cv2.resize(images_seg[i], (frame_size,frame_size), interpolation = cv2.INTER_AREA)
    img[:,:frame_size,:]= im_seg_resized 
    im_lin_resized =cv2.resize(images_lin[i], (frame_size,frame_size), interpolation = cv2.INTER_AREA)
    img[:,frame_size:,:]=  im_lin_resized 
    texxt=str(i+1)
    cv2.putText(img,texxt,(frame_size+10,12),cv2.FONT_HERSHEY_PLAIN,1,(0,255,255),1)          
    images.append(img)
    destin=os.path.join(images_out_path,"movie_%s.tif" % (i+1))
    cv2.imwrite(destin, img)
############## create and save movie
 print("Creating output movie and saving as .avi")
 video_name = os.path.join(outpath,"lineage_movie.avi")
 frame=images[0]
 height, width, layers = frame.shape
 video = cv2.VideoWriter(video_name, 0, 10, (width,height))
 for image in images:   
    video.write(np.uint8(image))
 cv2.destroyAllWindows()
 video.release()
 print("Finished")
 del images_seg
 del images_lin
 del images
##################################################
