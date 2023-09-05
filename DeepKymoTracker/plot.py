import cv2
import numpy as np
import os
import math
Bordersize=100


def create_color_dictionary(max_number_of_cells, N_cells):# parameter is the number of cells in frame 1  
  base_colors=[[255,0,0,255],#blue
        [0,255,255,255],#yellow
        [0,255,127,255],#spring green
        [0,0,255,255],#red
        [238,130,238,255],#violet       
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
  for k in range(n):
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
def paste_patch(destination,patch,a,b,c,d,color,alpha):   
    patch=patch.astype(np.uint8)          
    mask=patch.copy()  
    patch=cv2.cvtColor(patch, cv2.COLOR_GRAY2RGBA) 
    patch[mask==255]=color   
    alpha_patch = patch[:, :, 3]/255.0
    alpha_patch[mask==255]=alpha
    alpha_patch[mask!=255]=0.0
    alpha_dest = 1.0 - alpha_patch    
    for k in range(0, 3):
       destination[c:d, a:b, k] = (alpha_patch * patch[:, :, k] +alpha_dest * destination[c:d, a:b, k])      
    return destination
##########################################################################
def plot_frame(texts,cells,clip_centr,k,kk,raw_images,names,out_folders,coords, coords_old, colors):
       #print("coords_inside_plot before=", coords)
       destin_black=np.zeros((382,382),dtype="uint8")
       destin=raw_images[k+kk]      
       destin1=destin.copy()
       destin1_border=cv2.copyMakeBorder(destin1, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )     
       destin1_border = cv2.cvtColor(destin1_border,cv2.COLOR_GRAY2RGBA)
       fluor_1=destin1_border.copy()
       destin_black_border=cv2.copyMakeBorder(destin_black, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_REPLICATE )
       destin1_black_border = cv2.cvtColor(destin_black_border,cv2.COLOR_GRAY2RGBA)        
       coords=np.zeros((len(cells),2))
       segmented_patches_previous=[]      
       for kkk in range(len(cells)):       
         cv2.imwrite(os.path.join(out_folders[2],"segmentor_output_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][0])
         cv2.imwrite(os.path.join(out_folders[6],"refiber_output_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][1])
         cv2.imwrite(os.path.join(out_folders[7],"ensemble_output_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][2])
         cv2.imwrite(os.path.join(out_folders[8],"cleaned_output_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][3])         
         output_init_size=cells["cell_%s" % kkk][3]
         patch_with_contours=prepare_contours(output_init_size)
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]        
         #result_cartoon=paste_patch(destin1_black_border,output_init_size,a,b,c,d,Colors[kkk],1.0)        
         #result_with_contours=paste_patch(fluor_1,patch_with_contours,a,b,c,d,Colors[kkk],1.0)
         result_cartoon=paste_patch(destin1_black_border,output_init_size,a,b,c,d,colors[texts[kkk]],1.0)        
         result_with_contours=paste_patch(fluor_1,patch_with_contours,a,b,c,d,colors[texts[kkk]],1.0)
         
         xx,yy=cells["cell_%s" % kkk][6][0]+Bordersize,cells["cell_%s" % kkk][6][1]+Bordersize
         texxt=cells["cell_%s" % kkk][11]
         cv2.putText(result_with_contours,texxt,(int(xx)-10,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,1,colors[texxt],1)          
         #cv2.putText(result_with_contours,texts[kkk],(int(xx)-10,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,1,colors[texts[kkk]],1)  
         coords[kkk,0]=cells["cell_%s" % kkk][6][0]
         coords[kkk,1]=cells["cell_%s" % kkk][6][1]
         segmented_patches_previous.append([cells["cell_%s" % kkk][3],a,b,c,d])       
       cartoon_cropped=result_cartoon[Bordersize:382+Bordersize,Bordersize:382+Bordersize]             
       patch_binary=cv2.cvtColor(cartoon_cropped, cv2.COLOR_BGR2GRAY)
       patch_binary[patch_binary!=0]=255
     
       result_with_contours_cropped=result_with_contours[Bordersize:382+Bordersize,Bordersize:382+Bordersize]
       #print("coords_old=", coords_old)
       #for ii in range(len(coords_old)):# this is for debugging only
         #centre=(int(coords_old[ii][0]),int(coords_old[ii][1]))
         #centre_new=(int(coords[ii][0]),int(coords[ii][1]))
         #track_result=(int(clip_centr[kk][ii][0]),int(clip_centr[kk][ii][1]))
         #result_with_contours_cropped = cv2.circle(result_with_contours_cropped, centre, 5, (0,0,255,255), -1)
         #result_with_contours_cropped = cv2.circle(result_with_contours_cropped,track_result , 5, (255,0,0,255), -1)
         #result_with_contours_cropped = cv2.circle(result_with_contours_cropped, centre_new, 5, (0,255,0,255), -1)
       cv2.imwrite(rename_file(out_folders[3],names[k+kk]),result_with_contours_cropped)
       print("segmented frame number", k+kk)
       return  coords     

"""
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
 """
