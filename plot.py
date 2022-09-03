import cv2
import numpy as np
import os
from functions import rename_segmented,rename_file
Bordersize=int(96/2)+5+6
Colors=[[0,0,255,255],[0,128,255,255],[0,255,0,255],[255,0,0,255]]

############################################################################
def prepare_contours(input_image):# input_image must be gray. binary 0,255
    im2,contours, hierarchy = cv2.findContours(input_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    empty=np.zeros((96,96,3),np.uint8)
    cv2.drawContours(empty, contours, -1, (0,0,255), 1)
    empty = cv2.cvtColor(empty,cv2.COLOR_BGR2GRAY)
    empty[empty!=0]=255
    return empty
##########################################################
def prepare_patch(input_image):# input_image must be gray. binary 0,255
    im2,contours, hierarchy = cv2.findContours(input_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    empty=np.zeros((96,96,3),np.uint8)
    cv2.drawContours(empty, contours, -1, (0,0,255), -1)
    empty = cv2.cvtColor(empty,cv2.COLOR_BGR2GRAY)
    empty[empty!=0]=255
    return empty
###################################################################################
def paste(destin_image,patch,a,b,c,d,color,alpha):              
    mask=patch.copy()
    patch=cv2.cvtColor(patch, cv2.COLOR_GRAY2RGBA) 
    patch[mask==255]=color
    alpha_cell = patch[:, :, 3]/255.0
    alpha_cell[mask==255]=alpha
    alpha_cell[mask!=255]=0.0
    alpha_back = 1.0 - alpha_cell    
    for k in range(0, 3):
       destin_image[c:d, a:b, k] = (alpha_cell * patch[:, :, k] +alpha_back * destin_image[c:d, a:b, k])      
    return destin_image
#########################################################################
def paste_binary(patch,a,b,c,d,intensity):
    destin_image= np.zeros((382+2*Bordersize,382+2*Bordersize),dtype="uint8")   
    patch[patch==255]=intensity
    destin_image[c:d,a:b]=patch
    return destin_image
##########################################
def plot_frame(texts,cells,clip_centr,k,kk,fluor_images,destinations,names,p):   
       destin_black=np.zeros((382+2*Bordersize,382+2*Bordersize),dtype="uint8")
       destin_color_black = cv2.cvtColor(destin_black.copy(),cv2.COLOR_GRAY2RGBA) 
       fluor=fluor_images[k+kk]
       destin_fluor_contours=cv2.copyMakeBorder(fluor.copy(), top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
       destin_fluor_contours=cv2.cvtColor(destin_fluor_contours,cv2.COLOR_GRAY2RGBA)                   
       coords=np.zeros((len(cells),2))
       for kkk in range(len(cells)):       
         cv2.imwrite(os.path.join(destinations[2],"output_segmentor_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][0])
         cv2.imwrite(os.path.join(destinations[6],"output_refiner_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][1])
         cv2.imwrite(os.path.join(destinations[7],"output_ensemble_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][2])
         cv2.imwrite(os.path.join(destinations[8],"output_after_cleaning_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][3])         
         patch_segmented=prepare_patch(cells["cell_%s" % kkk][3])
         patch_with_contours=prepare_contours(cells["cell_%s" % kkk][3])
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]        
         result_cartoon=paste(destin_color_black,patch_segmented,a,b,c,d,Colors[kkk],1.0)        
         result_with_contours=paste(destin_fluor_contours,patch_with_contours,a,b,c,d,Colors[kkk],1.0)
         xx,yy=cells["cell_%s" % kkk][6][0]+Bordersize,cells["cell_%s" % kkk][6][1]+Bordersize
         cv2.putText(result_with_contours,texts[kkk],(int(xx)-10,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,1,Colors[kkk],1)        
         coords[kkk,0]=cells["cell_%s" % kkk][6][0]
         coords[kkk,1]=cells["cell_%s" % kkk][6][1]         
       cartoon_cropped=result_cartoon[Bordersize:382+Bordersize,Bordersize:382+Bordersize]       
       cv2.imwrite(rename_file(destinations[1],names[k+kk]),cartoon_cropped)# color_cartoon plot             
       cartoon_binary=cv2.cvtColor(cartoon_cropped, cv2.COLOR_BGRA2GRAY)
       cartoon_binary[cartoon_binary!=0]=255
       cv2.imwrite(rename_segmented(destinations[4],names[k+kk]),cartoon_binary)           
       result_with_contours_cropped=result_with_contours[Bordersize:382+Bordersize,Bordersize:382+Bordersize]
       cv2.imwrite(rename_file(destinations[3],names[k+kk]),result_with_contours_cropped)
       print("plotted segmented frame number", k+kk)                    
       return coords
#####################################################################################
