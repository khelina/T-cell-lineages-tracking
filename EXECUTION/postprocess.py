import numpy as np
import os
import cv2
#########################################################################
os.chdir("C:\\Users\\kfedorchuk\\Documents\\EXECUTE")
########################################################################################
Bordersize=int(96/2)+5+6
Size=96.0
########################################################################################
def create_sum_for_occlusion(first,second):#global coords    
    black1=np.zeros((382+2*Bordersize,382+2*Bordersize))          
    black1[first[9]:first[10],first[7]:first[8]]=first[3]
    black2=np.zeros((382+2*Bordersize,382+2*Bordersize))          
    black2[second[9]:second[10],second[7]:second[8]]=second[3]      
    summ=black1+black2
    summ=summ[Bordersize:382+Bordersize,Bordersize:382+Bordersize]   
    return summ# size 382x382
#########################################################################################
def detect_occlusion(first,second): # in 382x382 image         
     black1=np.zeros((382+2*Bordersize,382+2*Bordersize))          
     black1[first[9]:first[10],first[7]:first[8]]=first[3]
     black2=np.zeros((382+2*Bordersize,382+2*Bordersize))          
     black2[second[9]:second[10],second[7]:second[8]]=second[3]
     if np.all((black1/255+black2/255)<=1)==False:
         verdict="occlusion"
     else:
         verdict="no occlusions"
     return verdict
################################################################
def cut_into_two(im,x1,y1,x2,y2): 
  x00,y00=(x1+x2)/2,(y1+y2)/2
  k=(x1-x2)/(y2-y1)
  b=y00-k*x00
  y0=b
  y382=382*k+b
  x0=-b/k
  x382=(382-b)/k
  p=[(0,y0),(382,y382),(x0,0),(x382,382)]
  points=[p[i] for i in range(4) if (0<=p[i][0]<=382 and 0<=p[i][1]<=382)==True]
  im = cv2.line(im, (int(round(points[0][0])),int(round(points[0][1]))),(int(round(points[1][0])),int(round(points[1][1]))) ,(0,0,0), 2)
  im=im.astype("uint8")
  im1, contours, hierarchy = cv2.findContours(im,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)       
  conts=[]
  areas=[]
  for cnt in contours:
          conts.append(cnt)
          areas.append(cv2.contourArea(cnt))
  w=list(zip(areas,conts))
  ww=sorted(w,key=lambda student:student[0])
  ress = list(zip(*ww))
  contours_sorted=[ress[1][-1],ress[1][-2]]
  im=np.zeros((382,382,3),np.uint8)
  cv2.drawContours(im, contours_sorted, -1, (0,0,255), -1)
  im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
  im[im!=0]=255          
  return im# this is 382x382 image with separated 2 cells
 ##############################################
def associate(im_cut,x1,y1,x2,y2):# returns 2 cleaned patches with separated cells    
     im, contours, hierarchy = cv2.findContours(im_cut,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)        
     centroids=[]
     to_first=[]
     to_second=[]  
     for cnt in contours:      
       M = cv2.moments(cnt)    
       cX = int(M["m10"] / M["m00"])
       cY = int(M["m01"] / M["m00"])
       centroids.append([cX,cY])
       d1=(cX-x1)**2+(cY-y1)**2
       d2=(cX-x2)**2+(cY-y2)**2
       to_first.append(d1)
       to_second.append(d2)     
     w=list(zip(to_first,contours))
     ww=sorted(w,key=lambda student:student[0])
     ress = list(zip(*ww))      
     s=list(zip(to_second,contours))
     ss=sorted(s,key=lambda student:student[0])
     rezz = list(zip(*ss))     
     contours_sorted=[ress[1][0],rezz[1][0]]          
     first_im=np.zeros((im_cut.shape),dtype="uint8")
     cv2.drawContours(first_im, [contours_sorted[0]], 0, 255, -1)    
     first_im=cv2.copyMakeBorder(first_im, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT,value = 0)
     x1,x2,y1,y2=int(round(x1)),int(round(x2)),int(round(y1)),int(round(y2))
     first_patch=first_im[y1-48+Bordersize:y1+48+Bordersize,x1-48+Bordersize:x1+48+Bordersize]   
     second_im=np.zeros((im_cut.shape),dtype="uint8")
     cv2.drawContours(second_im, [contours_sorted[1]], 0, 255, -1)    
     second_im=cv2.copyMakeBorder(second_im, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT,value = 0)
     second_patch=second_im[y2-48+Bordersize:y2+48+Bordersize,x2-48+Bordersize:x2+48+Bordersize]    
     return first_patch,second_patch 
