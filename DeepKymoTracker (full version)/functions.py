import os
import cv2
import numpy as np
import math
from scipy.optimize import linear_sum_assignment
import itertools
import pickle
import copy
from plot import paste_benchmark_patch
######################################################## 
Bordersize=100
################## Apply Tracker-1  to predict centroids in Frame 1 with 1 cell only
def predict_first_frame(first_clip_compressed, model):
     test_samples=np.zeros((1,100,100,4))  
     VIDEO=np.zeros((100,100,4))    
     for ii in range(4):     
        frame0=first_clip_compressed[ii]
        frame=frame0/255.
        #frame=(frame0-np.mean(frame0))/np.std(frame0)
        VIDEO[:,:,ii]=frame               
     test_samples[0,:,:,:]=VIDEO
     test_samples=test_samples.reshape((1,100,100,4,1))   
     prediction=model.predict(test_samples,batch_size=1,verbose=0)   
     clip_centr=[(prediction[iii]*382.0).reshape((1,2)) for iii in range(4)]
     return clip_centr[0]
################ Apply Tracker-N to predict centroids in Frame 1

################ This is onl;y for Tracker-1-seeded
def draw_exact_pixel_markers_new(image,coord, cell_radius):
   N_cells=coord.shape[0]
   coord=np.round_(coord)
   coord=np.int_(coord)
   x1,y1=coord[0]  
   image[y1-cell_radius:y1+cell_radius,x1-cell_radius:x1+cell_radius]=255   
   return image
################## Prepare seed channel for the input to a tracker
def draw_exact_pixel_markers(image,coord, cell_radius):   
   r=cell_radius
   N_cells=coord.shape[0]
   coord=np.round_(coord)
   coord=np.int_(coord)
   x1,y1=coord[0]  
   image[y1-r:y1+r,x1-r:x1+r]=255
   if N_cells==1:
      return image
   else:
      x2,y2=coord[1] 
      image[y2-r:y2+r,x2-r:x2+r]=125
   if N_cells==2:
      return image
   else:
      x3,y3=coord[2] 
      image[y3-r:y3+r,x3-r:x3+r]=60
   if N_cells==3:
      return image
   else:
      x4,y4=coord[3]
      image[y4-r:y4+r,x4-r:x4+r]=30
   if N_cells==4:
      return image
   else:
      x5,y5=coord[4]
      image[y5-r:y5+r,x5-r:x5+r]=20 
      return image
#############################################################
def rename_file(destin,infile):       
 infile = os.path.normpath(infile) 
 old=infile.split(os.sep)
 new1=old[-1]
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
###################################################
def predict_tracking_general(coords,fluor_images,fluor_images_compressed,fluor_names,k,destination,trackers,n, cell_radius, frame_size): 
  N_cells=coords.shape[0]  
  # if clip length is too short replicate necessary number of frames
  remaining=4
  if n-k<4:# n-k= how many in the last clip      
       additional=4-(n-k)
       remaining=4-additional
       im=fluor_images_compressed[n-k-1]# was n-1
       for pp in range (additional):
           fluor_images_compressed.append(im)         
  clip_centr=[np.zeros((N_cells,2)) for ii in range(4)]# this is the format
  
   
  tracker_6=trackers[5]
  for ii in range(0,N_cells, 1):    
          cds=coords[ii:ii+1]
          centroids=predict_tracking(cds,fluor_images,fluor_images_compressed,fluor_names,k,destination,tracker_6,n, cell_radius, frame_size)    
          for kk in range(4):          
             for kkk in range(1):# was 2
                clip_centr[kk][ii+kkk]=centroids[kk][kkk]
  clip_centr=clip_centr[:(remaining)]  
  return clip_centr
######################################################
def predict_tracking(coords,fluor_images,fluor_images_compressed,fluor_names,k,destination,tracker,n, cell_radius, frame_size):
   VIDEO=np.zeros((100,100,5))
   print("frame_size=", frame_size)
   seed_empty=np.zeros((frame_size,frame_size), np.uint8)    
   coords_norm=np.zeros(coords.shape)  
   coords_norm[0,0]=coords[0][0]
   coords_norm[0,1]=coords[0][1]  
   markers=draw_exact_pixel_markers_new(seed_empty,coords_norm, int(cell_radius))
   seed_frame = cv2.resize(markers, (100, 100), interpolation=cv2.INTER_AREA)

#############################################
   seed_normalised=seed_frame/255.          
   #seed_normalised=(seed_frame-np.mean(seed_frame))/np.std(seed_frame)
   VIDEO[:,:,0]=seed_normalised  
   for ii in range(4):     
       frame_fl=fluor_images_compressed[0+ii]
       frame=frame_fl/255. 
       #frame=(frame_fl-np.mean(frame_fl))/np.std(frame_fl)
       VIDEO[:,:,ii+1]=frame
   ####################################
   for_debug=np.zeros((100,100,3))
   for_debug[:,:,0]=VIDEO[:,:,0]*100
   for_debug[:,:,1]=VIDEO[:,:,1]*100
   for_debug[:,:,2]=VIDEO[:,:,2]
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\debug\\debug_clip_%s.tif" %(k), for_debug)
   ######################
   test_samples=np.zeros((1,100,100,5))             
   test_samples[0,:,:,:]=VIDEO
   test_samples=test_samples.reshape((1,100,100,5,1))
   n_cells=coords.shape[0]
   #if n_cells==1:
       #test_samples=test_samples[:,:,:,1:,:]
   prediction=tracker.predict(test_samples,batch_size=1,verbose=0)  
   clip_centr=[(prediction[ii]*float(frame_size)).reshape((n_cells,2)) for ii in range(4)]  
   del test_samples
   del VIDEO
   del markers
   del seed_normalised
   del prediction
   return clip_centr
