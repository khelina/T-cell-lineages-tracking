import cv2
import numpy as np
import os
import math
from copy import deepcopy
#############################

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
def update_xs(xs,new_names, remaining_number_of_cells, previous_lineage_image, canvas_lineage_exec, canvas_size_p4, delta):
       print("I am inside update_xs")
       print("delta=", delta)
       lineage_image_width=previous_lineage_image.shape[1]
       print(" lineage_image_width BEFORE=", lineage_image_width)
       print(" previous_lineage_image.shape BEFORE=", previous_lineage_image.shape)
       #number_of_processed_cells=1
       cv2.imwrite(r"C:\Users\helina\Desktop\prevous_image_before.tif", previous_lineage_image)
       #remaining_number_of_cells=observed_max_number_of_cells- number_of_processed_cells
      # print("number_of_processed_cells=", number_of_processed_cells)
       #print("observed_max_number_of_cells=", observed_max_number_of_cells)
       #remaining_number_of_cells=1
       print("xs BEFORE=",xs)
       xs_internal, width_additional= create_additional_dictionary_of_xs(new_names,delta,remaining_number_of_cells)
       print("width_additional=",width_additional)
       print("xs_internal=",xs_internal)
       for ii in range(len(new_names)):
          new_name=new_names[ii]
          print("new_name=", new_name)
           
          #xs[new_name]=num_frames+20*(ii+1+number_of_added_new_cells)
          #xs[new_name]=num_frames+xs_internal[new_name]
          xs[new_name]=lineage_image_width+xs_internal[new_name]
          previous_lineage_image=np.concatenate((previous_lineage_image,np.zeros((previous_lineage_image.shape[0],width_additional,3), dtype=previous_lineage_image.dtype)), axis=1)
          print(" previous_lineage_image.shape AFTER=", previous_lineage_image.shape)
         
          lineage_image_width+=width_additional
          print(" lineage_image_width AFTER=", lineage_image_width)
          canvas_lineage_width=lineage_image_width*canvas_size_p4/previous_lineage_image.shape[0]
          
       cv2.imwrite(r"C:\Users\helina\Desktop\previous_lineage_image_after.tif", previous_lineage_image)   
       print(" canvas_lineage_width=", canvas_lineage_width)
       canvas_lineage_exec.config(width=canvas_lineage_width)
       print("xs AFTER=",xs)
       return xs, previous_lineage_image
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
  xs, delta=create_first_dictionary_of_xs(new_naive_names, num_frames,max_number_of_cells)    
  #print("ready for execution")
  #print("final_list", final_list)
  
  return colour_dictionary, new_naive_names, base_colours, colour_counter, unused_naive_names, xs, delta
#######################################

#############################
def create_first_dictionary_of_xs(initial_naive_names,num_frames,observed_max_number_of_cells):  
  m=len(initial_naive_names)
  kk=-1# kk=max number of potential divisions
  while True:
    kk+=1   
    if (2**(kk-1))<observed_max_number_of_cells-m+1<=(2**kk):
        number_of_potential_divisions=kk
        break
  print("number_of_potential_divisions=", number_of_potential_divisions)  
  potential_max_number_of_cells=(2**kk)*m
  max_number_of_cells_in_one_unit=2**kk 
  number_of_deltas_in_one_unit=(2**kk-1)*2
  total_number_of_deltas=m* number_of_deltas_in_one_unit+m+1  
  delta=int(num_frames/total_number_of_deltas)
  #print("delta=", delta)
  ##############################
  first_m=-int(number_of_deltas_in_one_unit/2)*delta 
  #print("first_m=", first_m)
  step_size_for_m=(number_of_deltas_in_one_unit+1)*delta
  #print("step_size_for_m=", step_size_for_m)
  #############################
  all_cell_names=initial_naive_names
  temp_list=all_cell_names
  for k in range(number_of_potential_divisions):# was n
    daughters=[]
    for item in temp_list:     
      a=item+"0"
      b=item+"1"      
      daughters =daughters+[a,b]
    temp_list =daughters   
    all_cell_names=all_cell_names+temp_list   
  print("all_cell_names=", all_cell_names)
  #######################################        
  cell_names_lengths =[len(item) for item in all_cell_names]
  max_name_length =max(cell_names_lengths)
  #print("max_name_length=", max_name_length)  
  xs={}
  
  for i in range(len(initial_naive_names)):
        xs[initial_naive_names[i]]=first_m+step_size_for_m*(i+1)   
  for k in range(len(all_cell_names)):# creates x-coordinates for all possible daughters                                # based on max_number_of_cells in the movie
       cell_name =all_cell_names[k]        
       kkk=len(cell_name)
       if kkk<max_name_length:         
         item_1=xs[cell_name]-delta*(2**(kk-kkk))
         item_2=xs[cell_name]+delta*(2**(kk-kkk))   
         xs[cell_name+"0"]=int(item_1)
         xs[cell_name+"1"]=int(item_2)
  print("xs inside create_first_dictinary of xs=", xs)
  print("delta=", delta)              
  return xs, delta
