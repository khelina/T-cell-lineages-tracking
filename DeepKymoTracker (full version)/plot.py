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
            print("ERROR: run out of colours")
            #colour_dictionary[cell_name]=base_colours[colour_counter-1-len(base_colours)]
    return colour_dictionary, colour_counter
######################################
### This function is for dealing with new cells - they need naive names": "a", "b", "c", .,, "aa", "bb",...
def update_naive_names_list(basic_naive_names, init_number_of_cells,naive_names_counter):# n = number of new (added) naive cells
    new_naive_names=[]
    start_basic_letter=naive_names_counter%26 
    for k in range(init_number_of_cells):
        naive_names_counter+=1       
        if naive_names_counter <=26:# 26= the lenght of English alphabet
             basic_name=basic_naive_names[k+start_basic_letter]
             new_naive_names.append(basic_name)
        else:
            cycle_number=naive_names_counter//26
            basic_name=basic_naive_names[naive_names_counter%26-1]
            real_name=basic_name*(cycle_number+1)
            new_naive_names.append(real_name)      
    return new_naive_names,naive_names_counter
########################################

########################################
################# when adding new cell
def update_xs_after_new_cells(xs,new_names,previous_lineage_image, canvas_lineage_exec, canvas_size_p4, delta,lin_image_widths):
       #print("I am inside update_xs")
       #print("delta=", delta)
       lineage_image_width=previous_lineage_image.shape[1]             
       xs_internal, width_additional= create_additional_dictionary_of_xs(new_names,delta)       
       lin_image_widths.append(width_additional)
       for ii in range(len(new_names)):
          new_name=new_names[ii]
          #print("new_name=", new_name)          
          xs[new_name]=lineage_image_width+xs_internal[new_name]
       previous_lineage_image=np.concatenate((previous_lineage_image,np.zeros((previous_lineage_image.shape[0],width_additional,3), dtype=previous_lineage_image.dtype)), axis=1)         
       lineage_image_width+=width_additional
       #print(" lineage_image_width AFTER=", lineage_image_width)
       canvas_lineage_width=canvas_size_p4+90*(len(lin_image_widths)-1)          
       canvas_lineage_exec.config(width=canvas_lineage_width)
       #print("xs AFTER=",xs)
       #print("lin_image_widths=",lin_image_widths)
       return xs, previous_lineage_image,lin_image_widths
###################################
def create_first_color_dictionary_for_train(init_number_of_cells):
  base_colours = [
    ([255, 0, 255, 255], "magenta"),             
    ([0, 165, 255, 255], "orange"),        
    ([0, 255, 255, 255], "yellow"),        
    ([0, 255, 0, 255], "lime"),            
    ([255, 255, 0, 255], "cyan"),          
    ([255, 0, 0, 255], "blue"),            
    ([0, 191, 255, 255], "deepskyblue"),       
    ([0, 69, 255, 255], "orange red"),       
    ([47, 255, 173, 255], "green"),   
    ([238, 130, 238, 255], "violet"),
    
    #([255, 128, 0, 255], "amber"),              # Amber
    #([255, 0, 128, 255], "rose"),               # Rose
    ([255, 20, 147, 255], "deeppink"),          # Deep Pink
    ([255, 105, 180, 255], "hotpink"),          # Hot Pink
    ([75, 0, 130, 255], "indigo"),              # Indigo
    ([148, 0, 211, 255], "purple"),             # Purple
    ([0, 128, 128, 255], "teal"),               # Teal
    ([255, 228, 196, 255], "bisque"),           # Bisque
    ([165, 42, 42, 255], "brown"),               # Brown
    ([0, 204, 204, 255], "turquoise"),          # Turquoise
    
    ([255, 255, 204, 255], "lightyellow"),      # Light Yellow
    ([135, 206, 250, 255], "lightskyblue"),     # Light Sky Blue
    ([250, 128, 114, 255], "salmon"),            # Salmon
    ([240, 230, 140, 255], "khaki"),             # Khaki
    #([255, 69, 0, 255], "redorange"),            # Red Orange
    ([255, 228, 181, 255], "mistyrose"),        # Misty Rose
    ([60, 179, 113, 255], "mediumseagreen"),    # Medium Sea Green
    ([153, 50, 204, 255], "darkorchid"),         # Dark Orchid
    ([150, 75, 0, 255], "chocolate"),            # Chocolate
    ([205, 133, 63, 255], "peru"),               # Peru

    ([255, 221, 51, 255], "gold"),               # Gold
    ([127, 255, 0, 255], "chartreuse"),          # Chartreuse
    ([0, 255, 191, 255], "mediumturquoise"),     # Medium Turquoise
    #([173, 255, 47, 255], "vividgreenyellow"),   # Vivid Green Yellow
    ([255, 228, 181, 255], "peachpuff"),         # Peach Puff
    ([102, 204, 255, 255], "lightblue"),         # Light Blue
    ([109, 185, 122, 255], "mediumspringgreen"), # Medium Spring Green
    ([255, 127, 80, 255], "lightcoral"),         # Light Coral
    ([255, 191, 0, 255], "goldenrod"),           # Goldenrod
    ([30, 144, 255, 255], "dodgerblue")          # Dodger Blue
]

       
  import string  
  basic_naive_names=list(string.ascii_lowercase)  
  #naive_names_counter=init_number_of_cells-1 
  
  if init_number_of_cells==1:
      new_naive_names=["1"]
      naive_names_counter=0    
  else:
      new_naive_names,naive_names_counter= update_naive_names_list(basic_naive_names,init_number_of_cells,0)  
  #colour_dictionary, colour_counter ={},0
  colour_dictionary, colour_counter=update_color_dictionary({},new_naive_names,base_colours, 0)
  #xs, init_delta=create_first_dictionary_of_xs(new_naive_names, num_frames)    
   
  return colour_dictionary, new_naive_names, base_colours, colour_counter, basic_naive_names, naive_names_counter
