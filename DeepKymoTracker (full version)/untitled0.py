import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Canvas
import numpy as np
import os
import cv2
from interface_functions import turn_image_into_tkinter

win= tk.Tk()

canvas_size=382

win.geometry('%dx%d+%d+%d' % (382, 500, 0, 0))
ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen

frame1 = tk.Frame(master=win , width=382, height=50, bg="blue")
frame1.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
frame2 = tk.Frame(master=win , width=canvas_size, height=canvas_size, bg="yellow")
frame2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
frame3 = tk.Frame(master=win , width=canvas_size, height=50, bg="green")
frame3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
global  canvas_zoom 
canvas_zoom = Canvas(frame2, bg="black", height=canvas_size, width=canvas_size)
canvas_zoom.pack(anchor='nw', fill='both', expand=True)

#########################################
global photo
image_path=r"C:\Users\helina\Desktop\zoom.tif"
image=cv2.imread(image_path,-1)
photo=turn_image_into_tkinter(image, 382)
image_zoom=canvas_zoom.create_image(0, 0, anchor=NW, image=photo)


image_size=image.shape
print("image_size=", image_size)
#############################################
def drag_start(event):
        """Begining drag of an object"""
        # record the item`s location
        global x,y
        x = event.x
        y = event.y

def drag_stop(event):
        """End drag of an object"""
        # reset the drag information 
        global x,y
        x = 0
        y = 0

def drag(event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        global x,y
        delta_x = event.x - x
        delta_y = event.y - y
        # move the object the appropriate amount
        canvas_zoom.move(image_zoom, delta_x, delta_y)
        # record the new position
        x = event.x
        y= event.y
canvas_zoom.bind( "<ButtonPress-1>", drag_start)
canvas_zoom.bind("token<ButtonRelease-1>", drag_stop)
canvas_zoom.bind("<B1-Motion>", drag)
#canvas_zoom.bind('<B1-Motion>', lambda event: drag_image( event,canvas_zoom, image_zoom))
####################################

win.mainloop()

def zoom_in():
                
        global  tk_image, my_image, x0, y0, image_object      
        my_image = cv2.resize(my_image,(int(my_image.shape[0] * 1.2), int(my_image.shape[1] * 1.2)), cv2.INTER_LINEAR)
        cv2.imwrite(r"C:\Users\helina\Desktop\my_image+zoomed_in.tif", my_image)
        new_shape=my_image.shape[0]
        x0_new, y0_new=x0*1.2,y0*1.2
        x0,y0=x0_new, y0_new
        print("x0,y0=", x0, y0)
        print("x0_new,y0_new=", x0_new, y0_new)
        tk_image =  turn_image_into_tkinter(my_image,new_shape)
        canvas.delete("all")
        image_object=canvas.create_image(360-x0_new, 360-y0_new, anchor="nw", image=tk_image)

def zoom_out():
        global  tk_image, my_image, x0, y0, image_object      
        my_image = cv2.resize(my_image,(int(my_image.shape[0] * 0.8), int(my_image.shape[1] * 0.8)), cv2.INTER_LINEAR)
        cv2.imwrite(r"C:\Users\helina\Desktop\my_image+zoomed_in.tif", my_image)
        new_shape=my_image.shape[0]
        x0_new, y0_new=x0*0.8,y0*0.8
        x0,y0=x0_new, y0_new
        
        tk_image =  turn_image_into_tkinter(my_image,new_shape)
        canvas.delete("all")
        image_object=canvas.create_image(360-x0_new, 360-y0_new, anchor="nw", image=tk_image)
       