################################################
def change_dictionary_after_cleaning(dictt,k,sum_clean,centroid):
    x=dictt["cell_%s" % k]
    a,b,c,d=x[7],x[8],x[9],x[10]
    x0,x1,x2=x[0],x[1],x[2]  
    x3=sum_clean
    x4,x5=x[4],x[5]   
    x6=centroid
    del x
    dictt["cell_%s" % k]=[x0,x1,x2,x3,x4,x5,x6,a,b,c,d]
    return dictt
############################################################
def Cleaner_2(cells):# if these are 2 separate cells Cleaner-2       
 for p in range(len(cells)-1):
        first=cells["cell_%s" % p]       
        for pp in range(p+1, len(cells)):
             second=cells["cell_%s" % pp]            
             verdict=detect_occlusion(first,second)
             if verdict=="occlusion":
                 print("occlusion detected for cells", p, pp)
                 x11,y11,x22,y22=first[6][0],first[6][1],second[6][0],second[6][1]
                 summ=create_sum_for_occlusion(first,second)
                 im_cut=cut_into_two(summ,x11,y11,x22,y22)                
                 first_patch,second_patch=associate(im_cut,x11,y11,x22,y22)
                 cells=change_dictionary_after_cleaning(cells,p,first_patch,[x11,y11])
                 cells=change_dictionary_after_cleaning(cells,pp,second_patch,[x22,y22]) 
 return cells
################################################################################
def find_areas_ratio(output_from_watershed): # output=RGB or grey   
    output=output_from_watershed.astype("uint8")
    im2,contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area_1=cv2.contourArea(contours[0])
    area_2=cv2.contourArea(contours[1])
    if area_1>area_2:
        ratio=area_1/area_2
    else:
        ratio=area_2/area_1     
    return ratio 
####################################################
def IoU(image_1, image_2): # both images are binary 0,255   
   img11=image_1/255 
   img22=image_2/255
   img=img11+img22
   intersection=np.sum(img[img==2.0])
   union=np.sum(img[img>0.0])
   iou=intersection/union  
   return iou
#########################################################
def Cleaner_1(output,art_frame):# leaves one (or 2 daughter cells) in the centre of 96x96 output from segmentation ensemble   
  im2, contours, hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                  
  if len(contours)==1:
      img=output
  else:
     ious=[]
     areas=[]
     contours_separated=[]
     patches_separated=[]
     for cnt in contours:
       one=np.zeros((96,96),dtype="uint8")
       one=cv2.drawContours(one,[cnt],0,255, -1)    
       iou= IoU(one,art_frame)
       area=cv2.contourArea(cnt)
       ious.append(iou)
       areas.append(area)
       contours_separated.append(cnt)
       patches_separated.append(one) 
     w=list(zip(ious,contours_separated,areas))
     ww=sorted(w,key=lambda student:student[0])
     ress = list(zip(*ww))        
     img=np.zeros((output.shape),dtype="uint8") 
     cv2.drawContours(img,[ress[1][-1]] , 0, 255, -1)
     if ress[2][-2]!=0.0:     
      if ress[2][-1]/ress[2][-2]<1.3:
          cv2.drawContours(img,[ress[1][-2]] , 0, 255, -1)
  return img
#######################################################
