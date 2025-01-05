import os
import cv2

source=r"D:\FEDERICO\Data15082018\Pos0301"
destin=r"C:\Users\asacco\OneDrive - Swinburne University\Desktop\PART_LAST_NE"
start_frame, last_frame=5001, 6000

for filename in os.listdir(source):
    if filename.endswith('.tif'):
        marker=int(filename[-13:-9])
        print("marker=", marker)
        if marker==last_frame+1:
            break
        if start_frame<=marker<=last_frame:
           full_name=os.path.join(source, filename)
           im=cv2.imread(full_name,-1)
           new_name=os.path.join(destin, filename)
           cv2.imwrite(new_name, im)



