import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import xlsxwriter
import os
import pickle
import re 
from PIL import ImageTk, Image
import tkinter
from copy import deepcopy
import shutil
import time
#############################################################
from print_excel import extract_lineage
##############################################################
### For rhe last step
## This function creates lineage_per_cell (out of lineage_per_frame) 
## It is executed  only after the movie has been tracked (button Create Output Movie)
## Lineage_per_cell will be used in the next steps
## Also, it is a better way of representing results
# This function creates current_lineage_image to be plotted for each frame during execution
# It is based on dictionary of xs (gives x-coordinate) and frame (which frame number, i.e. y-coordinate)
def create_lineage_image_one_frame(cells, previous_lineage_image, xs, frame, first_frame_number): 
 ###### prepare points for lineage images ######
 point_radius=10# radius of plotted point in lineage image
 size=previous_lineage_image.shape[0]
 points=[]# points (x,y) for plotting animated lineage (for current frame only: the previous points are in previous_lineage_image)
 keys=cells.keys()
 for key in keys:
   item=cells[key]# cells means that linage_per_frame_p4 is used for extraxting info about cells in this frame   
   cell_name=item[11]
   x=xs[cell_name]
   y = item[12]# y=frame_number
   y_internal=y-first_frame_number
   colour=item[15][:-1]   
   if size <=382:# for very short movies (otherwise the lines in current_linage_image will be too thick)    
       point_radius=1      
   points.append(((x,y_internal),colour)) 
   # more points for the  case of division (horizontal lines drawing)  
   if item[16]=="daughter-1":
          start=cell_name[:-1]                
          more_points=[((xx,y_internal),colour) for xx in range(xs[start+"0"],xs[start],1)]    
          points+=more_points 
   if item[16]=="daughter-2":      
          start=cell_name[:-1]                   
          more_points=[((xx,y_internal),colour) for xx in range(xs[start],xs[start+"1"],1)]    
          points+=more_points        
 ######### create lineage image at last                    
 for p in range(len(points)):
      cv2.circle(previous_lineage_image, points[p][0], point_radius, points[p][1], -1)
 current_lineage_image= previous_lineage_image

 return current_lineage_image    
##########################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
#################################################
def load_files(folder_dir):# load linegae images and segmented images to create final movie
 images=[]
 for filename in os.listdir(folder_dir):
   if filename.endswith(".tif"):
        full_name=os.path.join(folder_dir, filename)      
        image=cv2.imread(full_name,1)
        images.append(image)       
 return images
############ prepare images for output_movie
def create_output_movie(outpath,frame_size): 
 images_out_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)" ,"IMAGES_FOR_FINAL_MOVIE")
 images_seg=load_files(os.path.join(outpath,"TRACKED_BRIGHTFIELD_CHANNEL"))
 images_lin=load_files(os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)" ,"LINEAGE_IMAGES"))
 images=[]
 for i in range(len(images_lin)):
    img=np.zeros((frame_size,frame_size*2,3))
    im_seg_resized =cv2.resize(images_seg[i], (frame_size,frame_size), interpolation = cv2.INTER_AREA)
    img[:,:frame_size,:]= im_seg_resized 
    im_lin_resized =cv2.resize(images_lin[i], (frame_size,frame_size), interpolation = cv2.INTER_AREA)
    img[:,frame_size:,:]=  im_lin_resized 
    texxt=str(i+1)
    cv2.putText(img,texxt,(frame_size+10,12),cv2.FONT_HERSHEY_PLAIN,1,(0,255,255),1)          
    images.append(img)
    destin=os.path.join(images_out_path,"movie_%s.tif" % (i+1))
    cv2.imwrite(destin, img)
############## create and save movie
 print("Creating output movie and saving as .avi")
 video_name = os.path.join(outpath,"lineage_movie.avi")
 frame=images[0]
 height, width, layers = frame.shape
 video = cv2.VideoWriter(video_name, 0, 10, (width,height))
 for image in images:   
    video.write(np.uint8(image))
 cv2.destroyAllWindows()
 video.release()
 print("Finished")
 del images_seg
 del images_lin
 del images
##################################################
def change_dict(init_dict, prop, key, item):
   plots1 = deepcopy(init_dict)
   dicct =plots1[key]
   dicct[prop].append(item)
   init_dict[key]=dicct
   return init_dict
###################################################
def extract_info_from_file_name(file_name):
    #print("file_name=", file_name)
    first=file_name.index("_")
    cell_key =file_name[:first]
    res_name =file_name[first+1:]
    second =res_name.index("_")
    cell_property =res_name[:second]
    last_name =res_name[second+1:]
    third=last_name.index("_")
    frame_number =last_name[third+1:-4]
    #print("frame_number=", frame_number)
    return cell_key, cell_property, int(frame_number)
