import os
import cv2
import numpy as np
import math
from scipy.optimize import linear_sum_assignment
from itertools import combinations, combinations_with_replacement

Bordersize=100
Coeff=382.0/100.0
#TARGET=(255,255)
#Colors=[[0,255,255,255],[255,0,255,255],[0,255,0,255],[255,0,0,255],[255,255,0,255]]
###############################################################
def predict_first_frame(first_clip_compressed, model):
     test_samples=np.zeros((1,100,100,4))  
     VIDEO=np.zeros((100,100,4))    
     for ii in range(4):     
        frame0=first_clip_compressed[ii]    
        frame=(frame0-np.mean(frame0))/np.std(frame0)
        VIDEO[:,:,ii]=frame               
     test_samples[0,:,:,:]=VIDEO
     test_samples=test_samples.reshape((1,100,100,4,1))   
     prediction=model.predict(test_samples,batch_size=1,verbose=0)   
     clip_centr=[(prediction[iii]*382.0).reshape((1,2)) for iii in range(4)]
     return clip_centr[0]
#####################################################################
def predict_first_frame_for_N_cells(first_clip_compressed, model):
     test_samples=np.zeros((1,100,100,4))  
     VIDEO=np.zeros((100,100,4))    
     for ii in range(4):     
        frame0=first_clip_compressed[ii]    
        frame=(frame0-np.mean(frame0))/np.std(frame0)
        VIDEO[:,:,ii]=frame               
     test_samples[0,:,:,:]=VIDEO
     test_samples=test_samples.reshape((1,100,100,4,1))   
     prediction=model.predict(test_samples,batch_size=1,verbose=0)   
     clip_centr=[(prediction[iii]*382.0).reshape((1,2)) for iii in range(4)]
     return clip_centr[0]
################################################################
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
def rename_file(destin,infile):       
 infile = os.path.normpath(infile) 
 old=infile.split(os.sep)
 new1=old[-1]
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
####################################################
def predict_tracking_general(coords,fluor_images,fluor_images_compressed,fluor_names,k,destination,models,n):
  start=0
  n_cells=coords.shape[0]
  clip_centr=[np.zeros((n_cells,2)) for ii in range(4)]
  if n_cells % 2 ==1:
      cds=coords[0:3]
      #print("cds=", cds)
      centroids=predict_tracking(cds,fluor_images,fluor_images_compressed,fluor_names,k,destination,models,n)
    
      #print("centroids_for_3_cells=", centroids)
      for k in range(len(clip_centr)):
          #centroids=check_tracker_1(centroids,cds,k)
          #centroids, rule=labelling_equal(cds,centroids)
          for kk in range(3):
              clip_centr[k][kk]=centroids[k][kk]
          
      start=3
  for ii in range(start,n_cells, 2):
      #print("ii=",ii)
      cds=coords[ii:ii+2]
      centroids=predict_tracking(cds,fluor_images,fluor_images_compressed,fluor_names,k,destination,models,n)
      #print("centroids_for_2_cells=", centroids)
      for kk in range(len(clip_centr)):
          #centroids=check_tracker_1(centroids,cds,kk)
          #centroids, rule=labelling_equal(cds,centroids)
          for kkk in range(2):
              clip_centr[kk][ii+kkk]=centroids[kk][kkk]   
  return clip_centr
######################################################


def predict_tracking(coords,fluor_images,fluor_images_compressed,fluor_names,k,destination,models,n):
   test_samples=np.zeros((1,100,100,5))    
   im_list=[]
   names_list=[]   
   markers_empty = np.zeros((382,382), np.uint8)
   markers=draw_exact_pixel_markers(markers_empty,coords)
   n_cells=coords.shape[0]
   model_track=models[n_cells-1]  
   im_list.append(markers)  
   frame1 = cv2.resize(markers, (100, 100), interpolation = cv2.INTER_LANCZOS4)                    
     
   VIDEO=np.zeros((100,100,5))
   frame0=frame1
   frame=(frame0-np.mean(frame0))/np.std(frame0)
   VIDEO[:,:,0]=frame
   name0= os.path.join(destination,"frame_%s.tif" % k)
   names_list.append(name0)
   additional=4
   if n-k<4:
       #print("n-k=", n-k)
       additional=4-n+k
       #print("additional=",additional)
       im=fluor_images_compressed[n-1]
       for pp in range (additional):
           fluor_images_compressed.append(im)
       #fluor_names+=[fluor_names][n-1]* additional
  
   for ii in range(4):     
       frame1=fluor_images_compressed[k+ii]
       #name=fluor_names[k+ii]
       #names_list.append(name)
       #im_list.append(fluor_images[k+ii])
       frame0=frame1
       frame=(frame0-np.mean(frame0))/np.std(frame0)
       VIDEO[:,:,ii+1]=frame               
   test_samples[0,:,:,:]=VIDEO
   test_samples=test_samples.reshape((1,100,100,5,1))
   if n_cells==1:
       test_samples=test_samples[:,:,:,1:,:]
   prediction=model_track.predict(test_samples,batch_size=1,verbose=0)   
   clip_centr=[(prediction[ii]*382.0).reshape((n_cells,2)) for ii in range(4)]
   clip_centr=clip_centr[:(n-k)]
   #print("len(clip_centr)=",len(clip_centr))
   return clip_centr
###################################################

def check_tracker_1(clip_centr,coords,kk):# corrects tracking errors in frame kk
    distances=[]
    frame=clip_centr[kk]
    for i in range(len(coords)):       
     dist=math.sqrt((frame[i][0]-coords[i][0])**2+(frame[i][1]-coords[i][1])**2)
     distances.append(dist)    
    for ii in range(len(distances)):
        if distances[ii]>=20:
            frame[ii]=coords[ii]
            clip_centr[kk]=frame
    return clip_centr
#####################################################