#######################################
def create_first_color_dictionary(init_number_of_cells, num_frames): 
  base_colours = [
    ([255, 0, 255, 255], "magenta"),             
    ([0, 165, 255, 255], "orange"),        
    ([0, 255, 255, 255], "yellow"),        
    ([0, 255, 0, 255], "lime"),            
    ([255, 255, 0, 255], "cyan"),          
    ([255, 0, 0, 255], "blue"),            
    ([0, 191, 255, 255], "deepskyblue"),       
    ([0, 69, 255, 255], "orange red"),       
    ([47, 255, 173, 255], "green"),   
    ([238, 130, 238, 255], "violet"),
    
    #([255, 128, 0, 255], "amber"),              # Amber
    #([255, 0, 128, 255], "rose"),               # Rose
    ([255, 20, 147, 255], "deeppink"),          # Deep Pink
    ([255, 105, 180, 255], "hotpink"),          # Hot Pink
    ([75, 0, 130, 255], "indigo"),              # Indigo
    ([148, 0, 211, 255], "purple"),             # Purple
    ([0, 128, 128, 255], "teal"),               # Teal
    ([255, 228, 196, 255], "bisque"),           # Bisque
    ([165, 42, 42, 255], "brown"),               # Brown
    ([0, 204, 204, 255], "turquoise"),          # Turquoise
    
    ([255, 255, 204, 255], "lightyellow"),      # Light Yellow
    ([135, 206, 250, 255], "lightskyblue"),     # Light Sky Blue
    ([250, 128, 114, 255], "salmon"),            # Salmon
    ([240, 230, 140, 255], "khaki"),             # Khaki
    #([255, 69, 0, 255], "redorange"),            # Red Orange
    ([255, 228, 181, 255], "mistyrose"),        # Misty Rose
    ([60, 179, 113, 255], "mediumseagreen"),    # Medium Sea Green
    ([153, 50, 204, 255], "darkorchid"),         # Dark Orchid
    ([150, 75, 0, 255], "chocolate"),            # Chocolate
    ([205, 133, 63, 255], "peru"),               # Peru

    ([255, 221, 51, 255], "gold"),               # Gold
    ([127, 255, 0, 255], "chartreuse"),          # Chartreuse
    ([0, 255, 191, 255], "mediumturquoise"),     # Medium Turquoise
    #([173, 255, 47, 255], "vividgreenyellow"),   # Vivid Green Yellow
    ([255, 228, 181, 255], "peachpuff"),         # Peach Puff
    ([102, 204, 255, 255], "lightblue"),         # Light Blue
    ([109, 185, 122, 255], "mediumspringgreen"), # Medium Spring Green
    ([255, 127, 80, 255], "lightcoral"),         # Light Coral
    ([255, 191, 0, 255], "goldenrod"),           # Goldenrod
    ([30, 144, 255, 255], "dodgerblue")          # Dodger Blue
]     
  import string  
  basic_naive_names=list(string.ascii_lowercase)  
  #naive_names_counter=init_number_of_cells-1 
  
  if init_number_of_cells==1:
      new_naive_names=["1"]
      naive_names_counter=0    
  else:
      new_naive_names,naive_names_counter= update_naive_names_list(basic_naive_names,init_number_of_cells,0)  
  #colour_dictionary, colour_counter ={},0
  colour_dictionary, colour_counter=update_color_dictionary({},new_naive_names,base_colours, 0)
  xs, init_delta=create_first_dictionary_of_xs(new_naive_names, num_frames)    
   
  return colour_dictionary, new_naive_names, base_colours, colour_counter, basic_naive_names, xs, init_delta,naive_names_counter
