import cv2
import numpy as np
import os
import math
from copy import deepcopy
#############################
Bordersize=100
######################################
#### This function assigns a colour to new cells ( from base_colours list)
###### and adds new cells to colour_dictionary
def update_color_dictionary(colour_dictionary,new_cell_names,base_colours, colour_counter):    
    for k in range(len(new_cell_names)):
        colour_counter+=1
        #print("count=", colour_counter)
        cell_name =new_cell_names[k]
        if colour_counter <len(base_colours):
            colour_dictionary[cell_name]=base_colours[colour_counter-1]
        else:
            colour_dictionary[cell_name]=base_colours[colour_counter-1-len(base_colours)]
    return colour_dictionary, colour_counter
######################################
### This function is for dealing with new cells - they need naive names": "a", "b", "c", ....
def update_naive_names_list(unused_naive_names, n):# n = number of new (added) naive cells
    new_naive_names=[]
    for k in range(n):
        letter=unused_naive_names[0]
        new_naive_names.append(letter)
        unused_naive_names.remove(letter)
    return new_naive_names, unused_naive_names
################# when adding new cell
def update_xs(xs,new_names, num_frames,  lineage_image_size,number_of_added_new_cells):
       print("I am inside update_xs")
       for ii in range(len(new_names)):
          new_name=new_names[ii]
          print("new_name=", new_name)
          xs[new_name]=num_frames+20*(ii+1+number_of_added_new_cells)         
          #previous_lineage_image=np.concatenate((previous_lineage_image,np.zeros((lineage_image_size,40,3), dtype=previous_lineage_image.dtype)), axis=1)
       return xs
###################################
def create_first_color_dictionary(max_number_of_cells, init_number_of_cells, num_frames): 
  base_colours=[[238,238,0,255],#cyan 1
        [0,255,255,255],#yellow 10
        [0,255,127,255],#spring green 11
        [0,0,255,255],#red 100      
        [255,0,0,255],#blue 101
        [255,245,0,255],#turqoise 110
        [255,0,255,255],#magenta 111
        [255,191,0,255],#deep sky blue
        [235,111,131,255],#dark violet
        [71,99,255,255],#tomato
        [255,187,255,255],#plum
        [0,140,255,255],#orange
        [255,255,0,255],#aqua
        [147,20,255,255],#deep pink
        [239,238,0,255],#cyan
        [240,238,0,255],#cyan 1
        [0,255,254,255],#yellow 10
        [0,255,128,255]]#spring green 11
    
  n= int(math.log(max_number_of_cells,2)) +1
    
  import string
  unused_naive_names=list(string.ascii_lowercase)
  if max_number_of_cells>26:# if number of letters is bigger than English alphabet, then copy beginning from number 27
         copy_list=unused_naive_names.copy()
         additional=[copy_list[i]+copy_list[i] for i in range(len(copy_list))]            
         unused_naive_names+=additional
  if init_number_of_cells==1:
      new_naive_names=["1"]
     
  else:
      new_naive_names,unused_naive_names= update_naive_names_list(unused_naive_names,init_number_of_cells)
  ######################################
  
  ########################################
  colour_dictionary, colour_counter ={},0
  colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)
  xs=create_first_dictionary_of_xs(new_naive_names, num_frames,max_number_of_cells)    
  #print("ready for execution")
  #print("final_list", final_list)
  
  return colour_dictionary, new_naive_names, base_colours, colour_counter, unused_naive_names, xs
#######################################