def check_frame(count, cells, dict_of_divisions,cell_name,frame_number):# checks if division happens too early
    #print("entering check_frame")
    life_times={1:50,2:800,3:600, 4:600, 5:500,6:500,7:500}# keys=lengths of cell names; numbers -min number of frames between divisions
    #keys =list(dict_of_divisions.keys())
    #print("keys=", keys)
    cell_name =str(cell_name)
    #print("cell_name=", cell_name)
    #print("count_before=", count)
    if len(cell_name)==1:
        start=0
    else: 
        start=dict_of_divisions[cell_name[:-1]]       
    delta =frame_number-start
    #print("delta=", delta)
        
    if delta>life_times[len(cell_name)]:            
             for kk in range(len(cells)):
               current_name=cells["cell_%s" % kk][11]
               #print("current_name=", current_name)
               if current_name==cell_name:
                 number =kk
                 #print("number=", number)
                 count[number]=1
                 #print("division confirmed")
                 break 
    #print("count_after=", count)             
    return count

#######################################################
def refiner_predict(output_segm,fluor,bright,refiner):# output_1 is binary 0,255 image, not normalized
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
####################################################

#############################################
#im=cv2.imread("C:\\Users\\kfedorchuk\\Desktop\\seed_patch.tif",-1)
def find_centroids(im):# finds centroid of one cell present in an image
    print("entering find_centroids")
    if im.dtype!='uint8':
         im = im.astype('uint8')
    im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                         
    c=contours[0]
   
    M = cv2.moments(c)
    #print("M=", M)	
    if M["m00"]==0.:
        M["m00"]=0.001
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print("cX,cY in find_centroids=",[cX,cY])
    return cX,cY
#############################################

###################################################

def check_lost_1(final): 
    lost=np.zeros((382,382),dtype="uint8")
    lost[final==1]=255    
    return lost

####################################

#########################################################
def segment_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord):# segments frame and creates dictionary of cells 
         print("entering segment_patch")
         empty_fluor_base=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.min(empty_fluor)))
         empty_bright_base=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = float(np.mean(empty_bright)))
         ss=0
         x0,y0 =centroid[0],centroid[1]
         x00,y00=coord[0],coord[1]         
         zero_frame=np.zeros((382,382),dtype="uint8")
         seed_patch_base=cv2.copyMakeBorder(zero_frame, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )                
         seed_patch_base[int(round(y00))-20+Bordersize:int(round(y00))+20+Bordersize,int(round(x00))-20+Bordersize:int(round(x00))+20+Bordersize]=255# here I draw square               
         a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48           
         
         while True:          
          ss+=1
          empty_fluor_border=empty_fluor_base.copy()
          empty_bright_border=empty_bright_base.copy()
          seed_patch_border=seed_patch_base.copy()
          base=np.stack((empty_fluor_border,empty_bright_border,seed_patch_border),axis=2)       
          patch = base[c:d, a:b,:]          
          shape=(patch.shape[0],patch.shape[1])
          #print("ss=",ss)
         # print("patch.shape=",patch.shape)
          patch_input=cv2.resize(patch, (96,96), interpolation = cv2.INTER_AREA)
          seed_patch=patch_input[:,:,2]
          seed_patch = seed_patch.astype('uint8')
                              
          cX,cY=find_centroids(seed_patch)
          seed_patch[cY-20:cY+20,cX-20:cX+20]=255
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
              #print("break because no issues")
              break
          else:
             #print("increasing a,b,...")
             a1=a-1
             b1=b+1
             c1=c-1
             d1=d+1
             patch = base[c1:d1, a1:b1,:]          
             #if patch.shape[0]==patch.shape[1]:
             if (d1<382+2*Bordersize and b1<382+2*Bordersize and a1>0 and c1>0 ):
               a,b,c,d=a1,b1,c1,d1
               #print("continuing")
               continue           
             else:
              # print("break because reached the edge") 
               break
          
          
         #print("managed to get out of the loop")   
         ensemble_output=cv2.resize(ensemble_output, shape, interpolation = cv2.INTER_AREA)
         ensemble_output[ensemble_output!=0]=255
         if not np.any(ensemble_output)==True:#if the output patch is black                     
             art_output=np.zeros((382,382),dtype="uint8")
             circle_base=cv2.copyMakeBorder(art_output, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )                
             circle_centre=(int(round(x0))+Bordersize,int(round(y0))+Bordersize)
             cv2.circle(circle_base, circle_centre, 3, 255, -1) 
             #seed_patch_base[int(round(y00))-20+Bordersize:int(round(y00))+20+Bordersize,int(round(x00))-20+Bordersize:int(round(x00))+20+Bordersize]=255# here I draw square                             
             a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48           
             ensemble_output = circle_base[c:d, a:b] 
         #cleaned_output=ensemble_output
         cleaned_outputs=clean_patch(ensemble_output)
         return cleaned_outputs,a,b,c,d 
#########################################################
def clean_patch(output):# leaves 2 biggest cells in the  of 96 x 96 output from segmentation ensemble
  print("entering clean_patch....")
  if output.dtype!='uint8':
         output = output.astype('uint8') 
  cleaned_patches=[]# first patch has 1 biggest cell, 2nd - 2 biggest cells   
  im2, contours, hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                  
  #print("len(contours) in patch=", len(contours))
  if len(contours)==1:
      cleaned_patches=[output]    
  else:    
     areas=[]   
     contours_separated=[]    
     for cnt in contours:
         one=np.zeros((output.shape),dtype="uint8")
         one=cv2.drawContours(one,[cnt],0,255, -1)              
         area=cv2.contourArea(cnt)
         #print("area=", area)         
         areas.append(area)      
         contours_separated.append(cnt)
        
     w=list(zip(areas,contours_separated))
     ww=sorted(w,key=lambda student:student[0], reverse=True)#changed for distances
     ress = list(zip(*ww))
     areas =list(ress[0]) 
     #print("chosen_area=", areas[0])
     contours_separated=list(ress[1])
    
     for ii in range(2):
        cleaned_patch=np.zeros((output.shape),dtype="uint8")
        for iii in range(ii, ii+1):# leaves 2 biggest cells in a patch
          cv2.drawContours(cleaned_patch, [contours_separated[iii]] , 0, 255, -1)
        cleaned_patches.append(cleaned_patch)
     
  return cleaned_patches


###############################
def find_closest_coord(cX,cY,coords):
  distances=[]
  numbers=[]  
  for i in range(len(coords)):
          second=coords[i]         
          x2,y2=second[0],second[1]
          dist=(cX-x2)**2+(cY-y2)**2
          distances.append(dist)
          numbers.append(i)    
  index=distances.index(min(distances))
  number=numbers[index]  
  return number
