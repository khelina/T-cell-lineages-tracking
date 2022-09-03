import re
import os
import cv2
import numpy as np
from keras.models import model_from_json
from keras.optimizers import Adam
import tensorflow as tf
os.chdir("C:\\Users\\kfedorchuk\\Documents\\EXECUTE")# this is the directory of the folder EXECUTION`
from postprocess import Cleaner_1
######################################
N_channels=1 # for tracking networks
N_CHANNELS=3 # for ensemble (segmentation) network
N_frames=4 
N_cells=4 
Coeff=382.0/100.0
Colors=[[0,0,255,255],[0,128,255,255],[0,255,0,255],[255,0,0,255]]
Bordersize=48+5+6
#######################################################################
def standardize(frame): #normalizing per channel
     frame = frame.astype('float32')
     means = frame.mean(axis=(0,1), dtype='float64')
     stds = frame.std(axis=(0,1), dtype='float64')    
     frame = (frame - means) / stds
     return frame
##############################################################################
def create_output_folders(outpath):
   subfolders=[]
   subfolder_names=["TRACKED",
                 "TRACKED_PLUS_SEGMENTED_CARTOON",             
                 "PATCHES_FROM_SEGMENTOR",
                 "TRACKED_PLUS_CONTOURS",
                 "SEGMENTED_BLACK_AND_WHITE",
                 "TRACKED_CORRECTED",
                 "PATCHES_FROM_REFINER",
                 "PATCHES_FROM_ENSEMBLE",
                 "CLEANED_PATCHES"]              
   for i in range(len(subfolder_names)):
       destination=os.path.join(outpath,subfolder_names[i])
       os.mkdir(destination)
       subfolders.append(destination)
   return subfolders
##############################################################################################               
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##################################################################################
def load_images(folder_dir):
 fluor_files=[]
 bright_files=[]
 fluor_compressed=[]
 fluor_names=[]
 bright_names=[]
 inputs=[]
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
 inputs.append(fluor_compressed)
 inputs.append(fluor_files)
 inputs.append(bright_files)
 inputs.append(fluor_names)
 inputs.append(bright_names) 
 return inputs

############################################## 
def rename_file(destin,infile):       
 infile = os.path.normpath(infile) 
 old=infile.split(os.sep)
 new1=old[-1]
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
################################################
def rename_segmented(destin,infile):       
 infile = os.path.normpath(infile) 
 old=infile.split(os.sep)
 new1=old[-1]
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new) 
 newest=base+"_Segmented.tif" 
 return newest
#######################################################
def refiner_predict(output_segm,fluor,bright,model):# output_1 is binary 0,255 image, not normalized
    frame=np.zeros((96,96,3))
    frame[:,:,0]=np.array(fluor.reshape((96,96)),dtype="float32")               
    frame[:,:,1]=np.array(bright.reshape((96,96)),dtype="float32")
    frame[:,:,2]=np.array(output_segm.reshape((96,96)),dtype="float32")  
    means = frame.mean(axis=(0,1), dtype='float64')
    stds = frame.std(axis=(0,1), dtype='float64')    
    frame = (frame - means) / stds     
    frame=frame.reshape((1,96,96,3))
    segmentation=model.predict(frame, batch_size=1,verbose=0)  
    pred1=np.round(segmentation)
    output0=np.int_(pred1)
    output0=output0*255
    output=output0.reshape((96,96))
    output.astype(np.uint8)
    return output
###############################################################################
def recalculate_centres(cells):
    for i in range(N_cells):
        cell=cells["cell_%s" % i]       
        black=np.zeros((382,382),dtype="uint8")
        black_border=cv2.copyMakeBorder(black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
        a,b,c,d=cell[7],cell[8],cell[9],cell[10] 
        black_border[c:d, a:b]=cell[3]
        black_again=black_border[Bordersize:382+Bordersize,Bordersize:382+Bordersize]
        im2, contours, hierarchy = cv2.findContours(black_again.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
        if len(contours)==1:
         for c in contours:	
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])              
         x0=cell[0]
         x1=cell[1]
         x2=cell[2]
         x3=cell[3]
         x4=cell[4]
         x5=cell[5]
         #x6=[x00,y00]
         x6=[cX,cY]
         a,b,c,d=cell[7],cell[8],cell[9],cell[10]
         del cell
         cells["cell_%s" % i]=[x0,x1,x2,x3,x4,x5,x6,a,b,c,d]
    return cells
##############################################################################################
def draw_exact_pixel_markers(image,coord):
   N_cells=coord.shape[0]
   coord=np.round_(coord)
   coord=np.int_(coord)
   x1,y1=coord[0]  
   image[y1-20:y1+20,x1-20:x1+20]=255
   if N_cells==1:
      return image
   else:
      x2,y2=coord[1] 
      image[y2-20:y2+20,x2-20:x2+20]=125
   if N_cells==2:
      return image
   else:
      x3,y3=coord[2] 
      image[y3-20:y3+20,x3-20:x3+20]=60
   if N_cells==3:
      return image
   else:
      x4,y4=coord[3]
      image[y4-20:y4+20,x4-20:x4+20]=30
   if N_cells==4:
      return image
   else:
      x5,y5=coord[4]
      image[y5-20:y5+20,x5-20:x5+20]=20 
      return image