###############################

#######################################
def create_first_dictionary_of_xs(initial_naive_names,num_frames):
    #print("INSIDE creat_first_xs")
    m=len(initial_naive_names)
    init_delta=int(num_frames/(2*m))          
    xs={}  
    for i in range(len(initial_naive_names)):
        xs[initial_naive_names[i]]=init_delta*(2*i+1)
    #print("xs=", xs)
    #print("init_delta=", init_delta)
    return xs, init_delta
#############################
def update_xs_after_division(xs,daughter_1_name,daughter_2_name, mother_name,init_delta):       
    new_delta=int(init_delta/2**(len(mother_name)))   
    xs[daughter_1_name]= xs[mother_name]-new_delta
    xs[daughter_2_name]= xs[mother_name]+new_delta  
    return xs    
###################### when manually adding new cells
def create_additional_dictionary_of_xs(new_names,init_delta):  
  m=len(new_names)
  #print("INSIDE CREATE ADDITIONAL")
  #print("m=",m)
  total_number_of_deltas_for_additional=m*2   
  width_additional= total_number_of_deltas_for_additional*init_delta    
  xs_additional={}  
  for i in range(m):      
        xs_additional[new_names[i]]=init_delta*(2*i+1)        
  #print("xs_additional=",xs_additional)
  #print(" width_additional=", width_additional)        
  return xs_additional, width_additional
#################################################### 
def rename_file(destin,infile):# for bright or fluor images       
 infile = os.path.normpath(infile) 
 old =infile.split(os.sep)
 new1 =old[-1]
 
 new=os.path.join(destin,new1) 
 base,ext=os.path.splitext(new)
 newest=base+".tif" 
 return newest