###################################
def find_closest_cell(k,cells):
  distances=[]
  numbers=[]
  first=cells["cell_%s" % k] [6]
  x1,y1=first[0],first[1]
  for i in range(len(cells)):
      if i!=k:
          second=cells["cell_%s" % i] [6]         
          x2,y2=second[0],second[1]
          dist=(x1-x2)**2+(y1-y2)**2
          distances.append(dist)
          numbers.append(i)
      else:
          continue
  index=distances.index(min(distances))
  number=numbers[index]  
  return number
#######################################
def check_contours(image, coords, flag):
     check_binary=image.copy()
     check_binary[image!=0]=255
     check_binary = check_binary.astype('uint8')
     centroids, cnts, areas,moments=find_all_centroids(check_binary,flag, coords)
     return centroids, cnts, areas             
#########################################

##################################          

def segment_and_clean(dict_of_divisions,cells,count,coords,prev_frame,text,segmentor, refiner,empty_fluor,empty_bright,centroids,frame_number, manual_division_indicator,mother_number, out_folders):# clean the whole frame (when occlusions)
   print("entering segment_and_clean....")
   segmented_outputs=[]# list of all segmented patches (with 1 or2 contours) in frame  
   for p in range(len(centroids)):# Step-1: segment based on tracking results
      centroid=centroids[p]
      coord=coords[p]
      ensemble_outputs,a,b,c,d= segment_patch(segmentor, refiner,empty_fluor,empty_bright,centroid,coord)     
      segmented_outputs.append([ensemble_outputs,a,b,c,d,p])
      #for ii in range(len(ensemble_outputs)):          
       #cv2.imwrite(os.path.join(out_folders[5],"ensemble_output_%s_cell_%s_%s.tif") % (frame_number,p, ii), ensemble_outputs[ii])
   #detect occlusions
   #print("len(segmented_outputs)=", len(segmented_outputs))   
   temp_list=[]                         
   for pp in range(len(segmented_outputs)):
      patch1=segmented_outputs[pp]
      a1,b1,c1,d1=patch1[1],patch1[2],patch1[3],patch1[4]
      cell1=np.zeros((382,382),dtype="uint8")
      cell1=cv2.copyMakeBorder(cell1, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = 0 )                    
      cell1[c1:d1,a1:b1]=patch1[0][0]# patch with 1 biggest cell
      cell1=cell1[Bordersize:Bordersize+382,Bordersize:Bordersize+382]
      #cv2.imwrite(os.path.join(out_folders[5],"frame_%s_cell_%s.tif") % (frame_number,pp), cell1)
      ids1=[patch1[5]]
      #print("ids1=", ids1)
      if len(segmented_outputs)>1:
         cell1_test = cell1.astype('float64')
         summ=cell1_test/255.
         for ppp in range(len(segmented_outputs)):
           summ_local=cell1_test/255.
           if ppp!=pp:             
             patch2=segmented_outputs[ppp]
             a2,b2,c2,d2=patch2[1],patch2[2],patch2[3],patch2[4]
             cell2=np.zeros((382,382),dtype="uint8")
             cell2=cv2.copyMakeBorder(cell2, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = 0 )                    
             cell2[c2:d2,a2:b2]=patch2[0][0]# patch with 1 biggest cell
             cell2=cell2[Bordersize:Bordersize+382,Bordersize:Bordersize+382]
             id2=[patch2[5]]
             cell2_test = cell2.astype('float64')
             summ_local+=cell2_test/255. 
                              
             if np.any(summ_local==2)==True:
               print("summ_local=2!!!!")
               #print("id2=", id2)
               ids1+=id2
               summ+=summ_local
             summ_local = summ_local.astype('uint8')
    
             im2, contours, hierarchy = cv2.findContours(summ_local,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
             print("len(contours) in patch=", len(contours))
             if len(contours)==1:
                 area=cv2.contourArea(contours[0])
                 print("area=", area)
         summ = summ.astype('uint8')
         summ[summ!=0]=255        
         cx, cy=find_centroids(summ)
         a_new, b_new, c_new, d_new=int(round(cx))-48+Bordersize,int(round(cx))+48+Bordersize,int(round(cy))-48+Bordersize,int(round(cy))+48+Bordersize
         temp_list.append([summ,a_new,b_new,c_new,d_new, set(ids1)])
      #print("cell1.shape=", cell1.shape)
      else:
          temp_list.append([cell1,a1,b1,c1,d1, set(ids1)])
 
   list_of_ids =[temp_list[k][-1] for k in range(len(temp_list))]
   print("list_of_ids=", list_of_ids) 
   new_list_of_ids =[]
   final_list_set =[]
   for i in range(len(list_of_ids)):
          item =list_of_ids[i]
          if item not in new_list_of_ids:
              new_list_of_ids.append(item)       
              final_list_set.append(temp_list[i])
   print("new_list_of_ids=", new_list_of_ids)        
   final_list=[]
   for kk in range(len(final_list_set)):
       item=final_list_set[kk]
       sset=item[5]      
       llist=list(sset)
       new_item=[item[0], item[1], item[2], item[3], item[4], llist]
       final_list.append(new_item)
   for_print=[final_list[k][5] for k in range(len(final_list))]
   print("final_list_before clean=", for_print)
   final_list=clean_new_list(final_list)
   for_print=[final_list[k][5] for k in range(len(final_list))]
   print("final_list_after clean=", for_print)     
   final_list, final_centroids=split_with_final_list(final_list, coords,frame_number, out_folders)
   #for ii in range(len(final_list)):
       
    #cv2.imwrite(os.path.join(out_folders[5],"watersheded_%s_cell_%s.tif") % (frame_number,ii), final_list[ii][0])
   print("final_centroids=", final_centroids)
       
   ##################################################
   
   cells={}
   empty_fluor_base=empty_fluor_base=cv2.copyMakeBorder(empty_fluor, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = np.mean(empty_fluor))
   empty_bright_base=cv2.copyMakeBorder(empty_bright, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = np.mean(empty_bright))
   
   #print("len(final_list_after)=", len(final_list))   
   for kkk in range(len(final_list)):
       item=final_list[kkk]
       number=item[5][0]
       big_patch=item[0]
       #print("big_patch.shape=", big_patch.shape)
       x0,y0=final_centroids[number][0], final_centroids[number][1]# was number=kkk
            
       a,b,c,d=item[1], item[2],item[3], item[4]
       big_patch=cv2.copyMakeBorder(big_patch, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = 0 )                    
        
       ensemble_output= big_patch[c:d,a:b]
       #print("ensemble_output.shape=", ensemble_output.shape)
       ensemble_output = ensemble_output.astype('uint8')
       cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\ensemble\\ensemble_output_%s.tif" % kkk, ensemble_output)
       #print("text=", text)
       txt=text[number]
      
       #print("txt=", txt)
       #print("number=", number)
       segmentor_output, refiner_output, sum_clean=ensemble_output,ensemble_output,ensemble_output 
       cells["cell_%s" % number]=[segmentor_output,refiner_output,ensemble_output,sum_clean,empty_fluor_base,empty_bright_base,[x0,y0],a,b,c,d,txt, frame_number, prev_frame, coords] 
       #print("cells.name=", cells["cell_%s"][-2] % number)                                                                        
         
   coords=final_centroids    
   return count,cells, coords, text
##########################
def clean_new_list(new_list):
    list_of_sets_only=[set(item[5]) for item in new_list ]    
    sorted_list =sorted(list_of_sets_only,key=len, reverse=True)
    
    for item1 in sorted_list:
         the_rest=sorted_list.copy()
         the_rest.remove(item1)
         for item2 in the_rest:
           if item2.issubset(item1):
              sorted_list.remove(item2)
              
    final_list=[]          
    for item in new_list:
        if set(item[5]) in sorted_list:
            final_list.append(item)
        
    return final_list 
#######################################################   
def split_with_final_list(final_list, coords, frame_number, out_folders):
     print("entering split_with_final_list....")
     kernel = np.ones((3, 3),dtype="uint8")
     final_centroids=np.zeros((len(coords),2))
     
     new_final_list=[]                      
     for ppp in range(len(final_list)):
              #print("ppp=", ppp)
              countt=list(final_list[ppp][5])
                         
              curr_one_contour_item=final_list[ppp]
    
              if len(countt)>1:
              
                separated_cells=[]
                number=len(countt)
                watersheded=brute_force_separation(curr_one_contour_item[0], number)
                #cv2.imwrite(os.path.join(out_folders[1],"watersheded_%s_item_%s.tif") % (frame_number,ppp), watersheded*50)
                markers=[]# create markers (seeds) for seeded watershed
                for k in countt:                   
                    cX, cY=coords[k,:]
                    markers.append([cX,cY])
                print("markers_before=", markers)
                
                separated_centroids=np.zeros((number,2))
                markers_array=np.zeros((number,2))                            
                for i in range(number):
                   #print("i inside countt=", i)
                   base=np.zeros(((382,382)),dtype="float64")
                   base[watersheded==(i+1)]=255
                   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\New folder\\base_%s.tif" % i, base)   
                   base = cv2.erode(base, kernel)
                   bases=clean_patch(base)
                   base=bases[0]
                   base1=base.copy()
                   base1=base1.astype("uint8")
                   im2, contours, hierarchy = cv2.findContours(base1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                   print("len(contours) in base1=", len(contours))
                  
                   cX, cY=find_centroids(base)
                   separated_centroids[i,:]=np.array([[cX,cY]])
                   markers_array[i,:]=np.array([[markers[i][0],markers[i][1]]])
                  
                   separated_cells.append(base) 
                ############ apply hungarian to separated_cells
                print("separated_centroids=", separated_centroids)
                a,b,c,d=curr_one_contour_item[1],curr_one_contour_item[2],curr_one_contour_item[3],curr_one_contour_item[4]
                ordered_centroids, rule=hungarian(markers_array,separated_centroids)
                print("rule=", rule)
                left=[rule[p][0] for p in range(number)]
                right=[rule[pp][1] for pp in range(number)]
               
                print("ordered_centroids=", ordered_centroids)
                for ii in range(len(countt)):
                    print("ii=", ii)
                    index= right.index(ii)                   
                    internal_number=left[index]
                    print("internal_number=", internal_number)
                                   
                    external_number=countt[internal_number]
                    print("external_number=", external_number)
                  
                    new_item=[separated_cells[ii],a,b,c,d,[external_number]]# was ii=internal_number
                    new_final_list.append(new_item)
                    final_centroids[external_number,:]=ordered_centroids[internal_number]# was ordeered_centroids[internal_number] 
                    print("final_centroids=", final_centroids)              
              else:
                 
                  big_patch=curr_one_contour_item[0]
                  cX, cY=find_centroids(big_patch)
                
                  final_centroids[list(curr_one_contour_item[5])[0],:]=np.array([[cX,cY]]) 
                  print("final_centroids=", final_centroids)                                                  
                  new_final_list.append(curr_one_contour_item)
     
     return new_final_list, final_centroids
############################

def brute_force_separation(im1, number):
 print("entering brute_force...")
 #size =im1.shape[0]
 im1=im1.astype(np.uint8)
 image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt=contours[0]
 im=im1.copy()
 rect = cv2.minAreaRect(cnt)
 box = cv2.boxPoints(rect)
 box = np.int0(box)
 #im1 = cv2.drawContours(im1, [box], 0, 150, 1)
 d1 = dist(box[0],box[1])
 d2 = dist(box[1],box[2])
 if d1>d2:
     p1,p2,p3,p4 = box[0], box[1],box[2], box[3]
 else:
     p1,p2,p3,p4= box[1], box[2],box[3], box[0]
 #im1=cv2.cvtColor(im1, cv2.COLOR_GRAY2BGR)
 #im1 = cv2.circle(im1, (int(p1[0]),int(p1[1])), 2, (0,0,255), -1)    
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
 cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\otsu\\cut.tif",im)
 
 im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 print("len(contours) before=", len(contours))
 print("number=", n)                  
 if len(contours)>n:
     im=leave_n_biggest_contours(im,n)
     im2,contours, hierarchy=cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
     print("len(contours) after=", len(contours))                 
 base=np.zeros(((382,382)),dtype="float64")
 for k in range(len(contours)):
     img= np.zeros((382,382),dtype="uint8")
     cv2.drawContours(img,[contours[k]] , 0, 255, -1)
     base[img==255]=k+1
 return base
#############################################

#############################

def hungarian(frame1,frame2):# frame1.shape[0] should be = frame2.shape[0]
    #print("entering equal") 
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
def find_all_centroids(im1):
    im=im1.copy()
    im[im!=0]=255
    im = im.astype('uint8')
   
    im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                  
    cnts=[]
    centroids=[]
    areas=[]
    moments=[] 
    all_centroids=[]
    
    for i in range(len(contours)):	   
      M = cv2.moments(contours[i])
      if  M["m00"]!=0:
       area=cv2.contourArea(contours[i])
       if area!=0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])     
        centroids.append([cX,cY])       
        cnts.append(contours[i])
        areas.append(area)
        moments.append(M["m00"])        
    
    all_centroids=np.zeros((len(centroids),2))
    for k in range(len(areas)):
              all_centroids[k,:]=centroids[k]
        
         
    return all_centroids, cnts, areas,moments