############## Backup tracking by linear association ( when tracker outputs too big jumps)
def backup_track(clip_centr,coords,kk, cell_radius):# corrects tracking errors in frame kk
    distances=[]
    frame=clip_centr[kk]
    for i in range(len(coords)):       
     dist=math.sqrt((frame[i][0]-coords[i][0])**2+(frame[i][1]-coords[i][1])**2)
     if dist>=cell_radius:
         frame[i]=coords[i]
         clip_centr[kk]=frame
    return clip_centr
#################################################
def force_manual_IDs(clip_centr,coords,kk, cell_radius):# corrects tracking errors in frame kk
    if kk==0:
        clip_centr[kk]=coords
    else:
       frame=clip_centr[kk]
       for i in range(len(coords)):                 
           frame[i]=coords[i]
           clip_centr[kk]=frame   
    return clip_centr
######################################################
def force_manual_IDs_old(clip_centr,coords,kk, cell_radius):# corrects tracking errors in frame kk
    if kk==0:
        clip_centr[kk]=coords
    else:
       distances=[]
       frame=clip_centr[kk]
       for i in range(len(coords)):       
          dist=math.sqrt((frame[i][0]-coords[i][0])**2+(frame[i][1]-coords[i][1])**2)
          if dist>=cell_radius:
           frame[i]=coords[i]
           clip_centr[kk]=frame
   
    return clip_centr
#########################################
def refiner_predict(output_segm,fluor,bright,refiner):# output_segm is binary 0,255 image, not normalized
    frame=np.zeros((96,96,3))
    frame[:,:,0]=np.array(fluor.reshape((96,96)),dtype="float32")               
    frame[:,:,1]=np.array(bright.reshape((96,96)),dtype="float32")
    frame[:,:,2]=np.array(output_segm.reshape((96,96)),dtype="float32")  
    means = frame.mean(axis=(0,1), dtype='float64')
    stds = frame.std(axis=(0,1), dtype='float64')  
    stds[stds==0.0]=0.001
    frame = (frame - means) / stds     
    frame=frame.reshape((1,96,96,3))
    segmentation=refiner.predict(frame, batch_size=1,verbose=0)  
    pred1=np.round(segmentation)
    output0=np.int_(pred1)
    output0=output0*255
    output=output0.reshape((96,96))
    output.astype(np.uint8)
    return output
#############################################
def find_centroids(im):# finds centroid of one cell present in an image   
    if im.dtype!='uint8':
         im = im.astype('uint8')
    im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                         
    c=contours[0]   
    M = cv2.moments(c) 
    if M["m00"]==0.:
        M["m00"]=0.001
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])  
    return cX,cY
####################################
def extract_detected_intensities(final_list):
    ints=[]
    for i in range(len(final_list)):
        llist=final_list[i][5]
        ints+=llist
    return ints
#########################################################
def calculate_cell_parametres(segmented_patch,a,b,c,d, frame_size):
    image_with_one_cell_border=np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="uint8")     
    image_with_one_cell_border[c:d, a:b] = segmented_patch
    final_image=image_with_one_cell_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize] 
    im2, contours, hierarchy = cv2.findContours(final_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cell=contours[0]                          
    area=np.round(cv2.contourArea(cell),2)
    perimeter=np.round(cv2.arcLength(cell,True),2)
    circularity=np.round(4*math.pi*area/perimeter**2,2)     
    M = cv2.moments(cell) 
    if M["m00"]==0.:
        M["m00"]=0.001
    cX = np.round(M["m10"] / M["m00"],2)
    cY = np.round(M["m01"] / M["m00"],2)     
     
    return cX,cY,area,perimeter,circularity
############################################
def segment_manual_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord, cell_radius, frame_size, p_size,marker,final_mask,cell_number):# segments frame and creates dictionary of cells         
         #p_size=48 # this is  half of patch size (usually 96x96)
         value_1 = float(np.mean(empty_fluor))
         
         empty_fluor_base=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.min(empty_fluor)))
         empty_bright_base=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.mean(empty_bright)))
         ss=0
         x0,y0 =centroid[0],centroid[1]
         x00,y00=coord[0],coord[1]         
         zero_frame=np.zeros((frame_size,frame_size),dtype="uint8")
         seed_patch_base=cv2.copyMakeBorder(zero_frame, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )                
         seed_patch_base[int(round(y00))-cell_radius+Bordersize:int(round(y00))+cell_radius+Bordersize,int(round(x00))-cell_radius+Bordersize:int(round(x00))+cell_radius+Bordersize]=255# here I draw square               
         a,b,c,d=int(round(x0))+Bordersize-p_size,int(round(x0))+Bordersize+p_size,int(round(y0))+Bordersize-p_size,int(round(y0))+Bordersize+p_size           
         
         while True:          
          ss+=1
          empty_fluor_border=empty_fluor_base.copy()
          empty_bright_border=empty_bright_base.copy()
          seed_patch_border=seed_patch_base.copy()
          base=np.stack((empty_fluor_border,empty_bright_border,seed_patch_border),axis=2)       
          patch = base[c:d, a:b,:]          
          shape=(patch.shape[0],patch.shape[1])         
          patch_input=cv2.resize(patch, (96,96), interpolation = cv2.INTER_AREA)
          seed_patch=patch_input[:,:,2]
          seed_patch = seed_patch.astype('uint8')
                              
          cX,cY=find_centroids(seed_patch)
          seed_patch[cY-cell_radius:cY+cell_radius,cX-cell_radius:cX+cell_radius]=255
          patch_input[:,:,2]=seed_patch          
          patch_fluor=patch_input[:,:,0]
          patch_bright=patch_input[:,:,1]
          frame=standardize(patch_input)
          inframe=frame.reshape((1,96,96,3))       
          segmentation=segmentor.predict(inframe,batch_size=1,verbose=0)# Segmentor               
          segm=(np.int_(np.round(segmentation)))*255      
          segmentor_output=segm.reshape((96,96))
          segmentor_output=segmentor_output.astype(np.uint8)     
          refiner_output=refiner_predict(segmentor_output,patch_fluor,patch_bright,refiner)# Refiner        
          refiner_output=refiner_output.astype(np.uint8)
          ensemble_output=segmentor_output+refiner_output    
          test=ensemble_output.copy()          
          test[1:-1,1:-1]=0 
          if (np.all(test)==0)==True:             
              break
          else:            
             a1=a-1
             b1=b+1
             c1=c-1
             d1=d+1
             patch = base[c1:d1, a1:b1,:]                     
             if (d1<frame_size+2*Bordersize and b1<frame_size+2*Bordersize and a1>0 and c1>0 ):
               a,b,c,d=a1,b1,c1,d1              
               continue           
             else:
              # break because reached the edge of input image 
               break         
         ensemble_output=cv2.resize(ensemble_output, shape, interpolation = cv2.INTER_AREA)
         ensemble_output[ensemble_output!=0]=255
         cv2.imwrite(r"C:\Users\kfedorchuk\Desktop\ensemble_output.tif", ensemble_output)
         cleaned_output, final_mask=clean_manual_patch(ensemble_output, marker, a,b,c,d,frame_size,final_mask,cell_number)
         cv2.imwrite(r"C:\Users\kfedorchuk\Desktop\cleaned_output.tif", cleaned_output)
         return cleaned_output,a,b,c,d, final_mask  