#############################
def create_first_dictionary_of_xs(new_naive_names,num_frames,observed_max_number_of_cells):
  #n= int(math.log(max_number_of_cells,2)) +1
  #n=max_number_of_cells-len(new_naive_names)
  ### this is for one cell
  m=len(new_naive_names)
  kk=-2# kk=max number of potential divisions
  while True:
    kk+=1
    if (2**(kk-1))*m<observed_max_number_of_cells<=(2**kk)*m:
        number_of_potential_divisions=kk
        break
  #print("number_of_potential_divisions=", number_of_potential_divisions)
  ## n = final max number of potential divisions
  
  potential_max_number_of_cells=(2**kk)*m
  max_number_of_cells_in_one_unit=2**kk
  #print("potential_max_number_of_cells=", potential_max_number_of_cells)
  #print("actual_max_number_of_cells=", actual_max_number_of_cells)
  number_of_deltas_in_one_unit=(2**kk-1)*2
  #print("number_of_deltas_in_one_unit=", number_of_deltas_in_one_unit)
  total_number_of_deltas=m* number_of_deltas_in_one_unit+m+1
  
  #print("total_number_of_deltas=", total_number_of_deltas)
  #number_of_deltas_per_unit=int(number_of_deltas/m)
  #print("number_of_deltas_per_unit=", number_of_deltas_per_unit)
  delta=int(num_frames/total_number_of_deltas)
  #print("delta=", delta)
  ##############################
  first_m=-int(number_of_deltas_in_one_unit/2)*delta 
  #print("first_m=", first_m)
  step_size_for_m=(number_of_deltas_in_one_unit+1)*delta
  #print("step_size_for_m=", step_size_for_m)
  #############################
  all_cell_names=new_naive_names
  temp_list=all_cell_names
  for k in range(number_of_potential_divisions):# was n
    daughters=[]
    for item in temp_list:     
      a=item+"0"
      b=item+"1"      
      daughters =daughters+[a,b]
    temp_list =daughters   
    all_cell_names=all_cell_names+temp_list
   
  #print("all_cell_names=", all_cell_names)
  #######################################    
    
  numbers =[len(item) for item in all_cell_names]
  max_name_length =max(numbers)
  #print("max_name_length=", max_name_length)  
  xs={}
  
  for i in range(len(new_naive_names)):
        xs[new_naive_names[i]]=first_m+step_size_for_m*(i+1) 
  #print("xs for new_naive_names_only", xs)
        #xs[new_naive_names[i]]=int((num_frames/(len(new_naive_names)+1))*(i+1))
  for k in range(len(all_cell_names)):# creates x-coordinates for all possible daughters                                # based on max_number_of_cells in the movie
       cell_name =all_cell_names[k]        
       kkk=len(cell_name)
       if kkk<max_name_length:         
         item_1=xs[cell_name]-delta*(2**(kk-kkk))
         item_2=xs[cell_name]+delta*(2**(kk-kkk))   
         xs[cell_name+"0"]=int(item_1)
         xs[cell_name+"1"]=int(item_2)              
  return xs
 

####### xs contains x-coordinates for each cell (for plotting dynamic lineage)
# It is created based on cell names in Frame 1 (see function def_Close_popup)
# template = new_cell_names (naive) in Frame 1
def create_first_dictionary_of_xs_old( new_naive_names, num_frames,max_number_of_cells):    

  n= int(math.log(max_number_of_cells,2)) +1
  daughters_list=[]
  for k in range(n):# creates final_list - names of all possible daughters of initial cells
 
    for item in new_naive_names:     
      a=item+"0"
      b=item+"1"      
      daughters_list =daughters_list+[a,b]
  all_names_list =new_naive_names+daughters_list   
  first_text=new_naive_names_  
  name_lengths =[len(item) for item in new_naive_names]
  max_name_length =max(name_lengths)
  if len(new_naive_names)==1:# if there is only one cell in Frame 1
    xs ={"1":int(num_frames/2)}
  else:# of there are >1 cells in Frame 1 
    xs={}
    for i  in range(len(new_naive_names)):
        xs[new_naive_names[i]]=int((num_frames/(len(new_naive_names)+1))*(i+1))
  
  for k in range(len(new_naive_names)):# creates x-coordinates for all possible daughters
                                # based on max_number_of_cells in the movie
       cell_name =new_naive_names[k]        
       kk=len(cell_name)
       if kk<max_name_length:
         item_1=xs[cell_name]-num_frames/(2**(kk+1))
         item_2=xs[cell_name]+num_frames/(2**(kk+1))            
         xs[cell_name+"0"]=int(item_1)
         xs[cell_name+"1"]=int(item_2)              
  return xs
##################################
#### This function assigns colours to cells in Frame 1
def create_first_color_dictionary_wrong(max_number_of_cells, N_cells, colour_counter): 
  base_colours=[[238,238,0,255],#cyan 1
        [0,255,255,255],#yellow 10
        [0,255,127,255],#spring green 11
        [0,0,255,255],#red 100      
        [255,0,0,255],#blue 101
        [255,245,0,255],#turqoise 110
        [255,0,255,255],#magenta 111
        [255,191,0,255],#deep sky blue
        [235,111,131,255],#dark violet
        [71,99,255,255],#tomato
        [255,187,255,255],#plum
        [0,140,255,255],#orange
        [255,255,0,255],#aqua
        [147,20,255,255],#deep pink
        [238,238,0,255]]#cyan  
    
  n= int(math.log(max_number_of_cells,2)) +1
    
  import string
  unused_naive_names=list(string.ascii_lowercase)
  if max_number_of_cells>26:# if number of letters is bigger than English alphabet, then copy beginning from number 27
         copy_list=unused_naive_names.copy()
         additional=[copy_list[i]+copy_list[i] for i in range(len(copy_list))]            
         unused_naive_names+=additional
  if N_cells==1:
      new_naive_names=["1"]
     
  else:
      new_naive_names,unused_naive_names= update_naive_names_list(unused_naive_names, N_cells) 
  colour_dictionary ={}
  colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)    
  #print("ready for execution")
  #print("final_list", final_list)  
  return colour_dictionary, new_naive_names, base_colours, colour_counter, unused_naive_names