#############################

#################################################
def find_intensities(image):# finds intensities for one current cell
  intensities=[]
  m=int(np.max(image))
  for i in range(m+1):
   if np.any(image==i):
     intensities.append(i)    
  return intensities         
###############

#############


######################
def dist(A,B):
    d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    return d
#################
############



def extract_detected_intensities(final_list):
    ints=[]
    for i in range(len(final_list)):
        llist=final_list[i][1]
        ints+=llist
    return ints
######################################
def find_frame_intensities(real_cnts, prev_frame):
 #curr_frame=np.zeros((382,382),dtype="uint8")
 cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\prev_frame.tif", prev_frame*50) 
 frame_intensities=[]
 for k in range(len(real_cnts)):
        #cv2.drawContours(curr_frame,[real_cnts[k]] , 0, 255, -1)  
        curr_one_cell=np.zeros((382,382),dtype="uint8")
        cv2.drawContours(curr_one_cell,[real_cnts[k]] , 0, 255, -1)
        pr=np.zeros((382,382),dtype="float64")
        pr[curr_one_cell==255]=prev_frame[curr_one_cell==255]        
        intensities =find_intensities(pr)       
        if len(intensities)==1 and intensities[0]==0:# keep zero intensity if it is the only one
                    frame_intensities.append([real_cnts[k],intensities])            
        else:
           frame_intensities.append([real_cnts[k],intensities[1:]])# remove zero intensity
 return frame_intensities
    
    
