import cv2
import numpy as np
import copy
import math
#####################################
Bordersize=100
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
        print("len(contours) inside detect_figure_8_before=", len(cnts))
       
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
  print("len(contours) inside detect_figure_8_after=", len(cnts))
  return verdict,segmented_patch,im1# if no division, im1=segmented_patch, the cell is not cut
################ recalculate centres of daugher cells after division
def recalculate_centre(segmented_image,old_coords, frame_size):
     x0,y0=old_coords[0],old_coords[1]
     black=np.zeros((frame_size,frame_size),dtype="uint8")
     black_border=cv2.copyMakeBorder(black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
     a,b,c,d=int(round(x0))+Bordersize-48,int(round(x0))+Bordersize+48,int(round(y0))+Bordersize-48,int(round(y0))+Bordersize+48  
     black_border[c:d, a:b]=segmented_image
     black_again=black_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
     im2, contours, hierarchy = cv2.findContours(black_again,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)     
     c=contours[0]	
     M = cv2.moments(c)
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
     area=np.round(cv2.contourArea(c),2)
     perimeter=np.round(cv2.arcLength(c,True),2)
     circularity=np.round(4*math.pi*area/perimeter**2,2) 
     return cX,cY, area,perimeter,circularity
#################################################
def process_figure_8(im1,centre, frame_size):#separates figure into 2 cells and patches
    if im1.shape==(96,96,3):
             im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY) 
    im2, contours, hierarchy = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    parameters=[]
    separated_cells=[]
    print("len(contours) inside process_figure_8=", len(contours))
    for kkk  in range(len(contours)):	
        img=np.zeros((96,96),dtype="uint8")
        cv2.drawContours(img, contours, kkk, 255, -1)        
        separated_cells.append(img)       
        cX,cY, area,perimeter,circularity=recalculate_centre(img,(centre[0],centre[1]),frame_size)
        parameters.append(([cX,cY], area,perimeter,circularity))    
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
    
def update_dictionary_after_division(cut_patch,cells,text,count,indicator,coords, frame_size, colors):      
    N_cells=len(cells)
    print("N_cells=", N_cells)
    print("count=", count)
    print("BEFORE UPDATING CELLS")
    #debug(cells)
    for kkk in range(N_cells):#correcting cells dictionary if division
    
           print("kkk=", kkk)
           if count[kkk]==2:
              im1=cut_patch
              immmg, cnts, hier = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
              print("len(contours) before process_figure_8=", len(cnts))           
              separated_cells,parameters=process_figure_8(im1,cells["cell_%s" % kkk][6], frame_size)
              print("len(separated_cells) after process figure_8=", len(separated_cells))                                         
              indicator+=1                                         
              cells["cell_%s" % kkk][3]=separated_cells[0]
              cells["cell_%s" % kkk][6]=parameters[0][0] 
              cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\separated_1.tif", cells["cell_%s" % kkk][3])
              print("centois of daughter-1=",  cells["cell_%s" % kkk][6])
              print("separated-centroids=",parameters[0][0])
              print("frame_number=", cells["cell_%s" % kkk][12])
              text[kkk]+="0"
              print("text_daughter-1", text[kkk])
              cells["cell_%s" % kkk][11]=text[kkk]           
              cells["cell_%s" % kkk][15]=colors[text[kkk]]
              cells["cell_%s" % kkk][16]= "daughter-1"
              
              cells["cell_%s" % kkk][18]=parameters[0][1]#area 
              cells["cell_%s" % kkk][19]=parameters[0][2]#perimeter 
              cells["cell_%s" % kkk][20]=parameters[0][3]#circularity 
              print("color-1", colors[text[kkk]])
                       
              cellscopy=copy.deepcopy(cells)                               
              cells["cell_%s" % (N_cells)]=cellscopy["cell_%s" % kkk]
              print("N-cells before error=", N_cells)
              print("len(separated_cells before error)=", len(separated_cells))
              cells["cell_%s" % (N_cells)][3]=separated_cells[1]
              cells["cell_%s" % N_cells][6]=parameters[1][0] 
              #cells["cell_%s" % (N_cells)][6]=centroids[1]                                         
              text.append(text[kkk][:-1]+"1")
              print("text after creating daughter-2=", text)
              cells["cell_%s" % (N_cells)][11]=text[-1]             
              cells["cell_%s" % N_cells][15]=colors[text[-1]]             
              cells["cell_%s" % N_cells][16]= "daughter-2"
              cells["cell_%s" % N_cells][17]= N_cells# was N_CELLS-1
              print("text_daughter-2", text[-1])
              print("color-2", colors[text[-1]])
              print("separated-2=",parameters[1][0])
              print("cwntroids-2=",  cells["cell_%s" % kkk][6])
              cells["cell_%s" % N_cells][18]=parameters[1][1]#area 
              cells["cell_%s" % N_cells][19]=parameters[1][2]#perimeter 
              cells["cell_%s" % N_cells][20]=parameters[1][3]#circularity 
              cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\separated_2.tif",  cells["cell_%s" % (N_cells)][3]) 
              coords=np.concatenate((coords,np.array([cells["cell_%s" % (N_cells)][6][0],cells["cell_%s" % (N_cells)][6][1]]).reshape((1,2))) )             
              count[kkk]=0 
    N_cells=len(cells)
    print("AFTER UPDATING CELLS")
    #debug(cells)                                         
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