##############################################################

##########################################################
#import os
#infile=r"C:\Users\helina\Desktop\tracking new_alessandra\INPUT_MOVIE s30\5_w1BF_s30_t10_ch02.tif"
#destin=r"C:\Users\helina\Desktop\tracking new_alessandra\OUTPUT_INPUT_MOVIE s30\MASKS"
def rename_file(destin,infile):# for bright or fluor images       
 infile = os.path.normpath(infile) 
 old =infile.split(os.sep)
 new1 =old[-1]
 
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
#############################
def create_name_for_mask(bright_name):
    bright_name = os.path.normpath(bright_name) 
    old =bright_name.split(os.sep)# creates a list of strings which are usually separated by \
    new1 =old[-1]
    mask_name =new1[:-8]+"mask.tif" 
    return mask_name
######################################
def create_name_for_cleaned_patch(full_bright_name, kkk):
    full_bright_name = os.path.normpath(full_bright_name) 
    all_list =full_bright_name.split(os.sep)# creates a list of strings which are usually separated by \
    base_bright_name =all_list[-1]
    index_t=base_bright_name.find("_t")
    section_1 =base_bright_name[:index_t+1]
    section_1_new =section_1+"cell_%s_" % (kkk)
    section_2 = base_bright_name[index_t+1:-8]
    section_2_new=section_2+"patch.tif"
    patch_name=section_1_new+section_2_new       
    return patch_name