###########################################
#######################################
def segment_one_cell_at_a_time(segmentor, refiner,empty_fluor,empty_bright,centroid,cell_radius, frame_size, p_size, marker,final_mask,cell_number):        
      coord=centroid
      segmented_patch,a,b,c,d, final_mask= segment_manual_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord, cell_radius, frame_size, p_size, marker,final_mask,cell_number)                     
      segmented_frame= np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")
      segmented_frame[c:d,a:b]=segmented_patch
      segmented_frame=segmented_frame[Bordersize:Bordersize+frame_size,Bordersize:Bordersize+frame_size]   
      segmented_frame = segmented_frame.astype(np.uint8)                       
      return segmented_frame, segmented_patch,a,b,c,d, final_mask
#############
def refine_segmentation(segmentor, refiner,empty_fluor,empty_bright,centroid,cell_radius, frame_size, p_size, marker,final_mask,cell_number):        
      coord=centroid
      marker=centroid
      segmented_patch,a,b,c,d, final_mask= segment_manual_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord, cell_radius, frame_size, p_size, marker,final_mask,cell_number)                     
      segmented_frame= np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")
      segmented_frame[c:d,a:b]=segmented_patch
      segmented_frame=segmented_frame[Bordersize:Bordersize+frame_size,Bordersize:Bordersize+frame_size]   
      segmented_frame = segmented_frame.astype(np.uint8)                       
      return segmented_frame, segmented_patch,a,b,c,d, final_mask
          
#############
def clean_manual_patch(output_raw,marker,a,b,c,d,frame_size, final_mask,cell_number):# leave only the contour which contains marker when correcting 
# segmentation manually; otherwise, output empty patch
    x0,y0=int(round(marker[0])), int(round(marker[1]))
    if output_raw.dtype!='uint8':
         output_raw = output_raw.astype('uint8')
    im2, contours, hierarchy = cv2.findContours(output_raw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    counter=0
    for cnt in contours:
         big=np.zeros((frame_size+Bordersize*2,frame_size+Bordersize*2),dtype="uint8")
         one=np.zeros((output_raw.shape),dtype="uint8")
         one=cv2.drawContours(one,[cnt],0,255, -1)
         big[c:d,a:b]=one
         test_image=big[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
         cv2.imwrite(r"C:\Users\kfedorchuk\Desktop\test_image.tif", test_image)
         if test_image[y0,x0]==255:
             cleaned_patch=one
             counter+=1
             break
    if counter==0:
        cleaned_patch=np.zeros((output_raw.shape),dtype="uint8")
    # check that this contour does not intersect with neighbouring cells.
    # If it is the case, output empty patch
    print("counter=", counter)
    if counter!=0:
      mask_with_one_cell=paste_benchmark_patch(cleaned_patch,a,b,c,d,cell_number, frame_size)
      final_mask_copy=copy.deepcopy(final_mask)
      final_mask_copy[final_mask_copy==cell_number+1]=0# delete previous contour of cell
      final_mask_copy+=mask_with_one_cell# insert current contour of cell
      test_1, test_2=np.zeros(final_mask.shape),np.zeros(final_mask.shape)
      test_1[final_mask_copy==cell_number+1]=1
      test_2[mask_with_one_cell==cell_number+1]=1      
      if np.all(test_1==test_2)==True:
          print("no problem")
          final_mask=final_mask_copy
      else:
          cleaned_patch=np.zeros((output_raw.shape),dtype="uint8")
          print("there is a problem!!!!")
    return cleaned_patch, final_mask      
########################################

#############################
def segment_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord, cell_radius, frame_size, p_size, flag):# segments frame and creates dictionary of cells         
         #p_size=48 # this is  half of patch size (usually 96x96)
         value_1 = float(np.mean(empty_fluor))
         
         empty_fluor_base=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.min(empty_fluor)))
         empty_bright_base=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.mean(empty_bright)))
         ss=0
         x0,y0 =centroid[0],centroid[1]
         x00,y00=coord[0],coord[1]         
         zero_frame=np.zeros((frame_size,frame_size),dtype="uint8")
         seed_patch_base=cv2.copyMakeBorder(zero_frame, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )                
         seed_patch_base[int(round(y00))-cell_radius+Bordersize:int(round(y00))+cell_radius+Bordersize,int(round(x00))-cell_radius+Bordersize:int(round(x00))+cell_radius+Bordersize]=255# here I draw square               
         a,b,c,d=int(round(x0))+Bordersize-p_size,int(round(x0))+Bordersize+p_size,int(round(y0))+Bordersize-p_size,int(round(y0))+Bordersize+p_size           
         
         while True:          
          ss+=1
          empty_fluor_border=empty_fluor_base.copy()
          empty_bright_border=empty_bright_base.copy()
          seed_patch_border=seed_patch_base.copy()
          base=np.stack((empty_fluor_border,empty_bright_border,seed_patch_border),axis=2)       
          patch = base[c:d, a:b,:]          
          shape=(patch.shape[0],patch.shape[1])         
          patch_input=cv2.resize(patch, (96,96), interpolation = cv2.INTER_AREA)
          seed_patch=patch_input[:,:,2]
          seed_patch = seed_patch.astype('uint8')
                              
          cX,cY=find_centroids(seed_patch)
          seed_patch[cY-cell_radius:cY+cell_radius,cX-cell_radius:cX+cell_radius]=255
          patch_input[:,:,2]=seed_patch          
          patch_fluor=patch_input[:,:,0]
          patch_bright=patch_input[:,:,1]
          frame=standardize(patch_input)
          inframe=frame.reshape((1,96,96,3))       
          segmentation=segmentor.predict(inframe,batch_size=1,verbose=0)# Segmentor               
          segm=(np.int_(np.round(segmentation)))*255      
          segmentor_output=segm.reshape((96,96))
          segmentor_output=segmentor_output.astype(np.uint8)     
          refiner_output=refiner_predict(segmentor_output,patch_fluor,patch_bright,refiner)# Refiner        
          refiner_output=refiner_output.astype(np.uint8)
          ensemble_output=segmentor_output+refiner_output    
          test=ensemble_output.copy()          
          test[1:-1,1:-1]=0 
          if (np.all(test)==0)==True:             
              break
          else:            
             a1=a-1
             b1=b+1
             c1=c-1
             d1=d+1
             patch = base[c1:d1, a1:b1,:]                     
             if (d1<frame_size+2*Bordersize and b1<frame_size+2*Bordersize and a1>0 and c1>0 ):
               a,b,c,d=a1,b1,c1,d1              
               continue           
             else:
              # break because reached the edge of input image 
               break         
         ensemble_output=cv2.resize(ensemble_output, shape, interpolation = cv2.INTER_AREA)
         ensemble_output[ensemble_output!=0]=255
         if not np.any(ensemble_output)==True:#if the output patch is black                     
             art_output=np.zeros((frame_size,frame_size),dtype="uint8")
             circle_base=cv2.copyMakeBorder(art_output, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )                
             circle_centre=(int(round(x0))+Bordersize,int(round(y0))+Bordersize)
             cv2.circle(circle_base, circle_centre, 3, 255, -1)                 
             a,b,c,d=int(round(x0))+Bordersize-2*p_size,int(round(x0))+Bordersize+ 2*p_size,int(round(y0))+Bordersize-2*p_size,int(round(y0))+Bordersize+2*p_size           
             ensemble_output = circle_base[c:d, a:b]        
         #cleaned_output=clean_patch(ensemble_output, "first cleaning")
         cleaned_output=clean_patch(ensemble_output, flag)
         return cleaned_output,a,b,c,d  
