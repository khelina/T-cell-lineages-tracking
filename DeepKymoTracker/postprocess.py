import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
#import xlsxwriter
import os
import pickle
import re 
from PIL import ImageTk, Image
#############################################################
Bordersize=100
#######################################################
def create_lineage(lineage,outpath, colours):
  print("Creating lineage_per_cell and saving it in pickle file")
  a=[(lineage[i].keys(),i) for i in range(len(lineage))]
  #############################################     debug
  
      
  ################################
  
  #print(a)
  names=[]
  for k in range(len(lineage)):
    item =lineage[k]
    keys =list(item.keys())
    names+=[item[key][11] for key in keys]
  cell_names =list(set(names))
  #for_print=[]
  pedigree ={}
  for name in cell_names:
    pedigree["cell-%s" % name]=[]
  #print("pedigree initialised=", pedigree)  
  for i in range(len(lineage)):
     #print("i=", i)
     item =lineage[i]
     keys =list(item.keys())
     #print("item_keys=", keys)
     for key in keys:
        cell_name=item[key][11]
        frame=item[key][12]
        cX,cY=item[key][6][0],item[key][6][1]
        a,b,c,d=item[key][7],item[key][8],item[key][9],item[key][10]
       
        patch_before=item[key][3]
      
        base=np.zeros((382+2*Bordersize,382+2*Bordersize),dtype="uint8")
        base[c:d,a:b]=patch_before
        patch_after=base[int(cY)-48+Bordersize:int(cY)+48+Bordersize,int(cX)-48+Bordersize:int(cX)+48+Bordersize]
        ############# debug
        #if key=="cell_0":
          
           #file_path=os. path.join("C:\\Users\\kfedorchuk\\Desktop\\AFTER", "patch_after_%s.tif" % i)
           #cv2.imwrite(file_path, patch_after)
           
        im2, contours, hierarchy = cv2.findContours(patch_after,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        #print("i=", i)
        #print("key=", key)                   
        area=np.round(cv2.contourArea(contours[0]),2)
        perimeter=np.round(cv2.arcLength(contours[0],True),2)
        circularity=np.round(4*math.pi*area/perimeter**2,2)
        patch_color=np.zeros((patch_after.shape[0], patch_after.shape[1],3), np.uint8)       
        #print("cell_name=", cell_name)
        patch_color[patch_after==255]=colours[cell_name][:-1]
        add=[cell_name,frame,patch_color,[cX,cY],area,perimeter,circularity]       
        pedigree["cell-%s" % item[key][11]].append(add)
        #for_print.append([cell_name,frame])
        
           
  pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
  
 
  with open(pedigree_path, 'wb') as f:
         pickle.dump(pedigree, f)

  return pedigree
####################################################################
def create_lineage_movie_1(pedigree,colours,template,outpath, coords_very_first, num_frames):
 lineage_images=[]
 print("Creating images for animated pedigree and saving them in TEMPORARY FOLDER")
 act_cells =list(pedigree.keys())
 print("act_cells=", act_cells)
 cell_names =["cell-"+item for item in template if "cell-"+item in act_cells ]
 print("cell_names=", cell_names)
 total_items =[pedigree[cell_name][-1][1] for cell_name in cell_names]
 print("total_items=", total_items) 
 total_processed =max(total_items)+1# this is the number of processed frames in the input movie
 print("total_processed=", total_processed)

 divisions =[]
 for item in cell_names:
     if pedigree[item][-1][1]!=total_processed-1:
       divisions.append((pedigree[item][-1][1]+1,pedigree[item][-1][0]))
 divisions.sort()
 print("divisions=", divisions)
 ###################################
 #num_frames=2553
 #first_text="1"
 #divisions=[[500, "1"],[1000, "10"],[1500, "11"], [2000, "100"]]
 
 first_text=template[:len(coords_very_first)]
  # create list of x-coordinates for lineage
 #print("first_text=", first_text)
 if len(coords_very_first)==1:
   xs ={"1":int(num_frames/2)}
 else:
    xs={}
    for i  in range(len(first_text)):
        xs[first_text[i]]=int((num_frames/(len(first_text)+1))*(i+1))
###########################
 #xs ={"1":int(num_frames/2)} 
 for k in range(len(divisions)):
       cell_name =divisions[k][1]        
       kk=len(cell_name)
       item_1=xs[cell_name]-num_frames/(2**(kk+1))
       item_2=xs[cell_name]+num_frames/(2**(kk+1))            
       xs[cell_name+"0"]=int(item_1)
       xs[cell_name+"1"]=int(item_2)              
 print("xs=", xs) 

##########################        
 """       
 print("xs_before=", xs)      
 for ii in range(len(xs)): 
  for k in range(len(divisions)):
       delta=
       cell_name =divisions[k][1]        
       kk=len(cell_name)
       item_1=xs[cell_name]-delta
       item_2=xs[cell_name]+delta            
       xs[cell_name+"0"]=int(item_1)
       xs[cell_name+"1"]=int(item_2)
              
 print("xs_after=", xs)
 """  
 ######################################
 whole=[]
 for k in range(len(cell_names)):    
    for i in range(len(pedigree[cell_names[k]])):              
      whole.append([pedigree[cell_names[k]][i][0],pedigree[cell_names[k]][i][1],xs[cell_names[k][5:]],colours[cell_names[k][5:]][:3]])                
 #print("whole", whole)
 # lin is a list of x-coordinates and colors for each x-cordinate
       
 lin=[[whole[i]  for i in range(len(whole)) if whole[i][1]==k] for k in range(total_processed)]        
 
 lin_dict=[]
 for k in range(len(lin)):
     item=lin[k]
     dictt={}
     for kk in range(len(item)):
         elem=item[kk]
         dictt[elem[0]]=(elem[1],elem[2],elem[3])
     lin_dict.append(dictt)
 #print("lin_dict=", lin_dict)

     
###### prepare lineage images ######
 temp_path=os.path.join(outpath,"TEMPORARY_FOLDER")
 #temp_path="C:\\Users\\kfedorchuk\\Desktop\\DeepKymoTracker\\OUTPUT_2\\TEMPORARY_FOLDER"
 points=[]# points for plotting animated lineage
 for i in range(total_processed):    
   frame =lin_dict[i]
   keys=list(frame.keys())
   for key in keys:
       points.append(((frame[key][1],i),frame[key][2]))                   
   for d in range(len(divisions)):  
       if i==divisions[d][0]:
          start=divisions[d][1]                   
          more_points=[((kk,i),frame[start+"1"][2]) for kk in range(xs[start],xs[start+"1"],1)]    
          points+=more_points
          more_points=[((kk,i),frame[start+"0"][2]) for kk in range(xs[start+"0"],xs[start],1)]    
          points+=more_points                     
   im=np.zeros((num_frames,num_frames,3),dtype = "uint8")# create black frame and draw a pedigree in it 
   #print("len(points)=", len(points))
     
   for p in range(len(points)):
      cv2.circle(im, points[p][0], 10, points[p][1], -1)  
   im1= cv2.resize(im,(382,382), interpolation = cv2.INTER_AREA)
   #cv2.putText(im1,"000",(200,60),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),1) 
   dest =os.path.join(temp_path,"tree_%s.tif" % (i+1))
   cv2.imwrite(dest, im1)
   lineage_images.append(im1)
 still_lineage=im
 cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\still_lineage.tif", still_lineage) 
 print("len(lineage_images_inside)=",len(lineage_images))
 print("points=", points)
 return lineage_images, still_lineage
      
###############################
###########################################
def create_per_cell_info(pedigree, dirr, still_lineage, colours):

   per_cell_dict={}
   list_of_cell_names =list(pedigree.keys())
   for cell_name in list_of_cell_names:# creatse folder for each cell in OUTPUT folder
     #print("cell_name=", cell_name)
     path=os.path.join(dirr,cell_name)
     one_cell_images=[]
     red_patches=[]
     area_plots=[]
     perimeter_plots=[]
     circ_plots=[]
     cell_info=pedigree[cell_name]
     """
     if not os.path.exists(path):
        os.mkdir(path)    
     patches_path=os.path.join(path,cell_name +"patches")# here I store patches of each cell
     if not os.path.exists(patches_path):
        os.mkdir(patches_path)   
     red_patches_path=os.path.join(path,cell_name +"red_patches")     
     if not os.path.exists(red_patches_path):
        os.mkdir(red_patches_path)
     area_plots_path=os.path.join(path,cell_name +"area_plots")     
     if not os.path.exists(area_plots_path):
        os.mkdir(area_plots_path)       
     perimeter_plots_path=os.path.join(path,cell_name +"perimeter_plots")     
     if not os.path.exists(perimeter_plots_path):
        os.mkdir(perimeter_plots_path)
     circ_plots_path=os.path.join(path,cell_name +"circ_plots")     
     if not os.path.exists(circ_plots_path):
        os.mkdir(circ_plots_path)  
     """
     color=colours[cell_name[5:]][:-1]
     print("color=", color)       
     mask = (still_lineage == color).all(axis=-1)
     x=np.zeros(still_lineage.shape,dtype = "uint8")
     x[mask]=[255,255,255]
     gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
     z=np.where(gray==255)
     rows,cols =z[0], z[1]
     points =[(rows[ii], cols[ii]) for ii in range(len(rows))]
     
     for i in range(len(cell_info)):
       im=cell_info[i][2]     
       one_cell_images.append(im)
       frame_number =cell_info[i][1]+1
       #name =os.path.join(patches_path,cell_name +"_frame_%s" % frame_number)
       #cv2.imwrite(name +".tif",im)
######################
       init=still_lineage.copy()              
       for k in range(len(points)):
          if points[k][0]==frame_number:        
              cv2.circle(init,(points[k][1], points[k][0]), 3,[0,0,255],-1)
       #name =os.path.join(red_patches_path,cell_name +"red_frame_%s" % frame_number)
       #cv2.imwrite(name +".tif",init)
       red_patches.append(init)       
#####################       
       
       
       
################ create and save each cell video 
     """      
     video_name =os.path.join(path, cell_name +".avi")      
     video = cv2.VideoWriter(video_name, 0, 7, (96,96))
     for i in range(len(one_cell_images)):
       im1 = cv2.cvtColor(one_cell_images[i],cv2.COLOR_GRAY2RGB)
       frame_num =cell_info[i][1]+1
       cv2.putText(im1,"FRAME %s" % frame_num,(1,15),cv2.FONT_HERSHEY_DUPLEX,1/3,(0,0,255),1)             
       video.write(im1)
     cv2.destroyAllWindows()
     video.release() 
     """
##########################  plot diagrams
     a=pedigree[cell_name]
     first_frame_num=a[0][1]
     areas=[]
     perimeters=[]
     circularities=[]
     frames=[]
     centroids=[]
     
     for k in range(len(a)):
      areas.append(a[k][4])
      perimeters.append(a[k][5])
      circularities.append(a[k][6])
      frames.append(a[k][1])
      centroids.append(a[k][3])

     #x = [i for i in range(first_frame_num,first_frame_num +len(a),1)]
     x=frames
     """
     red_patches_path=os.path.join(path,cell_name +"red_patches")# here I store patches of each cell
     if not os.path.exists(red_patches_path):
        os.mkdir(patches_path)
     for xx in x:
        empty=still_linage_big_size
        cv2.circle(empty, (points[p][0][0],i), 2, (0,0,255), -1)
        im1= cv2.resize(empty,(382,382), interpolation = cv2.INTER_NEAREST)
     """
     
      
         
     area_plots=[] 
     perimeter_plots=[]
     circ_plots=[]
     for i in range(len(cell_info)):
       frame_number=frames[i]  
       #frame_number =cell_info[i][1]
       plt.plot(x, areas, 'yo', linewidth=0.5)
       plt.plot([frame_number],[areas[frame_number-first_frame_num]],'bo', linewidth=3.0)
       plt.xlabel('Frame')
       plt.ylabel('Area')
       plt.title('Area of '+cell_name)
       plt.savefig('areas.png')
       img = cv2.imread("areas.png")
       area_plot= Image.fromarray(img)
       area_plots.append(area_plot)    
       #name =os.path.join(area_plots_path,cell_name +"_frame_%s" % frame_number)
       #cv2.imwrite(name +".png",img)
       plt.close()      
    

       plt.plot(x, perimeters, 'go', linewidth=0.5)
       plt.plot([frame_number],[perimeters[frame_number-first_frame_num]],'bo',linewidth=3.0)
       plt.xlabel('Frame')
       plt.ylabel('Perimeter')
       plt.title('Perimeter '+cell_name)
       plt.savefig('perimeters.png')
       img = cv2.imread("perimeters.png")
       perimeter_plot= Image.fromarray(img)
       perimeter_plots.append(perimeter_plot)    
       #name =os.path.join(perimeter_plots_path,cell_name +"_frame_%s" % frame_number)
       #cv2.imwrite(name +".png",img)
       plt.close()   

       plt.plot(x, circularities, 'ro', linewidth=0.5)
       plt.plot([frame_number],[circularities[frame_number-first_frame_num]],'bo', linewidth=3.0)
       plt.xlabel('Frame')
       plt.ylabel('Circularity')
       plt.title('Circularity '+cell_name)
       plt.savefig('circularities.png')
       img = cv2.imread("circularities.png")
       circ_plot= Image.fromarray(img)
       circ_plots.append(circ_plot)    
       #name =os.path.join(circ_plots_path,cell_name +"_frame_%s" % frame_number)
       #cv2.imwrite(name +".png",img)
       
       
       plt.close()
     per_cell_dict[cell_name]=[one_cell_images,areas,perimeters,circularities,\
                               area_plots, perimeter_plots, circ_plots, frames, centroids,red_patches] 
################### CREATE EXCEL FILE  #############
     """
     workbook = xlsxwriter.Workbook(os.path.join(path,cell_name +".xlsx"))
 
     worksheet = workbook.add_worksheet()
     worksheet.set_column('B:B',12)
     worksheet.set_column('F:F',12)
     worksheet.set_column('G:G',12)
     worksheet.set_column('C:C',5)
     worksheet.set_column('D:D',5)
     worksheet.write('A1', 'Cell name')
     worksheet.write('B1', 'Frame')
     worksheet.write('C1', 'cX')
     worksheet.write('D1', 'cY')
     worksheet.write('E1', 'Area')
     worksheet.write('F1', 'Perimeter')
     worksheet.write('G1', 'Circularity') 
     row = 1
     x=pedigree[cell_name]
     for i in range(len(x)): 
      score = [cell_name, "Frame %s" % (x[i][1]+1), x[i][3][0],x[i][3][1],x[i][4],x[i][5],x[i][6]]
      for k in range(len(score)):
         worksheet.write(row, k, score[k])
      row+=1
    
     worksheet.insert_image('I1', 'areas.png')
     worksheet.insert_image('R1', 'perimeters.png')
     worksheet.insert_image('I21', 'circularities.png')    
     workbook.close()
     """    
   return per_cell_dict
#######################################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##################################################
def load_files(folder_dir):
 images=[]
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith(".tif"):
        full_name=os.path.join(folder_dir, filename)      
        image=cv2.imread(full_name,1)
        images.append(image)       
 return images
##########################################################

"""
pedigree_path="C:\\Users\\kfedorchuk\\Desktop\\DeepKymoTracker\\OUTPUT-2\\pedigree.pkl"        
with open(pedigree_path, 'rb') as f:
    pedigree = pickle.load(f)
"""
############################



def create_lineage_movie(pedigree,colours,template,outpath):
 print("Creating images for animated pedigree and saving them in TEMPORARY FOLDER")
 act_cells =list(pedigree.keys())
 cell_names =["cell-"+item for item in template if "cell-"+item in act_cells ]
 total_items =[pedigree[cell_name][-1][1] for cell_name in cell_names]   
 total =max(total_items)# this is the number of frames in the input movie
 
 divisions =[]
 for item in cell_names:
     if pedigree[item][-1][1]!=total:
       divisions.append((pedigree[item][-1][1]+1,pedigree[item][-1][0]))
 divisions.sort()
 print("divisions=", divisions)
 ###################################
 # create list of x-coordinates for lineage
 xs ={"1":int(total/2)} 
 for k in range(len(divisions)):
       cell_name =divisions[k][1]        
       kk=len(cell_name)
       item_1=xs[cell_name]-total/(2**(kk+1))
       item_2=xs[cell_name]+total/(2**(kk+1))            
       xs[cell_name+"0"]=int(item_1)
       xs[cell_name+"1"]=int(item_2)              
 print("xs=", xs)     
 #################################
 whole=[]
 for k in range(len(cell_names)):    
    for i in range(len(pedigree[cell_names[k]])):              
      whole.append([pedigree[cell_names[k]][i][0],pedigree[cell_names[k]][i][1],xs[cell_names[k][5:]],colours[cell_names[k][5:]][:3]])                
 
 # lin is a list of x-coordinates and colors per frame
       
 lin=[[whole[i]  for i in range(len(whole)) if whole[i][1]==k] for k in range(total)]        
 
 lin_dict=[]
 for k in range(len(lin)):
     item=lin[k]
     dictt={}
     for kk in range(len(item)):
         elem=item[kk]
         dictt[elem[0]]=(elem[1],elem[2],elem[3])
     lin_dict.append(dictt)
     
###### prepare lineage images ######
 temp_path=os.path.join(outpath,"TEMPORARY_FOLDER")
 #temp_path="C:\\Users\\kfedorchuk\\Desktop\\DeepKymoTracker\\OUTPUT_2\\TEMPORARY_FOLDER"

 points=[]# points for plotting animated lineage
 for i in range(total):  
   for d in range(len(divisions)): 
     frame =lin_dict[i]
     keys=list(frame.keys())
     for key in keys:
       points.append(((frame[key][1],i),frame[key][2]))                   
      
       if i==divisions[d][0]:
          start=divisions[d][1]                   
          more_points=[((kk,i),frame[start+"1"][2]) for kk in range(xs[start],xs[start+"1"],1)]    
          points+=more_points
          more_points=[((kk,i),frame[start+"0"][2]) for kk in range(xs[start+"0"],xs[start],1)]    
          points+=more_points 
          
   im=np.zeros((total,total,3))# create black frame and draw a pedigree in it   
   for p in range(len(points)):
      cv2.circle(im, points[p][0], 1, points[p][1], -1)
           
   im1= cv2.resize(im,(382,382), interpolation = cv2.INTER_AREA)
   #cv2.putText(im1,"000",(200,60),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),1) 
   dest =os.path.join(temp_path,"tree_%s.tif" % (i+1))
   cv2.imwrite(dest, im1)
      
 ##################################################
 div_dict ={}
 for item in divisions:
    div_dict[item[1]]=item[0]
 print("div_dict", div_dict)    
 yy ={}
 for fullkey in cell_names:
    key=fullkey[5:]
    if key=="1":
       yy[key]=int(div_dict[key]/2)
    else:
       if (key in div_dict):
        yy[key]=int((div_dict[key]+div_dict[key[:-1]])/2)
       else:
        yy[key]=int((total+div_dict[key[:-1]])/2)
 print("yy", yy)
########################################
 print("Creating still lineage and saving as .tif")
 still_lineage=im1
 #######################
 """ 
 wid=10# for letters
 height=10
 coeff =382/total
 div_points =[]
 for item in divisions:
     key=item[1]
     x,y=int(xs[key]*coeff),int(item[0]*coeff)     
     div_points.append((x,y))
     cv2.circle(still_lineage, (x,y), 5, [255,255,255], -1)
     cv2.putText(still_lineage,"%s" % item[0],(x-15,y+20),cv2.FONT_HERSHEY_PLAIN,1,[255,255,255],1)
 
 for item in cell_names:     
   patch=np.zeros((382,382,3))
   key=item[5:]
   xc=int(xs[key]*coeff)
   yc=int(yy[key]*coeff)
   length =len(key)
   width=int(length*wid/2)
   cv2.putText(patch,item[5:],(191-width,191+5),cv2.FONT_HERSHEY_PLAIN,1,Colors[key],1)
   patch=patch[191-height:191+height,191-width:191+width] 
   #cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\patch.tif", patch)
   still_lineage[yc-height:yc+height,xc-width:xc+width]= patch 
 """
 cv2.imwrite(os.path.join(outpath,"lineage.tif"), still_lineage)
 #######################
 
############ prepare images for movie

 print("Creating images for movie and saving in TEMPORARY_FOR_MOVIE folder")
 images_out_path=os.path.join(outpath,"TEMPORARY_FOR_MOVIE")

 images_seg=load_files(os.path.join(outpath,"TRACKED_PLUS_CONTOURS"))
 images_lin=load_files(temp_path)
 images=[]
 for i in range(len(images_lin)):
    img=np.zeros((382,382*2,3))
    img[:,:382,:]=images_seg[i]
    img[:,382:,:]=images_lin[i]
    images.append(img)
    destin=os.path.join(images_out_path,"movie_%s.tif" % (i+1))
    cv2.imwrite(destin, img)
############## create and save movie
 print("Creating output movie and saving as .avi")
 #image_folder = images_out_path
 video_name = os.path.join(outpath,"lineage_.avi")

 #images = [img for img in os.listdir(image_folder) if img.endswith(".tif")]
 #frame = cv2.imread(os.path.join(image_folder, images[0]))
 frame=images[0]
 height, width, layers = frame.shape
 video = cv2.VideoWriter(video_name, 0, 10, (width,height))
 for image in images:
    #video.write(cv2.imread(os.path.join(image_folder, image)))
    video.write(np.uint8(image))
 cv2.destroyAllWindows()
 video.release()
 print("Finished")

