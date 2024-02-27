import cv2
import numpy as np
import copy
import math
#####################################
Bordersize=100
######################################
def detect_division(cells, count, k,kk):# detects divisions in the whole frame     
       for_print=[]       
       cut_patches=[]
       for kkk in range(len(cells)):# building info list (figure 8 detections)
           verdict,segmented_patch,im1=detect_figure_8(cells["cell_%s" % kkk][3])                 
           if verdict=="division":
             count[kkk]+=1
             mother_name=cells["cell_%s" % kkk][11]# was [-2]
             if (count[kkk]==1):# ignoring the 1st division detection               
                 for_print.append("maybe")
             if count[kkk]==2:                                
                 for_print.append("yes")                
           else:        
               count[kkk]=0
               for_print.append("no")
               mother_name=[]
           cut_patches.append(im1)            
       return count,cut_patches, mother_name   
####################################
def detect_figure_8(segmented_patch):# detects division in patch
  verdict="no division"
  im1=segmented_patch.copy() 
  image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
  cnt1=contours[0]
  hull=cv2.convexHull(cnt1,returnPoints=False)
  defects=cv2.convexityDefects(cnt1,hull)
  im1 = cv2.cvtColor(im1,cv2.COLOR_GRAY2BGR)
  distances=[]
  fars=[]
  if defects is not None:
   for k in range(defects.shape[0]):
    s,e,f,d=defects[k,0]   
    far=tuple(cnt1[f][0]) 
    distances.append(d)
    fars.append(far)     
   w=list(zip(distances,fars))
   ww=sorted(w,key=lambda student:student[0],reverse=True)
   ress = list(zip(*ww))         
   distances_sorted=ress[0]
   if len(distances_sorted)>2:
       fars_sorted=ress[1]# Folter-1: covexity defects
       delta_dist=distances_sorted[1]/distances_sorted[2]
       if (distances_sorted[1]/distances_sorted[2]>=2.5):# was 3.77 before
        cv2.line(im1,fars_sorted[0],fars_sorted[1],(0,255,0),2)
        im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
        im1[im1==150]=0
        image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        parameters=[]      
        circularities=[]
        for cnt in contours:
          area=cv2.contourArea(cnt)
          if area==0.0:
              area=0.001
          perimeter=np.round(cv2.arcLength(contours[0],True),2)
          circularity=np.round(4*math.pi*area/perimeter**2,2)
          parameters.append((area,circularity))
        parameters=sorted(parameters,reverse=True)#filter-2:europds vs figure -8 shapes   
        if (len(parameters)==2):      
         if (parameters[0][0]/parameters[1][0])<=1.4:# was 1.3      
             if  (parameters[0][1]>0.8 and parameters[1][1]>0.8): 
                verdict="division"
   else:
      verdict="no division"
  else:
      verdict="no division"
  return verdict,segmented_patch,im1# if no division, im1=segmented_patch, the cell is not cut
################ recalculate centres of daugher cells after division
def recalculate_centre(segmented_image,old_coords, frame_size):
     x0,y0=old_coords[0],old_coords[1]
     black=np.zeros((frame_size,frame_size),dtype="uint8")
     black_border=cv2.copyMakeBorder(black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
     a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48  
     black_border[c:d, a:b]=segmented_image
     black_again=black_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
     im2, contours, hierarchy = cv2.findContours(black_again.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
     for c in contours:	
         M = cv2.moments(c)
         cX = int(M["m10"] / M["m00"])
         cY = int(M["m01"] / M["m00"])
     return cX,cY
#################################################
def process_figure_8(im1,centre, frame_size):#separates figure into 2 cells and patches
    if im1.shape==(96,96,3):
             im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY) 
    im2, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    centroids=[]
    separated_cells=[]
    for kkk  in range(len(contours)):	
        img=np.zeros((96,96),dtype="uint8")
        cv2.drawContours(img, contours, kkk, 255, -1)        
        separated_cells.append(img)       
        x,y=recalculate_centre(img,(centre[0],centre[1]),frame_size)
        centroids.append([x,y])    
    return separated_cells,centroids
#########################################################
def update_dictionary_after_division(cut_patches,cells,text,count,indicator,coords, frame_size, colors):      
    N_cells=len(cells) 
    for kkk in range(N_cells):#correcting cells dictionary if division         
           if count[kkk]==2:             
              im1=cut_patches[kkk]            
              separated_cells,centroids=process_figure_8(im1,cells["cell_%s" % kkk][6], frame_size)                                         
              indicator+=1                                         
              cells["cell_%s" % kkk][3]=separated_cells[0]
              cells["cell_%s" % kkk][6]=centroids[0]              
              text[kkk]+="0"
              cells["cell_%s" % kkk][11]=text[kkk]           
              cells["cell_%s" % kkk][15]=colors[text[kkk]]
              cells["cell_%s" % kkk][16]= "daughter-1"
                       
              cellscopy=copy.deepcopy(cells)                               
              cells["cell_%s" % (N_cells)]=cellscopy["cell_%s" % kkk]
              cells["cell_%s" % (N_cells)][3]=separated_cells[1]
              cells["cell_%s" % (N_cells)][6]=centroids[1]                                         
              text.append(text[kkk][:-1]+"1")
              cells["cell_%s" % (N_cells)][11]=text[-1]             
              cells["cell_%s" % N_cells][15]=colors[text[-1]]             
              cells["cell_%s" % N_cells][16]= "daughter-2"
              coords=np.concatenate((coords,np.array([cells["cell_%s" % (N_cells)][6][0],cells["cell_%s" % (N_cells)][6][1]]).reshape((1,2))) )             
              count[kkk]=0 
    N_cells=len(cells)                                         
    return cells,text,count,indicator,coords
###################checks if division happens too early
def check_division_frame_number(count, cells, dict_of_divisions,cell_name,frame_number):   
    life_times={1:50,2:800,3:500, 4:500}# keys=lengths of cell names; numbers -min number of frames between divisions
    keys =list(dict_of_divisions.keys()) 
    if cell_name in keys:
        delta =frame_number-dict_of_divisions[cell_name]      
        if delta<life_times[len(cell_name)]:            
             for kk in range(len(cells)):
               current_name=cells["cell_%s" % kk][11]
               if current_name==cell_name:
                 number =kk
                 count[number]=0
                 break              
    return count
#######################################
