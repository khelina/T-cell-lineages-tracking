import pickle
import os
import xlsxwriter
import numpy as np
import cv2
from preprocess import extract_red_frame_numbers
###############################################
Bordersize=100
#######################################

def update_changeable_params_history(changeable_params_history,outpath, mode):# was cells
    ch_param_path=os.path.join(outpath,"changeble_movie_parameters_history.pkl")  
    with open(ch_param_path, mode) as f:
        #pickle.dump(changeable_params_history, f,protocol=pickle.HIGHEST_PROTOCOL)
        for i in range(len(changeable_params_history)):
           pickle.dump(changeable_params_history[i], f,protocol=pickle.HIGHEST_PROTOCOL)
#############################################################
def extract_changeable_params_history(outpath, start_frame_internal):
    ch_parameters_path=os.path.join(outpath,"changeble_movie_parameters_history.pkl")
    changeable_params_history = []
    with (open(ch_parameters_path, "rb")) as openfile:
     while True:
        try:
            changeable_params_history.append(pickle.load(openfile))
        except EOFError:
            break
    p= start_frame_internal
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells=  changeable_params_history[p][0], changeable_params_history[p][1], changeable_params_history[p][2],\
    changeable_params_history[p][3], changeable_params_history[p][4], changeable_params_history[p][5], changeable_params_history[p][6], changeable_params_history[p][7], changeable_params_history[p][8]
    #print("history_of_ch_movie_params[-1]=",  history_of_ch_movie_params[-1])
    #print("len(history_of_ch_movie_params)=", len( history_of_ch_movie_params))    
    return xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history    
######################################## 
def update_lineage(llist,outpath, mode):# was cells
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")  
    with open(lineage_path, mode) as f:
        for i in range(len(llist)):
           pickle.dump(llist[i], f,protocol=pickle.HIGHEST_PROTOCOL)
####################################
def extract_const_movie_parameters(outpath):
    parameters_path=os.path.join(outpath,"constant_movie_parameters.pkl")
    list_of_const_movie_params = []
    with (open(parameters_path, "rb")) as openfile:
     while True:
        try:
            list_of_const_movie_params.append(pickle.load(openfile))
        except EOFError:
            break
    #print("list_of_const_movie_params", list_of_const_movie_params)
    frame_size, true_cell_radius_pickle, patch_size,max_number_of_cells,\
    num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number,\
    base_colours,contrast_value, number_cells_in_first_frame= list_of_const_movie_params[0],list_of_const_movie_params[1],list_of_const_movie_params[2],\
    list_of_const_movie_params[3],list_of_const_movie_params[4],list_of_const_movie_params[5],list_of_const_movie_params[6],list_of_const_movie_params[7],list_of_const_movie_params[8],\
    list_of_const_movie_params[9],list_of_const_movie_params[10],list_of_const_movie_params[11]
    
    return frame_size, true_cell_radius_pickle, patch_size,max_number_of_cells,\
           num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number,\
           base_colours,contrast_value,number_cells_in_first_frame
##########################
def extract_lineage(outpath):
    lineage_path=os.path.join(outpath,"lineage_per_frame.pkl")
    lineage_per_frame = []
    with (open(lineage_path, "rb")) as openfile:
     while True:
        try:
            lineage_per_frame.append(pickle.load(openfile))
        except EOFError:
            break    
    return lineage_per_frame
##############################
#####################################

###################################################
def load_red_names(source):
 red_names=[]
 for filename in os.listdir(source):        
    if filename.endswith("ch01.tif"):
     full_name=os.path.join(source, filename)
     red_names.append(full_name)    
 red_names_sorted =sorted(red_names)
 #print("len(red_names_sorted INSIDE)=",len(red_names_sorted))
 return red_names_sorted
###############################################

#######################################