#############################################################
### for the last step (visualise results): prepare images for display
def load_and_prepare_result_images(outpath, keys,progress_bar):
   
    names, names_1=[],[]     
    bright_images_path=os.path.join(outpath, "TRACKED_BRIGHTFIELD_CHANNEL")
    for filename in os.listdir(bright_images_path):       
          names.append(filename)
    total=len(names)
    patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PATCHES_FOR_RESULTS")
    for filename in os.listdir(patches_path):       
          names_1.append(filename)
    total_frames_1=len(names_1)
    total+=total_frames_1*5
          
    red_patches = {key:[] for key in keys}
    one_cell_patches = {key:[] for key in keys}
    dictt={"Area":[], "Perimeter": [], "Circularity": []}
    plots = {key:dictt for key in keys}
    
    red_patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"RED_LINEAGE_PATCHES")   
    one_cell_patches_path =os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PATCHES_FOR_RESULTS")
  
    plots_path =os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PLOTS")
    p=0   
    bright_names=[]
    for file_name in sorted_aphanumeric(os.listdir(bright_images_path)):             
        if file_name.endswith("ch02.tif"):         
          full_bright_name=os.path.join(bright_images_path,file_name)
          bright_names.append(full_bright_name)          
          p+=1
          progress_bar["value"]=(p/total)*100         
    folders=[red_patches_path, one_cell_patches_path, plots_path]        
    for folder in folders:     
      for filename in sorted_aphanumeric(os.listdir(folder)):       
        cell_key, cell_property, frame_number=extract_info_from_file_name(filename)             
        full_name=os.path.join(folder, filename)
        image=cv2.imread(full_name,-1)# was 0
        item=(image, frame_number)
        p+=1
        progress_bar["value"]=(p/total)*100  
        if cell_property=="red":           
            red_patches[cell_key].append(item)            
        elif cell_property=="patch":
             one_cell_patches[cell_key].append(item)                              
        else:                     
            plots=change_dict(plots, cell_property, cell_key, item)   
    return red_patches, one_cell_patches, plots, bright_names 
################################################################### 
######### This is for Step-5: creates VISUALISATION_HELPERS folder

