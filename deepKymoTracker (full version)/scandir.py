
import os
import time
import cv2
 
 
path_big = r"D:\FEDERICO\Data15082018\Pos0301"
path_small=r"D:\FEDERICO\Data15082018\Pos0701"

path_long=r"D:\FEDERICO\Data15082018\Pos0301\exp_130424 UGFP OT1 chAp2a2 DCs IL2 microman_Pos0301_t00025_ch00.tif"
path_short=r"D:\FEDERICO\Data15082018\Pos0701\exp_130614 UFGP OT1 DCS IL2 PE62L microman_Pos0701_t0023_ch00.tif"
################### small folder


start=time.time()
clip=[]
basename="D:\\FEDERICO\\Data15082018\\Pos0701\\exp_130614 UFGP OT1 DCS IL2 PE62L microman_Pos0701_t00"
for i in range(10,18,1):
    current_name="%s_ch00.tif" % (i+1)
    filename=basename +current_name
    print(filename)
    im_short=cv2.imread(filename, -1)
    clip.append(im_short)
finish_1=time.time()
for i in range(20,28,1):
    current_name="%s_ch00.tif" % (i+1)
    filename=basename +current_name
    print(filename)
    im_short=cv2.imread(filename, -1)
    clip.append(im_short)
finish_2=time.time()
elapsed_time_1=finish_1-start
elapsed_time_2=finish_2-finish_1
print("elapsed_time_1=", elapsed_time_1)
print("elapsed_time_2=", elapsed_time_2)
################   big folder

start=time.time()
clip=[]
basename="D:\FEDERICO\Data15082018\Pos0301\exp_130424 UGFP OT1 chAp2a2 DCs IL2 microman_Pos0301_t000"
for i in range(10,18,1):
    current_name="%s_ch00.tif" % (i+1)
    filename=basename +current_name
    print(filename)
    im_long=cv2.imread(filename, -1)
    clip.append(im_long)
finish_1=time.time()
for i in range(20,28,1):
    current_name="%s_ch00.tif" % (i+1)
    filename=basename +current_name
    print(filename)
    im_long=cv2.imread(filename, -1)
    clip.append(im_long)
finish_2=time.time()
elapsed_time_1=finish_1-start
elapsed_time_2=finish_2-finish_1
print("elapsed_time_1=", elapsed_time_1)
print("elapsed_time_2=", elapsed_time_2)
############################################# 
obj = os.scandir(path)
def load_one_clip(obj, start):
     clip_names=[]
     counter=0
     for entry in obj:
          counter+=1
          if (counter>=start) and (counter<=start+8):
             clip_names.append(entry.name)                    
          if counter==start+8:
              break
     return clip_names    
            
names= load_one_clip(obj, 7*2+1)
names          
            
obj.close()
##############################

def usingPIL(f): 
    im = Image.open(f)
    return np.asarray(im) 
def load_clip(k,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number): 
  fluor_names, bright_names =[],[]   
  fluor_images,fluor_images_compressed,bright_images=[],[],[]  
  for kk in range(4):
   if k+kk<num_frames:
    fluor_name=full_core_fluor_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch00.tif"  
    fluor_names.append(fluor_name)
    raw = cv2.imread(fluor_name, -1) 
    fluor_images.append(raw)
    raw2 = raw.copy()
    fluor_compressed = cv2.resize(raw2, (100, 100), interpolation=cv2.INTER_AREA)
    fluor_images_compressed.append(fluor_compressed)
    
    bright_name=full_core_bright_name+str(k+1+kk+first_frame_number).zfill(n_digits)+"_ch02.tif"
    bright_names.append(bright_name)
    bright= cv2.imread(bright_name, -1) # was 0   
    bright_images.append(bright)
    #print("bright_name=",bright_name)
    #print("fluor_name=",fluor_name)
  return  fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names    
#############################3

for filename in os.listdir(path):
    print(filename)

# A Simple Python program to demonstrate working
# of yield
 
# A generator function that yields 1 for the first time,
# 2 second time and 3 third time
 
 
def simpleGeneratorFun(start):
    yield start+1
    yield start+2
    yield start+3
 
 
# Driver code to check above generator function
start=5
for value in simpleGeneratorFun(start):
    print(value)
##############################

# A Python program to generate squares from 1
# to 100 using yield and therefore generator
 
# An infinite generator function that prints
# next square number. It starts with 1
 
 
def nextSquare():
    i = 1
 
    # An Infinite loop to generate squares
    while True:
        yield i*i
        i += 1  # Next execution resumes
        # from this point
 
 
# Driver code to test above generator
# function
for num in nextSquare():
    if num > 100:
        break
    print(num)