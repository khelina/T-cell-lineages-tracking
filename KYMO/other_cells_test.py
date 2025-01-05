import os
import cv2

source=r"C:\Users\helina\Downloads\PhC-C2DL-PSC\PhC-C2DL-PSC\01"
destination=r"C:\Users\helina\Desktop\tracking new_alessandra\INPUT_MOVIE_PSC\01"
if not os.path.exists(destination):
    os.makedirs(destination)
i=0
for filename in os.listdir(source):
     i+=1
     print("filename=",filename)
     old_full_name=os.path.join(source,filename)
     print("old_full_name=",old_full_name)
     #number=old_full_name[-8:-4]
     #print("number=",number)
     number=i
     base=old_full_name[:-11]
     print("base=",base)
     image=cv2.imread( old_full_name, -1)
     image_cut=image[:,:576]
     print("image_cut.shape=",image_cut.shape)
     new_number ="t"+str(number).zfill(3)
     new_name=new_number+"_ch00.tif"
     print("new_name=",new_name)
     full_name=os.path.join(destination,new_name)
     print("full_name=",full_name)
     cv2.imwrite(full_name,image_cut)
########## turn their lebales into binary (step 1)
import numpy as np
names =[]
init_dir=r"C:\Users\helina\Desktop\BLUR_RESULT\01_ERR_SEG"
for filename in os.listdir(init_dir):
     old_full_name=os.path.join(init_dir,filename)
     names.append(filename)
     

final_dir=r"C:\Users\helina\Desktop\BLUR_RESULT\LABELS"

for i in range(len(names)):
    filename=names[i]
    old_full_name=os.path.join(init_dir,filename)
    im=cv2.imread(old_full_name, -1)
    binary_image=np.zeros(im.shape,np.uint8)
    binary_image[im!=0]=255
    new_name=os.path.join(final_dir,filename)
    cv2.imwrite(new_name,binary_image)
######################rename masks for results
source=r"C:\Users\helina\Desktop\tracking new_alessandra\OUTPUT_BLUR\MASKS"
dest=r"C:\Users\helina\Desktop\BLUR_RESULT\12_RES"
i=-1
for filename in os.listdir(source):
     i+=1
     old_full_name=os.path.join(source,filename)
     im=cv2.imread(old_full_name, -1)
     new_name="mask"+str(i).zfill(3)+".tif"
     new_full_name=os.path.join(dest,new_name)
     cv2.imwrite(new_full_name,im)
######################################
import numpy as np
my_results_dir=r"C:\Users\helina\Desktop\BLUR_RESULT\12_RES"
binary_dir=r"C:\Users\helina\Desktop\BLUR_RESULT\LABELS"
final_labels_dir=r"C:\Users\helina\Desktop\BLUR_RESULT\TRA"
i=-1
for filename in os.listdir(binary_dir):
    i+=1
    binary_name=os.path.join(binary_dir,filename)
    my_result_name=os.path.join(my_results_dir,filename)
    seg_name="man_track"+str(i).zfill(3)+".tif"
    full_seg_name=os.path.join(final_labels_dir,seg_name)
    ##########################################
    result_image=cv2.imread(my_result_name,-1)
    seg_label_image=np.zeros(im.shape,np.uint16)
    binary_image=cv2.imread(binary_name,-1)
    im2, contours, hierarchy = cv2.findContours(binary_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:         
         test_image=np.zeros((binary_image.shape),dtype="uint8")
         test_image=cv2.drawContours(test_image,[cnt],0,255, -1)
         max_int =np.max(result_image[test_image==255])
         #print(" max_int =", max_int )
         if max_int!=0:
              seg_label_image[test_image==255]=max_int
    cv2.imwrite(full_seg_name, seg_label_image)
        
    
    
    