#############################################################
def predict_tracking(coords,fluor_images,fluor_images_compressed,fluor_names,k,destination,Models):
   test_samples=np.zeros((1,100,100,5))    
   im_list=[]
   names_list=[]   
   markers_empty = np.zeros((382,382), np.uint8)
   markers=draw_exact_pixel_markers(markers_empty,coords)
   model_track=Models[0]  
   im_list.append(markers)  
   frame1 = cv2.resize(markers, (100, 100), interpolation = cv2.INTER_LANCZOS4)                    
     
   VIDEO=np.zeros((100,100,5))
   frame0=frame1
   frame=(frame0-np.mean(frame0))/np.std(frame0)
   VIDEO[:,:,0]=frame
   name0= os.path.join(destination,"frame_%s.tif" % k)
   names_list.append(name0)  
  
   for ii in range(4):     
       frame1=fluor_images_compressed[k+ii]
       name=fluor_names[k+ii]
       names_list.append(name)
       im_list.append(fluor_images[k+ii])
       frame0=frame1
       frame=(frame0-np.mean(frame0))/np.std(frame0)
       VIDEO[:,:,ii+1]=frame               
   test_samples[0,:,:,:]=VIDEO
   test_samples=test_samples.reshape((1,100,100,5,1))
   if N_cells==1:
       test_samples=test_samples[:,:,:,1:,:]
   prediction=model_track.predict(test_samples,batch_size=1,verbose=0)   
   clip_centr=[(prediction[ii]*100.0*Coeff).reshape((N_cells,2)) for ii in range(4)]
   
   for ii in range(5):# plotting tracked results
      img=im_list[ii]
      name=names_list[ii]
      im1 = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)            
      if ii>0:
       x=np.int_(np.round_(prediction[ii-1]*100.0*Coeff).reshape((N_cells,2)))
       cv2.rectangle(im1,(x[0][0]-20,x[0][1]-20),(x[0][0]+20,x[0][1]+20),Colors[0],1)
       if N_cells>1:
         cv2.rectangle(im1,(x[1][0]-20,x[1][1]-20),(x[1][0]+20,x[1][1]+20),Colors[1],1)
       if N_cells>2:
         cv2.rectangle(im1,(x[2][0]-20,x[2][1]-20),(x[2][0]+20,x[2][1]+20),Colors[2],1)
       if N_cells>3:
         cv2.rectangle(im1,(x[3][0]-20,x[3][1]-20),(x[3][0]+20,x[3][1]+20),Colors[3],1)
       if N_cells>4:
         cv2.rectangle(im1,(x[4][0]-20,x[4][1]-20),(x[4][0]+20,x[4][1]+20),Colors[4],1)          
       newname = rename_file(destination,name)
       cv2.imwrite(newname,im1) 
   return clip_centr
########################################################################

def segment_frame(raw_images,bright_images,clip_centr,coords,k,kk,Models):# segments clip and creates dictionary of cells
       #create borders for input 382x382 frames to be able to cut out patches 
       empty_fluor=raw_images[k+kk]      
       empty_fluor_border1=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )            
       empty_bright=bright_images[k+kk]
       empty_bright_border1=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )            
       cells={}
       for kkk in range(N_cells):        
         x0,y0=clip_centr[kk][kkk][0],clip_centr[kk][kkk][1]
         x00,y00=coords[kkk][0],coords[kkk][1]         
         zero_frame=np.zeros((382,382),dtype="uint8")
         empty_zero_border=cv2.copyMakeBorder(zero_frame, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )                
         empty_zero_border[int(round(y00))-20+Bordersize:int(round(y00))+20+Bordersize,int(round(x00))-20+Bordersize:int(round(x00))+20+Bordersize]=255# here I draw square       
         empty_fluor_border=empty_fluor_border1.copy()
         empty_bright_border=empty_bright_border1.copy()         
         a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48           
         empty=np.stack((empty_fluor_border,empty_bright_border,empty_zero_border),axis=2)
         patch = empty[c:d, a:b,:]
         patch_fluor=empty_fluor_border[c:d,a:b]
         patch_bright=empty_bright_border[c:d,a:b]        
         patch_zero=empty_zero_border[c:d,a:b]       
         frame0=patch
         frame=standardize(frame0)
         inframe=frame.reshape((1,96,96,3))       
         segmentation=Models[1].predict(inframe,batch_size=1,verbose=0)# Segmentor       
         pred1=np.round(segmentation)
         output0=np.int_(pred1)
         output0=output0*255
         output_raw=output0.reshape((96,96))
         output_raw=output_raw.astype(np.uint8)     
         refiner_output=refiner_predict(output_raw,patch_fluor,patch_bright,Models[2])# Refiner        
         refiner_output=refiner_output.astype(np.uint8)
         ensemble_output=output_raw+refiner_output        
         sum_clean=Cleaner_1(ensemble_output,patch_zero)
         cells["cell_%s" % kkk]=[output_raw,refiner_output,ensemble_output,sum_clean,empty_fluor_border,empty_bright_border,[x0,y0],a,b,c,d]        
       return cells 
###################################################

