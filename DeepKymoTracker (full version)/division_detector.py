import cv2
import numpy as np
import copy
import math
from plot import update_color_dictionary
#####################################
#Bordersize=100
######################################
def detect_division(cells, count, k,kk):# detects divisions in the whole frame     
       for_print=[]
       cut_patch=[]
       for kkk in range(len(cells)):# building info list (figure 8 detections)
           segm_patch= cells["cell_%s" % kkk][3]        
           verdict,segmented_patch,im1=detect_figure_8(segm_patch)
           if verdict=="division":
             count[kkk]+=1
             mother_name=cells["cell_%s" % kkk][11]# was [-2]
             cut_patch=im1
             if (count[kkk]==1):# ignoring the 1st division detection               
                 for_print.append("maybe")
             if count[kkk]==2:                                
                 for_print.append("yes")
               
           else:        
               count[kkk]=0
               for_print.append("no")
               mother_name=[]
               
                  
       #immmg, cnts, hier = cv2.findContours(cut_patch,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
       
       #print("len(contours) inside detect_division=", len(cnts))
       return count,cut_patch, mother_name
####################################
def detect_figure_8(segmented_patch):# detects division in patch
  verdict="no division"
  im1=segmented_patch.copy() 
  image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
  cnt1=contours[0]
  hull=cv2.convexHull(cnt1,returnPoints=False)
  defects=cv2.convexityDefects(cnt1,hull)
 
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
        im1 = cv2.cvtColor(im1,cv2.COLOR_GRAY2BGR)
        cv2.line(im1,fars_sorted[0],fars_sorted[1],(0,255,0),2)
        im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
        im1[im1==150]=0
        image, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        parameters=[]      
        immmg, cnts, hier = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #print("len(contours) inside detect_figure_8_before=", len(cnts))
       
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
  immmg, cnts, hier = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #print("len(contours) inside detect_figure_8_after=", len(cnts))
  return verdict,segmented_patch,im1# if no division, im1=segmented_patch, the cell is not cut
################ recalculate centres of daugher cells after division
def recalculate_centre(segmented_image,old_coords, frame_size, bordersize, patch_size):
     x0,y0=old_coords[0],old_coords[1]
     black=np.zeros((frame_size,frame_size),dtype="uint8")
     black_border=cv2.copyMakeBorder(black, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_REPLICATE )
     a,b,c,d=int(round(x0))+bordersize-patch_size,int(round(x0))+bordersize+patch_size,int(round(y0))+bordersize-patch_size,int(round(y0))+bordersize+patch_size  
     black_border[c:d, a:b]=segmented_image
     black_border_copy=black_border.copy()
     black_again=black_border[bordersize:frame_size+bordersize,bordersize:frame_size+bordersize]
     im2, contours, hierarchy = cv2.findContours(black_again,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)     
     c=contours[0]	
     M = cv2.moments(c)
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
     area=np.round(cv2.contourArea(c),2)
     perimeter=np.round(cv2.arcLength(c,True),2)
     circularity=np.round(4*math.pi*area/perimeter**2,2)
     new_a,new_b,new_c,new_d =int(round(cX))+bordersize-patch_size,int(round(cX))+bordersize+patch_size,int(round(cY))+bordersize-patch_size,int(round(cY))+bordersize+patch_size
     
     new_patch=black_border_copy[new_c:new_d,new_a:new_b]     
     return cX,cY, area,perimeter,circularity, new_a,new_b,new_c,new_d, new_patch 
#################################################
def process_figure_8(im1,centre, frame_size, bordersize, patch_size):#separates figure into 2 cells and patches
    #if im1.shape==(96,96,3):
    if im1.shape==(2*patch_size,2*patch_size,3):    
             im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY) 
    im2, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    parameters=[]
    separated_cells=[]
   # print("len(contours) inside process_figure_8=", len(contours))
    for kkk  in range(len(contours)):	
        #img=np.zeros((96,96),dtype="uint8")
        img=np.zeros((2*patch_size,2*patch_size),dtype="uint8")
        cv2.drawContours(img, contours, kkk, 255, -1)
                
             
        cX,cY, area,perimeter,circularity, new_a,new_b,new_c,new_d, new_patch =recalculate_centre(img,(centre[0],centre[1]),frame_size, bordersize, patch_size)
        separated_cells.append(new_patch) 
        parameters.append(([cX,cY], area,perimeter,circularity, new_a,new_b,new_c,new_d ))    
    return separated_cells,parameters
#########################################################

def debug(cells):
  item=cells["cell_0"]
  name=item[11]
  centroid=item[6]
  daughter=item[16]
  int_number=item[17]
  print("name=", name)
  print("cemtroid=", centroid)
  print("daughter=", daughter)
  print("int_number=", int_number)
