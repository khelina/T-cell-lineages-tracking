import os
import pickle
import cv2
#outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE r"
outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE r"
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
lineage_per_frame=extract_lineage(outpath)
print("len(lineage_per_frame)=",len(lineage_per_frame))
destination="C:\\Users\\helina\\Desktop\\DEBUG"
x=lineage_per_frame
x[0].keys()

check_list=[]
for i in range(len(x)):
    item=x[i]
    keys=list(item.keys())
    print("keys=", keys)
    for key in keys:        
        frame_number=item[key][12]
        ext_cell_name=item[key][11]
        centr=item[key][6]
        check_list.append((key,frame_number,ext_cell_name))
        patch=item[key][3]
        patch_path=os.path.join(destination,"patch_%s.tif" %(i))
        cv2.imwrite(patch_path,patch)
    
print(check_list)

###############################
#################################################
###################################################
import pickle
import os
outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE_SHORT"
def extract_changeable_params_history(outpath):
    ch_parameters_path=os.path.join(outpath,"changeble_movie_parameters_history.pkl")
    list_of_ch_movie_params = []
    with (open(ch_parameters_path, "rb")) as openfile:
     while True:
        try:
            list_of_ch_movie_params.append(pickle.load(openfile))
        except EOFError:
            break
    #xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells= list_of_ch_movie_params[0],list_of_ch_movie_params[1],list_of_ch_movie_params[2],\
    #list_of_ch_movie_params[3],list_of_ch_movie_params[4],list_of_ch_movie_params[5],list_of_ch_movie_params[6],list_of_ch_movie_params[7],list_of_ch_movie_params[8]
    #return xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells
    return list_of_ch_movie_params
###################################################
list_of_ch_movie_params=extract_changeable_params_history(outpath)
print("list_of_ch_movie_params = ",list_of_ch_movie_params)
print("len(list_of_ch_movie_params)=",len(list_of_ch_movie_params))
####################################################
##########################################################
################################################################
import pickle
import os
outpath=r"C:\Users\helina\Desktop\DeepKymoTracker\OUTPUT_INPUT_MOVIE_SHORT"
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
lineage_per_frame =extract_lineage(outpath)
print("lineage_per_frame  = ",lineage_per_frame )
print("len(lineage_per_frame)  = ",len(lineage_per_frame ))
 
############################################
################################################
###################################
import pickle
import os
outpath=r"C:\Users\helina\Desktop"
##############################################
def record_list(llist,outpath, mode):# was cells
    destin_path=os.path.join(outpath,"experiment_pickle.pkl")  
    with open(destin_path, mode) as f:
        pickle.dump(llist, f,protocol=pickle.HIGHEST_PROTOCOL)
        #for i in range(len(llist)):
           #pickle.dump(llist[i], f,protocol=pickle.HIGHEST_PROTOCOL)
#####################################################llist
llist=[[1,0],[2,1],4,8,16]
record_list(llist,outpath, "wb")
new_list=[32, 64]
record_list(new_list,outpath, "ab")
###########################################
def extract_list(outpath):
    lineage_path=os.path.join(outpath,"experiment_pickle.pkl")
    extracted_list = []
    with (open(lineage_path, "rb")) as openfile:
     while True:
        try:
             extracted_list.append(pickle.load(openfile))
        except EOFError:
            break    
    return  extracted_list
#######################################
extracted_list =extract_list(outpath)
print(" extracted_list  = ", extracted_list )
print(" len(extracted_list)  = ",len( extracted_list ))
extracted_list[1]
#####################################
######### area of contour and pixel count are different
import cv2
import numpy as np
im = cv2.imread(r"C:\Users\helina\Desktop\contour.tif")
a = np.array(im[:,:,0])
_, contour, _ = cv2.findContours(a,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
area = cv2.contourArea(contour[0])
print(area)
print(np.count_nonzero(a))