################ Segment all cells in current frame  
def segment_and_clean(dict_of_divisions,cells,count,coords,text,segmentor, refiner,empty_fluor,empty_bright,centroids,frame_number, manual_id_indicator,mother_number, out_folders, cell_radius, frame_size, colours, p_size, flag):
   kernel= np.ones((3,3),np.uint8)
   #p_size=48 
   segmented_outputs=[]# list of all segmented patches (with 1 or2 contours) in frame     
   for p in range(len(centroids)):# Step-1: segment based on tracking results
      centroid=centroids[p]
      coord=coords[p]
      # ensemble_output= patch with the 1st biggest and the 2nd bigest contours
      ensemble_output,a,b,c,d= segment_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord, cell_radius, frame_size, p_size, flag)     
      segmented_outputs.append([ensemble_output,a,b,c,d,p])
      cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\segmented_outputs\\output_%s_frame_%s.tif" % (p, frame_number), ensemble_output)                    
   # put all segmented patches in one (382,382) frame  init_seg 
   init_seg= np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")
   parallel_image= np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")                       
   for pp in range(len(centroids)):      
      patch=segmented_outputs[pp]
      a,b,c,d=patch[1],patch[2],patch[3],patch[4]
      cell=np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")
      cell_parallel=np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="float64")
      image=patch[0]
      image = image.astype(np.float64)          
      cell[c:d,a:b]=image
      
      ###############################
      image_template=np.zeros(image.shape, dtype="float64")
      image_template[image!=0]=1.0
      cell_parallel[c:d,a:b]=(image_template*2**patch[5])/1000000 # the powers of 2 for each cell     
      init_seg+=cell
      parallel_image+=cell_parallel
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\init_seg\\frame_%s.tif" % (frame_number), parallel_image*10000000)                 
 #################### Step-2:try to improve segmentation of too small cells
   init_seg=init_seg[Bordersize:Bordersize+frame_size,Bordersize:Bordersize+frame_size]
   parallel_image=parallel_image[Bordersize:Bordersize+frame_size,Bordersize:Bordersize+frame_size]   
   corrected_seg=init_seg
   corrected_seg = corrected_seg.astype(np.uint8)  
   corrected_seg[corrected_seg!=0]=255  
   
   im2, contours, hierarchy = cv2.findContours(corrected_seg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  
   real_cells=[]  
   for ii in range(len(contours)):      
       real_binary_contour= np.zeros((frame_size,frame_size),dtype="uint8")
       real_binary_contour=cv2.drawContours(real_binary_contour,[contours[ii]] , 0, 255, -1)
       cX,cY= find_centroids(real_binary_contour)
       area=cv2.contourArea(contours[ii])            
       if cX!=0 and cY!=0:            
         a_n,b_n,c_n,d_n=int(round(cX))+Bordersize-p_size,int(round(cX))+Bordersize+p_size,int(round(cY))+Bordersize-p_size,int(round(cY))+Bordersize+p_size      
         real_cells.append([real_binary_contour,cX,cY,a_n,b_n,c_n,d_n,ii])                  
   #print("len(real_cells)=",len(real_cells))
   if manual_id_indicator=="yes":
       template=coords
   else:
       template=centroids
   
   final_list= find_frame_intensities_sorted(real_cells, parallel_image, coords, frame_size)
   #print("len(final_list)=",len(final_list))   
   final_list, final_centroids, number_of_splits=split_with_final_list(final_list, coords,frame_number, out_folders, frame_size) 
   mask_old=create_mask(final_list)
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\masks\\frame_%s.tif" % (frame_number), mask_old*50)                    
   ######## create cells={} - dictionary for each cell in a farme   
   cells={}
   empty_fluor_base=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = np.mean(empty_fluor))
   empty_bright_base=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = np.mean(empty_bright))       
   for kkk in range(len(final_list)):
       item=final_list[kkk]
       a_old,b_old,c_old,d_old=item[1], item[2],item[3], item[4]
       number=item[5][0]#internal cell number
       big_patch=item[0]
       big_patch_border=cv2.copyMakeBorder(big_patch, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = 0)
       ensemble_output_old= big_patch_border[c_old:d_old,a_old:b_old]  
       #########################################
      
       #dilation = cv2.dilate(big_patch,kernel,iterations = 2)
       x0,y0=final_centroids[number][0], final_centroids[number][1]       
       
       centroid=[x0,y0]
       ###################################################
       
       
       segmented_frame, refined_output,a,b,c,d, mask=refine_segmentation(segmentor, refiner,empty_fluor,empty_bright,centroid,cell_radius, frame_size, p_size, centroid,mask_old,number)
       if not np.any(refined_output)==True:# if all zeros in ensemble_output
         """
         dilated_output, mask=dilate_cell(ensemble_output,a,b,c,d,mask, number,frame_size)
         cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\dilated_output.tif", dilated_output)
         cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask.tif",mask)
         ensemble_output=dilated_output
         """
         ensemble_output=ensemble_output_old
         a,b,c,d= a_old,b_old,c_old,d_old
         mask=mask_old
       else:
         ensemble_output=refined_output
       ###############################################################
       #dilation=cv2.copyMakeBorder(dilation, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = 0 )                            
       #ensemble_output= dilation[c:d,a:b]    
       ensemble_output = ensemble_output.astype('uint8')
       #########
       cX,cY,area,perimeter,circularity= calculate_cell_parametres(ensemble_output,a,b,c,d, frame_size)
       ###########       
       txt=text[number]
       colour=colours[txt]
       division_indicator="no division"       
       sum_clean=ensemble_output 
       cells["cell_%s" % number]=[[],[],[],sum_clean,empty_fluor_base,empty_bright_base,[cX,cY],a,b,c,d,txt, frame_number, mask, coords, colour, division_indicator, number, area,perimeter,circularity]                                                                                    
   coords=final_centroids
   print("coords=", coords)
   print("coords.shape=", coords.shape)
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\new_masks\\frame_%s.tif" % (frame_number), mask*50)                   
       
   return count,cells, coords, text, number_of_splits
