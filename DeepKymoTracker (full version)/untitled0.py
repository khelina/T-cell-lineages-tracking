import numpy as np
import itertools
import cv2
#################
def find_intensities(image):# find all intensities in an image
  x=list(np.unique(image))
  x.remove(0.0) 
  y=[float(format(float(str(x[i])), 'f')) for i in range(len(x))] 
  return y         
###############
# create intensitiy dictionary for n_cells.
# These intensities are powers of 2 divided by 1000000.
# for instance: for n_cells=2, int_dictionary={'1e-06': [0], '2e-06': [1], '3e-06': [0, 1]} 
def create_intensity_dictionary(n_cells):    
     cell_ids =[ii for ii in range(n_cells)]
     all_combinations =[]
     for i in range(1,n_cells+1):
          combinations = list(itertools.combinations(cell_ids, i))
          all_combinations+=combinations
    
     int_dictionary ={}    
     for k in range(len(all_combinations)):
         combo =all_combinations[k]
         summ=0
         for kk in range(len(combo)):
            summ+=2**combo[kk]
         int_dictionary[str(summ)]=list(combo) # summ=1,2,3,4,5,...
     return int_dictionary  
###############################################
init_image=cv2.imread(r"C:\Users\helina\Desktop\int_image.tif",-1)
init_intensities=find_intensities(init_image)
print('init_intensities=',init_intensities)
binaries=[bin(int(init_intensities[i]))[2:] for i in range(len(init_intensities))]
print('binaries=',binaries)
counts=[]
for k in range(len(binaries)):
   item=binaries[k]
   cnt = item.count('1')
   counts.append(cnt)
print('counts=',counts)
##################################################
intensity_dictionary_for_frame=create_intensity_dictionary(3)
print("intensity_dictionary_for_frame=", intensity_dictionary_for_frame)
################# clean mask of the cell
def remove_cell_from_mask(cell_number, init_image, intensity_dictionary_for_frame):

    keys=list(intensity_dictionary_for_frame.keys())
    print("keys=", keys)

    for key in keys:
        item=intensity_dictionary_for_frame[key]
        print("item=", item)
        if cell_number in item:
            bad_int=int(key)
            init_image[init_image==bad_int]=0
    return init_image
    
###########################################
init_image=remove_cell_from_mask(1, init_image, intensity_dictionary_for_frame)
cv2.imwrite(r"C:\Users\helina\Desktop\cleaned_image.tif",init_image)