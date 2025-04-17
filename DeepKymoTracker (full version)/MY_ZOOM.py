import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
from interface_functions import turn_image_into_tkinter

root = tk.Tk()

global window_p5_size,frame_p5_size, coeff 
window_p5_size =600
frame_p5_size=719
#resize_coeff=window_p5_size /frame_p5_size

canvas_fluor_p5 = tk.Canvas(root, bg="black", height=window_p5_size, width=window_p5_size)
canvas_fluor_p5.pack(fill=tk.BOTH, expand=True)
global delta_x,delta_y
delta_x, delta_y=0,0
global  image_origin_x,image_origin_y, factor_in, factor_out,zoom_coeff

factor_in, factor_out=1,1
image_origin_x,image_origin_y=0,0
zoom_coeff=1
#center_x, center_y=300, 300


def load_image(filename):
        # Load the image using OpenCV
        global my_image,my_image_resized, tk_image, image_object
        my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
        my_image_resized=my_image.copy()
        my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
        tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
        image_object=canvas_fluor_p5.create_image(0, 0, anchor=tk.NW, image=tk_image)
        print("bbox initial=", canvas_fluor_p5.bbox(image_object))
                
def drag_start(event):
        # start drag of an object
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
        global x,y, x0,y0, image_origin_x, image_origin_y, center_x, center_y
        delta_x = event.x - x
        delta_y = event.y - y
        print("delta_x, delta_y=", delta_x, delta_y)
        #canvas.move(image_object, delta_x, delta_y)
        #image_object=canvas.create_image(360-x0,360-y0, anchor="nw", image=tk_image)
        # record the new position
        x = event.x
        y= event.y
        # recalculater center of image_resized after dragging
        #print("image_origin_x, image_origin_y before drag=", image_origin_x, image_origin_y)
        image_origin_x+=delta_x
        image_origin_y+=delta_y
        canvas_fluor_p5.delete("all")
        print("image_origin_x, image_origin_y after drag=", image_origin_x, image_origin_y)     
        x0, y0=(300-image_origin_x)/zoom_coeff,(300-image_origin_y)/zoom_coeff#x0, y0 - for original photo
        print("x0, y0=", x0, y0)
        image_object=canvas_fluor_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=tk_image)
        print("bbox after dragging=", canvas_fluor_p5.bbox(image_object))
