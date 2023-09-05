import cv2
import numpy as np
import copy
import math
Bordersize=100
######################################
def detect_division(cells, count, k,kk):# detects divisions in the whole frame     
       for_print=[]       
       cut_patches=[]
       for kkk in range(len(cells)):# building info list (figure 8 detections)
           verdict,segmented_patch,im1=detect_figure_8(cells["cell_%s" % kkk][3])
           #print("cell=",cells["cell_%s" % kkk][-2])
           #cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\issues\\frame_%s_cell_%s.tif" % (k+kk,kkk), cells["cell_%s" % kkk][3])
           #print("verdict=", verdict)           
           if verdict=="division":
             count[kkk]+=1
             mother_name=cells["cell_%s" % kkk][11]# was [-2]
             if (count[kkk]==1):# ignoring the 1st division detection               
                 for_print.append("maybe")
             if count[kkk]==2:                                
                 for_print.append("yes")
                 #cell_name=cells["cell_%s" % kkk][-2]
           else:        
               count[kkk]=0
               for_print.append("no")
               mother_name=[]
           cut_patches.append(im1)            
       return count,cut_patches, mother_name   
#######################################

####################################
def detect_figure_8(segmented_patch):# detects division in patch
  verdict="no division"
  im1=segmented_patch.copy()
  #im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
  #im1 = im1.astype('uint8')
  image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #print("len(contours) in division detector=", len(contours))
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
  #print("distances_sorted=", distances_sorted)
   if len(distances_sorted)>2:
       fars_sorted=ress[1]# Folter-1: covexity defects
       #if (distances_sorted[0]>1000 and distances_sorted[1]>1000 and distances_sorted[2]<250):
       delta_dist=distances_sorted[1]/distances_sorted[2]
       #print("delta_dist=", delta_dist)

       if (distances_sorted[1]/distances_sorted[2]>=2.5):# was 3.77 before
        cv2.line(im1,fars_sorted[0],fars_sorted[1],(0,255,0),2)
        im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
        im1[im1==150]=0
        image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        parameters=[]
        #perimeters=[]
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
         #print("areas_ratio=",parameters[0][0]/parameters[1][0])
         if (parameters[0][0]/parameters[1][0])<=1.4:# was 1.3      
             if  (parameters[0][1]>0.8 and parameters[1][1]>0.8): 
                verdict="division"
   else:
      verdict="no division"
  else:
      verdict="no division"
  return verdict,segmented_patch,im1# if no division, im1=segmented_patch, the cell is not cut
#################################################################

