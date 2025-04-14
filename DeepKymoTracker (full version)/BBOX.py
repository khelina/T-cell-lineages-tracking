import tkinter as tk
import cv2
from interface_functions import turn_image_into_tkinter



root = tk.Tk()
canvas = tk.Canvas(root,width=719,height=719)
canvas.pack()
#image_object = canvas.create_rectangle(100,200, 500, 500,
                       #fill = "BLUE")
                       
my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
my_image_resized=my_image.copy()
my_image_resized= cv2.resize(my_image_resized,(400,400), cv2.INTER_LINEAR)      
tk_image =  turn_image_into_tkinter(my_image_resized,400)
image_object=canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                
print("initial bbox=", canvas.bbox(image_object))
global delta_x,delta_y
delta_x, delta_y=0,0
################################################
def drag_start(event):     
        global x,y
        x = event.x
        y = event.y
#########################################
def drag_stop(event):        
        global x,y
        x = 0
        y = 0
#######################################
def drag(event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        global x,y
        delta_x = event.x - x
        delta_y = event.y - y
        x = event.x
        y= event.y
        print("delta_x, delta_y=", delta_x, delta_y)
        canvas.move(image_object,delta_x,delta_y)
        
        bbx = canvas.bbox(image_object)
        print("bbx=", bbx)
#################################################

#############################################
def wheel(event):
        ''' Zoom with mouse wheel '''
        global  image_object
        
        if  event.delta == -120:  # scroll down
            canvas.scale(image_object, canvas.winfo_width() / 2, canvas.winfo_height() / 2, 1.2, 1.2)
        if   event.delta == 120:  # scroll up
           canvas.scale(image_object, canvas.winfo_width() / 2, canvas.winfo_height() / 2, 0.8, 0.8)
#####################################################
canvas.bind( "<ButtonPress-1>", drag_start)
canvas.bind("token<ButtonRelease-1>", drag_stop)
canvas.bind("<B1-Motion>", drag)
canvas.bind('<MouseWheel>', wheel)
###################################################


root.mainloop()