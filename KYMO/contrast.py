import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import *

cwd = os.getcwd()

from interface_functions import turn_image_into_tkinter


win= tk.Tk()
global window_size, image, cliplimit, init_image, photo_image
window_size, cliplimit=600,IntVar()
cliplimit.set(0.)

####################################
frame1 = tk.Frame(master=win, width=window_size, height=window_size)
frame1.pack()
frame2 = tk.Frame(master=win, width=window_size, height=50)
frame2.pack()
frame3 = tk.Frame(master=win, width=window_size, height=50)
frame3.pack()
canvas = Canvas(frame1, height=window_size, width=window_size, bg="black")
canvas.pack(anchor='nw', fill='both', expand=True)
init_image=cv2.imread(r"C:\Users\helina\Desktop\init_image.tif", 0)

image_size=init_image.shape[0]
photo_image=turn_image_into_tkinter(init_image,window_size)     
canvas.create_image(0,0, anchor=NW, image=photo_image)
##################################################
def change_contrast(value):   
    canvas.delete("all")
    cliplimit_slider.config(label="Cliplimit =  "+ value)
    init_image_copy=init_image.copy()   
    if value!="0":       
      clahe = cv2.createCLAHE(clipLimit=float(value))
      cl=clahe.apply(init_image_copy)      
      result=cl
    else:     
      result=init_image      
    global photo_image
    photo_image=turn_image_into_tkinter(result,window_size)     
    canvas.create_image(0,0, anchor=NW, image=photo_image)
##################################################

################################################ 
global cliplimit_slider    
cliplimit_slider=Scale(frame2,from_=0,to=100,orient=HORIZONTAL,troughcolor="#513B1C",variable=cliplimit,activebackground="red",label="Cliplimit = " +str(int(cliplimit.get())),command=change_contrast, length=150, showvalue=0)
cliplimit_slider.pack()


  
win.mainloop()
##################################################