#######################################################
def dilate_cell(ensemble_output,a,b,c,d,mask, cell_number,frame_size):
   print("cell_number=", cell_number)
   kernel= np.ones((3,3),np.uint8)
   previous_patch=ensemble_output
   previous_mask=mask
   while True:   
      ensemble_output = cv2.dilate(previous_patch,kernel,iterations = 1)    
      mask_with_one_cell=paste_benchmark_patch(ensemble_output,a,b,c,d,cell_number, frame_size)
      mask_copy=copy.deepcopy(mask)
      mask_copy[mask_copy==cell_number+1]=0# delete previous contour of cell
      mask_copy+=mask_with_one_cell# insert current contour of cell
      test_1, test_2=np.zeros(mask.shape),np.zeros(mask.shape)
      test_1[mask_copy==cell_number+1]=1
      test_2[mask_with_one_cell==cell_number+1]=1
      cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask_copy.tif", mask_copy*50)
      cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\test_1.tif", test_1*50) 
      cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\test_2.tif", test_2*50)                          
      if np.all(test_1==test_2)==True:
          print("no problem so far")
          previous_mask=mask_copy
          previous_patch=ensemble_output
          continue
      else:
          print("break from the loop ! ")
          improved_patch=previous_patch
          mask=previous_mask
          break
   return improved_patch,mask
         
##########################################################
def create_mask(final_list):
    frame_shape=final_list[0][0].shape
    mask= np.zeros(frame_shape,dtype="float64")      
    for i in range(len(final_list)):
      base = np.zeros(frame_shape,dtype="float64")     
      one_cell_image=final_list[i][0]
      cell_number=final_list[i][5][0]            
      base[one_cell_image==255]=cell_number+1               
      mask+=base
    return mask

