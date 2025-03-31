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
###############################################
image_path=r"C:\Users\helina\Desktop\zoom.tif"
image=cv2.imread(image_path,-1)
photo=turn_image_into_tkinter(image, 382)
canvas_zoom.create_image(0, 0, anchor=NW, image=photo)
#################################################




win.mainloop()