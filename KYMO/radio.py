from tkinter import *


root.mainloop()

import cv2
import numpy as np

im=cv2.imread(r"C:\Users\helina\Desktop\still_lineage.tif", -1)

im1=cv2.resize(im, (382,382), interpolation = cv2.INTER_LINEAR)
cv2.imwrite(r"C:\Users\helina\Desktop\result.tif", im1)

im_new=np.zeros((3000,3000*2+100,3), np.uint8)
im_new[:3000,:3000, :]=im
cv2.imwrite(r"C:\Users\helina\Desktop\new_result.tif", im_new)


im2=cv2.resize(im_new, (382+100*2,382), interpolation = cv2.INTER_LINEAR)
cv2.imwrite(r"C:\Users\helina\Desktop\result_final.tif", im2)