#####################################
"""
def clean_final_list_sorted(frame_intensities):# intensities are from previous frame
   # removes repetitions 
   #frame_intensities =[[300,[1,4]],[400,[1]],[500,[3]],[100,[2]]]    
   new_frame_intensities =[]
   #all_ints =set([i for i in range(1, N_cells)])
   all_ints =set(extract_detected_intensities(frame_intensities))
   lenghts=[len(frame_intensities[n][1]) for n in range(len(frame_intensities))]
   mm =max(lenghts)
   
   first_ints =[]    
   for k in range(len(frame_intensities)):
         cnt=frame_intensities[k][0]
         intt=frame_intensities[k][1][0]
         iou=frame_intensities[k][2][0]
         first_ints.append(intt)
         new_frame_intensities.append([cnt,[intt],[iou]])
   used_intensities =set(first_ints)
   not_used = list(all_ints.difference(used_intensities))
   
                
   for pp in range(mm):
              print("not_used=", not_used)
              #print("new_frame_intensities=", new_frame_intensities )
              not_used_copy =not_used.copy() 
              for kk in range(len(frame_intensities)): 
                    if len(frame_intensities[kk][1])>pp:
                         #pr_cnt=frame_intensities[kk][0][pp]
                         pr_int=frame_intensities[kk][1][pp]
                         pr_iou=frame_intensities[kk][2][pp]
                         if pr_int in not_used:
                           #new_frame_intensities[kk][0].append(pr_cnt) 
                           new_frame_intensities[kk][1].append(pr_int)
                           new_frame_intensities[kk][2].append(pr_iou)
                           if pr_int in not_used_copy:
                                not_used_copy.remove(pr_int)
              not_used=not_used_copy
              if len(not_used)==0:
                      break
             
   for_print=[new_frame_intensities[i][1:] for i in range(len(new_frame_intensities))]
   print("final_list_after everyting=", for_print)         
     
      
   return new_frame_intensities, for_print       
         
               
         
###################################
def clean_final_list_sorted_1(frame_intensities):# intensities are from previous frame

     #frame_intensities =[[100,[1,2]], [200, [2]],[300,[3]],[400,[4]],[500,[5]]]    
     new_frame_intensities =[]
     all_ints =set(extract_detected_intensities(frame_intensities))
     first_ints =[]    
     for k in range(len(frame_intensities)):
         cnt=frame_intensities[k][0]
         intt=frame_intensities[k][1][0]
         first_ints.append(intt)
         new_frame_intensities.append([cnt,[intt]])
     used_intensities =set(first_ints)
     
     if used_intensities!=all_ints: 
         not_used = list(all_ints.difference(used_intensities))
         
         for i in range(len(not_used)):
             intt=not_used[i]
             for kk in range(len(frame_intensities)):
                    pr_int_list=frame_intensities[kk][1]
                    curr_int_list=new_frame_intensities[kk][1]
                    if intt  in pr_int_list:
                        curr_int_list.append(intt)
             
             
     for_print=[new_frame_intensities[i][1] for i in range(len(new_frame_intensities))]
     print("final_list_after everyting=", for_print)         
     
      
     return new_frame_intensities, for_print       
         
               
         
###################################
def clean_final_list_first(frame_intensities):# goves priority to  contour with 1 intensitiy only deleting from other contours 
     #frame_intensities =[[100,[2]], [200, [1,2]], [300,[0]], [400,[3,4]],[500,[2]]]     
     new_ints =frame_intensities.copy()    
     for_print=[]    
     for_print =[frame_intensities[i][1:] for i in range(len(frame_intensities))]
     print("for_print_intensities inside clean_final_list_first=", for_print)
     #frame_intensities_copy=frame_intensities.copy()
     for kk in range(len(new_ints)):
         item = new_ints[kk]
         if len(item[1])==1 and item[1]!=0:
             sure_number=item[1][0]
             #new_ints.append((item[0], [sure_number]))
             for kkk in range(len(frame_intensities)):# now we remove sure numbers from other contours
                 int_list=frame_intensities[kkk][1]
                 if len(int_list)>1:                     
                      if sure_number in int_list and kkk!=kk:
                          actual_contour=frame_intensities[kkk][0]
                          int_list_copy=int_list.copy()
                          ious=frame_intensities[kkk][2]
                          ious_copy=ious.copy()
                          int_list_copy.remove(sure_number)
                          frame_intensities[kkk]=[actual_contour, int_list_copy,ious_copy]
        
                          
                        
     for_print=[new_ints[i][1] for i in range(len(new_ints))]
     print("new_ints=", for_print)
     
     for kk in range(len(frame_intensities)):
         item= frame_intensities[kk]       
         if len(item[1])>1 and item not in final_list:
               final_list.append((item[0], item[1]))
               #for_print.append(item[1][1:])
         if len(item[1])==1 and item[1]==0:
              final_list.append((item[0], item[1]))
            
     for_print=[frame_intensities[i][1:] for i in range(len(frame_intensities))]
     print("final_list_after initial clean=", for_print)         
     
      
     return frame_intensities, for_print       
         
               
         
          
#############################
def compile_final_list_1(prev_frame, curr_frame):     
     final_list=[]
     frame_intensities=[]
     for_print=[]
     im2, contours, hierarchy = cv2.findContours(curr_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)           
     for k in range(len(contours)):
         curr_one_cell=np.zeros((382,382),dtype="uint8")
         cv2.drawContours(curr_one_cell,[contours[k]] , 0, 255, -1)
         pr=np.zeros((382,382),dtype="float64")
               
         pr[curr_one_cell==255]=prev_frame[curr_one_cell==255]        
         intensities =find_intensities(pr)
         frame_intensities.append([contours[k],intensities])
     for_print=[frame_intensities[i][1] for i in range(len(frame_intensities))]
     print("for_print_intensities=", for_print)
     for kk in range(len(frame_intensities)):
         item= frame_intensities[kk]
         if len(item[1])==2:
             sure_number=item[1][-1]
             final_list.append((item[0], [sure_number]))
             for_print.append([sure_number])
             for kkk in range(len(frame_intensities)):
                 int_list=frame_intensities[kkk][1]
                 actual_contour=frame_intensities[kkk][0]
                 if sure_number in int_list and kkk!=kk:
                     int_list_copy=int_list.copy()
                     int_list_copy.remove(sure_number)                   
                     frame_intensities[kkk]=[[actual_contour, sure_number]]
     for_print=[final_list[i][1] for i in range(len(final_list))]
     print("for_print_fianl_list=", for_print)
     for kk in range(len(frame_intensities)):
         item= frame_intensities[kk]       
         if len(item[1])>2:
               final_list.append((item[0], item[1][1:]))
               for_print.append(item[1][1:])
         if len(item[1])==1:
              final_list.append((item[0], item[1]))
              for_print.append(item[1])
     return final_list, for_print       
         
"""          
##############################
def create_previous_frame(cells):
    previous_frame= np.zeros((382,382),dtype="float64")      
    for i in range(len(cells)):
      base = np.zeros((382+Bordersize*2,382+Bordersize*2),dtype="float64")  
      patch=cells["cell_%s" % i][3]
      patch = patch.astype('float64')  
      a,b,c,d=cells["cell_%s" % i][7],cells["cell_%s" % i][8],cells["cell_%s" % i][9],cells["cell_%s" % i][10]
      base[c:d,a:b]=patch
      base=base[Bordersize:Bordersize+382,Bordersize:Bordersize+382]
      base[base==255]=i+1               
      previous_frame+=base
    return previous_frame
 
