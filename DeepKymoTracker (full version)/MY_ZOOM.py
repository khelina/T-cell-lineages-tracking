import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
from interface_functions import turn_image_into_tkinter

root = tk.Tk()
global window_p5_size,frame_p5_size, coeff
window_p5_size =600
frame_p5_size=719
coeff=window_p5_size /frame_p5_size
canvas = tk.Canvas(root, bg="black", height=window_p5_size, width=window_p5_size)
canvas.pack(fill=tk.BOTH, expand=True)
global delta_x,delta_y
delta_x, delta_y=0,0

def load_image(filename):
        # Load the image using OpenCV
        global my_image,my_image_resized, tk_image, image_object, container, imscale,delta, width, height
        my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
        my_image_resized=my_image.copy()
        my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
        tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
        image_object=canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                
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
        global x,y, image_object, x0,y0, x0_new_in,x0_new_out,y0_new_in,y0_new_out, center_x,center_y, x_last,y_last
        delta_x = event.x - x
        delta_y = event.y - y      
        #canvas.move(image_object, delta_x, delta_y)
        #image_object=canvas.create_image(360-x0,360-y0, anchor="nw", image=tk_image)
        # record the new position
        x = event.x
        y= event.y
        # recalculater center of image_resized after dragging
        center_x+=delta_x
        center_y+=delta_y
        canvas.delete("all")
        print("x_last, y_last=", x_last, y_last)
        image_object=canvas.create_image(center_x-x_last,center_y-y_last, anchor="nw", image=tk_image)
def wheel(event):
        ''' Zoom with mouse wheel '''
        global  tk_image, my_image_resized, x0, y0,image_object, factor_in, factor_out,x0_new_in,x0_new_out,y0_new_in,y0_new_out, center_x, center_y, x_last, y_last, coeff
        
        if  event.delta == -120:  # scroll down
          factor_out*=0.8
          factor_in*=0.8
          my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
          my_image_resized=my_image.copy()
          my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_resized = cv2.resize(my_image_resized,(int(my_image_resized.shape[0] * factor_out ), int(my_image_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)      
          new_shape=my_image_resized.shape[0]
          x0_new_out, y0_new_out=x0*factor_out,y0*factor_out    
          tk_image =  turn_image_into_tkinter(my_image_resized,new_shape)
          canvas.delete("all")
          # cell in the centre of canvas
          image_object=canvas.create_image(center_x-x0_new_out, center_y-y0_new_out, anchor="nw", image=tk_image)
          x_last, y_last= x0_new_out, y0_new_out
        if   event.delta == 120:  # scroll up
          factor_in*=1.2
          factor_out*=1.2
          my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
          my_image_resized=my_image.copy()
          my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_resized = cv2.resize(my_image_resized,(int(my_image_resized.shape[0] * factor_in), int(my_image_resized.shape[1] * factor_in)), cv2.INTER_LINEAR)       
          new_shape=my_image_resized.shape[0]
          x0_new_in, y0_new_in=x0*factor_in,y0*factor_in

          tk_image =  turn_image_into_tkinter(my_image_resized,new_shape)
          canvas.delete("all")
          image_object=canvas.create_image(center_x-x0_new_in, center_y-y0_new_in, anchor="nw", image=tk_image)
          x_last, y_last= x0_new_in, y0_new_in
          print("x_last, y_last=", x_last, y_last)# last cell center coords
          coeff=new_shape/frame_p5_size
###############################################
def savePosn(event):
       global lastx, lasty
       lastx, lasty = event.x, event.y
       print(" lastx, lasty=", lastx, lasty)

def addLine(event):
        global coeff
        canvas.create_line((lastx, lasty, event.x, event.y), fill="red", width=5)
        savePosn(event)
        points.append([[int(round(lastx-center_x+x_last)),int(round(lasty-center_y+y_last))]])
        points_for_original.append([[int(round((lastx-center_x+x_last)/coeff)),int(round((lasty-center_y+y_last)/coeff))]])
        #points_for_original.append([[int(round(lastx-center_x+x_last)),int(round(lasty-center_y+y_last))]])
        print("len(points)=", len(points))
def start_drawing():    
    canvas.unbind("all")
    canvas.bind("<Button-1>", savePosn)
    canvas.bind("<B1-Motion>", addLine)
    global points, points_for_original
    points=[]
    points_for_original=[]
    
def stop_drawing():
   
    canvas.unbind("all")
    canvas.bind( "<ButtonPress-1>", drag_start)
    canvas.bind("token<ButtonRelease-1>", drag_stop)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind('<MouseWheel>', wheel)
#######################################
global x0, y0, frame_size, factor_in, factor_out, center_x,center_y, x_last, y_last
x0, y0=107*coeff, 54*coeff
#x0, y0=54, 673# coordinates of the cell of interest
frame_p5_size=719
factor_in, factor_out=1,1
x0_new_in,x0_new_out,y0_new_in,y0_new_out, x_last, y_last=x0,x0,y0,y0, x0, y0
#center_x, center_y=360, 360
center_x, center_y=window_p5_size/2, window_p5_size/2
def start_zoom():
    global my_image_resized, tk_image, image_object
    canvas.delete("all")   
    tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
    image_object=canvas.create_image(center_x-x0,center_y-y0, anchor="nw", image=tk_image)
    
def stop_zoom():
    global my_image_resized, tk_image, image_object, my_image
    canvas.delete("all")
    ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)#
    print("my_image_resized.shape=", my_image_resized.shape)
    cv2.drawContours(my_image_resized,[ctr],0,(255,255,255),2)
    cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_resized.tif", my_image_resized)
    ##################################
    ctr_origin = np.array(points_for_original).reshape((-1,1,2)).astype(np.int32)#
    cv2.drawContours(my_image,[ctr_origin],0,(255,255,255),2)
    cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_origin.tif", my_image)
    #################################
    tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
    image_object=canvas.create_image(0,0, anchor="nw", image=tk_image)
    
################################################
load_image(r"C:\Users\helina\Desktop\zoom.tif")


start_zoom_button = tk.Button(root, text="Start zooming", command=start_zoom).pack(side=tk.LEFT)
stop_zoom_button = tk.Button(root, text="Stop zooming", command=stop_zoom).pack(side=tk.LEFT)
start_draw_button = tk.Button(root, text="Start drawing", command=start_drawing).pack(side=tk.LEFT)
stop_draw_button = tk.Button(root, text="Stop drawing", command=stop_drawing).pack(side=tk.LEFT)

canvas.bind( "<ButtonPress-1>", drag_start)
canvas.bind("token<ButtonRelease-1>", drag_stop)
canvas.bind("<B1-Motion>", drag)
canvas.bind('<MouseWheel>', wheel)
root.mainloop()