#######################################################
def recalculate_centre(segmented_image,old_coords):
     x0,y0=old_coords[0],old_coords[1]
     black=np.zeros((382,382),dtype="uint8")
     black_border=cv2.copyMakeBorder(black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
     a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48  
     black_border[c:d, a:b]=segmented_image
     black_again=black_border[Bordersize:382+Bordersize,Bordersize:382+Bordersize]
     im2, contours, hierarchy = cv2.findContours(black_again.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
     for c in contours:	
         M = cv2.moments(c)
         cX = int(M["m10"] / M["m00"])
         cY = int(M["m01"] / M["m00"])
     return cX,cY
#################################################
def process_figure_8(im1,centre):#separates figure into 2 cells and patches
    if im1.shape==(96,96,3):
             im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY) 
    im2, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    centroids=[]
    separated_cells=[]
    for kkk  in range(len(contours)):	
        img=np.zeros((96,96),dtype="uint8")
        cv2.drawContours(img, contours, kkk, 255, -1)        
        separated_cells.append(img)       
        x,y=recalculate_centre(img,(centre[0],centre[1]))
        centroids.append([x,y])    
    return separated_cells,centroids
###############################################
def check_tracker(clip_centr,coords):# corrects tracking errors in the beginning of a clip
    distances=[]
    for i in range(len(coords)):       
     dist=math.sqrt((clip_centr[0][i][0]-coords[i][0])**2+(clip_centr[0][i][1]-coords[i][1])**2)
     distances.append(dist)   
    if np.any(np.array(distances)>=40):
        clip_centr=[coords]*4
    return clip_centr
###################################################
def assign(separated_cells,centroids,true_centre): 
  x0,y0=true_centre[0],true_centre[1]    
  x1,y1=centroids[0][0],centroids[0][1]
  x2,y2=centroids[1][0],centroids[1][1]
  d1=(x1-x0)**2+(y1-y0)**2
  d2=(x2-x0)**2+(y2-y0)**2 
  d=np.array([d1,d2])
  i=np.argmin(d) 
  im=separated_cells[i]
  for i in range(len(centroids)):     
      im=separated_cells[i].copy()
      zero=np.zeros((382+Bordersize,382+Bordersize))
      zero[centroids[i][1]+Bordersize-48:centroids[i][1]+Bordersize+48,centroids[i][0]+Bordersize-48:centroids[i][0]+Bordersize+48]=im
      im[im==255]=100   
      im[centroids[i][1]+Bordersize-5:centroids[i][1]+Bordersize+5,centroids[i][0]+Bordersize-5:centroids[i][0]+Bordersize+5]=255         
  return im
####################################################

################################################################################### 
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
######################################

#########################################################
def update_dictionary_after_division(cut_patches,cells,text,count,indicator,coords):   
    #print("entering update_dictionary")
    N_cells=len(cells) 
    #print("N_cells before updating dict=", N_cells)
    #print("COUNT=",count)
    for kkk in range(N_cells):#correcting cells dictionary if division
           #print("cell number=",kkk)
           if count[kkk]==2:
             # print("division in cell ",kkk)
              im1=cut_patches[kkk]
            
              separated_cells,centroids=process_figure_8(im1,cells["cell_%s" % kkk][6])                            
              #print("len(centroids=", len(centroids))
              indicator+=1                                         
              cells["cell_%s" % kkk][3]=separated_cells[0]
              cells["cell_%s" % kkk][6]=centroids[0]
              #print("the first cell_centroids",cells["cell_%s" % kkk][6])
              text[kkk]+="0"
              cells["cell_%s" % kkk][11]=text[kkk]
              #texts.append(texts[kkk]+"0")  
              cellscopy=copy.deepcopy(cells)                               
              cells["cell_%s" % (N_cells)]=cellscopy["cell_%s" % kkk]
              cells["cell_%s" % (N_cells)][3]=separated_cells[1]
              cells["cell_%s" % (N_cells)][6]=centroids[1]                 
              #print("the second cell_centroids",cells["cell_%s" % N_cells][6])            
              text.append(text[kkk][:-1]+"1")
              cells["cell_%s" % (N_cells)][11]=text[-1]
              coords=np.concatenate((coords,np.array([cells["cell_%s" % (N_cells)][6][0],cells["cell_%s" % (N_cells)][6][1]]).reshape((1,2))) )
              #print("coords after first division=",coords) 
              count[kkk]=0 
    N_cells=len(cells)
    #print("N_cells_after_updating dict=", N_cells)
    #print("count=",count)                                         
    return cells,text,count,indicator,coords

###############################################
def update_dictionary_after_division_2(cut_patches,cells,texts,count,indicator,coords):       
    N_cells=len(cells)    
    for kkk in range(N_cells):#correcting cells dictionary if division           
           if count[kkk]==2:
              im1=cut_patches[kkk]            
              separated_cells,centroids=process_figure_8(im1,cells["cell_%s" % kkk][6])                                
              indicator+=1
              #copy_1=copy.deepcopy(cells) 
             
              texts[kkk]+="0"             
              #number_1=texts[kkk]
              #cells["cell_%s" % number_1]=copy_1["cell_%s" % number_1]
              #cells["cell_%s" % number_1][3]=separated_cells[0]
              #cells["cell_%s" % number_1][6]=centroids[0] 
                                       
              cells["cell_%s" % kkk][3]=separated_cells[0]
             
              cells["cell_%s" % kkk][6]=centroids[0] 
              #cells["cell_%s" % kkk].append(centroids[0])            
            
              texts.append(texts[kkk][:-1]+"1")
              #number_2=texts[kkk][-1]
              cellscopy=copy.deepcopy(cells) 
               
              #cells["cell_%s" % number_2]=cellscopy["cell_%s" % number_1]
              #cells["cell_%s" % number_2][3]=separated_cells[1]
             # cells["cell_%s" % number_2][6]=centroids[1] 
                 
              cells["cell_%s" % (N_cells)]=cellscopy["cell_%s" % kkk]
              cells["cell_%s" % (N_cells)][3]=separated_cells[1]
              cells["cell_%s" % (N_cells)][6]=centroids[1]                                 
              #coords=np.concatenate((coords,np.array([cells["cell_%s" % number_2][6][0],cells["cell_%s" % number_2][6][1]]).reshape((1,2))) )                       
              coords=np.concatenate((coords,np.array([cells["cell_%s" % (N_cells)][6][0],cells["cell_%s" % (N_cells)][6][1]]).reshape((1,2))) )             
              count[kkk]=0 
    N_cells=len(cells)                                        
    return cells,texts,count,indicator,coords
#########################################################
"""
cell_name="10"
dict_of_divisions={'1': 66, '10': 677}
count=np.array([1,2,0,0,0])
frame_number=70
cells={"cell_0":["1"],"cell_1":["10"]}
"""

def check_frame(count, cells, dict_of_divisions,cell_name,frame_number):# checks if division happens too early
    #print("entering check_frame")
    life_times={1:50,2:800,3:500, 4:500}# keys=lengths of cell names; numbers -min number of frames between divisions
    keys =list(dict_of_divisions.keys())
    #print("keys=", keys)
    if cell_name in keys:
        delta =frame_number-dict_of_divisions[cell_name]
        #print("delta=", delta)
        if delta<life_times[len(cell_name)]:            
             for kk in range(len(cells)):
               current_name=cells["cell_%s" % kk][11]
               if current_name==cell_name:
                 number =kk
                 count[number]=0
                 break              
    return count
#######################################









"""
def division_vs_badsegm(cells, count):
   final_verdicts=[]
   mitotic_cell=[]
   if len(cells)>=2:       
    for p in range(len(cells)):        
        first=cells["cell_%s" % p]
        if (count[p]!=0):
          second_number=find_closest_cell(p,cells)        
          a1,b1,c1,d1=first[7],first[8],first[9],first[10]     
          black1=np.zeros((382,382))
          black1=cv2.copyMakeBorder(black1, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )            
          patch1=first[3].copy()
          if patch1.shape==(96,96,3):
             patch1 = cv2.cvtColor(patch1,cv2.COLOR_BGR2GRAY) 
          patch1[patch1==255]=50
          black1[c1:d1,a1:b1]=patch1
          second=cells["cell_%s" % second_number]         
          a2,b2,c2,d2=second[7],second[8],second[9],second[10]     
          black2=np.zeros((382,382))
          black2=cv2.copyMakeBorder(black2, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )            
          patch2=second[3].copy()
          if patch2.shape==(96,96,3):
             patch2 = cv2.cvtColor(patch2,cv2.COLOR_BGR2GRAY) 
          patch2[patch2==255]=1
          black2[c2:d2,a2:b2]=patch2         
          black=black1+black2
        
          if np.any(black==51):
            final_verdicts.append("no")
            count[p]=0
           
          else:
            final_verdicts.append("yes")
            mitotic_cell=first[-2]
        else:            
            final_verdicts.append("no")
   else:
            mitotic_cell= cells["cell_0"][-2]             
   return count, mitotic_cell
"""