def create_current_frame(previous_frame_1):
     previous_frame=previous_frame_1.copy()       
     previous_frame[previous_frame!=0]=255
     previous_frame = previous_frame.astype('uint8')
     im2, contours, hierarchy = cv2.findContours(previous_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)           
     current_frame=np.zeros((382,382),dtype="uint8")
     for p in range(len(contours)):
         cv2.drawContours(current_frame,[contours[p]] , 0, 255, 1)
     return current_frame
#############################################

######################################################### 

 

#################################################
"""
def correct_splitting(final_list,prev_distances, current_distances):
  ratios_per_frame =[]
  for i in range(len(prev_distances)):
        first=prev_distances[i][0]
        second=current_distances[i][0]
        ratio=second/first
        ratios_per_frame.append((ratio,prev_distances[i][1],prev_distances[i][2]))
  print("ratios_per_frame=", ratios_per_frame)
  big_dist=[]
  for ii in range(len(ratios_per_frame)):
        d = ratios_per_frame[ii][0]
        cell_1 =ratios_per_frame[ii][1]
        cell_2=ratios_per_frame[ii][2]          
        if d>1.3:# distance increased, cells should be together            
             big_dist.append([d,cell_1, cell_2])
  if len(big_dist)!=0:         
    big_dist_sorted=sorted(big_dist, reverse=True)
    biggest=big_dist_sorted[0]    
    print("big_dist=", big_dist)
    print("biggest=", biggest)   
    culprit=biggest[2]
    friend=biggest[1]
    print("culprit=", culprit)
    #print("friend=", friend)                ]    
    for iii in range(len(final_list)):
              item=final_list[iii][1]
              print("item=", item)             
              if culprit in item:
                   item.remove(culprit) 
              if friend in item:
                  item.append(culprit)  
  return final_list    



#################################################
def correct_splitting_2(final_list,prev_distances, current_distances):
    ratios_per_frame =[]
    for i in range(len(prev_distances)):
        first=prev_distances[i][0]
        second=current_distances[i][0]
        ratio=second/first
        ratios_per_frame.append((ratio,prev_distances[i][1],prev_distances[i][2]))
    print("ratios_per_frame=", ratios_per_frame)
    small_dist=[]
    big_dist=[]
    for ii in range(len(ratios_per_frame)):
        d = ratios_per_frame[ii][0]
        cell_1 =ratios_per_frame[ii][1]
        cell_2=ratios_per_frame[ii][2]   
        if d<0.6:# distance decreased: cells should not be together         
            small_dist.append([cell_1, cell_2])    
        if d>1.8:# distance increased, cells should be together            
             big_dist.append([cell_1, cell_2]) 
    print("small_dist=", small_dist)
    print("big_dist=", big_dist)
    cells_to_be_moved=[]
    for kk in range(len(big_dist)):
         a=big_dist[kk]
         for kkk in range(len(big_dist)):
             b=small_dist[kkk]             
             bad_cell=list(set(a) & set(b))
             print("bad_cell=", bad_cell)
             if len(bad_cell)!=0:
                  union=list(set(list(set(a)) +list (set(b))))
                  print("union=", union)
                  union.remove(bad_cell[0])
                  print("others=", union)
                  for i in range(len(union)):
                      if union[i] in b:                          
                          rem=union[i]
                      if union[i] in a:                          
                          add=union[i]                     
                  cells_to_be_moved.append((bad_cell[0],rem,add))
    print("cells_to_be_moved=", cells_to_be_moved)
    if len(cells_to_be_moved)!=0:
       for ii in range(len(cells_to_be_moved)):
         culprit=cells_to_be_moved[ii][0]
         for iii in range(len(final_list)):
              item=final_list[iii][1]
              if cells_to_be_moved[ii][1] in item:
                   item.remove(culprit) 
              if cells_to_be_moved[ii][2] in item:
                  item.append(culprit)  
    return final_list    

############################################
def correct_splitting_1(final_list,prev_distances, current_distances):
    ratios_per_frame =[]
    for i in range(len(prev_distances)):
        first=prev_distances[i][0]
        second=current_distances[i][0]
        ratio=second/first
        ratios_per_frame.append((ratio,prev_distances[i][1],prev_distances[i][2]))
    print("ratios_per_frame=", ratios_per_frame)
    for ii in range(len(ratios_per_frame)):
        d = ratios_per_frame[ii][0]
        cell_1 =ratios_per_frame[ii][1]
        cell_2=ratios_per_frame[ii][2]   
        if d<0.5:# distance decreased: cells should not be together         
          for kk in range(len(final_list)):
              item=final_list[kk][1]
              if len(item)>1 and cell_1 in item:
                  item.remove(cell_2)         
        if d>2:# distance increased, cells should be together            
            for kk in range(len(final_list)):
              item=final_list[kk][1]# item is a list
              if  cell_1 in item:
                  item.append(cell_2)  
    return final_list    

"""        
########################################################