##############################################   
def split_with_final_list(final_list, coords, frame_number, out_folders, frame_size):     
     final_centroids=np.zeros((len(coords),2))
     number_of_splits=0
     new_final_list=[]
     #print("len(final_list)=",len(final_list))                      
     for ppp in range(len(final_list)):           
              countt=list(final_list[ppp][5])                         
              curr_one_contour_item=final_list[ppp]    
              if len(countt)>1:
                number_of_splits+=1
                separated_cells=[]
                number=len(countt)               
                markers=[]# create markers (seeds) for seeded watershed
                for k in countt:                   
                    cX, cY=coords[k,:]#was k-1
                    markers.append([cX,cY])                                             
                markers=check_markers(curr_one_contour_item[0], markers)           
                watersheded=seeded_watershed_final(curr_one_contour_item[0],markers)
                n=check_watershed(watersheded,number, frame_size)              
                if n!=number:# if watershed fails go to brute force                    
                     watersheded=brute_force_separation(curr_one_contour_item[0], number, frame_size)                                                
                separated_centroids=np.zeros((number,2))
                markers_array=np.zeros((number,2))                            
                for i in range(number):                  
                   base=np.zeros(((frame_size,frame_size)),dtype="float64")
                   base[watersheded==(i+1)]=255                  
                   bases=clean_patch(base, "second cleaning")
                   base=bases[0]
                   base1=base.copy()
                   base1=base1.astype("uint8")
                   im2, contours, hierarchy = cv2.findContours(base1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                   cX, cY=find_centroids(base)
                   separated_centroids[i,:]=np.array([[cX,cY]])
                   markers_array[i,:]=np.array([[markers[i][0],markers[i][1]]])                  
                   separated_cells.append(base) 
                ############ apply hungarian to separated_cells               
                a,b,c,d=curr_one_contour_item[1],curr_one_contour_item[2],curr_one_contour_item[3],curr_one_contour_item[4]
                ordered_centroids, rule=hungarian(markers_array,separated_centroids)              
                left=[rule[p][0] for p in range(number)]
                right=[rule[pp][1] for pp in range(number)]                           
                for ii in range(len(countt)):                  
                    index= right.index(ii)                   
                    internal_number=left[index]
                    external_number=countt[internal_number]
                    new_item=[separated_cells[ii],a,b,c,d,[external_number]]
                    new_final_list.append(new_item)
                    final_centroids[external_number,:]=ordered_centroids[internal_number]                               
              else:
                 
                  big_patch=curr_one_contour_item[0]                 
                  cX, cY=find_centroids(big_patch)               
                  final_centroids[list(curr_one_contour_item[5])[0],:]=np.array([[cX,cY]])                                                                
                  new_final_list.append(curr_one_contour_item)
     
     return new_final_list, final_centroids, number_of_splits
############################
def brute_force_separation(im1, number, frame_size):
 im1=im1.astype(np.uint8)
 image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt=contours[0]
 im=im1.copy()
 rect = cv2.minAreaRect(cnt)
 box = cv2.boxPoints(rect)
 box = np.int0(box)
 d1 = dist(box[0],box[1])
 d2 = dist(box[1],box[2])
 if d1>d2:
     p1,p2,p3,p4 = box[0], box[1],box[2], box[3]
 else:
     p1,p2,p3,p4= box[1], box[2],box[3], box[0]   
 n=number 
 ort =np.array([(p1[0]-p2[0])/n,(p1[1]-p2[1])/n] )
 if d1>d2:
    for ii in range(1,n):
       point_1 = (int(round((p2+ii*ort)[0]))-1,int(round((p2+ii*ort)[1]))+1) 
       point_2 = (int(round((p3+ii*ort)[0]))+1,int(round((p3+ii*ort)[1]))-1)
       im=cv2.line(im1, point_1, point_2, (0, 0, 0), thickness=2)
 else:
    for ii in range(1,n):
       point_1 = (int(round((p2+ii*ort)[0]))-1,int(round((p2+ii*ort)[1]))-1) 
       point_2 = (int(round((p3+ii*ort)[0]))+1,int(round((p3+ii*ort)[1]))+1)         
       im=cv2.line(im1, point_1, point_2, (0, 0, 0), thickness=2)
 
 im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                
 if len(contours)>n:
     im=leave_n_biggest_contours(im,n)
     im2,contours, hierarchy=cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                 
 base=np.zeros(((frame_size,frame_size)),dtype="float64")
 for k in range(len(contours)):
     img= np.zeros((frame_size,frame_size),dtype="uint8")
     cv2.drawContours(img,[contours[k]] , 0, 255, -1)
     base[img==255]=k+1
 return base
#############################
def hungarian(frame1,frame2):# frame1.shape[0] should be = frame2.shape[0]  
    n=frame1.shape[0]   
    M=np.zeros((n,n))
    for p in range(n):
        for q in range(n):
            M[p,q]=dist(frame1[p],frame2[q])
    row_ind, col_ind = linear_sum_assignment(M)
    indexes=[(row_ind[i],col_ind[i]) for i in range(n)]
    label=np.zeros((n,2))
    rule=np.zeros((n,2),dtype=np.int8)
    for t in range(n):
        c=indexes[t][0]
        d=indexes[t][1]
        label[c]=frame2[d]
        rule[t]=np.array([c,d])
    return label, rule
#################
def find_intensities(image):# finds intensities for one current cell
  x=list(np.unique(image))
  x.remove(0.0) 
  y=[float(format(float(str(x[i])), 'f')) for i in range(len(x))] 
  return y         
###############
def dist(A,B):
    d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    return d
 ################################
def create_int_dictionary(n_cells):     
     cell_ids =[ii for ii in range(n_cells)]
     all_combinations =[]
     for i in range(1,n_cells+1):
          combinations = list(itertools.combinations(cell_ids, i))
          all_combinations+=combinations
    
     int_dictionary ={}    
     for k in range(len(all_combinations)):
         combo =all_combinations[k]
         summ=0
         for kk in range(len(combo)):
            summ+=2**combo[kk]
         int_dictionary[str(summ/1000000)]=list(combo) # summ=1,2,3,4,5,...
     #print("int_dictionary=", int_dictionary)
     return int_dictionary  
############################################### 
def find_frame_intensities_sorted(real_cells, parallel_frame, coords, frame_size):
    n_cells=coords.shape[0]
    int_dictionary =create_int_dictionary(n_cells)
    frame_intensities=[]
    for k in range(len(real_cells)):          
        curr_one_cell=real_cells[k][0]       
        one_cell_image=np.zeros((frame_size,frame_size),dtype="float64")
        one_cell_image[curr_one_cell==255]=parallel_frame[curr_one_cell==255]        
        intensities =find_intensities(one_cell_image)
        #print("k=", k)
        #print("intensities=", intensities)
        a,b,c,d=real_cells[k][3],real_cells[k][4],real_cells[k][5],real_cells[k][6],         
        frame_intensities.append([curr_one_cell, a,b,c,d, intensities])    
    # expand on basic intensities 1,2,4,6,8,16,.....
    basic_frame_intensities=[]
    for kk in range(len(frame_intensities)):
        old_item=frame_intensities[kk]
        old_ints =old_item[5]
        new_ints=[]
        for kkk in range(len(old_ints)):
            key =old_ints[kkk]
            new_ints+=int_dictionary[str(key)]
        contour,a,b,c,d= old_item[0],old_item[1],old_item[2],old_item[3],old_item[4]         
        basic_frame_intensities.append([contour,a,b,c,d,list(set(new_ints))])    
    # preference is given to [1] and 1 is deleted from other int lists
    for kk in range(len(basic_frame_intensities)):         
         item = basic_frame_intensities[kk]
         item_ints=item[5]
         if len(item_ints)==1:# these are sure ids!
             sure_number=item_ints[0]          
             for kkk in range(len(basic_frame_intensities)):# now we remove sure numbers from other contours
                 int_list=basic_frame_intensities[kkk][5]
                 if len(int_list)>1:                     
                      if sure_number in int_list and kkk!=kk:
                          actual_contour=basic_frame_intensities[kkk][0]
                          int_list_copy=int_list.copy()                         
                          int_list_copy.remove(sure_number)
                          a,b,c,d=basic_frame_intensities[kkk][1],basic_frame_intensities[kkk][2],basic_frame_intensities[kkk][3],basic_frame_intensities[kkk][4]
                          basic_frame_intensities[kkk]=[actual_contour,a,b,c,d, int_list_copy]                              
    rep_check_list =[]
    for i in range(len(basic_frame_intensities)):
        rep_check_list+=basic_frame_intensities[i][5]
    unique =[]    
    dupes =[]
    for ii in range(len(rep_check_list)):
        item=rep_check_list[ii]
        if item in unique:
            dupes.append(item)           
            unique.remove(item)
        elif item in dupes:
            pass
        else:
            unique.append(item)     
     # remove repetitions
    for dupe in dupes:# deal with each dupe separately        
         numbers =[k for k in range(len(basic_frame_intensities)) if dupe in basic_frame_intensities[k][5]]
         # find centroids of all contours with the same dupe intensity     
         contour_centroids=[]
         for kk in numbers:
             contour=basic_frame_intensities[kk][0]
             cX, cY=find_centroids(contour)
             contour_centroids.append((cX,cY))
         # now, find which of them is closest to dupe in previous frame
         right_internal_number=find_closest_contour(contour_centroids,coords[dupe])
         right_contour_number=numbers[right_internal_number]        
         # finally, clear final list of the dupe except the contour with right number
         for kkk in range(len(basic_frame_intensities)):
            item= basic_frame_intensities[kkk][5]
            if (kkk!=right_contour_number and dupe in item):
                item.remove(dupe)
    # remove contours with empty lists []
    final_list=[]
    for kkk in range(len(basic_frame_intensities)):
            item= basic_frame_intensities[kkk]
            if len(item[5])!=0:
                final_list.append(item)       
    for_print =[final_list[i][5] for i in range(len(final_list))]
    #print("frame_intensities_sorted=", for_print)
    return final_list        
 ################################# Ditch too small contours after applyting watereshed
def check_watershed(watersheded,number, frame_size):  
  img= np.zeros((frame_size,frame_size),dtype="float64")
  kernel = np.ones((3, 3),dtype="float64")
  for i in range(number):
    base=np.zeros(((frame_size,frame_size)),dtype="float64")
    base[watersheded==(i+1)]=255                        
    base = cv2.erode(base, kernel)
    img+=base 
  img=img.astype(np.uint8)                        
  im2, contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)           
  count=0
  for i in range(len(contours)):
      area=cv2.contourArea(contours[i])
      if area>=100: 
          count+=1
  return count