def plot_per_cell_info_old(pedigree, outpath, still_lineage, label_feedback, progress_bar, first_frame_number_p6,label_create_p6):
   start_time = time.clock()
   counter=0
   red_patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"RED_LINEAGE_PATCHES")  
   plots_path= os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PLOTS")  
   one_cell_patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PATCHES_FOR_RESULTS")   
   list_of_cell_names =list(pedigree.keys())
   label_feedback.config(text="Cells discovered inside function:  " +str(list_of_cell_names))
   for cell_name in list_of_cell_names:# creatse folder for each cell in OUTPUT folder
     counter+=1
     label_feedback.config(text="Cells discovered:  " +str(list_of_cell_names)+"\nCreating results for:  " +str(cell_name))
     label_create_p6.config(text="Creating results for:  " +str(cell_name))
     specific_cell_dirr=os.path.join(outpath,'RESULTS_PER_CELL',cell_name)    
     one_cell_images=[]
     red_patches=[]
     area_plots=[]
     perimeter_plots=[]
     circ_plots=[]
     cell_info=pedigree[cell_name]
     total=len(cell_info)# total number of frames for this particular cell       
     color=pedigree[cell_name][0][7]               
     mask = (still_lineage == color).all(axis=-1)
     x=np.zeros(still_lineage.shape,dtype = "uint8")
     x[mask]=[255,255,255]
     gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
     z=np.where(gray==255)
     rows,cols =z[0], z[1]
     points =[(rows[ii], cols[ii]) for ii in range(len(rows))]
     ################## create red lineage plots     
     for i in range(len(cell_info)):# it is the number of frames for this cell
       im=cell_info[i][2]     
       one_cell_images.append(im)
       frame_number =cell_info[i][1]
       name =os.path.join(one_cell_patches_path,cell_name +"_patch_frame_%s" % frame_number)
       cv2.imwrite(name +".tif",im)

       init=still_lineage.copy()# plot red points in lineage              
       for k in range(len(points)):
          if points[k][0]==frame_number-first_frame_number_p6:        
              cv2.circle(init,(points[k][1], points[k][0]), 1,[0,0,255],-1)
       name =os.path.join(red_patches_path,cell_name +"_red_frame_%s" % frame_number)
       cv2.imwrite(name +".tif",init)
       red_patches.append(init)        
     #####################  plot diagrams
     a=pedigree[cell_name]
     first_frame_num=a[0][1]
     areas=[]
     perimeters=[]
     circularities=[]
     frames=[]
     centroids=[]
     #######################################################
     for k in range(len(a)):# it is the number of frames for this cell
        areas.append(a[k][4])
        perimeters.append(a[k][5])
        circularities.append(a[k][6])
        frames.append(a[k][1])
        centroids.append(a[k][3])
     ########################################################             
     area_plots=[] 
     perimeter_plots=[]
     circ_plots=[]
     x=[frames[kk] for kk in range (len(frames))]
     progress_bar["value"]=0 
     ############################################
     for i in range(len(cell_info)):
       progress_bar["value"]=(i/total)*100 
       frame_number=frames[i]        
       plt.plot(x, areas, 'yo', markersize=5)
       plt.plot([frame_number],[areas[frame_number-first_frame_num]],'bo', markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Area')
       plt.title('Area of '+cell_name)
       
       areas_path=os.path.join(specific_cell_dirr,'areas.png')
       plt.savefig(areas_path)
       img = cv2.imread(areas_path)
       area_plot= Image.fromarray(img)        
       name =os.path.join(plots_path,cell_name +"_Area_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)
       plt.close() 
       
       g = plt.figure()
       plt.plot(x, areas, 'yo', markersize=5)
       plt.xlabel('Frame')
       plt.ylabel('Area')
       plt.title('Area of '+cell_name)       
       g.clear()
       plt.close(g)

       plt.plot(x, perimeters, 'go', linewidth=0.5)
       plt.plot([frame_number],[perimeters[frame_number-first_frame_num]],'bo',markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Perimeter')
       plt.title('Perimeter '+cell_name)
       perimeters_path=os.path.join(specific_cell_dirr,'perimeters.png')
       plt.savefig(perimeters_path)
       img = cv2.imread(perimeters_path)
       
       perimeter_plot= Image.fromarray(img)         
       name =os.path.join(plots_path,cell_name +"_Perimeter_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)
       plt.close() 
       hh = plt.figure()
       plt.plot(x, perimeters, 'go', markersize=5)
       plt.xlabel('Frame')
       plt.ylabel('Perimeter')
       plt.title('Perimeter of '+cell_name)      
       hh.clear()
       plt.close(hh) 

       plt.plot(x, circularities, 'ro', linewidth=0.5)
       plt.plot([frame_number],[circularities[frame_number-first_frame_num]],'bo', markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Circularity')
       plt.title('Circularity '+cell_name)
       circularities_path=os.path.join(specific_cell_dirr,'circularities.png')
       plt.savefig(circularities_path)
       img = cv2.imread(circularities_path)       
       circ_plot= Image.fromarray(img)        
       name =os.path.join(plots_path,cell_name +"_Circularity_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)     
       plt.close()
       ggg = plt.figure()
       plt.plot(x, circularities, 'ro', linewidth=0.5)
       plt.xlabel('Frame')
       plt.ylabel('Circularity')
       plt.title('Circularity of '+cell_name)       
       ggg.clear()
       plt.close(ggg)     
     os.remove(areas_path)
     os.remove( perimeters_path)
     os.remove( circularities_path)
     total_time=time.clock() - start_time
     print(total_time, "total time per cell")
     print("total=", total)
     if counter==1:
        time_per_cell=total_time/total
        print("time_per_cell=", time_per_cell)
     else:
        print("another cell") 
#########################################
def plot_per_cell_info(pedigree, outpath, still_lineage, label_feedback, progress_bar, first_frame_number_p6,label_create_p6):
   start_time = time.clock()
   counter=0
   time_lapsed=0
   time_per_cell=0
   estimated_whole_time=0
   time_remaining=100
   list_of_cell_names =list(pedigree.keys())
   n_cells= len(list_of_cell_names)
   added_n_frames=0
   for cell in  list_of_cell_names:
            added_n_frames+=len(pedigree[cell])
   print("added_n_frames=",added_n_frames)
   red_patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"RED_LINEAGE_PATCHES")  
   plots_path= os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PLOTS")  
   one_cell_patches_path=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS" ,"PATCHES_FOR_RESULTS")   
   
   label_feedback.config(text="Cells discovered inside function:  " +str(list_of_cell_names))
   for cell_name in list_of_cell_names:# creatse folder for each cell in OUTPUT folder
     counter+=1
     label_feedback.config(text="Cells discovered:  " +str(list_of_cell_names)+"\nCreating results for:  " +str(cell_name))
     
     specific_cell_dirr=os.path.join(outpath,'RESULTS_PER_CELL',cell_name)    
     one_cell_images,red_patches,area_plots,perimeter_plots,circ_plots=[],[],[],[],[]
     
     cell_info=pedigree[cell_name]
     total=len(cell_info)# total number of frames for this particular cell       
     color=pedigree[cell_name][0][7]               
     mask = (still_lineage == color).all(axis=-1)
     x=np.zeros(still_lineage.shape,dtype = "uint8")
     x[mask]=[255,255,255]
     gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
     z=np.where(gray==255)
     rows,cols =z[0], z[1]
     points =[(rows[ii], cols[ii]) for ii in range(len(rows))]
     #####################  prepare areas and perims for plots    
     first_frame_num=cell_info[0][1]
     areas=[cell_info[i][4] for i in range(len(cell_info)) ]
     perimeters=[cell_info[i][5] for i in range(len(cell_info))]
     circularities=[cell_info[i][6] for i in range(len(cell_info))]
     frames=[cell_info[i][1] for i in range(len(cell_info))]
     centroids=[cell_info[i][3] for i in range(len(cell_info))]
     x=[frames[kk] for kk in range (len(frames))]     
     ############################################
     for i in range(len(cell_info)):
       progress_bar["value"]=(i/total)*100
       time_lapsed+=time_per_cell
       time_remaining= estimated_whole_time-time_lapsed
    
       if counter==1:
         text_time="Unknown"
       else:
          text_time=str(time_remaining)
       label_create_p6.config(text="Creating results for:  " +str(cell_name)+
                            "\nEstimated time remaining: "+text_time)
       ##################################
       im=cell_info[i][2]     
       one_cell_images.append(im)
       frame_number =cell_info[i][1]
       name =os.path.join(one_cell_patches_path,cell_name +"_patch_frame_%s" % frame_number)
       cv2.imwrite(name +".tif",im)

       init=still_lineage.copy()# plot red points in lineage              
       for k in range(len(points)):
          if points[k][0]==frame_number-first_frame_number_p6:        
              cv2.circle(init,(points[k][1], points[k][0]), 1,[0,0,255],-1)
       name =os.path.join(red_patches_path,cell_name +"_red_frame_%s" % frame_number)
       cv2.imwrite(name +".tif",init)
       red_patches.append(init) 
       #####################################
       #frame_number=frames[i]        
       plt.plot(x, areas, 'yo', markersize=5)
       area=cell_info[i][4]
       #plt.plot([frame_number],[areas[frame_number-first_frame_num]],'bo', markersize=10)
       plt.plot([frame_number],[area],'bo', markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Area')
       plt.title('Area of '+cell_name)
       
       areas_path=os.path.join(specific_cell_dirr,'areas.png')
       plt.savefig(areas_path)
       img = cv2.imread(areas_path)
       area_plot= Image.fromarray(img)        
       name =os.path.join(plots_path,cell_name +"_Area_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)
       plt.close() 
       
       g = plt.figure()
       plt.plot(x, areas, 'yo', markersize=5)
       plt.xlabel('Frame')
       plt.ylabel('Area')
       plt.title('Area of '+cell_name)       
       g.clear()
       plt.close(g)

       plt.plot(x, perimeters, 'go', linewidth=0.5)
       perimeter=cell_info[i][5]
       
       plt.plot([frame_number],[perimeter],'bo',markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Perimeter')
       plt.title('Perimeter '+cell_name)
       perimeters_path=os.path.join(specific_cell_dirr,'perimeters.png')
       plt.savefig(perimeters_path)
       img = cv2.imread(perimeters_path)
       
       perimeter_plot= Image.fromarray(img)         
       name =os.path.join(plots_path,cell_name +"_Perimeter_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)
       plt.close() 
       hh = plt.figure()
       plt.plot(x, perimeters, 'go', markersize=5)
       plt.xlabel('Frame')
       plt.ylabel('Perimeter')
       plt.title('Perimeter of '+cell_name)      
       hh.clear()
       plt.close(hh) 

       plt.plot(x, circularities, 'ro', linewidth=0.5)
       circularity=cell_info[i][6]
       plt.plot([frame_number],[circularity],'bo', markersize=10)
       plt.xlabel('Frame')
       plt.ylabel('Circularity')
       plt.title('Circularity '+cell_name)
       circularities_path=os.path.join(specific_cell_dirr,'circularities.png')
       plt.savefig(circularities_path)
       img = cv2.imread(circularities_path)       
       circ_plot= Image.fromarray(img)        
       name =os.path.join(plots_path,cell_name +"_Circularity_frame_%s" % frame_number)
       cv2.imwrite(name +".png",img)     
       plt.close()
       ggg = plt.figure()
       plt.plot(x, circularities, 'ro', linewidth=0.5)
       plt.xlabel('Frame')
       plt.ylabel('Circularity')
       plt.title('Circularity of '+cell_name)       
       ggg.clear()
       plt.close(ggg)     
     os.remove(areas_path)
     os.remove( perimeters_path)
     os.remove( circularities_path)
     total_time=time.clock() - start_time
     
     if counter==1:
        time_per_cell=total_time/total
        
        estimated_whole_time=added_n_frames*time_per_cell       
        time_lapsed+=total_time
        time_remaining= estimated_whole_time-time_lapsed
     
     
         