#############################
def create_name_for_mask(bright_name, basename):
    bright_name = os.path.normpath(bright_name) 
    old =bright_name.split(os.sep)# creates a list of strings which are usually separated by \
    new1 =old[-1]
    mask_name =new1[:-8]+basename
    #mask_name =new1[:-8]+"mask.tif" 
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
def prepare_contours(binary_patch, fill_indicator):# input_image must be gray. binary 0,255
    binary_patch = binary_patch.astype('uint8')
    im2,contours, hierarchy = cv2.findContours(binary_patch,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    patch_with_contour=np.zeros((binary_patch.shape[0],binary_patch.shape[0],3),np.uint8)    
    cv2.drawContours( patch_with_contour, contours, -1, (0,0,255), fill_indicator)    
    patch_with_contour = cv2.cvtColor( patch_with_contour,cv2.COLOR_BGR2GRAY)
    patch_with_contour[ patch_with_contour!=0]=255
    return  patch_with_contour    
#############################################################
def paste_patch(destin_image,patch,a,b,c,d,color,alpha, frame_size, bordersize):
    destin_image_border=cv2.copyMakeBorder(destin_image, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,  borderType= cv2.BORDER_CONSTANT, value = float(np.mean(destin_image)) )    
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
    destin_image_cropped=destin_image_border[bordersize:frame_size+bordersize,bordersize:frame_size+bordersize]    
    return destin_image_cropped
################### create mask image for MASKS folder
def paste_benchmark_patch(patch,a,b,c,d,cell_number, frame_size, bordersize):    
    image_with_one_cell_border=np.zeros((frame_size+2*bordersize,frame_size+2*bordersize),dtype="uint64")     
    patch=patch.astype(np.uint64)            
    mask=deepcopy(patch)
    patch[mask==255]=2**cell_number                  
    image_with_one_cell_border[c:d, a:b] = patch    
    final_image=image_with_one_cell_border[bordersize:frame_size+bordersize,bordersize:frame_size+bordersize]     
    return final_image
#########################################
def plot_frame(cells,clip_centr,k,kk,fluor_images,fluor_names,out_folders,coords, coords_old, bright_images, bright_names, frame_size, n_digits, first_frame_number, contrast_value, current_lineage_image, patch_size,red_images, red_names, bordersize):      
       destin_mask=np.zeros((frame_size,frame_size),dtype="uint64")       
       destin_fluor=fluor_images[kk]
       destin_bright=bright_images[kk]
       destin_red=red_images[kk]
       bright_name=bright_names[kk]
       destin_segmented =np.zeros((frame_size,frame_size),dtype="uint8")
       if contrast_value!="0":              
           clahe = cv2.createCLAHE(clipLimit=float(contrast_value))
           imm=clahe.apply(destin_fluor)
           destin_fluor=imm
       coords=np.zeros((len(cells),2))
       #############################
       lineage_name=create_name_for_lineage_image(bright_name)      
       full_lineage_name =os.path.join(out_folders[4],"LINEAGE_IMAGES",lineage_name)
       cv2.imwrite(full_lineage_name, current_lineage_image) 
       still_lineage=current_lineage_image
       cv2.imwrite(os.path.join(os.path.dirname(out_folders[0]),"still_lineage.tif"), still_lineage)
        
       destin_fluor = cv2.cvtColor(destin_fluor,cv2.COLOR_GRAY2BGRA)    
       destin_bright = cv2.cvtColor(destin_bright,cv2.COLOR_GRAY2BGRA)
       if red_names[kk]!="0":
           destin_red = cv2.cvtColor(destin_red,cv2.COLOR_GRAY2BGRA)    
       destin_segmented = cv2.cvtColor(destin_segmented,cv2.COLOR_GRAY2BGRA) 
                 
       for kkk in range(len(cells)):
         patch_name=create_name_for_cleaned_patch(bright_name, kkk)         
         cv2.imwrite(os.path.join(out_folders[4],"CLEANED_PATCHES",patch_name), cells["cell_%s" % kkk][3])                       
         output_patch=cells["cell_%s" % kkk][3]        
         patch_with_contours=prepare_contours(output_patch,1)
         a,b,c,d=cells["cell_%s" % kkk][7],cells["cell_%s" % kkk][8],cells["cell_%s" % kkk][9],cells["cell_%s" % kkk][10]                 
         collour=cells["cell_%s" % kkk][15][0]         
         xx,yy=cells["cell_%s" % kkk][6][0],cells["cell_%s" % kkk][6][1]
         texxt=cells["cell_%s" % kkk][11]
         
         coords[kkk,0],coords[kkk,1]=xx, yy
         centroid=cells["cell_%s" % kkk][6]
         ##############################################
         destin_bright=paste_patch(destin_bright,patch_with_contours,a,b,c,d,collour,1.0, frame_size, bordersize)        
         destin_fluor=paste_patch(destin_fluor,patch_with_contours,a,b,c,d,collour,1.0, frame_size,bordersize)
         if red_names[kk]!="0":
             destin_red=paste_patch(destin_red,patch_with_contours,a,b,c,d,collour,1.0, frame_size,bordersize)
         ################################################    
         start_point, end_point=(int(centroid[0]-patch_size), int(centroid[1]-patch_size)), (int(centroid[0]+patch_size), int(centroid[1]+patch_size))        
         one_cell_mask =paste_benchmark_patch(output_patch,a,b,c,d,kkk, frame_size,bordersize)         
         destin_mask+= one_cell_mask
         mask_name=create_name_for_mask(bright_name,"mask.npy")
         destin_mask_for_plot=np.round(destin_mask)
         destin_mask_for_plot=destin_mask_for_plot.astype(np.uint64)
         ###################################################
         patch_with_filled_contour=prepare_contours(output_patch,-1)
         destin_segmented =paste_patch(destin_segmented,patch_with_filled_contour,a,b,c,d,collour,1.0, frame_size, bordersize)
         destin_segmented =cv2.cvtColor(destin_segmented , cv2.COLOR_RGBA2RGB)
         segmented_name=create_name_for_mask(bright_name,"segmented_colour.tif")   
         ##################################################
         binary_segm=destin_mask.copy()     
         binary_segm = binary_segm.astype(np.uint8)
         binary_segm[destin_mask!=0]=255
         binary_segm_name=create_name_for_mask(bright_name,"segmented_binary.tif")  
         #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),destin_cartoon)
         #cv2.imwrite(rename_file(out_folders[1],names[k+kk]),black_and_white)
         #benchmark_seg ="mask"+str(k+1+kk+first_frame_number).zfill(n_digits)+".tif"
         ##############################################
         cv2.putText(destin_fluor,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1) 
         cv2.putText(destin_bright,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)
         if red_names[kk]!="0":         
              cv2.putText(destin_red,texxt,(int(xx)-5,int(yy)+5),cv2.FONT_HERSHEY_PLAIN,0.7,collour,1)
     
       cv2.imwrite(rename_file(out_folders[1],fluor_names[kk]),destin_fluor)# plot destin_fluor to RESULT FLUOR folder       
       cv2.imwrite(rename_file(out_folders[0],bright_names[kk]),destin_bright)#plot destin_bright to RESULT BRIGHT folder
       if red_names[kk]!="0":
            cv2.imwrite(rename_file(out_folders[2],red_names[kk]),destin_red)#plot destin_bright to RESULT BRIGHT folder
       #cv2.imwrite(os.path.join(out_folders[4],"MASKS",mask_name),destin_mask_for_plot)
       np.save(os.path.join(out_folders[4],"MASKS",mask_name),destin_mask_for_plot)
       cv2.imwrite(os.path.join(out_folders[5],segmented_name),destin_segmented)
       cv2.imwrite(os.path.join(out_folders[6],binary_segm_name), binary_segm)        
       return  coords, destin_fluor     
########################################