#############################################
def dist(A,B):
    d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    return d
########################################
def standardize(frame): #normalizing per channel
     frame = frame.astype('float32')
     means = frame.mean(axis=(0,1), dtype='float64')
     stds = frame.std(axis=(0,1), dtype='float64')    
     frame = (frame - means) / stds
     return frame
#######################################################
def leave_n_biggest_contours(im,n):    
     im = im.astype(np.uint8)
     im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                    
     areas=[]    
     for cnt in contours:      
       area=cv2.contourArea(cnt)     
       areas.append(area)      
     w=list(zip(contours,areas))
     ww=sorted(w,key=lambda student:student[-1],reverse=True)
     ress = list(zip(*ww))        
     img=np.zeros((im.shape),dtype="uint8")
     for i in range(n):
       cv2.drawContours(img,[ress[0][i]] , 0, 255, -1)      
     return img
##################################################
def check_markers(img, markers):
    new_markers=[]
    for i in range(len(markers)):
        marker=markers[i]
        x0,y0=int(marker[0]),int(marker[1])
        if img[y0,x0]==0:
           nonzero = np.argwhere(img == 255)
           distances = np.sqrt((nonzero[:,0] - y0) ** 2 + (nonzero[:,1] - x0) ** 2)
           nearest_index = np.argmin(distances)
           marker=nonzero[nearest_index]         
           new_markers.append(np.array([marker[1], marker[0]]))
        else:
            new_markers.append(np.array([x0,y0]))
    return new_markers
########################################
def seeded_watershed_final(img,markers):# img.shape=382 x 382    
     img=img.astype(np.uint8)   
     kernel= np.ones((3,3),np.uint8) 
     opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel, iterations = 1)
    
     sure_bg = cv2.dilate(opening,kernel,iterations=1)    
     sure_fg=np.zeros(img.shape,dtype="uint8")
     for i in range(len(markers)):
       x1,y1=int(markers[i][0]),int(markers[i][1])      
       sure_fg[(y1-1):(y1+1),(x1-1):(x1+1)]=255     
     unknown= cv2.subtract(sure_bg,sure_fg) 
    
     ret, markers = cv2.connectedComponents(sure_fg)
     markers = markers+1    
     markers[unknown!=0] = 0    
     img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
     markers = cv2.watershed(img,markers)    
     markers_1=markers.copy()
     markers_1=markers_1-1   
     
     return markers_1#markers_1.shape = 382 x 382