def check_watershed(watersheded,number):  
  img= np.zeros((382,382),dtype="float64")
  kernel = np.ones((3, 3),dtype="float64")
  for i in range(number):
    base=np.zeros(((382,382)),dtype="float64")
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
  
####################################################

##############################################
def update_dictionary_new(rule,dictt,final_centroids,bases):
    new_dict={}
    for i in range(rule.shape[0]):
        old_number=int(rule[i][1])
        new_number=int(rule[i][0])
        x=dictt["cell_%s" % old_number]
        x0,y0=final_centroids[new_number][0],final_centroids[new_number][1]
        txt,frame=x[11], x[12]
        a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48           
        base=bases[new_number]
        patch=base[c:d,a:b]
        patch = patch.astype('uint8')
        
        
        x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12=x[0],x[1],x[2],patch,x[4],x[5],[x0,y0],a,b,c,d,txt,frame           
        new_dict["cell_%s" % new_number]=[x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12]
    del dictt
    return new_dict



#########################################

#####################################

##########################
def erode_watershed(watersheded_image):
    shape =watersheded_image.shape
    result=np.zeros(shape,dtype="uint8")
    kernel = np.ones((3, 3),dtype="uint8")
    for i in range(2):
      base=np.zeros(shape,dtype="uint8")
      base[watersheded_image==(i+1)]=255
      eroded = cv2.erode(base, kernel)
      result[eroded==255]=255
    return result
###########################################

####################################
def sum_of_distances(coords,ress):   
    disst=[dist(coords[i],ress[i]) for i in range(coords.shape[0])]
    return sum(disst)
####################################################

###################################################
"""
def find_all_centroids_1(im, flag, coords):
    im = im.astype(np.uint8)
  
    #print("image.shape_before find cnts=", im.shape)
    im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                  
    cnts=[]
    centroids=[]
    areas=[]
    moments=[] 
    all_centroids=[]
    good_contours=[]
    good_areas=[]
    good_moments=[]
    for i in range(len(contours)):	   
      M = cv2.moments(contours[i])
      if  M["m00"]!=0:
       area=cv2.contourArea(contours[i])
       if area!=0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])     
        centroids.append([cX,cY])       
        cnts.append(contours[i])
        areas.append(area)
        moments.append(M["m00"])
    #print("centroids in find=", centroids)
    #print("areas in find=", areas)
    #print("moments in find=", moments)
    if len(centroids)==0:
        good_contours=[]
        good_centroids=[]
        good_areas=[]
        good_moments=[] 
        all_centroids=np.zeros(coords.shape)
    else:
        if flag=="do not clean":
          good_centroids= centroids
          good_contours= cnts
          good_areas= areas
          good_moments= moments 
          all_centroids=np.zeros((len(centroids),2))
          for k in range(len(areas)):
              all_centroids[k,:]=centroids[k]
        
        if flag=="clean":
          w=list(zip(cnts,centroids, moments,areas))
          ww=sorted(w,key=lambda student:student[-1],reverse=True)
          ress = list(zip(*ww))        
          contours_sorted=ress[0]
          centroids_sorted=ress[1]
          moments_sorted=ress[2]
          areas_sorted=ress[3]
    
    
          if len(contours)>len(coords):# ignore big cells, but do not overclean
            thresh=350.0         
            good_areas=[areas_sorted[i] for i in range(len(areas_sorted)) if areas_sorted[i]>=thresh and moments_sorted[i]!=0.0]
            n=len(good_areas)
            if n<len(coords):             
               for k in range(n, len(coords)):
                   good_areas.append(areas_sorted[k])
            good_contours=[contours_sorted[kk] for kk in range(len(good_areas))]
            good_centroids=[centroids_sorted[kk] for kk in range(len(good_areas))]
            good_moments=[moments_sorted[kk] for kk in range(len(good_areas))]
            all_centroids=np.zeros((len(good_centroids),2))
            for k in range(len(good_centroids)):
               all_centroids[k,:]=good_centroids[k] 
               
          if len(contours)<=len(coords):
            thresh=50.0
            good_areas=[areas_sorted[i] for i in range(len(areas_sorted)) if areas_sorted[i]>=thresh and moments_sorted[i]!=0.0]
            good_contours=[contours_sorted[kk] for kk in range(len(good_areas))]
            good_centroids=[centroids_sorted[kk] for kk in range(len(good_areas))]
            good_moments=[moments_sorted[kk] for kk in range(len(good_areas))]
            all_centroids=np.zeros((len(good_centroids),2))
            for k in range(len(good_centroids)):
              all_centroids[k,:]=good_centroids[k]
         
    return all_centroids, good_contours, good_areas, good_moments
"""
#############################################
def dist(A,B):
    d=math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    return d