###########################
def create_name_for_lineage_image(bright_name):
    bright_name = os.path.normpath(bright_name) 
    old =bright_name.split(os.sep)# creates a list of strings which are usually separated by \
    new1 =old[-1]
    lineage_name =new1[:-8]+"tree.tif" 
    return lineage_name
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
    destin_image_border=cv2.copyMakeBorder(destin_image, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize,  borderType= cv2.BORDER_CONSTANT, value = float(np.mean(destin_image)) )
    debug_destin_image =destin_image_border.copy()
    debug_destin_image= cv2.cvtColor(debug_destin_image,cv2.COLOR_BGRA2GRAY)   
     #borderType= cv2.BORDER_CONSTANT, value = float(np.min(empty_fluor))
    patch=patch.astype(np.uint8)
    debug_patch=deepcopy(patch)
    debug_destin_image[c:d, a:b] = debug_patch      
    mask=patch.copy()  
    patch=cv2.cvtColor(patch, cv2.COLOR_GRAY2RGBA) 
    patch[mask==255]=color 

    alpha_patch = patch[:, :, 3]/255.0
    alpha_patch[mask==255]=alpha
    alpha_patch[mask!=255]=0.0
    alpha_dest = 1.0 - alpha_patch    
    for k in range(0, 3):
       destin_image_border[c:d, a:b, k] = (alpha_patch * patch[:, :, k] +alpha_dest * destin_image_border[c:d, a:b, k])
    ######### this rectangle is for debugging
    #a_old,b_old,c_old,d_old=olds[kkk][0],olds[kkk][1],olds[kkk][2],olds[kkk][3]
    #destin_image_border = cv2.rectangle(destin_image_border, (b_old,d_old), (a_old,c_old), color[:-1], 1)
    ##############################################
    
    destin_image_cropped=destin_image_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
    #cv2.putText(destin_image_cropped,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,color,1) 
    #cv2.putText(destin_bright,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)         
    #cv2.putText(destin_red,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
    return destin_image_cropped,  debug_destin_image
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
def plot_frame(cells,clip_centr,k,kk,fluor_images,fluor_names,out_folders,coords, coords_old, bright_images, bright_names, frame_size, n_digits, first_frame_number, contrast_value, current_lineage_image, p_size,red_images, red_names):      
       destin_mask=np.zeros((frame_size,frame_size),dtype="uint16")       
       destin_fluor=fluor_images[kk]
       destin_bright=bright_images[kk]
       destin_red=red_images[kk]
       bright_name=bright_names[kk]
       if contrast_value!="0":              
           clahe = cv2.createCLAHE(clipLimit=float(contrast_value))
           imm=clahe.apply(destin_fluor)
           destin_fluor=imm
       #############################
       lineage_name=create_name_for_lineage_image(bright_name)
      
       full_lineage_name =os.path.join(out_folders[4],"LINEAGE_IMAGES",lineage_name)
       cv2.imwrite(full_lineage_name, current_lineage_image) 
       still_lineage=current_lineage_image
       cv2.imwrite(os.path.join(os.path.dirname(out_folders[5]),"still_lineage.tif"), still_lineage)
 
       #########################################
       
       destin_fluor = cv2.cvtColor(destin_fluor,cv2.COLOR_GRAY2BGRA)    
       destin_bright = cv2.cvtColor(destin_bright,cv2.COLOR_GRAY2BGRA)
       destin_red = cv2.cvtColor(destin_red,cv2.COLOR_GRAY2BGRA)    
        
       coords=np.zeros((len(cells),2))           
       for kkk in range(len(cells)):
         
        
         patch_name=create_name_for_cleaned_patch(bright_name, kkk)
         #print("patch_name=", patch_name)
         cv2.imwrite(os.path.join(out_folders[4],"CLEANED_PATCHES",patch_name), cells["cell_%s" % kkk][3])               
         #cv2.imwrite(os.path.join(out_folders[8],"segmented_patch_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][3])         
         output_patch=cells["cell_%s" % kkk][3]
         patch_with_contours=prepare_contours(output_patch)
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]        
         
         collour=cells["cell_%s" % kkk][15]
         
         xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         texxt=cells["cell_%s" % kkk][11]
         
         destin_bright, debug_bright_image=paste_patch(destin_bright,patch_with_contours,a,b,c,d,collour,1.0, frame_size)        
         destin_fluor, debug_fluor_image=paste_patch(destin_fluor,patch_with_contours,a,b,c,d,collour,1.0, frame_size)
         destin_red, debug_red_image=paste_patch(destin_red,patch_with_contours,a,b,c,d,collour,1.0, frame_size)
         centroid=cells["cell_%s" % kkk][6]
         #print("centroid=", centroid)
         start_point, end_point=(int(centroid[0]-p_size), int(centroid[1]-p_size)), (int(centroid[0]+p_size), int(centroid[1]+p_size))
         #print("start_point, end_point=", start_point, end_point)
         #destin_fluor = cv2.rectangle(destin_fluor, start_point, end_point, collour[:-1], 1)
         #destin_fluor = cv2.rectangle(destin_fluor, (b,d), (a,c), collour[:-1], 1)
         one_cell_mask =paste_benchmark_patch(output_patch,a,b,c,d,kkk, frame_size)
         destin_mask+= one_cell_mask
         #xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         #texxt=cells["cell_%s" % kkk][11]
         
         cv2.putText(destin_fluor,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
         cv2.putText(destin_bright,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)         
         cv2.putText(destin_red,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
         
                  
         coords[kkk,0],coords[kkk,1]=xx, yy
       cv2.imwrite(rename_file(out_folders[5],fluor_names[kk]), debug_fluor_image)
       #print("check_fluor_destin   ",rename_file(out_folders[3],fluor_names[kk]))       
       cv2.imwrite(rename_file(out_folders[1],fluor_names[kk]),destin_fluor)# plot destin_fluor to RESULT FLUOR folder
       
       cv2.imwrite(rename_file(out_folders[0],bright_names[kk]),destin_bright)#plot destin_bright to RESULT BRIGHT folder
       cv2.imwrite(rename_file(out_folders[2],red_names[kk]),destin_red)#plot destin_bright to RESULT BRIGHT folder
       #black_and_white=destin_mask.copy()     
       #black_and_white=black_and_white.astype(np.uint8)
       #black_and_white[destin_mask!=0]=255
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),destin_cartoon)
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),black_and_white)
       #benchmark_seg ="mask"+str(k+1+kk+first_frame_number).zfill(n_digits)+".tif"
       
       mask_name=create_name_for_mask(bright_name)
       #print("mask_name=", mask_name)
       #behchmark_seg ="mask"+str(k+kk+1).zfill(n_digits)+".tif"       
       cv2.imwrite(os.path.join(out_folders[4],"MASKS",mask_name),destin_mask)
       return  coords, destin_fluor     
########################################