##################### 
def find_closest_contour(contour_centroids,coord):
  distances=[]
  numbers=[]
  cX, cY=coord[0], coord[1]  
  for i in range(len(contour_centroids)):
          second=contour_centroids[i]         
          x2,y2=second[0],second[1]
          dist=(cX-x2)**2+(cY-y2)**2
          distances.append(dist)
          numbers.append(i)    
  index=distances.index(min(distances))
  number=numbers[index]  
  return number
#########################################################
def clean_patch_old(output,flag): 
  if output.dtype!='uint8':
         output = output.astype('uint8')     
  im2, contours, hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                     
  if len(contours)==1:
      if flag=="second cleaning":
           cleaned_patches=[output]
           return cleaned_patches
      else:
          cleaned_patch=output
          return cleaned_patch
  else:    
     areas=[]   
     contours_separated=[]    
     for cnt in contours:
         one=np.zeros((output.shape),dtype="uint8")
         one=cv2.drawContours(one,[cnt],0,255, -1)              
         area=cv2.contourArea(cnt)             
         areas.append(area)      
         contours_separated.append(cnt)        
     w=list(zip(areas,contours_separated))
     ww=sorted(w,key=lambda student:student[0], reverse=True)
     ress = list(zip(*ww))
     areas =list(ress[0])     
     contours_separated=list(ress[1])    
     if flag=="second cleaning":
       cleaned_patches=[]# first patch has 1 biggest cell, 2nd - 2 biggest cells
       for ii in range(2):
          cleaned_patch=np.zeros((output.shape),dtype="uint8")
          for iii in range(ii, ii+1):# leaves 2 biggest cells in a patch
            cv2.drawContours(cleaned_patch, [contours_separated[iii]] , 0, 255, -1)
            cleaned_patches.append(cleaned_patch)
       return cleaned_patches# output is a list of 2 pathces with 2 separate biggest contours in each
     else:
        cleaned_patch=np.zeros((output.shape),dtype="uint8")
        n_contours=2
        #if areas[1]<100:
            #n_contours=1
        for iii in range(n_contours):# leaves 2 biggest cells in a patch for Mohammed movies
          cv2.drawContours(cleaned_patch, [contours_separated[iii]] , 0, 255, -1)        
        return cleaned_patch# output is one patch with 2 boggest contours in it  
################################
 
###############################

def clean_patch(output_raw,flag):
  
  if output_raw.dtype!='uint8':
         output_raw = output_raw.astype('uint8')
         
         
  im2_uneroded, contours_uneroded, hierarchy_uneroded = cv2.findContours(output_raw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  #print("len(contours) in the patch before erosion=", len(contours_uneroded))      
  kernel= np.ones((3,3),np.uint8)
  output = cv2.erode(output_raw,kernel,iterations = 2)
  #output = cv2.morphologyEx(output_raw,cv2.MORPH_OPEN,kernel, iterations = 1)
    
  im2, contours, hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  if len(contours)<len(contours_uneroded):
      output=output_raw
      contours=contours_uneroded
  #print("len(contours) in the eroded patch=", len(contours)) 

                  
  if len(contours)==1:
      if flag=="second cleaning":
           cleaned_patches=[output]
           return cleaned_patches
      else:
          cleaned_patch=output
          return cleaned_patch
  else:    
     areas=[]   
     contours_separated=[]    
     for cnt in contours:
         one=np.zeros((output.shape),dtype="uint8")
         one=cv2.drawContours(one,[cnt],0,255, -1)              
         area=cv2.contourArea(cnt)             
         areas.append(area)      
         contours_separated.append(cnt)        
     w=list(zip(areas,contours_separated))
     ww=sorted(w,key=lambda student:student[0], reverse=True)
     ress = list(zip(*ww))
     areas =list(ress[0])     
     contours_separated=list(ress[1])    
     if flag=="second cleaning":
       cleaned_patches=[]# first patch has 1 biggest cell, 2nd - 2 biggest cells
       for ii in range(2):
          cleaned_patch=np.zeros((output.shape),dtype="uint8")
          for iii in range(ii, ii+1):# leaves 2 biggest cells in a patch
            cv2.drawContours(cleaned_patch, [contours_separated[iii]] , 0, 255, -1)
            cleaned_patches.append(cleaned_patch)
       return cleaned_patches# output is a list of 2 pathces with 2 separate biggest contours in each
     else:
        cleaned_patch=np.zeros((output.shape),dtype="uint8")
        n_contours=2
        if areas[1]<100:
            n_contours=1
        for iii in range(n_contours):# leaves 2 biggest cells in a patch for Mohammed movies
          cv2.drawContours(cleaned_patch, [contours_separated[iii]] , 0, 255, -1)        
        return cleaned_patch# output is one patch with 2 boggest contours in it
#####################################################################
def extract_lineage(outpath):
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")
    lineage_per_frame = []
    with (open(lineage_path, "rb")) as openfile:
     while True:
        try:
            lineage_per_frame.append(pickle.load(openfile))
        except EOFError:
            break    
    return lineage_per_frame
##############################
def create_previous_frame(cells, frame_size):
    previous_frame= np.zeros((frame_size,frame_size),dtype="float64")      
    for i in range(len(cells)):
      base = np.zeros((frame_size+Bordersize*2,frame_size+Bordersize*2),dtype="float64")  
      patch=cells["cell_%s" % i][3]
      patch = patch.astype('float64')  
      a,b,c,d=cells["cell_%s" % i][7],cells["cell_%s" % i][8],cells["cell_%s" % i][9],cells["cell_%s" % i][10]
      base[c:d,a:b]=patch
      base=base[Bordersize:Bordersize+frame_size,Bordersize:Bordersize+frame_size]
      base[base==255]=i+1               
      previous_frame+=base
    return previous_frame
############################################################# 
def update_lineage(llist,outpath, mode):# was cells
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")  
    with open(lineage_path, mode) as f:
        for i in range(len(llist)):
           pickle.dump(llist[i], f,protocol=pickle.HIGHEST_PROTOCOL)