#############################################
def wheel(event):
        ''' Zoom with mouse wheel '''
        global  tk_image, my_image_resized, x0, y0,image_object, factor_in, factor_out, coeff, image_origin_x, image_origin_y, resize_coeff 
        #print("image_origin_x, image_origin_y before ZOOM=", image_origin_x, image_origin_y)
        if  event.delta == -120:  # scroll down
          factor_out*=0.8
          factor_in*=0.8
          print("factor_in, factor_out=",factor_in, factor_out)
          my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
          my_image_resized=my_image.copy()
          my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_resized = cv2.resize(my_image_resized,(int(my_image_resized.shape[0] * factor_out ), int(my_image_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)      
          new_shape=my_image_resized.shape[0]
          
          #print("image_origin_x, image_origin_y after zoom out=", image_origin_x, image_origin_y)
          x0_new_out, y0_new_out=x0*factor_out,y0*factor_out    
          tk_image =  turn_image_into_tkinter(my_image_resized,new_shape)
          canvas_fluor_p5.delete("all")
        
          image_origin_x, image_origin_y=300-x0_new_out,300-y0_new_out
          image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=tk_image)
          resize_coeff=new_shape/frame_p5_size
          zoom_coeff=new_shape/window_p5_size
        if   event.delta == 120:  # scroll up
          factor_in*=1.2
          factor_out*=1.2
          print("factor_in, factor_out=",factor_in, factor_out)
          my_image = cv2.imread(r"C:\Users\helina\Desktop\zoom.tif",1)
          my_image_resized=my_image.copy()
          my_image_resized= cv2.resize(my_image_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_resized = cv2.resize(my_image_resized,(int(my_image_resized.shape[0] * factor_in), int(my_image_resized.shape[1] * factor_in)), cv2.INTER_LINEAR)       
          new_shape=my_image_resized.shape[0]
          
          print("image_origin_x, image_origin_y after zoom in=", image_origin_x, image_origin_y)
          x0_new_in, y0_new_in=x0*factor_in,y0*factor_in

          tk_image =  turn_image_into_tkinter(my_image_resized,new_shape)
          canvas_fluor_p5.delete("all")
          image_origin_x, image_origin_y=300-x0_new_in,300-y0_new_in
          image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=tk_image)
        
          zoom_coeff=new_shape/window_p5_size
          resize_coeff=new_shape/frame_p5_size

###############################functions from GUI_execute.py
################################################
"""
def start_drawing():    
    canvas_fluor_p5.unbind("all")
    #canvas.bind("<Button-1>", savePosn)
    canvas_fluor_p5.bind("<Button-1>",  get_x_and_y)
    canvas_fluor_p5.bind("<B1-Motion>", addLine)
    print("initial bbox=", canvas.bbox(image_object))
    global points, points_for_original
    points=[]
    points_for_original=[]
"""
####################################################
def activate_hand_drawing_mode_for_one_cell():
    #bound_box=canvas_fluor_p5.bbox(image_object)
    #side=bound_box[2]-bound_box[0]
    #new_origin_x, new_origin_y=bound_box[0],bound_box[1]
    
    #button_activate_hand_drawing_mode_for_one_cell.configure(background = 'red')
    #update_flash([button_save_hand_drawing_for_one_cell])
    #dialog_label_5.config(text="Draw the contour of the cell with the left mouse. Warning:  Be careful not to draw on neughbouring close cells!\n If you want to undo right-click the mouse anywhere in the image.\nOnce you are finished, push Button 4b.")
    canvas_fluor_p5.unbind("all")
    #canvas_fluor_p5.unbind_all("<Button-1>")  
    canvas_fluor_p5.bind("<Button-1>", get_x_and_y)    
    #canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse, add="+")
    canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse)   
    global cell_contour_fl, cell_contour_br,points, mask_hand, points_for_original# for the clicked cell
    cell_contour_fl=[]
    cell_contour_br=[]
    points, points_for_original=[],[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
###########################################
###########################################
def get_x_and_y(event):
    global lasx,lasy
    lasx,lasy=event.x,event.y         
#########################################

############################################    
def draw_with_mouse(event):
    global coeff
    global lasx,lasy, line_fl, line_br
   
    line_fl=canvas_fluor_p5.create_line((lasx,lasy,event.x,event.y), fill="red", width=5)
    get_x_and_y(event)
    #line_br=canvas_bright_p5.create_line((lasx,lasy,event.x,event.y), fill="red", width=5)
    cell_contour_fl.append(line_fl)
    #cell_contour_br.append(line_br)   
    #lasx,lasy=event.x,event.y
    #points.append([[int(round(lasx/window_p5_size*frame_p5_size)),int(round(lasy/window_p5_size*frame_p5_size))]])
    
    points.append([[int(round(lasx/zoom_coeff-image_origin_x)),int(round(lasy/zoom_coeff-image_origin_y))]])
    points_for_original.append([[int(round((lasx/zoom_coeff-image_origin_x)/(resize_coeff))),int(round((lasy/zoom_coeff-image_origin_y)/(resize_coeff)))]])
#######################################
def erase_line():# in case you are not happy with your hand contour and want to delete it
    global cell_contour_fl, cell_contour_br, points,mask_hand, final_mask
    for i in range(len(cell_contour_fl)):        
         canvas_fluor_p5.delete(cell_contour_fl[i])
         canvas_bright_p5.delete(cell_contour_br[i])
    points=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    final_mask[final_mask==cell_number+1]=0
   
    cell_contour_fl=[]
    cell_contour_br=[]
##############################################
#######################################
###################################################

def start_zoom():   
    global my_image_resized, tk_image, points
    points=None
    canvas_fluor_p5.delete("all")   
    tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
    canvas_fluor_p5.create_image(0,0, anchor="nw", image=tk_image)    
    canvas_fluor_p5.bind( "<ButtonPress-1>", drag_start)
    canvas_fluor_p5.bind("token<ButtonRelease-1>", drag_stop)
    canvas_fluor_p5.bind("<B1-Motion>", drag)
    canvas_fluor_p5.bind('<MouseWheel>', wheel)


def stop_zoom():
    global my_image_resized, tk_image, my_image, points
    canvas_fluor_p5.delete("all")
    if points:
      ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)#
      print("my_image_resized.shape=", my_image_resized.shape)
      cv2.drawContours(my_image_resized,[ctr],0,(255,255,255),2)
      ctr_origin = np.array(points_for_original).reshape((-1,1,2)).astype(np.int32)#
      cv2.drawContours(my_image,[ctr_origin],0,(255,255,255),2)
    cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_origin.tif", my_image)
    cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_resized.tif", my_image_resized)
    #################################
    tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
    canvas_fluor_p5.create_image(0,0, anchor="nw", image=tk_image)
    canvas_fluor_p5.unbind("all")
    #canvas.bind( "<ButtonPress-1>", drag_start)# now you can start with another cell
    #canvas.bind("token<ButtonRelease-1>", drag_stop)
    #canvas.bind("<B1-Motion>", drag)
    #canvas.bind('<MouseWheel>', wheel)
################################################
load_image(r"C:\Users\helina\Desktop\zoom.tif")


start_zoom_button = tk.Button(root, text="Start zooming", command=start_zoom).pack(side=tk.LEFT)
stop_zoom_button = tk.Button(root, text="Stop zooming", command=stop_zoom).pack(side=tk.LEFT)
start_draw_button = tk.Button(root, text="Start drawing", command=activate_hand_drawing_mode_for_one_cell).pack(side=tk.LEFT)
#stop_draw_button = tk.Button(root, text="Stop drawing", command=stop_drawing).pack(side=tk.LEFT)


root.mainloop()