###############################################################
def IoU(image_1, image_2): # both images are binary (from 0 to 255)   
   img11=image_1/255 
   img22=image_2/255
   img=img11+img22
   intersection=np.sum(img[img==2.0])
   union=np.sum(img[img>0.0])
   IoU=intersection/union  
   return IoU
##########################################################

    
########################################################
def labelling_general(frame1,frame2): # this is the nearest neighbor, rearranges order of centroids in frame 2
    print("entering general") 
    n=frame1.shape[0]
    m=frame2.shape[0]
    M =np.zeros((n,m))
    for p in range(n):
        for q in range(m):
            M[p,q]=dist(frame1[p],frame2[q])
    
    indexes=[]
    for i in range(n):
        ind = np.unravel_index(np.argmin(M, axis=None), M.shape)
        indexes.append(ind)
        (a,b)=ind
        M[a,:]=500 
    #label=np.zeros((n,2))
    rule =np.zeros((n,2),dtype=np.int8)
    for t in range(n):
        c=indexes[t][0]
        d=indexes[t][1]
        #label[c]=frame2[d]
        rule[t]=np.array([c,d])
    return  rule
########################################

##################################


#####################################

############################################################

def standardize(frame): #normalizing per channel
     frame = frame.astype('float32')
     means = frame.mean(axis=(0,1), dtype='float64')
     stds = frame.std(axis=(0,1), dtype='float64')    
     frame = (frame - means) / stds
     return frame

#######################################################
def leave_n_biggest_contours(im,n):
     #print("entering leave_n_biggest_contours")
     im = im.astype(np.uint8)
     im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                    
     areas=[]    
     for cnt in contours:      
       area=cv2.contourArea(cnt)
       print("area=", area)
       areas.append(area)      
     w=list(zip(contours,areas))
     ww=sorted(w,key=lambda student:student[-1],reverse=True)
     ress = list(zip(*ww))        
     img=np.zeros((im.shape),dtype="uint8")
     for i in range(n):
       cv2.drawContours(img,[ress[0][i]] , 0, 255, -1)      
     return img

##########################################################
def find_areas_ratio(output_from_watershed): # output=RGB or grey   
    output=output_from_watershed.astype("uint8")
    im2,contours, hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   
    area_1=cv2.contourArea(contours[0])
    area_2=cv2.contourArea(contours[1])   
    if (area_1==0. or area_2==0.):
        ratio="none"
    else:
      if area_1>area_2:
        ratio=area_1/area_2
      else:
        ratio=area_2/area_1     
    return ratio 
#########################################################
def leave_two_biggest_contours(im):
     im2, contours, hierarchy = cv2.findContours(im,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                    
     areas=[]    
     for cnt in contours:      
       area=cv2.contourArea(cnt)     
       areas.append(area)      
     w=list(zip(contours,areas))
     ww=sorted(w,key=lambda student:student[-1],reverse=True)
     ress = list(zip(*ww))        
     img=np.zeros((im.shape),dtype="uint8") 
     cv2.drawContours(img,[ress[0][0]] , 0, 255, -1)
     cv2.drawContours(img,[ress[0][1]] , 0, 255, -1)
     return img
############################
def myFunc(e):
  return e[0]
################################################### 
#markers_before=np.array( [[352., 134.], [339., 106.]])
def find_nearest_white(img, target):
    nonzero = np.argwhere(img == 255)
    distances = np.sqrt((nonzero[:,0] - target[1]) ** 2 + (nonzero[:,1] - target[0]) ** 2)
    nearest_index = np.argmin(distances)
    return nonzero[nearest_index]
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
           #print("changed marker=", marker)
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
###########################################

#####################################

def seeded_watershed(img,x1,y1,x2,y2):# img.shape=382 x 382    
     img=img.astype(np.uint8)   
     kernel= np.ones((3,3),np.uint8) 
     opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel, iterations = 3)
    
     sure_bg = cv2.dilate(opening,kernel,iterations=1)    
     sure_fg=np.zeros(img.shape,dtype="uint8")
     sure_fg[(y1-1):(y1+1),(x1-1):(x1+1)]=255
     sure_fg[(y2-1):(y2+1),(x2-1):(x2+1)]=255
     unknown= cv2.subtract(sure_bg,sure_fg) 
    
     ret, markers = cv2.connectedComponents(sure_fg)
     markers = markers+1    
     markers[unknown!=0] = 0    
     img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
     markers = cv2.watershed(img,markers)    
     markers_1=markers.copy()
     markers_1=markers_1-1   
    
     return markers_1#markers_1.shape = 382 x 382
#####################################################################

####################
#####################################################

def recalculate_centres(cells):
    for i in range(len(cells)):
        cell=cells["cell_%s" % i]          
        black=np.zeros((382,382),dtype="uint8")
        black_border=cv2.copyMakeBorder(black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
        a,b,c,d=cell[7],cell[8],cell[9],cell[10] 
        black_border[c:d, a:b]=cell[3]
        black_again=black_border[Bordersize:382+Bordersize,Bordersize:382+Bordersize]
        im2, contours, hierarchy = cv2.findContours(black_again.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)     
        if len(contours)==1:
         for c in contours:	
          M = cv2.moments(c)
          if M["m00"]==0.0:
            M["m00"] =0.001
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])              
         x0,x1,x2,x3,x4,x5=cell[0],cell[1],cell[2],cell[3],cell[4], cell[5]         
         x6=[cX,cY]
         a,b,c,d,txt,fr=cell[7],cell[8],cell[9],cell[10],cell[11], cell[12]
         del cell        
         cells["cell_%s" % i]=[x0,x1,x2,x3,x4,x5,x6,a,b,c,d,txt,fr]
    return cells

#######################################################################################