def create_lineage_per_cell(lineage_per_frame,outpath, frame_size):
  software_dir,output_dir=os.path.split(outpath)
  origin= os.path.join(software_dir,output_dir[7:])
  red_names_sorted=load_red_names(origin)
  list_of_red_numbers =extract_red_frame_numbers(red_names_sorted)
  #print("len(red_names_sorted)=", len(red_names_sorted))
  names=[]
  for k in range(len(lineage_per_frame)):
    item =lineage_per_frame[k]
    keys =list(item.keys())
    names+=[item[key][11] for key in keys]
  cell_names =list(set(names))# all cell names encountered in movie
  dirr=os.path.join(outpath,"CELLS_INFO_WITHOUT_DIAGRAMS_EXCEL")
  if not os.path.exists(dirr):
        os.mkdir(dirr)
  #list_of_cell_names =list(lineage_per_cell.keys())
  for cell_name in cell_names:#
      path=os.path.join(dirr,cell_name)# create folders "1", "10", etc. for segmented images of each cell  
      if not os.path.exists(path):
          os.mkdir(path)
      subdirs=["Segmented frames", "Segmented patches","Fluor patches","Red patches"]
      for sub in subdirs:
          subdir=os.path.join(path,sub)
          if not os.path.exists(subdir):
             os.mkdir(subdir) 
  
  pedigree_per_cell ={}

  for name in cell_names:
    pedigree_per_cell[name]=[]
    for i in range(len(lineage_per_frame)):   
      item =lineage_per_frame[i]
      frame_keys =list(item.keys())     
      for key in frame_keys:
          cell_id=item[key][11]
          if name==cell_id:
           
            
            frame_number=item[key][12]
            cX,cY=item[key][6][0],item[key][6][1]
            area=item[key][18]
            perimeter=item[key][19]
            circularity=item[key][20]
            bounding_box=item[key][2]
            ####
            #print("name = ", name)
            #print("key = ", key)
            #print("cell_id = ", cell_id)
            big_patch_border=np.zeros((frame_size+2*Bordersize, frame_size+2*Bordersize), np.uint8)
            a,b,c,d=item[key][7], item[key][8],item[key][9], item[key][10]
            big_patch_border[c:d,a:b]=item[key][3]

            big_one_cell_image=big_patch_border[Bordersize:frame_size+Bordersize,Bordersize:frame_size+Bordersize]
            destin_big=os.path.join(dirr, cell_id,"Segmented frames")
            big_name=os.path.join(destin_big,"segm_frame_cell_%s_frame_%s.tif" % (cell_id,frame_number))
            cv2.imwrite(big_name,big_one_cell_image)
            
            #######
            segm_patch=item[key][3]
            destin_segm=os.path.join(dirr, cell_id,"Segmented patches")
            segm_name=os.path.join(destin_segm,"segm_patch_cell_%s_frame_%s.tif" % (cell_id,frame_number))
            cv2.imwrite(segm_name,segm_patch)
            
            ############
            fl_init=item[key][4]
            fl_border=np.copy(fl_init)
            fl_border[big_patch_border==0]=0
            fl_patch= fl_border[c:d,a:b]
            av_fluor=np.round(np.ma.masked_equal(fl_patch, 0).mean(), 2)# average intensity of fluor cell
                     
            destin_fl_patch=os.path.join(dirr, cell_id,"Fluor patches")
            
            fl_patch_name=os.path.join(destin_fl_patch,"fluor_patch_cell_%s_frame_%s.tif" % (cell_id,frame_number))
            cv2.imwrite(fl_patch_name,fl_patch)
            
            if frame_number in list_of_red_numbers:
               index=list_of_red_numbers.index(frame_number)
               red_name= red_names_sorted[index]           
               red_image=cv2.imread(red_name,-1)           
               red_border=cv2.copyMakeBorder(red_image, top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value = np.mean(red_image))            
               red_border[big_patch_border==0]=0
               red_patch= red_border[c:d,a:b]            
               destin_red_patch=os.path.join(dirr, cell_id,"Red patches")
               red_patch_name=os.path.join(destin_red_patch,"red_patch_cell_%s_frame_%s.tif" % (cell_id,frame_number))
               cv2.imwrite(red_patch_name,red_patch)
               av_red=np.round(np.ma.masked_equal(red_patch, 0).mean(), 2)
            else:
                av_red="---"
            ######################################
            
            add=[frame_number,[cX,cY],area,perimeter,circularity, bounding_box, av_fluor, av_red] 
            pedigree_per_cell[name].append(add)
  print("  list_of_red_numbers=",   list_of_red_numbers)             
  pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
  with open(pedigree_path, 'wb') as f:
         pickle.dump(pedigree_per_cell, f)  
  return pedigree_per_cell
###############################################
def create_lineage_for_Lorenzo(outpath, frame_size):
    #print("outpath=", outpath)
    lineage_per_frame=extract_lineage(outpath)
    lineage_per_cell=create_lineage_per_cell(lineage_per_frame,outpath, frame_size)
    
    dirr=os.path.join(outpath,"CELLS_INFO_WITHOUT_DIAGRAMS_EXCEL")
    if not os.path.exists(dirr):
        os.mkdir(dirr)
    list_of_cell_names =list(lineage_per_cell.keys())
    for cell_name in list_of_cell_names:#
       path=os.path.join(dirr,cell_name)# create folders "1", "10", etc. for segmented images of each cell  
       if not os.path.exists(path):
          os.mkdir(path)
       x=lineage_per_cell[cell_name]
             
       #print("path for excel=", path)
       workbook = xlsxwriter.Workbook(os.path.join(path,cell_name +".xlsx"))     
       worksheet = workbook.add_worksheet()
       worksheet.set_column('B:B',12)
       worksheet.set_column('F:F',12)
       worksheet.set_column('G:G',12)
       worksheet.set_column('C:C',5)
       worksheet.set_column('D:D',5)
       worksheet.set_column('H:H',5)
       worksheet.set_column('I:I',5)
       worksheet.set_column('J:J',5)
       worksheet.set_column('K:K',5)
       worksheet.set_column('L:L',12)
       worksheet.set_column('M:M',12)
       
       
       worksheet.write('A1', ' Cell name')
       worksheet.write('B1', ' Frame')
       worksheet.write('C1', '  cX')
       worksheet.write('D1', '  cY')
       worksheet.write('E1', ' Area')
       worksheet.write('F1', ' Perimeter')
       worksheet.write('G1', ' Circularity')
       worksheet.write('H1', '  x')
       worksheet.write('I1', '  y')
       worksheet.write('J1', '  w')
       worksheet.write('K1', '  h')
       worksheet.write('L1', '  Av_fluor')
       worksheet.write('M1', '  Av_red')
       #x=lineage_per_cell[cell_name]
       
       row = 1
       for i in range(len(x)): 
          score = [cell_name, "Frame %s" % (x[i][0]), x[i][1][0],x[i][1][1],x[i][2],x[i][3],x[i][4],x[i][5][0],
                   x[i][5][1],x[i][5][2],x[i][5][3],x[i][6],x[i][7] ]
          ['None' if v is None else v for v in score]
          #print("score=", score)
          #one_cell_big_image=x[i][6]
          #file_name=os.path.join(path,"cell_%s_frame_%s.tif" % (cell_name,x[i][0]+1))
          #cv2.imwrite(file_name,one_cell_big_image)
          for k in range(len(score)):
            worksheet.write(row, k, score[k])
          row+=1
        
       workbook.close()
    return lineage_per_cell