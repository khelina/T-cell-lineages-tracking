import cv2
import numpy as np
import os
import math
#############################
Bordersize=100
######################################
def create_color_dictionary(max_number_of_cells, N_cells): 
  base_colors=[[238,238,0,255],#cyan
        [0,255,255,255],#yellow
        [0,255,127,255],#spring green
        [0,0,255,255],#red       
        [255,0,0,255],#blue
        [255,245,0,255],#turqoise
        [255,0,255,255],#magenta
        [255,191,0,255],#deep sky blue
        [235,111,131,255],#dark violet
        [71,99,255,255],#tomato
        [255,187,255,255],#plum
        [0,140,255,255],#orange
        [255,255,0,255],#aqua
        [147,20,255,255],#deep pink
        [238,238,0,255]]#cyan  
    
  n= int(math.log(max_number_of_cells,2)) +1
  if N_cells==1:
    final_list =["1"]
  else:
     import string
     list_of_letters=list(string.ascii_lowercase)
     if N_cells>26:
         copy_list=list_of_letters.copy()
         additional=[copy_list[i]+copy_list[i] for i in range(len(copy_list))]            
         list_of_letters+=additional 
     final_list=list_of_letters[:N_cells]
  temp_list=final_list
  for k in range(n):# was n
    new_list=[]
    for item in temp_list:     
      a=item+"0"
      b=item+"1"      
      new_list =new_list+[a,b]
    temp_list =new_list   
    final_list=final_list+new_list
  
  m=len(final_list)//len(base_colors)+1
  base_colours=base_colors*m
  colours ={}
  for i in range(len(final_list)):
      colours[final_list[i]]=base_colours[i]
  print("ready for execution")    
  return colours, final_list
############################################################## 
def rename_file(destin,infile):       
 infile = os.path.normpath(infile) 
 old=infile.split(os.sep)
 new1=old[-1]
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
############################################################################
def prepare_contours(input_image):# input_image must be gray. binary 0,255
    input_image = input_image.astype('uint8')
    im2,contours, hierarchy = cv2.findContours(input_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    empty=np.zeros((input_image.shape[0],input_image.shape[0],3),np.uint8)
    cv2.drawContours(empty, contours, -1, (0,0,255), 1)
    empty = cv2.cvtColor(empty,cv2.COLOR_BGR2GRAY)
    empty[empty!=0]=255
    return empty
#############################################################
def paste_patch(destin_image,patch,a,b,c,d,color,alpha, frame_size):
    destin_image_border=cv2.copyMakeBorder(destin_image, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE ) 
    patch=patch.astype(np.uint8)          
    mask=patch.copy()  
    patch=cv2.cvtColor(patch, cv2.COLOR_GRAY2RGBA) 
    patch[mask==255]=color   
    alpha_patch = patch[:, :, 3]/255.0
    alpha_patch[mask==255]=alpha
    alpha_patch[mask!=255]=0.0
    alpha_dest = 1.0 - alpha_patch    
    for k in range(0, 3):
       destin_image_border[c:d, a:b, k] = (alpha_patch * patch[:, :, k] +alpha_dest * destin_image_border[c:d, a:b, k])
    destin_image_cropped=destin_image_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
    return destin_image_cropped
##########################################################################
def paste_benchmark_patch(patch,a,b,c,d,cell_number, frame_size):    
    image_with_one_cell_border=np.zeros((frame_size+2*Bordersize,frame_size+2*Bordersize),dtype="uint16")     
    patch=patch.astype(np.uint16)          
    mask=patch.copy()     
    patch[mask==255]=cell_number+1            
    image_with_one_cell_border[c:d, a:b] = patch
    final_image=image_with_one_cell_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]     
    return final_image
#######################################################
def plot_frame(cells,clip_centr,k,kk,fluor_images,names,out_folders,coords, coords_old, bright_images, bright_names, frame_size):      
       destin_benchmark=np.zeros((frame_size,frame_size),dtype="uint16")       
       destin_fluor=fluor_images[kk]      
       destin_bright=bright_images[kk]
       destin_fluor = cv2.cvtColor(destin_fluor,cv2.COLOR_GRAY2RGBA)    
       destin_bright = cv2.cvtColor(destin_bright,cv2.COLOR_GRAY2RGBA)
        
       coords=np.zeros((len(cells),2))           
       for kkk in range(len(cells)):               
         cv2.imwrite(os.path.join(out_folders[4],"cleaned_output_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][3])# was [9]         
         output_init_size=cells["cell_%s" % kkk][3]
         patch_with_contours=prepare_contours(output_init_size)
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]        
         
         collour=cells["cell_%s" % kkk][15]
         destin_bright=paste_patch(destin_bright,patch_with_contours,a,b,c,d,collour,1.0, frame_size)        
         destin_fluor=paste_patch(destin_fluor,patch_with_contours,a,b,c,d,collour,1.0, frame_size)
        
         one_cell_benchmark =paste_benchmark_patch(output_init_size,a,b,c,d,kkk, frame_size)
         destin_benchmark+= one_cell_benchmark
         xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         texxt=cells["cell_%s" % kkk][11]
       
         cv2.putText(destin_fluor,texxt,(int(xx)-10,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,1,collour,1) 
         cv2.putText(destin_bright,texxt,(int(xx)-10,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,1,collour,1)         
                  
         coords[kkk,0],coords[kkk,1]=xx, yy
              
       cv2.imwrite(rename_file(out_folders[2],names[kk]),destin_fluor)#was [3]
       cv2.imwrite(rename_file(out_folders[5],bright_names[kk]),destin_bright)# was [9]
       black_and_white=destin_benchmark.copy()
     
       black_and_white=black_and_white.astype(np.uint8)
       black_and_white[destin_benchmark!=0]=255
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),destin_cartoon)
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),black_and_white)
       behchmark_seg ="mask"+str(str(k+kk).zfill(3))+".tif"      
       cv2.imwrite(os.path.join(out_folders[0], behchmark_seg),destin_benchmark)
       return  coords, destin_fluor     
