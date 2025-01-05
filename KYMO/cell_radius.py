import cv2
import tkinter as tk
from tkinter import *
import os


cwd = os.getcwd()

from interface_functions import turn_image_into_tkinter


win= tk.Tk()
window_size=800
frame1 = tk.Frame(master=win, width=window_size, height=window_size)
frame1.pack()
frame2 = tk.Frame(master=win, width=window_size, height=50)
frame2.pack()

canvas = Canvas(frame1, height=window_size, width=window_size, bg="black")
canvas.pack(anchor='nw', fill='both', expand=True)
image=cv2.imread(r"C:\Users\helina\Desktop\ex_147.tif", -1)
image_size=image.shape[0]
photo_image=turn_image_into_tkinter(image,window_size)     
canvas.create_image(0,0, anchor=NW, image=photo_image)

global centres, circles,scaled_cell_radius, true_cell_radius
centres, circles,scaled_cell_radius, true_cell_radius =[],[],IntVar(),IntVar()

scaled_cell_radius.set(20)
true_cell_radius.set(int(round(scaled_cell_radius.get()*image_size/window_size)))
print("true_radius=",true_cell_radius.get())
def draw_first_circles(event):# draw red circles on borders to measure intensities
    rad=scaled_cell_radius.get()
    circle=canvas.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline = "green",width = 2)
    centres.append([int(round(event.x)), int(round(event.y))])
    circles.append(circle)
   
    #print("centres=", centres)

def change_radius(value):# draw red circles on borders to measure intensities  
  new_circles=[]
  scaled_cell_radius=int(value)
  true_cell_radius.set(int(round(scaled_cell_radius*image_size/window_size)))
  radius_slider.config(label="Cell radius =  "+str(true_cell_radius.get())) 
  #radius_slider.set(cell_radius)
  global circles
  for k in range(len(centres)):
       canvas.delete(circles[k])
       new_circle=canvas.create_oval(centres[k][0]-scaled_cell_radius,centres[k][1]-scaled_cell_radius,centres[k][0]+scaled_cell_radius,centres[k][1]+scaled_cell_radius,outline = "green",width = 2) 
       #canvas.create_oval(event.x-value,event.y-value,event.x+value,event.y+value,outline = "red",width = 2)
       #coords.append([event.x, event.y])
       new_circles.append(new_circle)
  circles=new_circles
###################################################
def save_cell_radius():
    patch_size=int(round(true_cell_radius.get()*2.4))
    print("cell_radius, patch_size=", true_cell_radius.get(), patch_size)
    return true_cell_radius, patch_size
 
global radius_slider    
radius_slider=Scale(frame2,from_=1,to=100,orient=HORIZONTAL,troughcolor="#513B1C",activebackground="red",label="Cell radius = "+str(int(true_cell_radius.get())),variable=scaled_cell_radius, command=change_radius, length=150, showvalue=0)
radius_slider.pack()

button_save=tk.Button(frame2,text="Save",activebackground="red", command=save_cell_radius)
button_save.pack()    
canvas.bind("<Button-1>",draw_first_circles)

win.mainloop()