########################################
def create_additional_dictionary_of_xs(initial_new_names,delta,remaining_number_of_cells):
  
  m=len(initial_new_names)
  kk=-1# kk=max number of potential divisions
  while True:
    kk+=1   
    if (2**(kk-1))<remaining_number_of_cells-m+1<=(2**kk):
        number_of_potential_divisions=kk
        break  
  potential_max_number_of_cells=(2**kk)*m
  max_number_of_cells_in_one_unit=2**kk 
  number_of_deltas_in_one_unit=(2**kk-1)*2 
  total_number_of_deltas_for_additional=m* number_of_deltas_in_one_unit+m   
  width_additional= total_number_of_deltas_for_additional*delta  
  first_m=-int(number_of_deltas_in_one_unit/2)*delta-delta
  step_size_for_m=(number_of_deltas_in_one_unit+1)*delta 
  #############################
  all_cell_names=initial_new_names
  temp_list=all_cell_names
  for k in range(number_of_potential_divisions):# was n
    daughters=[]
    for item in temp_list:     
      a=item+"0"
      b=item+"1"      
      daughters =daughters+[a,b]
    temp_list =daughters   
    all_cell_names=all_cell_names+temp_list
 
  cell_names_lengths =[len(item) for item in all_cell_names]
  max_name_length =max(cell_names_lengths)
  #print("max_name_length=", max_name_length)  
  xs_additional={}
  
  for i in range(len(initial_new_names)):
        xs_additional[initial_new_names[i]]=first_m+step_size_for_m*(i+1) 
  #print("xs for new_naive_names_only", xs)
        #xs[new_naive_names[i]]=int((num_frames/(len(new_naive_names)+1))*(i+1))
  for k in range(len(all_cell_names)):# creates x-coordinates for all possible daughters                                # based on max_number_of_cells in the movie
       cell_name =all_cell_names[k]        
       kkk=len(cell_name)
       if kkk<max_name_length:         
         item_1=xs_additional[cell_name]-delta*(2**(kk-kkk))
         item_2=xs_additional[cell_name]+delta*(2**(kk-kkk))   
         xs_additional[cell_name+"0"]=int(item_1)
         xs_additional[cell_name+"1"]=int(item_2)              
  return xs_additional, width_additional
 
 

####### xs contains x-coordinates for each cell (for plotting dynamic lineage)
# It is created based on cell names in Frame 1 (see function def_Close_popup)
# template = new_cell_names (naive) in Frame 1
 
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
    section_2_new=section_2+"ptch.tif"
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
def paste_patch(destin_image,patch,a,b,c,d,color,alpha, frame_size, bordersize):
    destin_image_border=cv2.copyMakeBorder(destin_image, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,  borderType= cv2.BORDER_CONSTANT, value = float(np.mean(destin_image)) )
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
    
    destin_image_cropped=destin_image_border[bordersize:frame_size+bordersize,bordersize:frame_size+bordersize]
    #cv2.putText(destin_image_cropped,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,color,1) 
    #cv2.putText(destin_bright,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)         
    #cv2.putText(destin_red,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
    return destin_image_cropped,  debug_destin_image
################### create mask image for MASKS folder
def paste_benchmark_patch(patch,a,b,c,d,cell_number, frame_size, bordersize):    
    image_with_one_cell_border=np.zeros((frame_size+2*bordersize,frame_size+2*bordersize),dtype="uint64")     
    patch=patch.astype(np.uint64)
    print("np.max(patch) before=",np.max(patch))          
    mask=deepcopy(patch)
    patch[mask==255]=2**cell_number     
    #patch[mask==255]=cell_number+1 
    print("np.max(patch) after=",np.max(patch))            
    image_with_one_cell_border[c:d, a:b] = patch
    print("np.max(image_with_one_cell_border)=", np.max(image_with_one_cell_border))
    print("image_with_one_cell_border.dtype=", image_with_one_cell_border.dtype)
    final_image=image_with_one_cell_border[bordersize:frame_size+bordersize,bordersize:frame_size+bordersize]     
    return final_image
#######################################################