##################################################          
def update_dictionary_after_division(cut_patch,cells,curr_frame_cell_names,count,indicator,coords, frame_size, colour_dictionary,bordersize, patch_size,base_colours, colour_counter):      
    N_cells=len(cells)
    print("colour_dictionary=", colour_dictionary)
    print("count=", count)
    print("text=", curr_frame_cell_names)
    print("BEFORE UPDATING CELLS")
    #debug(cells)
    for kkk in range(N_cells):#correcting cells dictionary if division
    
           print("kkk=", kkk)
           if count[kkk]==2:
              im1=cut_patch
              immmg, cnts, hier = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
              print("len(contours) before process_figure_8=", len(cnts))           
              separated_cells,parameters=process_figure_8(im1,cells["cell_%s" % kkk][6], frame_size,bordersize, patch_size)
              print("len(separated_cells) after process figure_8=", len(separated_cells))                                         
              indicator+=1                                         
              cells["cell_%s" % kkk][3]=separated_cells[0]
              cells["cell_%s" % kkk][6]=parameters[0][0] 
              cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\separated_1.tif", cells["cell_%s" % kkk][3])
              print("centois of daughter-1=",  cells["cell_%s" % kkk][6])
              print("separated-centroids=",parameters[0][0])
              print("frame_number=", cells["cell_%s" % kkk][12])
              curr_frame_cell_names[kkk]+="0"
             
              print("text_daughter-1", curr_frame_cell_names[kkk])
              colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,[curr_frame_cell_names[kkk]],base_colours, colour_counter)
              print("colour_dictionary after daughter-1=",colour_dictionary)
              cells["cell_%s" % kkk][11]=curr_frame_cell_names[kkk]           
              cells["cell_%s" % kkk][15]=colour_dictionary[curr_frame_cell_names[kkk]]
              cells["cell_%s" % kkk][16]= "daughter-1"
              
              cells["cell_%s" % kkk][18]=parameters[0][1]#area 
              cells["cell_%s" % kkk][19]=parameters[0][2]#perimeter 
              cells["cell_%s" % kkk][20]=parameters[0][3]#circularity
              
              cells["cell_%s" % kkk][7]=parameters[0][4]#a 
              cells["cell_%s" % kkk][8]=parameters[0][5]#b 
              cells["cell_%s" % kkk][9]=parameters[0][6]#c
              cells["cell_%s" % kkk][10]=parameters[0][7]#d
                        
              print("color-1", colour_dictionary[curr_frame_cell_names[kkk]])
                       
              cellscopy=copy.deepcopy(cells)                               
              cells["cell_%s" % (N_cells)]=cellscopy["cell_%s" % kkk]
              print("N-cells before error=", N_cells)
              print("len(separated_cells before error)=", len(separated_cells))
              cells["cell_%s" % (N_cells)][3]=separated_cells[1]
              cells["cell_%s" % N_cells][6]=parameters[1][0] 
              #cells["cell_%s" % (N_cells)][6]=centroids[1]                                         
              curr_frame_cell_names.append(curr_frame_cell_names[kkk][:-1]+"1")
              print("text after creating daughter-2=", curr_frame_cell_names)
              
              cells["cell_%s" % (N_cells)][11]=curr_frame_cell_names[-1]
              colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,[curr_frame_cell_names[-1]],base_colours, colour_counter)
              cells["cell_%s" % N_cells][15]=colour_dictionary[curr_frame_cell_names[-1]]             
              cells["cell_%s" % N_cells][16]= "daughter-2"
              cells["cell_%s" % N_cells][17]= N_cells# was N_CELLS-1
              print("text_daughter-2", curr_frame_cell_names[-1])
              
              print("colour_dictionary after daughter-2=",colour_dictionary)
              print("color-2", colour_dictionary[curr_frame_cell_names[-1]])
              print("separated-2=",parameters[1][0])
              print("cwntroids-2=",  cells["cell_%s" % kkk][6])
              cells["cell_%s" % N_cells][18]=parameters[1][1]#area 
              cells["cell_%s" % N_cells][19]=parameters[1][2]#perimeter 
              cells["cell_%s" % N_cells][20]=parameters[1][3]#circularity
              
              cells["cell_%s" % N_cells][7]=parameters[1][4]#a 
              cells["cell_%s" % N_cells][8]=parameters[1][5]#b 
              cells["cell_%s" % N_cells][9]=parameters[1][6]#c
              cells["cell_%s" % N_cells][10]=parameters[1][7]#d
              cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\separated_2.tif",  cells["cell_%s" % (N_cells)][3]) 
              coords=np.concatenate((coords,np.array([cells["cell_%s" % (N_cells)][6][0],cells["cell_%s" % (N_cells)][6][1]]).reshape((1,2))) )             
              count[kkk]=0 
    N_cells=len(cells)
    print("AFTER UPDATING CELLS")
    #debug(cells)                                         
    return cells,curr_frame_cell_names,count,indicator,coords,colour_dictionary, colour_counter
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
"""
import pickle
import numpy as np
import os
def extract_lineage(outpath):
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")
    lineage = []
    with (open(lineage_path, "rb")) as openfile:
     while True:
        try:
            lineage.append(pickle.load(openfile))
        except EOFError:
            break    
    return lineage
x=extract_lineage("C:\\Users\\kfedorchuk\\Desktop\\DeepKymoTracker_fro_user\\OUTPUT_INPUT_MOVIE Pos0201")
"""