#########################################
def plot_frame(cells,clip_centr,k,kk,fluor_images,fluor_names,out_folders,coords, coords_old, bright_images, bright_names, frame_size, n_digits, first_frame_number, contrast_value, current_lineage_image, patch_size,red_images, red_names, bordersize):      
       destin_mask=np.zeros((frame_size,frame_size),dtype="uint64")       
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
       if red_names[kk]!="0":
           destin_red = cv2.cvtColor(destin_red,cv2.COLOR_GRAY2BGRA)    
        
       coords=np.zeros((len(cells),2))           
       for kkk in range(len(cells)):
         
        
         patch_name=create_name_for_cleaned_patch(bright_name, kkk)
         #print("patch_name=", patch_name)
         cv2.imwrite(os.path.join(out_folders[4],"CLEANED_PATCHES",patch_name), cells["cell_%s" % kkk][3])               
         #cv2.imwrite(os.path.join(out_folders[8],"segmented_patch_%s_cell_%s.tif") % (k+kk,kkk), cells["cell_%s" % kkk][3])         
         output_patch=cells["cell_%s" % kkk][3]
         print("np.max(output_patch)=", np.max(output_patch))
         patch_with_contours=prepare_contours(output_patch)
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]        
         
         collour=cells["cell_%s" % kkk][15]
         
         xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         texxt=cells["cell_%s" % kkk][11]
         
         destin_bright, debug_bright_image=paste_patch(destin_bright,patch_with_contours,a,b,c,d,collour,1.0, frame_size, bordersize)        
         destin_fluor, debug_fluor_image=paste_patch(destin_fluor,patch_with_contours,a,b,c,d,collour,1.0, frame_size,bordersize)
         if red_names[kk]!="0":
             destin_red, debug_red_image=paste_patch(destin_red,patch_with_contours,a,b,c,d,collour,1.0, frame_size,bordersize)
         centroid=cells["cell_%s" % kkk][6]
         #print("centroid=", centroid)
         start_point, end_point=(int(centroid[0]-patch_size), int(centroid[1]-patch_size)), (int(centroid[0]+patch_size), int(centroid[1]+patch_size))
         #print("start_point, end_point=", start_point, end_point)
         #destin_fluor = cv2.rectangle(destin_fluor, start_point, end_point, collour[:-1], 1)
         #destin_fluor = cv2.rectangle(destin_fluor, (b,d), (a,c), collour[:-1], 1)
         one_cell_mask =paste_benchmark_patch(output_patch,a,b,c,d,kkk, frame_size,bordersize)
         print("np.max(one_cell_mask)=", np.max(one_cell_mask))
         print("one_cell_mask.dtype=", one_cell_mask.dtype)
         destin_mask+= one_cell_mask
         #xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         #texxt=cells["cell_%s" % kkk][11]
         
         cv2.putText(destin_fluor,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
         cv2.putText(destin_bright,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)
         if red_names[kk]!="0":         
              cv2.putText(destin_red,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
         
                  
         coords[kkk,0],coords[kkk,1]=xx, yy
       cv2.imwrite(rename_file(out_folders[5],fluor_names[kk]), debug_fluor_image)
       #print("check_fluor_destin   ",rename_file(out_folders[3],fluor_names[kk]))       
       cv2.imwrite(rename_file(out_folders[1],fluor_names[kk]),destin_fluor)# plot destin_fluor to RESULT FLUOR folder
       
       cv2.imwrite(rename_file(out_folders[0],bright_names[kk]),destin_bright)#plot destin_bright to RESULT BRIGHT folder
       if red_names[kk]!="0":
            cv2.imwrite(rename_file(out_folders[2],red_names[kk]),destin_red)#plot destin_bright to RESULT BRIGHT folder
       #black_and_white=destin_mask.copy()     
       #black_and_white=black_and_white.astype(np.uint8)
       #black_and_white[destin_mask!=0]=255
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),destin_cartoon)
       #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),black_and_white)
       #benchmark_seg ="mask"+str(k+1+kk+first_frame_number).zfill(n_digits)+".tif"
       
       mask_name=create_name_for_mask(bright_name)
       print("destin_mask.dtype=", destin_mask.dtype)
       print("np.max(destin_mask)=", np.max(destin_mask))
       destin_mask_for_plot=np.round(destin_mask)
       destin_mask_for_plot=destin_mask_for_plot.astype(np.uint64)
       print("np.max(destin_mask_for_plot)=", np.max(destin_mask_for_plot))
       #behchmark_seg ="mask"+str(k+kk+1).zfill(n_digits)+".tif"       
       cv2.imwrite(os.path.join(out_folders[4],"MASKS",mask_name),destin_mask_for_plot)
       return  coords, destin_fluor     
########################################
