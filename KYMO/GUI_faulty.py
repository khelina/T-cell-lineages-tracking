import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import numpy as np
import os
import cv2
import time
import shutil
import traceback
import threading
import tensorflow as tf
import keras
from keras.optimizers import Adam
from keras.models import model_from_json
import time
#import pygame
import gc
import pickle
from threading import Thread
from functools import partial
import copy
import tifffile as tiff
#import imagecodecs
#############################################################################
win= tk.Tk()
win.geometry('1530x2000')
bg_color,all_font,button_color,result_color,label_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA"

win.config(bg=bg_color)
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: PROCESS MULTIPAGE TIFF", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING","PAGE 5: CORRECT SEGMENTATION", "PAGE 6: VISUALISE RESULTS"]
global page_number
page_number = tk.IntVar(master=win, value=1)
num = page_number.get()
#print("page_number=", num)
win.withdraw()

################## Create pages and buttons to switch between pages
##################################################################   
def go_to_page(num):# num (1,2,3,4,5)= the page you want to go to    
    #print("page_number entering go_to_page=", num)
    page_number.set(num)
    for ii in range(6):
        if (ii+1)!=num:
           old_page=pages[ii]
           old_page.withdraw()           
        else:    
           new_page=pages[num-1]
           new_page.deiconify()
          
    #print("page_number exiting go_to_page=", num) 
################################################      
pages=[]
for i in range(6):
    page=tk.Toplevel(master=win, width=1530, height=2000, bg="black")
    page.geometry('1530x2000')
    page.config(bg=bg_color)
    page.title(page_titles[i])    
    pages.append(page)   
    
#####################################################
for k in range(1,len(pages),1):# display only title page
    pages[k].withdraw() 
###############################################
global flashers
flashers={}
global start_flash, stop_flash, turn_image_into_tkinter
from interface_functions import start_flash, stop_flash,turn_image_into_tkinter
global trackers, segmentor, refiner
trackers, segmentor, refiner= None, None, None

###########################################################################
############################   PAGE 1 : TITLE  ##############################
###############################################################################
page1=pages[0]

frame1_page1 = tk.Frame(master=page1, width=1530, height=100, bg=bg_color)
frame1_page1.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page1 = tk.Frame(master=page1, width=765, height=500, bg=bg_color)
frame2_page1.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page1 = tk.Frame(master=page1, width=1530, height=30, bg=bg_color)
frame3_page1.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

#########################################################
tk.Label(frame1_page1, text="DeepKymoTracker",
              bg="yellow", fg="red", font=("Times", "58")).grid(row=0, column=0, padx=300,columnspan=3, pady=10)
tk.Label(frame2_page1, text="CONTENTS:",
              bg="black", fg="yellow", font=("Times", "20")).grid(row=0, column=1, padx=3, pady=(200,0))
###########################################################
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: PROCESS MULTIPAGE TIFF", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING", "PAGE 5: CORRECT SEGMENTATION","PAGE 6: VISUALISE RESULTS" ]              
for i in range(1,6):
    Label(frame2_page1, text= "STEP %s: " % (i)+ page_titles[i][7:],bg="black",fg="yellow",font=all_font).grid(row=1+i,column=1,pady=5, padx=5)     
    Button(frame2_page1, text= "GO TO STEP %s" % (i),bg=button_color,font=all_font,command=partial(go_to_page,i+1)).grid(row=1+i,column=0,pady=5, padx=200)
###############################################
cwd = os.getcwd()
im=Image.open(os.path.join(cwd,"logo.tif"))
im=im.resize((500,500))
img = ImageTk.PhotoImage(im)
# Create a Label Widget to display the text or Image
logo_label = Label(frame2_page1, image = img, bg="brown")
logo_label.grid(row=0, column=2,rowspan=5, padx=5, pady=(100,0))

###########################################################################
############################   PAGE 2 : PROCESS TIF  ##############################
###############################################################################
page2=pages[1]
frame1_page2 = tk.Frame(master=page2, width=1530, height=50, bg=bg_color)
frame1_page2.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame2_page2.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame3_page2.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame4_page2 = tk.Frame(master=page2, width=382, height=382, bg=bg_color)
frame4_page2.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame5_page2 = tk.Frame(master=page2, width=382, height=382, bg=bg_color)
frame5_page2.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame6_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame6_page2.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame7_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame7_page2.grid(row=5, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame8_page2 = tk.Frame(master=page2, width=1530, height=50, bg=bg_color)
frame8_page2.grid(row=6, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

canvas_fluor_p2 = Canvas(frame4_page2, bg=bg_color, height=382, width=382)
canvas_fluor_p2.pack(anchor='nw', fill='both', expand=True)

canvas_bright_p2= Canvas(frame5_page2, bg=bg_color, height=382, width=382)
canvas_bright_p2.pack(anchor='nw', fill='both', expand=True)

#####################################################
#global  flashers
#flashers ={}
global  load_image_names,cut_all
from interface_functions import cut_all
###############################
global progressbar_page2
progressbar_page2 = ttk.Progressbar(frame3_page2,orient='horizontal',mode='determinate',length=280)
progressbar_page2.grid(row=0, column=3,padx=20)
########################################
global menu_variable
menu_variable=StringVar()
menu_variable.set("Select movie name:")
######################################
global load_and_process_page2,sorted_aphanumeric,extract_movie_name,save_images_page2
from helper_functions_page2 import load_and_process_page2,sorted_aphanumeric,extract_movie_name,save_images_page2
#######################################
def create_movie_for_display(value):
    global movie_name
    movie_name=value
    print("movie_name=",movie_name)
    global fluor_images, bright_images   
    number_of_frames=0
    for filename in sorted_aphanumeric(os.listdir(path)):
      if "thumb" not in filename and filename.endswith(".TIF"):
        index_s,index_t=filename.find("_s"),filename.find("_t")
        exact_name =filename[index_s+1:index_t]     
        if exact_name==movie_name:
           number_of_frames+=1
    
    global fluor_images, bright_images,fluor_names, bright_names
    fluor_images, bright_images,fluor_names, bright_names=load_and_process_page2(path,number_of_frames,progressbar_page2,frame3_page2, movie_name)
        
    global photo_fl, photo_br# the same image in PIL (for display)
    global fl,br# the image in opencv (as array, can measure intensities)
    fl=fluor_images[0]# 0 is very important!!!!
    photo_fl=turn_image_into_tkinter(fl,382)     
    canvas_fluor_p2.create_image(0,0, anchor=NW, image=photo_fl)
    br=bright_images[0]# 0 is very important!!!!
    photo_br=turn_image_into_tkinter(br, 382)     
    canvas_bright_p2.create_image(0,0, anchor=NW, image=photo_br)
    global frame_slider    
    frame_slider=Scale(frame6_page2,from_=1,to=len(fluor_images),orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p2, length=150, showvalue=0)
    frame_slider.grid(row=2, column=0)
    frame_slider.set(13)
    ######################## 
def slide_p2(value):
    canvas_bright_p2.delete("all")
    canvas_fluor_p2.delete("all")
    image_number=int(value)    
    frame_slider.config(label="Frame "+str(value))       
    br_image=bright_images[image_number-1]    
    global br_final  
    br_final=turn_image_into_tkinter(br_image, 382)     
    canvas_bright_p2.create_image(0,0, anchor=NW, image=br_final)
    fl_image=fluor_images[image_number-1]     
    global fl_final
    fl_final=turn_image_into_tkinter(fl_image, 382)       
    canvas_fluor_p2.create_image(0,0, anchor=NW, image=fl_final)
#############################################
def explore_folder():# check which movies are inside the folder and create menu with their names
   names=[]
   global path
   path=filedialog.askdirectory()#
   for filename in os.listdir(path):
      if "thumb" not in filename and filename.endswith(".TIF"):
         index_s,index_t=filename.find("_s"),filename.find("_t")
         exact_name =filename[index_s+1:index_t]
         if exact_name not in names:
           names.append(exact_name)

   movie_names_int =[int(x[1:]) for x in names]
   movie_names_int.sort()
   movie_names =["s"+str(y) for y in movie_names_int]
   print("movie_names=", movie_names)
   global movies_menu
   
   movies_menu = OptionMenu(frame3_page2,menu_variable, *movie_names, command=create_movie_for_display)
   movies_menu.grid(row=0, column=1, padx=30)
   movies_menu.config(bg=label_color, font=all_font, activebackground="red")
   movies_menu["menu"].config(bg=label_color,activebackground="red") 
############################################################
l_page_name=tk.Label(frame1_page2,text= "STEP 1: PROCESS MULTIPAGE TIFF", bg="yellow", fg="red", font=("Times", "24"))
l_page_name.grid(row=0, column=1,padx=250)

l_feedback=tk.Label(frame2_page2,text= "Welcome to STEP 1 of the pipeline!\n\nClick Button 1 to open file menu,\n then navigate to the folder containing movies\n and click on it.",bg="black", fg="yellow", font=all_font) 
l_feedback.grid(row=0, column=0, padx=250)

button_choose_folder=tk.Button(frame3_page2,text="1. Choose folder with movies",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=lambda: explore_folder())
button_choose_folder.grid(row=0,column=0)

button_save_movie=tk.Button(frame7_page2,text="2. Save processed movie",bg='#9ACD32',activebackground="red",font=all_font , command=lambda: save_images_page2(movie_name,l_feedback,bright_names,fluor_names, bright_images, fluor_images))
button_save_movie.grid(row=0,column=0, padx=20)

###########################################################################
############################   PAGE 3 : CUT WELL  ##############################
###############################################################################
page3=pages[2]

frame1_page3 = tk.Frame(master=page3, width=1528, height=50, bg=bg_color)
frame1_page3.grid(row=0, column=0,rowspan = 1, columnspan = 4,sticky = W+E+N+S)

frame2_page3 = tk.Frame(master=page3, width=382, height=30, bg=bg_color)
frame2_page3.grid(row=1,column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame3_page3 = tk.Frame(master=page3, width=382, height=30, bg=bg_color)
frame3_page3.grid(row=1, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame4_page3 = tk.Frame(master=page3, width=382, height=30, bg=bg_color)
frame4_page3.grid(row=1, column=2,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame6_page3 = tk.Frame(master=page3, width=382, height=382, bg=bg_color)
frame6_page3.grid(row=2,column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame7_page3 = tk.Frame(master=page3, width=382, height=382, bg=bg_color)
frame7_page3.grid(row=2, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame8_page3 = tk.Frame(master=page3, width=382, height=382, bg=bg_color)
frame8_page3.grid(row=2, column=2,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame14_page3 = tk.Frame(master=page3, width=250, height=382, bg=bg_color)
frame14_page3.grid(row=2, column=3,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame10_page3 = tk.Frame(master=page3, width=382, height=100, bg=bg_color)
frame10_page3.grid(row=3, column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame11_page3 = tk.Frame(master=page3, width=300, height=100, bg=bg_color)
frame11_page3.grid(row=3, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame12_page3 = tk.Frame(master=page3, width=300+382*2, height=100, bg=bg_color)
frame12_page3.grid(row=3, column=2,rowspan = 1, columnspan = 2,sticky = W+E+N+S)

frame13_page3 = tk.Frame(master=page3, width=300+382*2, height=100, bg=bg_color)
frame13_page3.grid(row=4, column=0,rowspan = 1, columnspan = 4,sticky = W+E+N+S)
############################################
global canvas_left, canvas_mid, canvas_right
canvas_left = Canvas(frame6_page3, bg=bg_color, height=382, width=382)
canvas_left.pack(anchor='nw', fill='both', expand=True)
canvas_mid = Canvas(frame7_page3, bg=bg_color, height=382, width=382)
canvas_mid.pack(anchor='nw', fill='both', expand=True)
canvas_right = Canvas(frame8_page3, bg=bg_color, height=382, width=382)
canvas_right.pack(anchor='nw', fill='both', expand=True)
###################################################
l_title=tk.Label(frame1_page3,text= "STEP-2: CUT WELL", bg="yellow", fg="red", font=("Times", "24"))
l_title.grid(row=0, column=1,padx=2)
l_finish = tk.Label(frame1_page3, justify=tk.LEFT, text=" This window allows you to cut out a well of interest out of initial cell movie. \n\nTo choose raw movie , press Button 1."
                    "\nThen, navigate to your raw movie, open it and click on ANY BRIGHT field image" ,fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
l_finish.grid(row=1, column=0,columnspan=4, sticky=W, pady=10)
############################################################
global low_thr,upp_thr 
low_thr, upp_thr=IntVar(), IntVar()
low_thr.set(0)
#im=np.zeros((382,382))

global cols, rows, cx, cy, length, M, imm
cols,rows,cx,cy, length,M, imm =382,382,0,0,1,np.zeros((2,3)),np.zeros((382,382))

global coords_1, my_path,intensities,bright_names,iik
coords_1,my_path,intensities,bright_names=[],'',[], []

iik=canvas_mid.create_oval(100-1,100+1,100+1,100+1,outline = "black",fill = "black",width = 2)
##############################################
"""
global  flashers
flashers ={}
"""
global start_flash, stop_flash, turn_image_into_tkinter, load_image_names,cut_all
from interface_functions import start_flash, stop_flash, turn_image_into_tkinter, cut_well_from_image
from preprocess import load_image_names
##################################################
def select_one_bright():    
    global my_path, my_destin, bright_names_sorted,fluor_names_sorted 
    my_path=filedialog.askopenfilename()
    movie_dir=os.path.dirname(my_path)
    bright_names_sorted,fluor_names_sorted =load_image_names(movie_dir)
        
    my_destin_1=os.getcwd() 
    my_destin=os.path.join(my_destin_1,"INPUT_MOVIE "+os.path.basename(movie_dir))
    l_input.config(text="Source :         "+movie_dir+",    "+str(len(bright_names_sorted))+" frames\nDestination :  "+my_destin)
    if not os.path.exists(my_destin):
      os.mkdir(my_destin)
     
    global photo_first# the same image in PIL (for display)
    global first_bright# the image in opencv (as array, can measure intensities)
    first_bright=cv2.imread(my_path,0)# 0 is very important!!!!
    photo_first=turn_image_into_tkinter(first_bright, 382)
    
    canvas_left.create_image(0,0, anchor=NW, image=photo_first)
    l_finish.config(text="Now, click on the dark border of the well(s) 2-3 times to measure intensities.\nThen click Button 2."
                    "\nThe thresholded image will appear in the window to the right.")
    stop_flash("select", page3, flashers)  
    button_select.config(bg=button_color)
    canvas_left.bind("<Button-1>", draw_circle_p3)
####################################################
button_select=tk.Button(frame1_page3 ,text="1. Go to raw movie",bg='#9ACD32', font='TkDefaultFont 10 bold' ,activebackground="red", command=select_one_bright)
button_select.grid(row=3,column=0)
start_flash([button_select],"select", page3, flashers)

l_input=tk.Label(frame1_page3,justify=tk.LEFT, text="Source :         \nDestination :  ", fg=result_color, bg="black", font=all_font)
l_input.grid(row=3, column=1, pady=10)

button_threshold=tk.Button(frame2_page3,text="2. Apply initial threshold",bg=button_color,activebackground="red", font=all_font, command=lambda: apply_thresh())
button_threshold.grid(row=0, column=0,padx=10,pady=20)
global  seeds
seeds=[]

#########################################################
def draw_circle_p3(event):# draw red circles on borders to measure intensities
    global coords_1
    global intensities
    canvas_left.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,outline = "red",fill = "red",width = 2)
    coords_1.append([event.x, event.y])  
    intensity=first_bright[int(event.y*imm.shape[1]/382),int(event.x*imm.shape[0]/382)]
    intensities.append(intensity)
    if len(coords_1)==2:
        start_flash([button_threshold], "thresh",page3,flashers)   
###################################################################
def low_thresh(value):      
    low=float(value)
    high=upp_thr.get()
    global thresh
    ret,thresh = cv2.threshold(first_bright,low,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold (it is now from 130 to 255)   
    thresh[thresh!=0]=255
    lower.config(label="Threshold = "+str(value))
    global thr_image
    thr_image=turn_image_into_tkinter(thresh, 382)    
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image)    
######################## respond to upper_thresh slider and thresh image accordingly 
def upper_thresh(value):
    high=float(value)
    low=low_thr.get()
    global thresh_1
    ret,thresh_1 = cv2.threshold(first_bright,low,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold (it is now from 130 to 255)   
    thresh_1[thresh_1!=0]=255
    upper.config(label="Upper threshold = "+str(value))
    global thr_image_1
    thr_image_1=turn_image_into_tkinter(thresh_1, 382)   
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image_1)
##################### respond to button Apply thresh (this is initial thresholding, before using  thersh sliders)
def apply_thresh():
    global lower, upper
    lower.config(variable=low_thr,label="Threshold = "+str(low_thr.get()))
    #lower=Scale(frame3_page3, from_=0,to=255,orient=HORIZONTAL,variable=low_thr,length=150,bg=label_color,	
    #showvalue=0,troughcolor="#513B1C",label="Threshold = "+str(low_thr.get()), command=low_thresh,
    #activebackground="red", font=all_font)
    #lower.grid(row=0, column=0,padx=10,pady=5)
    #######################    
    upper=Scale(frame3_page3, from_=0,to=255,orient=HORIZONTAL,variable=upp_thr,troughcolor="#513B1C",label="Upper threshold = "+str(upp_thr.get()),command=upper_thresh,
    showvalue=0,activebackground="red", bg=label_color, length=150, font=all_font)
    #upper.grid(row=0, column=1,padx=10,pady=5)
    #############################
    canvas_left.delete("all")
    canvas_mid.delete("all")
    canvas_right.delete("all")
    canvas_left.create_image(0,0, anchor=NW, image=photo_first)
    global low
    global high
    low=min(intensities)
    high=max(intensities)
    global thresh
    ret,thresh = cv2.threshold(first_bright,low,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold (it is now from 130 to 255)   
    thresh[thresh!=0]=255
    global thr_image
    thr_image=turn_image_into_tkinter(thresh, 382)    
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image)
    lower.set(low)
    upper.set(high)
    l_finish.configure(text="The borders of wells should become SOLID white line, WITHOUT INTERRUPTIONS."
                       "\nImprove thresholded image if necessary\nby sliding the bar below to change threshold."
                       "\nFinally, click on the well of interest.")
    stop_flash("thresh", page3, flashers)
    #start_flash([button_display],"display", page3, flashers)
    button_threshold.config(bg=button_color)
    start_flash([lower,upper], "slide_thresh",page3,flashers) 
    canvas_mid.bind("<Button-1>", choose_well)
##########################

################################# 
def choose_well(event):# click on the well of interest, get green circle and red rectangle  
    global iik
    canvas_mid.delete(iik)
    global seed, seeds    
    i=canvas_mid.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,outline = "green",fill = "green",width = 5)
    seed=(int(event.x*thresh.shape[1]/382), int(event.y*thresh.shape[0]/382))
    seeds.append(seed)
    print("seed=", seed)
    print("len(seeds)=", len(seeds))
    if len(seeds)==1:
         print("started display flash")
         start_flash([button_display],"display", page3, flashers)
    im_thr=thresh.copy()
    mask=None
    fill_image=cv2.floodFill(im_thr, mask, seed, 255,flags=8)# here you define the centre of the well (there are 4 in total)
    fill_image = thresh | im_thr
    fill_image-=thresh   
    closing = cv2.morphologyEx(fill_image, cv2.MORPH_CLOSE, (5,5))    
    _,contours, hierarchy = cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    print("len(contours)=", len(contours))
    cnt=contours[0]
    
    global box,first_x0  
    rect = cv2.minAreaRect(cnt)      
    box = cv2.boxPoints(rect)     
    box = np.int0(np.round(box))      
    first_x0=box[0][0]
    
      
    global closing_2
    closing_1=cv2.cvtColor(closing,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(closing_1,[box],0,(0,0,255),5)# draw red rect around detected well 
    closing_2=turn_image_into_tkinter(closing_1, 382)   
    canvas_right.create_image(0,0, anchor=NW, image=closing_2)    
    ######## here it draws red rect in fluorescent image of canvas_left
    im_copy=first_bright.copy()# 
    global photo_im_red,angle,rows,cols,M
    im_red=cv2.cvtColor(im_copy,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(im_red,[box],0,(0,0,255),5)    
    photo_im_red=turn_image_into_tkinter(im_red, 382)   
    canvas_left.create_image(0,0, anchor=NW, image=photo_im_red)
    angle=rect[2]+90.
   
    rows,cols = first_bright.shape 
    M = cv2.getRotationMatrix2D((int(round(cols/2)),int(round(rows/2))),angle,1)   
    l_finish.configure(text="Check that the well has been detected correctly: a red frame should appear around the well.\nIf it is not correct go back to sliding bar."
                       "\nFinally, push Button 3 to check the result.")    
############################################

######################################################
def cut_first_well():# cut well in the first image and display it in canvas_mid
 l_finish.configure(text="It is important to manually correct shift in Frame 1. Push Button 4 and drag the image with mouse to eliminate the shift."
                       "\nFinally, push Button 5 to check the results.")     
 global canvas_mid 
 canvas_mid.delete("all")
 global  well_size
 #################### draw temp image (binary) to rotate it and find rect_new
 print("first box=", box)
 temp=np.zeros(first_bright.shape, np.uint8)
 cv2.drawContours(temp,[box],0,255,-1)
 dst = cv2.warpAffine(temp,M,(cols,rows))
 #cv2.imwrite(r"C:\Users\kfedorchuk\Desktop\dst.tif", dst)
####################  4. calculate its borders   
 _,contours_new, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt_new=contours_new[0]
 rect_new = cv2.minAreaRect(cnt_new)             
 box_final = cv2.boxPoints(rect_new)    
 box_final = np.int0(np.round(box_final))
 print("first box_final=", box_final)
 xs=[box_final[k][0] for k in range(4)]
 ys=[box_final[k][1] for k in range(4)]
 index=ys.index(min(ys))
 global x_min_first, y_min_first
 x_min_first=xs[index]
 y_min_first=ys[index]
 
 #x_min_first, x_max=min(xs), max(xs)
 #y_min_first, y_max=min(ys), max(ys)
 print(" first x_min_first, y_min_first=", x_min_first," , ", y_min_first)
#############################################  
 global well_size
 well_size=382
####### 5. apply 
 global rot_bright
 rot_bright = cv2.warpAffine(first_bright,M,(cols,rows))
 global cut_bright
 cut_bright=rot_bright[y_min_first:y_min_first+well_size, x_min_first:x_min_first+well_size]
 #cut_bright = cv2.rotate(cut_bright_init, cv2.ROTATE_90_COUNTERCLOCKWISE)
 ##############################################
 global final_1
 final_1=turn_image_into_tkinter(cut_bright, 382) 
 canvas_mid.create_image(0,0, anchor=NW, image=final_1)
 seeds=[]
 upper.config(bg=label_color)
 lower.config(bg=label_color)
 global delta_x, delta_y
 delta_x, delta_y=0,0
######################################################

######################################################
def edit_first_frame_shift():
    canvas_mid.unbind("<Button-1>")
    canvas_mid.bind('<B1-Motion>', move)
    canvas_mid.bind("<ButtonRelease>", cut_and_save_first)
       
    canvas_mid.delete("all")  
    global x_img,y_img, points, x_last,y_last,dx,dy, x0,y0, br_image
    x0,y0=x_min_first, y_min_first
    #print("x0=", x0)
    #print("y0", y0)
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x0,y0,0,0
    points=[]
    global new_name
    head, tail=os.path.split(my_path)
    new_name=os.path.join(my_destin,tail)
    br_image= rot_bright
    global image1,imageFinal
    
    original_size=br_image.shape[0]
    image1=turn_image_into_tkinter(br_image, original_size)      
    imageFinal = canvas_mid.create_image(-x_min_first, -y_min_first, image = image1,anchor='nw')
    #canvas_right.create_image(-x_min-Margin, -y_min-Margin, image = image1,anchor='nw') 
###########################################################
def cut_and_save_first(event):
    global points, br_image, new_name, x0,y0, x_last, y_last, delta_x,delta_y
    points=[]
    
    #print("x_Last=", x_last)
    #print("y_last=", y_last)
    delta_x, delta_y=x_last-x0,y_last-y0
    patch=br_image[y_last:y_last+382, x_last:x_last+382]
    #patch=br_image[-y_last+y0+Margin:-y_last+382+y0+Margin, -x_last+x0+Margin:-x_last+382+x0+Margin]
    #print("patch.shape=", patch.shape)       
    cv2.imwrite(new_name, patch)
    global corrected_patch
    corrected_patch=turn_image_into_tkinter(patch, 382)      
    #imageFinal = canvas_right.create_image(x_img, y_img, image = image1,anchor='nw')
    canvas_mid.delete("all")
    canvas_mid.create_image(0,0, image = corrected_patch,anchor='nw')

############################################## command=lambda:threading.Thread(target=cut_and_save_fluor).start()
button_fluor=tk.Button(frame14_page3,text="7. Apply to all fluorescent",bg=button_color,activebackground="red",font=all_font, command=lambda: Thread(target=cut_fluor_wells).start())
button_fluor.grid(row=0, column=0,padx=10,pady=2)

l_fluor=Label(frame11_page3,text="      ", font=all_font,bg=bg_color, fg=result_color)
l_fluor.grid(row=5,column=0,padx=2)
################################  Frame 13

#################################
global new_fl_names
new_fl_names= None
#################################
   
def cut_bright_wells():
  #print("seed=", seed)
  #bright_names_sorted,fluor_names_sorted =load_image_names(source)
  global rotation_matrices,new_br_names, rotated_images, boxes, final_boxes
  rotation_matrices, new_br_names, rotated_images=[],[],[]
  boxes, final_boxes=[],[]
  for k in range(len(bright_names_sorted)):
    print("frame_number=", k+1)
    bright_name=bright_names_sorted[k]
    bright_image=cv2.imread(bright_name,-1)  
    final_bright,M,x_min, x_max,y_min, y_max, rows, cols, rot_indicator, rot_bright=cut_well_from_image(bright_image,seed,well_size,first_x0, delta_x, delta_y)
    rotation_matrices.append((M,x_min, x_max,y_min, y_max, rows, cols, rot_indicator))
    rotated_images.append(rot_bright) 
    final_bright_squeezed=cv2.resize(final_bright, (382,382), interpolation = cv2.INTER_AREA)
    #final_fluor_squeezed=cv2.resize(final_fluor, (382,382), interpolation = cv2.INTER_AREA)
    head, tail=os.path.split(bright_name)
    #new_name=os.path.join(destin_folder,tail)
    new_br_name=os.path.join(my_destin,tail)
    new_br_names.append(new_br_name)    
    #print("new_name=", new_name)
    cv2.imwrite(new_br_name, final_bright_squeezed)
    if k==0:
        global first_tk
        first=final_bright_squeezed
        first_tk=turn_image_into_tkinter(first, 382)
  global frame_slider    
  frame_slider=Scale(frame12_page3,from_=1,to=len(bright_names_sorted),orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide, length=150, showvalue=0)
  frame_slider.grid(row=2, column=0)
  frame_slider.set(1)

  #frame_slider.grid_remove()
  #seeds=[]
  upper.config(bg=label_color)
  lower.config(bg=label_color)
  l_bright.config(text="Bright images processed, total = " + str(len(new_br_names))+" frames")     
  l_finish.config(text="Scroll through frames to ensure that the well fits completely into each frame.\nIf it does not push Button 6 to repeat the procedure with a current frame."
                 "\nOtherwise, push Button 7 to apply to ALL FLUORESCENT images")  
 
  start_flash([button_fluor],"fluor", page3, flashers)
  button_bright.config(bg=button_color)
  canvas_right.delete("all")
  canvas_right.create_image(0,0, anchor=NW, image=first_tk)      
     
##################################
    
def cut_fluor_wells():

 stop_flash("fluor", page3, flashers)
 button_fluor.config(bg="red")
 progressbar_fluor = ttk.Progressbar(frame11_page3, orient='horizontal',mode='determinate',length=280)
 progressbar_fluor.grid(row=0, column=0,padx=10)
 l_fluor.config(bg="black")
  
 canvas_mid.delete("all")
 #############################
 global rotation_matrices,new_fl_names, first_tk_fl
 
 new_fl_names=[]
 for k in range(len(fluor_names_sorted)):
    print("fluorescent frame number = ", k+1)
    fluor_name=fluor_names_sorted[k]
    fluor_image=cv2.imread(fluor_name,-1)
    info=rotation_matrices[k] 
    M,x_min, x_max,y_min, y_max, rows, cols, rot_indicator=info[0], info[1],info[2],info[3],info[4], info[5], info[6], info[7]    
    rot_fluor = cv2.warpAffine(fluor_image,M,(cols,rows))
    #width, height=x_max-x_min,y_max-y_min
    #side=max(width,height)
    side=382
    cut_fluor=rot_fluor[y_min:y_min+side,x_min:x_min+side]
    #cut_fluor = cv2.rotate(cut_fluor_init, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if rot_indicator=="yes":
        final_fluor = cv2.rotate(cut_fluor, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        final_fluor=cut_fluor
    #final_fluor=rot_fluor[y_min-Margin:y_max+1+Margin,x_min-Margin:x_max+1+Margin]          
    final_fluor_squeezed=cv2.resize(final_fluor, (382,382), interpolation = cv2.INTER_AREA)
    head, tail=os.path.split(fluor_name)
    new_fl_name=os.path.join(my_destin,tail)
    new_fl_names.append(new_fl_name)   
    cv2.imwrite(new_fl_name, final_fluor_squeezed) 
    if k==0:       
        first_fl=final_fluor_squeezed
        first_tk_fl=turn_image_into_tkinter(first_fl, 382)
 canvas_mid.create_image(0,0, anchor=NW, image=first_tk_fl)
 frame_slider.set(1)               
 l_finish.config(text="Finished!\nThe input movie has been created and stored in folder\n "+str(my_destin)+
                 "\nNow, you are ready to proceed to STEP 3 of the pipeline.")
 l_fluor.config(text="Fluor images processed, total = " + str(len(new_fl_names))+" frames")
 stop_flash("fluor", page3, flashers)
 button_fluor.config(bg=button_color)    
###################################################

##################################################
button_bright=tk.Button(frame4_page3,text="5. Apply to all bright",bg=button_color,activebackground="red",font=all_font, justify=LEFT,command=lambda:[Thread(target=cut_bright_wells).start(),stop_flash("bright", page3, flashers)])
button_bright.grid(row=0, column=0,padx=10)

l_bright=Label(frame12_page3,text="      ", font=all_font,bg=bg_color, fg=result_color)
l_bright.grid(row=1,column=0,padx=2) 
##############################################
######################### scroll through all bright images
def slide(value):
    canvas_right.delete("all")
    image_number=int(value)    
    frame_slider.config(label="Frame "+str(value))       
    br_image=cv2.imread(new_br_names[image_number-1])
    global br_final  
    br_final=turn_image_into_tkinter(br_image, 382)     
    canvas_right.create_image(0,0, anchor=NW, image=br_final)
    if new_fl_names:
      fl_image=cv2.imread(new_fl_names[image_number-1])
      global fl_final
      fl_final=turn_image_into_tkinter(fl_image, 382)       
      canvas_mid.create_image(0,0, anchor=NW, image=fl_final)
######################################################################
def move(event):# drag image with mouse
    global x_img,y_img, points, x_last,y_last,dx,dy, imageFinal
    x, y = event.x, event.y   
    points.append([x,y])       
    if len(points)>1:
         dx, dy=x-x_img,y-y_img
         canvas_right.move(imageFinal, dx,dy)
         canvas_right.update()
         x_last-=dx
         y_last-=dy                
    x_img = x
    y_img = y
#####################  move image inside canvas_right with mouse ( correct shift in one particular frame)

   
################### save edits to current frame by releasing the mouse 
def cut_and_save(event):
    global points, br_image, new_name, x0,y0, x_last, y_last
    points=[]
    
    print("x_Last=", x_last)
    print("y_last=", y_last)
    patch=br_image[y_last:y_last+382, x_last:x_last+382]
    #patch=br_image[-y_last+y0+Margin:-y_last+382+y0+Margin, -x_last+x0+Margin:-x_last+382+x0+Margin]
    print("patch.shape=", patch.shape)       
    cv2.imwrite(new_name, patch)
    global corrected_patch
    corrected_patch=turn_image_into_tkinter(patch, 382)      
    #imageFinal = canvas_right.create_image(x_img, y_img, image = image1,anchor='nw')
    canvas_right.delete("all")
    canvas_right.create_image(0,0, image = corrected_patch,anchor='nw')
    
##################### activate editing frame shift for current frame in canvas_right
def edit_frame_shift():
    canvas_right.unbind_all("<Button-1>")  
    canvas_right.bind('<B1-Motion>', move)
    canvas_right.bind("<ButtonRelease>", cut_and_save)
    frame_number=frame_slider.get()
    print("frame_number=", frame_number)
    item=rotation_matrices[frame_number-1]
    x_min, x_max,y_min, y_max=item[1],item[2],item[3],item[4]
    
    canvas_right.delete("all")
  
    global x_img,y_img, points, x_last,y_last,dx,dy, rotated_images, x0,y0, br_image
    x0,y0=x_min, y_min
    #x0, y0=int(round((x_max+x_min)/2)),int(round((y_max+y_min)/2))
    print("x0=", x0)
    print("y0", y0)
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x0,y0,0,0
    points=[]
    
    br_image= rotated_images[frame_number-1]
    global image1, new_name, imageFinal
    new_name=new_br_names[frame_number-1]
    original_size=br_image.shape[0]
    image1=turn_image_into_tkinter(br_image, original_size)      
    imageFinal = canvas_right.create_image(-x_min, -y_min, image = image1,anchor='nw')
    #canvas_right.create_image(-x_min-Margin, -y_min-Margin, image = image1,anchor='nw')
#################################################################    
####################################
lower=Scale(frame3_page3, from_=0,to=255,orient=HORIZONTAL,variable=low_thr,length=150,bg=label_color,	
    showvalue=0,troughcolor="#513B1C",label="Threshold = "+str(None), command=low_thresh,
    activebackground="red", font=all_font)
lower.grid(row=0, column=0,padx=10,pady=5)
#######################################################
button_display=tk.Button(frame3_page3,text="3. Cut well",bg=button_color,activebackground="red",font=all_font, command=lambda:[cut_first_well(), start_flash([button_bright],"bright", page3, flashers), stop_flash("slide_thresh",page3,flashers) ])
button_display.grid(row=1, column=0,padx=10) 

button_first_shift_edit=tk.Button(frame3_page3,text="4. Edit well shift in Frame 1",bg=button_color,activebackground="red",font=all_font, command=edit_first_frame_shift)
#button_first_shift_edit.grid(row=1, column=0,padx=10,pady=(100,10))
button_first_shift_edit.grid(row=2, column=0,padx=10,pady=5)

#canvas_left.bind("<Button-1>", draw_circle)
#canvas_mid.bind("<Button-1>", choose_well)
####################################################################
button_shift_edit=tk.Button(frame4_page3,text="6. Edit well shift in current frame",bg=button_color,activebackground="red",font=all_font, command=edit_frame_shift)
button_shift_edit.grid(row=2, column=0,padx=10,pady=(10,10))


##############################################################



###########################################################################
############################   PAGE 4 : EXECUTE AND CORRECT TRACKING ##############################
###############################################################################
page4=pages[3]
page4.config(bg=bg_color)
frame1_page4 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame1_page4.grid(row=0, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

frame2_page4 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame2_page4.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3_page4 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame3_page4.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame4_page4 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame4_page4.grid(row=1, column=2, rowspan=2, columnspan=1, sticky=W+E+N+S)

frame5_page4 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame5_page4.grid(row=2, column=0, rowspan=1, columnspan=1)

frame6_page4 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame6_page4.grid(row=2, column=1, rowspan=1, columnspan=1)

frame7_page4 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame7_page4.grid(row=2, column=2, rowspan=1, columnspan=1)

frame8_page4 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame8_page4.grid(row=3, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame9_page4 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame9_page4.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame10_page4 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame10_page4.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame11_page4 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame11_page4.grid(row=4, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

canvas_previous = Canvas(frame5_page4, bg=bg_color, height=382, width=382)
canvas_previous.pack(anchor='nw', fill='both', expand=True)
canvas_current = Canvas(frame6_page4, bg=bg_color, height=382, width=382)
canvas_current.pack(anchor='nw', fill='both', expand=True)
##########################################
########################### These labels do not change
label_previous = tk.Label(frame8_page4, text="Previous Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_previous.grid(row=0, column=5, padx=100)

label_current = tk.Label(frame9_page4, text="Current Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_current.grid(row=0, column=0,padx=100)

label_lineage = tk.Label(frame10_page4, text="Lineage", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_lineage.grid(row=0, column=0, padx=100)
################################
canvas_lineage = Canvas(frame7_page4, bg=bg_color, height=382, width=382)
canvas_lineage.grid(row=0,column=0)
###################################################
global window_size, max_number_of_cells
#cell_radius=20# ususally 20, for 256x256 movies it is 7 
#patch_size=48 # usually 48, i.e. 96 x 96; for 256x256 it is =16  
#frame_size=382
window_size=382
max_number_of_cells=32

##################################


global show_3_canvases
from interface_functions import show_3_canvases

#####################################
global  lineage_per_frame_p4,start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions, cells
lineage_per_frame_p4,start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions, cells = None,1, {},{},{},{}
global out_folders, count, pedigree, flag
out_folders, pedigree,flag = [], None ," "
count = np.zeros((100), dtype="uint8")


global my_dir, edit_id_indicator
my_dir, edit_id_indicator = '', StringVar()
edit_id_indicator.set("no")

global per_cell_dict
per_cell_dict = {}
global clicked
clicked = StringVar()
clicked.set("Begin with 1 cell")

title_label = tk.Label(frame1_page4, text="STEP 3: EXECUTE AND CORRECT TRACKING",
              bg="yellow", fg="red", font=("Times", "24"))
title_label.grid(row=0, column=1, padx=2, sticky="n")
#################
def load_models(software_folder):    
    os.chdir(software_folder)
    global predict_first_frame, create_output_folders,\
        detect_division, update_dictionary_after_division, check_division_frame_number, predict_tracking, predict_tracking_general, backup_track, predict_first_frame, segment_and_clean,\
        create_previous_frame, plot_frame, create_color_dictionary,\
        create_pedigree, create_output_movie, create_models, extract_lineage,create_dictionary_of_xs,\
        create_lineage_image_one_frame, extract_file_name, load_clip, update_lineage,force_manual_IDs,create_lineage_for_Lorenzo

    from preprocess import create_output_folders, create_models, extract_file_name,load_clip

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_division_frame_number)

    from functions import (predict_tracking_general,  backup_track, predict_first_frame, segment_and_clean,
                           hungarian, create_previous_frame, predict_tracking, extract_lineage, update_lineage,force_manual_IDs)
    
    from plot import plot_frame, create_color_dictionary
    from postprocess import create_pedigree,  create_output_movie, create_dictionary_of_xs, create_lineage_image_one_frame
    from keras.models import model_from_json
    from extract_lineage_for_Lorenzo import create_lineage_for_Lorenzo

    from keras.optimizers import Adam
    global models, directory
    
    directory = os.path.join(software_folder, "TRAINED MODELS")
    model_names = ["Tracker-6","Segmentor", "Refiner"]
    #model_names = ["Tracker-1", "Tracker-2", "Tracker-3","Tracker-4","Tracker-5","Tracker-6",
                   #"Segmentor", "Refiner"]
    models = []
    for name in model_names:
                
        full_name = os.path.join(directory, name)
        print("full_name=", full_name)
        json_file = open(full_name + "-model.json", "r")
        model_read = json_file.read()
        json_file.close()        
        models.append((model_read, full_name)) 
    global tracker,segmentor,refiner  
    tracker, segmentor, refiner=create_models(models) 
    feedback_label.configure(text="Loading input movie ...")    
###########
input_info_label = tk.Label(frame1_page4, text=my_dir, bg="brown")
input_info_label.grid(row=2, column=1, padx=2)

progressbar = ttk.Progressbar(
    frame9_page4, orient='horizontal', mode='determinate', length=100)
#################################
def choose_folder():  
    button_load.configure(background = 'red')
    global my_dir
    my_dir = filedialog.askdirectory()
    input_info_label.config(text= "Input movie:"+ "\n"+str(my_dir)+"\n", fg="#00FFFF", bg="black")

    global out_folders, outpath, software_folder
    software_folder = os.path.dirname(my_dir)
    load_models(software_folder)
    input_movie_folder = os.path.basename(my_dir)
    outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    else:
        shutil.rmtree(outpath)# delete OUPUT if it exists
        os.mkdir(outpath)# create OUTPUT
    out_folders = create_output_folders(outpath)    
    ######## calcilate number of frames, core name in file names
    ######## and n_digits in numbering files in input movie 
    all_names_fluor=[]
    all_names_bright=[]
    for filename in os.listdir(my_dir):   
        if filename.endswith("ch00.tif"):
            feedback_label.configure(text="Loading input movie ...")                      
            full_name_fluor = os.path.join(my_dir, filename)
            all_names_fluor.append(full_name_fluor)
        else:
            full_name_bright = os.path.join(my_dir, filename)
            all_names_bright.append(full_name_bright)
    global num_frames, full_core_fluor_name, n_digits, first_frame_number, full_core_bright_name
    num_frames=len(all_names_fluor)
    full_core_fluor_name, n_digits, first_frame_number= extract_file_name(all_names_fluor[0])    
    input_info_label.config(text= "Input movie:"+ "\n"+str(my_dir)+"\nNumber of frames: "+str(num_frames), fg="#00FFFF", bg="black")
    del all_names_fluor
    full_core_bright_name, n_digits, first_frame_number= extract_file_name(all_names_bright[0])
    print("n_digits=", n_digits)
    del all_names_bright
    ########### load the first clip         
    global fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names                 
    fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(0,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number)
    global  frame_size, previous_lineage_image     
    frame_size=fluor_images[0].shape[0]
    global cell_radius,patch_size
    if frame_size==256:
        cell_radius, patch_size=7, 16
    else:
        cell_radius, patch_size=20, 48
    print("frame_size_before=", frame_size)
    if num_frames<=382:
        size=num_frames#this is the size of lineage image
    else:
        size=num_frames
    previous_lineage_image =np.zeros((size, size,3), dtype="uint8") 
    feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))   
    button_load.configure(background = '#9ACD32')   
    start_flash([R1, R2],"radio", page4, flashers)
######################################################
button_load = Button(frame1_page4, text="1. Click to open file menu and then select input movie folder",
               bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=choose_folder).start(), stop_flash("load", page4, flashers), feedback_label.configure(text="Loading input movie ...") ])
button_load.grid(row=2, column=0, padx=10, pady=20)
start_flash([button_load],"load", page4, flashers)
label_min_cells = tk.Label(
    frame1_page4, text="2. How many cells are there in Frame-1 ?",font='TkDefaultFont 10 bold', bg=label_color)
label_min_cells.grid(row=3, column=0, padx=2)
########################################


global manual_popup_centroids, coords_very_first # coords_very_first is necessary for plotting lineage later
manual_popup_centroids, coords_very_first= [],[]
################################
def begin_with_one_cell():# after pushing button "1 cell"
    stop_flash("radio", page4, flashers)
    feedback_label.configure(text="Calculating position of cell in Frame 1 ...")
    R1.configure(bg="red")
    R2.configure(bg=button_color)
    global coords, coords_very_first
    
           
    full_name = os.path.join(directory, "Tracker-1")
    print("full_name=", full_name)
    json_file = open(full_name + "-model.json", "r")
    model_read = json_file.read()
    json_file.close()        
        
    tracker_1 = model_from_json(model_read)
    tracker_1.load_weights(full_name + "-weights.h5")   
    tracker_1.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
       
    coords = predict_first_frame(fluor_images_compressed, tracker_1)  
    coords_very_first= coords.tolist()
    print("coords=", coords)    
    global colours, template_names, prev_frame
    colours, template_names = create_color_dictionary(
        max_number_of_cells, coords.shape[0])# 10 =maximum number of cells
    global xs
    xs=create_dictionary_of_xs( template_names, coords_very_first, num_frames)
  
    global text
    text = template_names[:coords.shape[0]]
    
    R2.configure(bg=button_color, fg="black")
    R1.configure(bg="black", fg="#00FFFF")
    
    start_flash([button_execute], "exec", page4, flashers)
    feedback_label.config(text="The centroids of the cell in Frame 1 has been calculated.\n\nTo start execution, press Button 3.")    
####################################   
R1 = Radiobutton(frame1_page4, text="1 cell", value="1 cell", font=all_font, variable=clicked, command=begin_with_one_cell, background=button_color, activebackground="red")
R1.grid(row=3, column=1, pady=10)
############################
def create_popup_canvas():
    stop_flash("radio", page4, flashers)
    feedback_label.configure(text="Waiting for manual assignment of cell positions in Frame 1 ...")
    R1.configure(bg=button_color, fg="black")
    global popup, popup_window_size
    popup_window_size=700
    popup = tk.Toplevel(master=page4, width=popup_window_size, height=popup_window_size)
    sub1 = tk.Frame(master=popup, width=popup_window_size, height=50, bg="#A52A2A")
    sub1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    global label_click_popup
    label_click_popup = tk.Label(
        sub1, text="Click on each cell with the left button of the mouse,\nthen save", bg="black",fg="yellow", font='TkDefaultFont 10 bold')
    label_click_popup.pack()
     
    sub2 = tk.Frame(master=popup, width=popup_window_size, height=popup_window_size, bg="#A52A2A")
    sub2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

    global canvas_popup
    canvas_popup = Canvas(sub2, bg='black', height=popup_window_size, width=popup_window_size)
    canvas_popup.pack(anchor='nw', fill='both', expand=True)
    canvas_popup.bind("<Button-1>", draw_circle)
    
      
    sub3 = tk.Frame(master=popup, width=popup_window_size, height=50, bg="#A52A2A")
    sub3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    global button_save_popup
    button_save_popup = Button(sub3, text="Save", bg=button_color,activebackground="red", command=close_popup_canvas)
    button_save_popup.pack()
    start_flash([button_save_popup], "save", popup,flashers)
    
    full_name = fluor_names[0]
    global photo  
    photo = Image.open(full_name)
    photo = photo.resize((popup_window_size, popup_window_size), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(photo)
    canvas_popup.create_image(0, 0, anchor=NW, image=photo)
    stop_flash("label", popup,flashers)
    stop_flash("radio", page4, flashers)
    label_min_cells.configure(background = label_color)   
#############################

#################################    
def close_popup_canvas():      
     
      stop_flash("save", popup,flashers)    
      global coords, manual_popup_centroids, coords_very_first    
      stop_flash("click", popup, flashers)
      start_flash([button_save_popup], "save", popup, flashers)
      coords_very_first=manual_popup_centroids
      global colours, template_names
      colours, template_names = create_color_dictionary(
        max_number_of_cells, len(manual_popup_centroids))# 10 =maximum number of cells
     
      global xs
      xs=create_dictionary_of_xs( template_names, coords_very_first, num_frames)   
      N_cells=len(manual_popup_centroids)      
      global text, flag,  edit_id_indicator
      text = template_names[:N_cells]# names of cell in the current frame
      flag="manual centroids"
      edit_id_indicator.set("yes")
      coords = np.zeros((N_cells, 2))
      print("xs=", xs)
      print("template_names=", template_names)
      print("text=", text)
      print("xs=", xs)
      
      #prev_frame = np.zeros((frame_size, frame_size), dtype="float64")
     
      for i in range(N_cells):
        coords[i] = manual_popup_centroids[i]
        
      print("coords=", coords)
      R2.configure(text =str(len(coords))+ " cells" ,background="black", fg="#00FFFF")
      feedback_label.config(text="The positions of cells in Frame 1 has been saved.\n\nTo start execution, press Button 3.")
      stop_flash("save", popup, flashers)
      start_flash([button_execute], "exec", page4, flashers)   
      popup.destroy()
    
#######################################
R2 = Radiobutton(frame1_page4, text="More than 1 cell",background=button_color, font='TkDefaultFont 10 bold',
                 value="More than 1 cell", activebackground="red",variable=clicked, command=create_popup_canvas)
R2.grid(row=3, column=2)
################ draw red spots in popup canvas in response to mouse click
def draw_circle(event):
    canvas_popup.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    manual_popup_centroids.append([event.x/popup_window_size*frame_size, event.y/popup_window_size*frame_size])
####################################################  
global text, variable_stop, manual_division_indicator, mother_number
text, variable_stop, manual_division_indicator, mother_number=StringVar(), "Do not stop", StringVar(), IntVar()
manual_division_indicator.set("no")
#############################################################

zero_image = Image.new('RGB', (window_size, window_size))
zero_image = ImageTk.PhotoImage(zero_image)
global lineage_images, output_images
lineage_images, output_images, lineage_images_cv2=[], [zero_image],[] 
############################################################
def clear_memory_of_models(tracker, segmentor, refiner):     
     keras.backend.clear_session()    
     if segmentor:       
        del segmentor     
     if refiner:
         del refiner        
     if tracker:      
          del tracker    
     tf.reset_default_graph() 
###########################################
def cut_lineage(start_frame): # after manual editing
    lineage_per_frame_p4=extract_lineage(outpath)
    del lineage_per_frame_p4[(start_frame)-1:]# was -1       
    update_lineage(lineage_per_frame_p4,outpath,'wb')
    global output_images,lineage_images,lineage_images_cv2    
    del output_images[(start_frame):]   
    global previous_lineage_image    
    previous_lineage_image=lineage_images_cv2[start_frame-1]   
    del lineage_images_cv2[(start_frame-1):] 
    del lineage_images[(start_frame-1):]         
    global dict_of_divisions 
    print("dict_of_divisios before cut_lineage=", dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val < start_frame}
    print("dict_of_divisios after cut_lineage=", dict_of_divisions) 
###########################################################
def create_big_monitor_popup():
    
    global popup_monitor, popup_window_size
    popup_window_size=800
    popup_monitor = tk.Toplevel(master=page4, width=popup_window_size*2, height=popup_window_size)
         
    sub1_mon = tk.Frame(master=popup_monitor, width=popup_window_size, height=popup_window_size, bg="#A52A2A")
    sub1_mon.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    sub2_mon = tk.Frame(master=popup_monitor, width=popup_window_size, height=popup_window_size, bg="#A52A2A")
    sub2_mon.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    global canvas_popup_previous, canvas_popup_current
    canvas_popup_previous = Canvas(sub1_mon, bg='black', height=popup_window_size, width=popup_window_size)
    canvas_popup_previous.pack(anchor='nw', fill='both', expand=True)
    
       
    canvas_popup_current = Canvas(sub2_mon, bg='black', height=popup_window_size, width=popup_window_size)
    canvas_popup_current.pack(anchor='nw', fill='both', expand=True)
         
    sub3_mon = tk.Frame(master=popup_monitor, width=popup_window_size, height=400, bg="yellow")
    sub3_mon.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    sub4_mon = tk.Frame(master=popup_monitor, width=popup_window_size, height=400, bg="yellow")
    sub4_mon.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
#####################################
import time
########################################################
def execute():
 start_time=time.time()
 try:
    canvas_previous.delete("all")
    canvas_current.delete("all")
    canvas_lineage.delete("all")
    button_execute.configure(background = 'red')
    stop_flash("exec", page4, flashers)
    label_edit_results.configure(text=" ")
    label_edit_instructions.configure(text=" ")
    feedback_label.config(text="Wait, loading models ...", fg="yellow")
    global lineage_images, output_images, lineage_per_frame_p4, pedigree, previous_lineage_image     
    if lineage_per_frame_p4:
        del lineage_per_frame_p4
    if pedigree:
        del pedigree
    
    global variable_stop, start_frame, tracker, segmentor, refiner# this variable allows to stop the loop (controlled by Stop button)     
    global coords, prev_frame,  count, text, cells, old_number_of_cells, edit_id_indicator    
    N_cells = coords.shape[0]
    division_indicator=0
    centroids_for_benchmarking=[coords]
    n =num_frames  
    k = start_frame-1  # the first frame of clip     
    kk = 0  # the number of frame within clip   
    clear_memory_of_models(tracker, segmentor, refiner)
    tracker, segmentor, refiner=create_models(models)   
    feedback_label.config(text="Execution is about to begin ...")
    start_flash([button_pause],"pause", page4, flashers)
    progressbar.grid(row=1, column=0, padx=20)
    progressbar["value"]=((start_frame)/num_frames)*100
    while k < n:
        global fluor_images, fluor_images_compressed,bright_images, fluor_names, bright_names
        if k>0:
         del fluor_images, fluor_images_compressed,bright_images, fluor_names, bright_names 
         fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(k,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number)
       
        clip_centr = predict_tracking_general(
                coords, fluor_images, fluor_images_compressed, fluor_names, k, out_folders[0], tracker,n, cell_radius, frame_size)
        print("TRACKING PREDICTED FOR CLIP BEGINNING WITH FRAME  ", k+1)
        print("clip_centr=", clip_centr) 
       
        
        for kk in range(len(clip_centr)):# it is actually 4 (number of frames in clip)
            print("FRAME NUMBER = ", k+kk+1)# segmenting all the 4 frames in the clip
            progressbar["value"]=((k+kk+1)/num_frames)*100
            time.sleep(0.02)
            frame9_page4.update_idletasks()
            print("edit_id_indicator.get()=",edit_id_indicator.get())
            if  edit_id_indicator.get()=="yes" and kk==0:
                clip_centr=force_manual_IDs(clip_centr,coords,kk, cell_radius)
                edit_id_indicator.set("no")
            else:
                clip_centr =  backup_track(
                   clip_centr, coords, kk, cell_radius)  # correct too big jumps
                      
            tracked_centroids=clip_centr[kk]
            print("corrected centroids=", tracked_centroids)     
            empty_fluor = fluor_images[kk]         
            empty_bright = bright_images[kk]            
            count, cells, coords,  text, number_of_splits = segment_and_clean(
                dict_of_divisions, cells, count, coords,text, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, k+kk, edit_id_indicator, mother_number, out_folders, cell_radius, frame_size, colours, patch_size, "first cleaning")
            #splits.append(number_of_splits)           
            print("cell names after segmentation=", list(cells.keys()))           
            ################## Division Detector,look for figure 8 shape          
            if manual_division_indicator.get()=="yes":
                daughter_1_name=mother_name+"0"
                daughter_2_name=mother_name+"1"
                for key in cells.keys():
                    name=cells[key][11]
                    if name==daughter_1_name:                     
                        cells[key][16]="daughter-1"
                    if name==daughter_2_name:
                        cells[key][16]="daughter-2"                           
            else:
               division_indicator = 0  
               count, cut_patch, mother_8_name = detect_division(
                   cells, count, k, kk)             
               if (np.any(count == 2) or np.any(count == 1)):                  
                   if mother_8_name != []:
                       count = check_division_frame_number(
                           count, cells, dict_of_divisions, mother_8_name, k+kk)                      
               if np.any(count == 2):
                 
                   
                   cells, text, count, division_indicator, coords = update_dictionary_after_division(
                       cut_patch, cells, text, count, division_indicator, coords, frame_size, colours)
               if division_indicator == 1 and mother_8_name != []:                   
                   dict_of_divisions[mother_8_name] = k+kk
                   print("mother_cell_name =", mother_8_name)                  
                   print("8-figure division detected in frame ", k+kk)                 
            ####################################################                       
            if manual_division_indicator.get()=="yes":
                 manual_division_indicator.set("no")
               
            update_lineage([cells],outpath,'ab')# upload cells to pickle (to make lineage_per_frame)
            feedback_label.config(text="Execution in progress: \nFrame "+ str(k+kk+1)+"\n - If you need to stop for editing, press Button 3a."
                            "\n - Otherwise, wait until execution is finished.")
            label_current.configure(text="Current frame: " +str(k+kk+1), fg="red")           
            N_cells = len(cells)
            print("cells after division detector=", list(cells.keys()))
            print("n_digits_inside execute=", n_digits)
            coords, destin_fluor = plot_frame(cells, clip_centr, k, kk,
                                fluor_images, fluor_names, out_folders, coords, coords, bright_images, bright_names, frame_size , n_digits, first_frame_number)          
            current_lineage_image=create_lineage_image_one_frame(out_folders,cells, previous_lineage_image, xs, k+kk)
            
            previous_lineage_image=current_lineage_image# need it for the next lineage image                      
            image_seg=destin_fluor
            photo_image_seg=turn_image_into_tkinter(image_seg, window_size)
            canvas_current.create_image(0,0,anchor=NW,image=photo_image_seg)
            output_images.append(photo_image_seg)
                     
            image_lin=current_lineage_image
            image_lin_copy=copy.deepcopy(image_lin)         
            lineage_images_cv2.append(image_lin_copy)                    
            photo_image_lin=turn_image_into_tkinter(image_lin, window_size)
            canvas_lineage.create_image(0,0,anchor=NW,image=photo_image_lin)          
            lineage_images.append(photo_image_lin)
           
            centroids_for_benchmarking.append(coords)            
            #prev_frame = create_previous_frame(cells, frame_size)
                              
            if (division_indicator == 1):
                print("division occured in frame ", k+kk+1)              
                dict_of_divisions[text[-1][:-1]] = k+kk
                break        
        if (division_indicator == 1):
            k = k+kk+1
            N_cells = coords.shape[0]
            #clear_memory_of_models(trackers, segmentor, refiner)
            #trackers, segmentor, refiner=create_models(N_cells, models)              
        else:
            k += 4                
        if variable_stop=="Stop":              
               start_frame=k+1                                                                  
               stop_flash("pause", page4,flashers)
               break       
 except:
       feedback_label.config(text="Stopped due to error", fg="#DF0101", font='TkDefaultFont 10 bold')      
       #start_frame=k+kk+1            
       print("Stopped due to error!!!!!")
       tk.messagebox.showerror('Error',traceback.format_exc())
       stop_flash("pause", page4,flashers)     
 if variable_stop=="Stop":
     feedback_label.config(text="You stopped execution manually. \nPress Button 4 to check results." )
     variable_stop="Do not stop"
 else:
     feedback_label.config(text="Execution finished! \nPress Button 4 to check results." )
     finish_time=time.time()
     execution_time=finish_time-start_time
     print("execution_time=", execution_time)
 button_execute.configure(background = '#9ACD32')
 start_flash([button_display],"display", page4, flashers)
 stop_flash("pause", page4, flashers)
 button_pause.configure(background = '#9ACD32')
 print("dict_of_divisions after execution =", dict_of_divisions) 
###############################################
button_execute = Button(frame2_page4, text="3. Execute", font='TkDefaultFont 10 bold', 
               bg='#9ACD32', activebackground="red",command=lambda:[threading.Thread(target=execute).start(), stop_flash("exec", page4, flashers)])               
button_execute.grid(row=0, column=0, pady=20)

feedback_label = tk.Label(frame1_page4, text=" Welcome to STEP 3 of the pipeline! \n\nTo choose input movie you want to track, press Button 1. ",fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
feedback_label.grid(row=1, column=0,columnspan=4, sticky=W)
#############################################################
def stop_execution_manually():
    button_execute.configure(background = button_color)
    global variable_stop
    variable_stop = "Stop"
    button_pause.configure(background = '#9ACD32')
#################################################################    
button_pause = Button(frame2_page4, text="3a. Pause ",activebackground="red",
               bg='#9ACD32', font='TkDefaultFont 10 bold', command=lambda: [stop_execution_manually(), stop_flash("pause", page4, flashers)])
button_pause.grid(row=0, column=2, padx=10, pady=20)  
#############################
def slide_frames(value):
    image_number = int(value)    
    show_3_canvases(canvas_previous,canvas_current,canvas_lineage,output_images,lineage_images,image_number)
##############################################
def display_first_frame():
    image_number=1    
    show_3_canvases(canvas_previous,canvas_current,canvas_lineage,output_images,lineage_images,image_number)
    progressbar.grid_forget() 
       
    global pedigree, lineage_per_frame_p4
    lineage_per_frame_p4=extract_lineage(outpath)
    # creates and saves per cell pedigree  
    pedigree = create_pedigree(lineage_per_frame_p4, outpath, frame_size) 
        
    feedback_label.config(text="Check results by sliding the bar under Current Frame."
                    "\n - If you need to edit cell IDs, press Button 5."
                    "\n - If you need to edit missed division, press Button 6."
                    "\n - If you are happy with the result press Button 7 to create lineage movie.")   
    global view_slider
    view_slider = Scale(frame9_page4, from_=1, to=len(
        output_images)-1, orient=HORIZONTAL, troughcolor="green", command=slide_frames, length=370)      
    view_slider.grid(row=0, column=0, pady=5)
    button_display.configure(background = '#9ACD32')  
    threading.Thread(target=start_flash([button_start_id, button_start_division], "edit", page4, flashers)).start()  
################################################
button_display = Button(frame2_page4, text="4. Display result", font='TkDefaultFont 10 bold', 
               bg='#9ACD32',activebackground="red", command=lambda: [display_first_frame(), stop_flash("display", page4, flashers)])
button_display.grid(row=2, column=0, padx=20)
##################################
global manual_IDs,manual_centroids,mother_name 
manual_IDs,  manual_centroids, mother_name=[], [], None
###########3#######################
def get_cell_IDs_manually(event):# gets cell ID from previous frame during editing
    global manual_IDs  
    keys=list(lineage_per_frame_p4[int(view_slider.get())-2].keys())#was -2  
    previous_image=lineage_per_frame_p4[int(view_slider.get())-2][keys[0]][13]
    
    #previous_resized =cv2.resize(previous_image, (window_size,window_size), interpolation = cv2.INTER_AREA)  
    #cell_number=int(previous_resized[event.y,event.x])-1
    cell_number=int(previous_image[int(event.y/window_size*frame_size),int(event.x/window_size*frame_size)]-1)
    manual_IDs.append(cell_number)
    print("manual_IDs=", manual_IDs)     
    cell_name_internal="cell_"+ str(cell_number) 
    cell_name_external=lineage_per_frame_p4[int(view_slider.get())-2][cell_name_internal][11]# was -1  
    cell_names_external.append(cell_name_external)    
    colour_four_channel=colours[cell_name_external]    
    colour_three_channel=colour_four_channel[:-1]
    colour_three_channel.reverse()    
    global colour
    colour="#%02x%02x%02x" % tuple(colour_three_channel)
    canvas_previous.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    label_edit_results.configure(text="Cells chosen in Previous Frame:\n " + str(cell_names_external) +"\n", bg="black")  
########################
def get_centroids_manually(event):
 
    canvas_current.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    manual_centroids.append([event.x/window_size*frame_size, event.y/window_size*frame_size])   
    label_edit_results.configure(text="Cells chosen in Previous Frame:\n " + str(cell_names_external) +"\n""Centroids assigned in Current Frame:\n " + str(manual_centroids), bg="black")
######################################
def start_editing_IDs():
    label_edit_instructions.configure(text="Click on the cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on the same cell in Current Frame \nMake sure you click on the centroid!")
  
    feedback_label.configure(text="First, click on the cell of interest in Previous Frame.\n"
               "Then, click on its desired position in Current Frame.\n You can repeat it MULTIPLE TIMES.\nFinally, save edits by pressing 5a.Save ID edits.")    
    global manual_centroids, manual_IDs, cell_names_external
    manual_centroids, manual_IDs, cell_names_external=[],[], [] 
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    start_flash([button_save_id], "save_id", page4, flashers)
    threading.Thread(target=stop_flash("edit", page4, flashers)).start()
    stop_flash("edit", page4, flashers)
    button_start_division.configure(background = '#9ACD32')
    button_start_id.configure(background = 'red')
    print("dict_of_divisions after start_editing_IDs =", dict_of_divisions) 
####################################################
def stop_editing_IDs():
    button_start_id.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>") 
    global start_frame, lineage_per_frame, edit_id_indicator
    edit_id_indicator.set("yes")
    
    start_frame=int(view_slider.get())
    print("start_frame=", start_frame)
    keys=list(lineage_per_frame_p4[start_frame-1].keys())   
    coords_old=lineage_per_frame_p4[start_frame-1][keys[0]][14]
    print("coords_old=", coords_old)
    #############another error is here
    for i in range(len(manual_centroids)):
        coords_old[manual_IDs[i]]=manual_centroids[i] 
    #############
    global coords, text
    coords=coords_old 
    print("coords=", coords)
    global prev_frame    
    prev_frame=lineage_per_frame_p4[start_frame-1][keys[0]][13]    
    feedback_label.config(text="")
    print("text_before=",text) 
    cut_lineage(start_frame)
    
    text1=[lineage_per_frame_p4[start_frame-2][key][11] for key in keys]
    print("text1=",text1)
    numbers=[lineage_per_frame_p4[start_frame-2][key][17] for key in keys]
    print("numbers=",numbers)
    w=list(zip(numbers,text1))
    ww=sorted(w,key=lambda student:student[0])
    ress = list(zip(*ww))
    text =list(ress[1])        
    
    
    print("text_after=",text)
    

    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    start_flash([button_execute],"exec", page4, flashers)
    stop_flash("save_id", page4, flashers)
    view_slider.grid_remove()
    label_current.configure( text="Current frame", fg="black" )
    button_save_id.configure(background = '#9ACD32')  
    button_save_division.configure(background = '#9ACD32')
    feedback_label.config(text="You finished editing IDs.\n To resume execution, press Button 3." )
    print("dict_of_divisions after stop_editing_IDs =", dict_of_divisions) 
###################################################

##################################################
def start_editing_division():   
    label_edit_instructions.configure(text="Click on mother cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on daughter cells in Current Frame \nMake sure you click on centroids!")
    print("started manual division editing.....")
    global mother_number
    mother_number=None 
    feedback_label.configure(text="First, click on mother cell in Previous Frame.\n"
               "Then, click on daughter cells in Current Frame.\nYou can do it ONLY ONCE.\n Finally, save by pressing 6a. Save division edits.")    
    global manual_centroids, manual_IDs,cell_names_external
    manual_centroids, manual_IDs, cell_names_external=[],[],[]   
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    #button_final_movie.configure(background = button_color)
    start_flash([button_save_division],"save_division", page4, flashers)  
    threading.Thread(target=stop_flash("edit", page4, flashers)).start()
    button_start_division.configure(background = 'red')
    button_start_id.configure(background = '#9ACD32')
    #button_final_movie.configure(background = '#9ACD32')
########################################
def stop_editing_division():
    button_start_division.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>")
    global text, prev_frame
    text=[]  
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())    
    keys=list(lineage_per_frame_p4[start_frame-1].keys())# from previous frame was -2   
    prev_frame=lineage_per_frame_p4[start_frame-1][keys[0]][13]# prev_frame-1 is not a mistake!!! was -1
   
    coords_old=lineage_per_frame_p4[start_frame-1][keys[0]][14] 
    global manual_IDs, mother_number, mother_name    
    manual_division_indicator.set("yes")
    mother_number=manual_IDs[0] 
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage_per_frame_p4[start_frame-2][mother_name_internal][11]
    mother_color=lineage_per_frame_p4[start_frame-2][mother_name_internal][-2]
                                        
    daughter_1_number=mother_number
    daughter_2_number=len(coords_old)    
    daughter_1_name=mother_name+"0"
    daughter_2_name=mother_name+"1"
    
    all_cell_numbers=[]# from prev_frame, for creating daughter names
    m=int(np.max(prev_frame))
    for i in range(1,m+1):
      if np.any(prev_frame==i):
          all_cell_numbers.append(i-1)     
    all_cell_numbers_sorted =sorted(all_cell_numbers)
    dict_keys=list(lineage_per_frame_p4[start_frame-2].keys()) # in case there are overlaps in previous frame after segmentation
    for num in all_cell_numbers_sorted:
        cell_key="cell_"+str(num)
        if cell_key in dict_keys:
            true_cell_name=lineage_per_frame_p4[start_frame-2][cell_key][11] 
            text.append(true_cell_name)
    text[mother_number]=daughter_1_name
    text.append(daughter_2_name)  
    coords_daughter_1=manual_centroids[0]
    coords_daughter_2=manual_centroids[1]
    coords_old[mother_number]=coords_daughter_1    
    coords_old=np.concatenate((coords_old,np.array(coords_daughter_2).reshape((1,2))))    
    global  coords
    coords=coords_old 
    global dict_of_divisions
    print("dict_of_divisions before =", dict_of_divisions)
    dict_of_divisions[mother_name] = start_frame-1
    print("dict_of_divisions after =", dict_of_divisions)
    cut_lineage(start_frame)
    print("dict_of_divisions final =", dict_of_divisions)
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    view_slider.grid_remove()
    label_current.configure( text="Current frame", fg="black" )
    start_flash([button_execute], "exec", page4, flashers)
    stop_flash("save_division", page4, flashers)
    button_start_division.configure(background = '#9ACD32')
    button_save_division.configure(background = '#9ACD32')
    feedback_label.config(text="You finished editing missed division.\n To resume execution, press Button 3." )   
#######################################
button_start_id = Button(frame3_page4, text="5. Start editing IDs", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:start_editing_IDs())
button_start_id.grid(row=0, column=0)

label_edit_instructions = tk.Label(frame3_page4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow", width=50, height=4)
label_edit_instructions.grid(row=2, column=0, columnspan=2)

button_save_id = Button(frame3_page4, text="5a. Save ID edits", activebackground="red",font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:stop_editing_IDs())
button_save_id.grid(row=3, column=0)
###############################################################
button_start_division = Button(frame4_page4, text="6. Start editing division", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:[threading.Thread(start_editing_division()).start(), stop_flash("edit", page4, flashers)])
button_start_division.grid(row=6, column=0)

label_edit_results = tk.Label(frame4_page4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="#00FFFF", width=45, height=4)
label_edit_results.grid(row=7, column=0)

button_save_division = Button(frame4_page4, text="6a. Save division edits",activebackground="red", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:stop_editing_division())
button_save_division.grid(row=8, column=0, columnspan=1)
###########################################################################
############################## PAGE-5 (STEP-4): CORRECT SEGMENTATION #######
#############################################################################
page5=pages[4]
page5.title("4. CORRECT SEGMENTATION")
page5.config(bg=bg_color)
from helpers_for_PAGE_4 import delete_contour_with_specific_colour,update_lineage_after_manual_segm_correction, load_models_p5, load_tracked_movie
from plot import paste_patch, prepare_contours,paste_benchmark_patch
#from functions import seeded_watershed_final
from interface_functions import turn_image_into_tkinter,display_both_channels, show_2_canvases
from postprocess import create_output_movie
from extract_lineage_for_Lorenzo import create_lineage_for_Lorenzo
from functions import  clean_manual_patch, segment_manual_patch,segment_one_cell_at_a_time
############ LAYOUT

page5.geometry('1530x2000')
#bg_color,all_font,button_color,result_color,label_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA"

global window_p5_size
window_p5_size =600

frame1_page5 = tk.Frame(master=page5, width=1528, height=5, bg=bg_color)
frame1_page5.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page5 = tk.Frame(master=page5, width=1528, height=50, bg=bg_color)
frame2_page5.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page5 = tk.Frame(master=page5, width=1528, height=50, bg=label_color)
frame3_page5.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame4_page5 = tk.Frame(master=page5, width=1528, height=50, bg=bg_color)
frame4_page5.grid(row=3, column=0, rowspan=1, columnspan=4,sticky=W+E+N+S)
############################################################################
frame5_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size, bg=bg_color)
frame5_page5.grid(row=4, column=0,rowspan=1,columnspan=1, sticky=W)

frame6_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size , bg=bg_color)
frame6_page5.grid(row=4, column=1,rowspan=1,columnspan=1, sticky=W)

frame7_page5 = tk.Frame(master=page5, width=100 , height=window_p5_size , bg=bg_color)
frame7_page5.grid(row=4,column=2,rowspan=1,columnspan=1, sticky=W)
#################################################################

frame8_page5 = tk.Frame(master=page5, width=50, height=window_p5_size, bg=bg_color)
frame8_page5.grid(row=5, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

######### POPULATE WITH WIDGETS

global canvas_fluor_p5
canvas_fluor_p5 = Canvas(frame6_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_fluor_p5.pack(anchor='nw', fill='both', expand=True)
global canvas_bright_p5
canvas_bright_p5 = Canvas(frame5_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_bright_p5.pack(anchor='nw', fill='both', expand=True)


l_title = tk.Label(frame1_page5, text="STEP 4: CORRECT SEGMENTATION",
              bg="yellow", fg="red", font=("Times", "24"))
l_title.grid(row=0, column=3, padx=500, sticky="n")


dialog_label_5 = tk.Label(frame3_page5, text=" Welcome to Step-4.\nThis page allows you to manually correct segmentation in a tracked movie."
                          "\nTo load a tracked movie, click Button 1 and navigate to OUTPUT_MOVIE_[specific movie name]",
                          fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=200,height=4)
dialog_label_5.grid(row=0, column=0, sticky="w")
##########################################

#global cell_radius, patch_size, frame_size
global list_of_modified_frames, points
#cell_radius_p5=20# ususally 20, for 256x256 movies it is 7 
#patch_siz_p5e=48 # usually 48, i.e. 96 x 96; for 256x256 it is =16  

list_of_modified_frame, points=[], []

###########################################


###################################################
def slide_frames_p5(value):
    image_number = int(value)    
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,image_number, window_p5_size)    
############################# load all mecessary images
global button_load_p5
def choose_and_load_tracked_movie():
    global button_load_p5
    #button_load.configure(background = 'red')
    global output_dir, input_dir,software_folder
    output_dir = filedialog.askdirectory()
    #software_folder = os.path.dirname(output_dir)       
    head_tail=os.path.split(output_dir)
    head =head_tail[0]
    tail =head_tail[1]
    input_movie_name=tail[7:]
    input_dir  =os.path.join(head,input_movie_name)
    
    global path_filled_brights,path_filled_fluors,path_masks
    global empty_fluors, empty_brights, filled_fluors, filled_brights, masks
    global lineage_per_frame_p5
    dialog_label_5.config(text="loading tracked movie...")
    path_filled_brights,path_filled_fluors,path_masks, empty_fluors, empty_brights, filled_fluors, filled_brights, masks, lineage_per_frame_p5=load_tracked_movie(input_dir,output_dir)
    global frame_p5_size
    frame_p5_size=int(empty_fluors[0].shape[0])
    global cell_radius_p5,patch_size_p5
    if frame_p5_size==256:
        cell_radius_p5, patch_size_p5=7, 16
    else:
        cell_radius_p5, patch_size_p5=20, 48
    
    print("frame_p5_size=",frame_p5_size)
    global photo_filled_fluors, photo_filled_brights
    dialog_label_5.config(text="Preparing images for display...")
    photo_filled_fluors=[ turn_image_into_tkinter(filled_fluors[i], window_p5_size) for i in range(len(masks))]
    dialog_label_5.config(text="Prepared 50 % of images for display")
    photo_filled_brights=[ turn_image_into_tkinter(filled_brights[i], window_p5_size) for i in range(len(masks))]
    dialog_label_5.config(text="To check segmentation in each frame, use the slide bar below."
                            "\nIf manual correction is needed in a ceartain frame, push button 2.")
    
   
  
    global canvas_fluor_p5, canvas_bright_p5

    image_number=1    
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,image_number, window_p5_size)     
    global view_slider_p5
    view_slider_p5 = Scale(frame4_page5, from_=1, to=len(
        masks), orient=HORIZONTAL, troughcolor="green", command=slide_frames_p5, length=370)      
    view_slider_p5.grid(row=1, column=2, pady=2)
    button_load.configure(background = button_color)
    
################################################
#global modified_cell_IDs,final_mask
#modified_cell_IDs,final_mask=[],np.zeros((frame_size,frame_size), np.uint16)

############# This is the 1st type of segmentation correction: just click on cells
############# in any order. You do not need to save. 
###################################################
global old_cell_color, old_cell_number
old_cell_color, old_cell_number=[255,255,255,255],-2

#############################################
def get_frame_info():
    button_frame_info.configure(background = 'red')
    
    global segmentor, refiner
    if segmentor==None and refiner==None:      
        software_folder = os.getcwd() 
        segmentor, refiner= load_models_p5(software_folder)
        dialog_label_5.config(text="Loaded models")
    global frame_number
    frame_number=view_slider_p5.get()
    print("frame_number=", frame_number)
    global frame_dictionary
    frame_dictionary=lineage_per_frame_p5[frame_number-1]
    keys=list(frame_dictionary.keys())
    global cells_in_current_frame_sorted
    cells_in_current_frame=[(frame_dictionary[key][11],frame_dictionary[key][15],frame_dictionary[key][17]) for key in keys]    
    cells_in_current_frame_sorted=sorted(cells_in_current_frame,key=lambda student: student[2])
    text_for_print=[cells_in_current_frame_sorted[i][0] for i in range(len(cells_in_current_frame_sorted))]
    print("cells_in_current_frame_sorted=", cells_in_current_frame_sorted)
    dialog_label_5.config(text="Cells detected in the current frame :  " +str(text_for_print)+
                          "\nThere are 2 manul segmentation techniques available: 1. Button 3 (fast correction) where correction is achieved just by clicking on the cell"
                          "   2.  Button 4 (hand drawing) where correction is done by drawing with the mouse."
                          "\nIt is recommended to start with Button 3.")
    global modified_cell_IDs
    modified_cell_IDs=[]
    global mask, empty_fluor, empty_bright
    mask=masks[frame_number-1]
    empty_fluor=empty_fluors[frame_number-1]
    empty_bright=empty_brights[frame_number-1]
    global filled_fluor_init, filled_bright_init
    filled_fluor_init=filled_fluors[frame_number-1]
    filled_bright_init=filled_brights[frame_number-1]    
    #######################################
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_init,filled_bright_init,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
    #########################################    
    global path_filled_bright, path_filled_fluor,path_mask
    path_filled_bright, path_filled_fluor,path_mask= path_filled_brights[frame_number-1],path_filled_fluors[frame_number-1],path_masks[frame_number-1]
    global final_mask, filled_fluor,filled_bright
    final_mask, filled_fluor, filled_bright = copy.deepcopy(mask),copy.deepcopy(filled_fluor_init), copy.deepcopy(filled_bright_init)
    #final_mask=mask.copy()
    button_frame_info.configure(background = button_color)
    
    
##########################################################
def start_editing_by_clicking():
   canvas_fluor_p5.unbind_all("<Button-1>")
   canvas_fluor_p5.unbind_all("<Button-1>")   
   canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)
   canvas_fluor_p5.unbind_all("<Button-3>")
  
   canvas_fluor_p5.bind("<Button-3>", extract_cell_ID_and_marker_by_right_click)
   button_start.configure(background = 'red')
   dialog_label_5.config(text="\nIn the right image, right-click on the cell you want to correct.")
##################################################
def extract_cell_ID_and_marker_by_right_click(event):
    global marker, cell_number,cell_color, mask
    marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
    cell_number=mask[marker[1],marker[0]]-1
    cell_color=cells_in_current_frame_sorted[cell_number][1]
    cell_ID=cells_in_current_frame_sorted[cell_number][0]
    dialog_label_5.config(text="Chosen cell ID="+str(cell_ID)+"\nmarker=" +str(marker))
    print("cell_number=", cell_number)
    print("marker=", marker)
    dialog_label_5.config(text="Start left-clicking on the cell itself and on the surrouning background to see how segmentation changes."
                          "\nOnce you are happy wiht the result, repeat the process all over again with another cell, or if you are finished, click Button 6."
                          "\nYou can  undo by clicking Button 2 and then starting editing the frame all over again. Warning: you cannot undo edits after pushing Button 6 !")
############################################
def edit_by_clicking(event):
      points=[]
      kernel= np.ones((3,3),np.uint8)     
      global centroid, final_mask
      centroid=[event.x/window_p5_size*frame_p5_size,event.y/window_p5_size*frame_p5_size]    
      dialog_label_5.config(text=str(centroid))
     
      segmented_frame, segmented_patch,a,b,c,d, final_mask=segment_one_cell_at_a_time(segmentor, refiner,empty_fluor,empty_bright,centroid,cell_radius_p5, frame_p5_size, patch_size_p5, marker,final_mask,cell_number)
      #dilated_patch = cv2.dilate(segmented_patch,kernel,iterations = 2)
      patch_with_contours=prepare_contours(segmented_patch)    
      global filled_fluor, filled_bright
      if cell_number not in modified_cell_IDs:
          modified_cell_IDs.append(cell_number)
          #list_of_modified_frames.append([frame_number,modified_cell_IDs])
      #print("modified_cell_IDs=",modified_cell_IDs)
      dialog_label_5.config(text="If you are unable to achieve good segmentation by just clicking, start hand drawing mode by pushing Button 4.")
      # print("list_of_modified_frames=",list_of_modified_frames)
      filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
      filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)    
      filled_fluor=paste_patch(filled_fluor,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size)
      filled_bright=paste_patch(filled_bright,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size)
      ############################################
      #global final_mask
      #mask_with_one_cell=paste_benchmark_patch(segmented_patch,a,b,c,d,cell_number, frame_p5_size)
      #final_mask[final_mask==cell_number+1]=0# delete previous contour of cell
      #final_mask+=mask_with_one_cell# insert current contour of cell
          
      global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5     
      canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
 
###############################################

############# This is the 2nd type of segmentation correction:
############# Splitting mergeed cells . Need to save the edits after you finish.
        
#############################################
def get_cell_IDs(event):# gets cell ID from previous frame during Type 2 editing         
  cell_number=mask[int(event.y/window_p5_size*frame_p5_size),int(event.x/window_p5_size*frame_p5_size)]-1
  if cell_number>=0:   
    manual_IDs.append(cell_number)
    print("manual_IDs=", manual_IDs)     
    global occluded_cell_color    
    colour_four_channel=cells_in_current_frame_sorted[cell_number][1]    
    #colour_four_channel=colors[cell_number]    
    colour_three_channel=colour_four_channel[:-1]
    colour_three_channel.reverse()    
    
    occluded_cell_color="#%02x%02x%02x" % tuple(colour_three_channel)
    canvas_bright_p5.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=occluded_cell_color, fill=occluded_cell_color, width=2)
    centroid_label.config(text="Manual_IDs = "+ str(manual_IDs))  
########################
def get_cell_centroids(event):# for splitting merged cell
    canvas_fluor_p5.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=occluded_cell_color, fill=occluded_cell_color, width=2)
    manual_centroids.append([event.x/window_p5_size*frame_p5_size, event.y/window_p5_size*frame_p5_size])   
    centroid_label.config(text="Manual_centroids = "+ str(manual_centroids))
############ This is the 3rd type of segmentation correction:
############ manual drawing with mouse.Needs saving after each cell

def choose_one_cell():
    dialog_label_5.config(text="Right-click on the cell you want to correct. Its contours should disappear.")
    button_choose_one_cell.configure(background = 'red')
    button_start.configure(background = button_color)
    
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")
    #canvas_fluor_p5.unbind("<Button-1>")
    #canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.bind("<Button-3>", get_one_cell_ID)
###########################################################
def get_one_cell_ID(event): # for hand drawing
   
  global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5  
  global hand_cell_number,hand_cell_color, filled_fluor, filled_bright, colour_four_channel         
  hand_cell_number=final_mask[int(event.y/window_p5_size*frame_p5_size),int(event.x/window_p5_size*frame_p5_size)]-1
  if hand_cell_number>=0:
   if hand_cell_number not in modified_cell_IDs:
        modified_cell_IDs.append(hand_cell_number)
   final_mask[final_mask==hand_cell_number+1]=0         
   colour_four_channel=cells_in_current_frame_sorted[hand_cell_number][1]    
   colour_three_channel=colour_four_channel[:-1]
   colour_three_channel.reverse()    
   print("hand_cell_number=", hand_cell_number)
   hand_cell_color="#%02x%02x%02x" % tuple(colour_three_channel)
   #canvas_fluor.create_oval(event.x-2, event.y-2, event.x+2,
                       #event.y+2, outline="red", fill="red", width=2)
   filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,colour_four_channel)
   filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,colour_four_channel)
    
       
   canvas_bright,canvas_fluor,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
   
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\filled_fluor_after_click.tif", filled_fluor)
   dialog_label_5.config(text="To be able to start hand drawing, push Button 4a.")   
########################
def start_drawing_with_mouse():
    button_hand_draw.configure(background = 'red')    
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")
    canvas_fluor_p5.bind("<Button-1>", get_x_and_y)    
    canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse, add="+")
    canvas_fluor_p5.bind("<Button-3>",erase_line)
    #canvas_fluor_p5.bind("<Button-3>",erase_line, add="+")
    global cell_contour_fl, cell_contour_br,points, mask_hand
    cell_contour_fl=[]
    cell_contour_br=[]
    points=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    dialog_label_5.config(text="Draw the contour of the cell with the left mouse. Warning:  Be careful not to draw on neughbouring close cells!\n If you want to undo right-click the mouse anywhere in the image.\nOnce you are finished, push Button 4b.")
########################################
def get_x_and_y(event):
    global lasx,lasy
    lasx,lasy=event.x,event.y
         
#########################################    
def draw_with_mouse(event):
    global lasx,lasy, line_fl, line_br
    line_fl=canvas_fluor_p5.create_line((lasx,lasy,event.x,event.y), fill="red", width=5)
    line_br=canvas_bright_p5.create_line((lasx,lasy,event.x,event.y), fill="red", width=5)
    cell_contour_fl.append(line_fl)
    cell_contour_br.append(line_br)   
    lasx,lasy=event.x,event.y
    points.append([[int(round(lasx/window_p5_size*frame_p5_size)),int(round(lasy/window_p5_size*frame_p5_size))]]) 
#############################################################      
def erase_line(event):# in case you are not happy with your hand contour and want to delete it
    global cell_contour_fl, cell_contour_br, points,mask_hand, final_mask
    for i in range(len(cell_contour_fl)):        
         canvas_fluor_p5.delete(cell_contour_fl[i])
         canvas_bright_p5.delete(cell_contour_br[i])
    points=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    final_mask[final_mask==hand_cell_number+1]=0
    if hand_cell_number  in modified_cell_IDs:
       modified_cell_IDs.remove(hand_cell_number)
    cell_contour_fl=[]
    cell_contour_br=[]
##########################################################    
def save_hand_drawing():
    button_hand_draw.configure(background = button_color)
    button_choose_one_cell.configure(background = button_color) 
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, points    
    ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)
    final_mask[final_mask==hand_cell_number+1]=0
    cv2.drawContours(mask_hand,[ctr],0,(255,255,255),-1)
    final_mask[mask_hand==255]=hand_cell_number+1
    
    
    cv2.drawContours(filled_fluor,[ctr] , 0, colour_four_channel, 1)
    cv2.drawContours(filled_bright,[ctr] , 0, colour_four_channel, 1)
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask_after_3.tif", final_mask*10)  
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask_hand.tif", mask_hand)
   
    points=[]
    
    if hand_cell_number not in modified_cell_IDs:
       modified_cell_IDs.append(hand_cell_number) 
    dialog_label_5.config(text="If you want to hand draw  another cell, push Button 4 once again.\n If you are finished with the current frame, press Button 6."
                          "\nIf you are finished with the whole movie, press Button 7.")
################################################################

def save_edits_for_frame(): #saves all eduts in current frame and modifues linage for this frame     
    button_save_frame.configure(background = 'red')
    button_start.configure(background = button_color) 
    update_lineage_after_manual_segm_correction(final_mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,cells_in_current_frame_sorted,frame_p5_size, patch_size_p5)    
    lineage_per_frame_p5[frame_number-1]=frame_dictionary
       
    cv2.imwrite(path_filled_bright, filled_bright )# rewrite RESULTS_BRIGHR
    cv2.imwrite(path_filled_fluor, filled_fluor)# rewrite RESULTS_FLUOR
    cv2.imwrite(path_mask, final_mask) # rewrite MASKS)
    
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)         
    global photo_filled_fluors, photo_filled_brights, filled_fluors, filled_brights# update frames on the screen
    photo_filled_fluors[frame_number-1]=photo_fluor
    photo_filled_brights[frame_number-1]=photo_bright
    filled_fluors[frame_number-1]=filled_fluor
    filled_brights[frame_number-1]=filled_bright
    #global masks
    #masks[frame_number-1]=final_mask
    button_save_frame.configure(background = button_color)
    dialog_label_5.config(text="You have 3 oprions now:\n  - Go to the next frame ( by using the slide bar) \n - Finish editing the movie (by pushing Button 7)"
                            "\n - Leave it for some other time (by clicking  Exit or Next")
##########################################
def create_final_movie():# create final movie + pedigree_per_cell (simplified, i.e. only centroids and areas)
    dialog_label_5.config(text="Creating lineage and final movie...")
    global output_dir 
    print("output_dir=", output_dir)       

    dialog_label_5.config(text="Lineage per cell is stored in" +str(output_dir))
    global frame_p5_size
    lineage_per_cell=create_lineage_for_Lorenzo(output_dir, frame_p5_size)
    dialog_label_5.config(text="Lineage per cell is stored in" +str(output_dir)+
                          "Creating final movie...")
    create_output_movie(output_dir, frame_p5_size)       
    dialog_label_5.config(text="Lineage per cell is stored in  " +str(os.path.join(output_dir,"lineage_per_cell.pkl"))+
                          "\nFinal movie is in  " + str(os.path.join(output_dir,"lineage_movie.avi")))
############### widgets in Page 5


button_load_p5 = Button(frame2_page5, text="1. Click to open file menu and choose OUTPUT folder", command=lambda:threading.Thread(target=choose_and_load_tracked_movie).start(), bg=button_color, font=all_font,activebackground="red")
button_load_p5.grid(row=0,column=0, padx=20, pady=20)


button_frame_info = Button(frame3_page5, text="2. Click to extract current frame info", command=get_frame_info,bg=button_color, font=all_font,activebackground="red")
button_frame_info.grid(row=1,column=0, padx=500)
   

button_start = Button(frame4_page5, text="3. Click to start fast correction", command=start_editing_by_clicking,bg=button_color, font=all_font,activebackground="red")
button_start.grid(row=0, column=0, padx=100)

#########################################################
button_choose_one_cell = Button(frame4_page5, text="4. Click to start hand drawing",  command=choose_one_cell,bg=button_color, font=all_font,activebackground="red")
button_choose_one_cell.grid(row=0, column=1, padx=100)

button_hand_draw = Button(frame4_page5, text="4a. Start drawing with mouse",command=start_drawing_with_mouse,bg=button_color, font=all_font,activebackground="red")
button_hand_draw.grid(row=1, column=1, padx=100)

button_save_hand_drawing = Button(frame4_page5, text="4b. Save hand drawing", command=save_hand_drawing,bg=button_color, font=all_font,activebackground="red")
button_save_hand_drawing.grid(row=2, column=1, padx=100)
###################################################################

##################################################################

button_save_frame = Button(frame4_page5, text="6. Save edits \nfor current frame", command=save_edits_for_frame,bg=button_color, font=all_font,activebackground="red")
button_save_frame.grid(row=0, column=3,padx=100)

global button_final_movie
button_final_movie = Button(frame7_page5, text="7. Create final movie\n and \npedigree", command=create_final_movie,bg=button_color, font=all_font,activebackground="red")
button_final_movie.grid(row=1, column=0)    
    

################################################################################
#####################################   PAGE 6: RESULTS  #########################
###########################################
page6=pages[5]
page6.title("5. VISUALISE RESULTS")
page6.config(bg=bg_color)
######################################
frame1_page6 = tk.Frame(master=page6, width=1528, height=50, bg=bg_color)
frame1_page6.grid(row=0, column=0, rowspan=1, columnspan=4, sticky=W+E+N+S)

frame2_page6 = tk.Frame(master=page6, width=1528, height=30, bg=bg_color)
frame2_page6.grid(row=1, column=0, rowspan=1, columnspan=4, sticky=W+E+N+S)

frame3_page6 = tk.Frame(master=page6, width=1528, height=50, bg=bg_color)
frame3_page6.grid(row=2, column=0, rowspan=1, columnspan=4, sticky=W+E+N+S)

frame4_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame4_page6.grid(row=3, column=0, rowspan=1, columnspan=1)

frame5_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame5_page6.grid(row=3, column=1, rowspan=1, columnspan=1)

frame6_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame6_page6.grid(row=3, column=2, rowspan=1, columnspan=1)

frame7_page6 = tk.Frame(master=page6, width=100, height=382, bg=bg_color)
frame7_page6.grid(row=3, column=3, rowspan=1, columnspan=1)

frame8_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame8_page6.grid(row=4, column=0, rowspan=1, columnspan=1)

frame9_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame9_page6.grid(row=4, column=1, rowspan=1, columnspan=1)

frame10_page6 = tk.Frame(master=page6, width=382, height=382, bg=bg_color)
frame10_page6.grid(row=4, column=2, rowspan=1, columnspan=1)

frame11_page6 = tk.Frame(master=frame9_page6, width=382, height=50, bg=bg_color)
frame11_page6.grid(row=7, column=0, rowspan=1, columnspan=1)

######################################################
canvas_4 = Canvas(frame4_page6, bg=bg_color, height=382, width=382)
canvas_4.pack(anchor='nw', fill='both', expand=True)

canvas_5 = Canvas(frame5_page6, bg=bg_color, height=382, width=382)
canvas_5.pack(anchor='nw', fill='both', expand=True)

canvas_6 = Canvas(frame6_page6, bg=bg_color, height=382, width=382)
canvas_6.grid(row=0,column=0)

canvas_8 = Canvas(frame8_page6, bg=bg_color, height=250, width=382)
canvas_8.grid(row=0,column=0)
############################   sub1   ############################################
l_title = tk.Label(frame1_page6, text="STEP 6: VISUALISE RESULTS",
              bg="yellow", fg="red", font=("Times", "24"))
l_title.grid(row=0, column=3, padx=500, sticky="n")
############################## sub2 #####################
progress_bar = ttk.Progressbar(frame3_page6, orient='horizontal',mode='determinate',length=280)
progress_bar.grid(row=0, column=0,padx=10)
progress_bar.grid_remove()
#########################################################
l_loaded = tk.Label(frame3_page6, text=" \n\n\n",
              bg="black", fg=result_color, font=all_font)
l_loaded.grid(row=0, column=1, padx=10)
l_loaded.grid_remove()
##################################################
options_cells = [""]
global chosen_1, chosen_2
chosen_1, chosen_2 = StringVar(page6),StringVar(page6)
chosen_1.set("Choose cell ID")
chosen_2.set("Choose cell property")
#options_cell=""    

##############################################################

global extract_info_from_file_name

from postprocess import (sorted_aphanumeric, change_dict,extract_info_from_file_name, create_pedigree, create_per_cell_info,
              load_result_images)
from functions import extract_lineage


def retrieve():
    stop_flash("begin", page6, flashers)
    progress_bar.grid(row=0, column=0,padx=10)
    b_retrieve.config(bg="red")
    b_create.config(bg=button_color)
    global my_dir,out_folders, outpath, software_folder, options_cells, drop_1, pedigree
   
    my_dir = filedialog.askdirectory()# input movie folder (full path) 
    input_movie_folder = os.path.basename(my_dir)
    software_folder = os.path.dirname(my_dir)     
    outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
    print("outpath=", outpath)
    pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
    with open(pedigree_path, 'rb') as handle:
         pedigree = pickle.load(handle)   
    global keys   
    keys=list(pedigree.keys())
    label_feedback.config(text="\nRetrieving results ...\n\n\n")   
    chosen_1.set("Choose cell ID")
    chosen_2.set("Choose cell property")
    progress_bar.grid(row=0, column=0,padx=10)
    global red_patches, one_cell_patches, plots, bright_images
    red_patches, one_cell_patches, plots, bright_images=load_result_images(outpath, keys, progress_bar)
    b_retrieve.config(bg=button_color)
   # drop_1.config(bg = "black",font=all_font,fg=result_color)
    #drop_2.config(bg = "black",font=all_font,fg="yellow")
    label_feedback.config(text="1. Choose cell ID,\n2. Then choose cell property (Area, Perimeter, or Circularity."+
                          "\n3. Use scrollbar to explore results.")
    l_loaded.grid(row=0, column=1, padx=10)
    l_loaded.config(text="Retrieved results for movie:\n"+ os.path.join(software_folder, input_movie_folder)+
                    "\nExcel files can be accessed at\n"+ os.path.join(outpath,"CELLS_INFO_EXCEL"))
    drop_1.destroy()
    drop_1 = OptionMenu(frame3_page6, chosen_1, *keys,  command= create_patch_slider)
    drop_1.grid(row=3, column=0, padx=200)
    drop_1.config(bg = label_color,font=all_font,activebackground="red")
    drop_1["menu"].config(bg=label_color,activebackground="red")
    b_retrieve.config(bg=button_color)
    start_flash([drop_1],"choose_cell", page5, flashers)    
#############################################
def create_results():
    stop_flash("begin", page5, flashers)
    b_create.config(bg="red")
    global my_dir,out_folders, outpath, software_folder, options_cells, drop_1, pedigree
    
    my_dir = filedialog.askdirectory()# input movie folder (full path) 
    input_movie_folder = os.path.basename(my_dir)
    software_folder = os.path.dirname(my_dir)     
    outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
    label_feedback.config(text="\nCreating results ...\n\n\n")  
    progress_bar.grid(row=0, column=0,padx=10)
    global pedigree  
    lineage_per_frame=extract_lineage(outpath)
    pedigree = create_pedigree(lineage_per_frame, outpath,frame_size)# pedigree is also saved in pickle file
    print("pickle file has been created!!!!!")
    #keys_1=list(pedigree.keys())
    #label_feedback.config(text="Cells discovered:  " +str(keys_1))
    del lineage_per_frame
    global per_cell_dict
    
    still_lineage=cv2.imread(os.path.join( outpath,"still_lineage.tif"), -1)
    create_per_cell_info(
        pedigree, outpath, still_lineage,label_feedback, progress_bar)
    #print("len(per_cell_dictionary=", len(pedigree))
    #print("per_cell_dictionary.keys()=", pedigree.keys())
    global keys   
    keys=list(pedigree.keys())
    drop_1.destroy()
    drop_1 = OptionMenu(frame3_page6, chosen_1, *keys,  command= create_patch_slider)
    drop_1.grid(row=3, column=0, padx=200)
    drop_1.config(bg = label_color,font=all_font,activebackground="red")
    drop_1["menu"].config(bg=label_color,activebackground="red")
    global red_patches, one_cell_patches, plots, bright_images
    label_feedback.config(text="\nLoading results ...\n\n\n") 
    red_patches, one_cell_patches, plots, bright_images=load_result_images(outpath, keys, progress_bar)
    l_loaded.grid(row=0, column=1, padx=10)
    #l_loaded.config(text="Created results for movie:\n"+ os.path.join(software_folder, input_movie_folder))
    l_loaded.config(text="Created results for movie:\n"+ os.path.join(software_folder, input_movie_folder)+
                    "\nExcel files can be accessed at\n"+ os.path.join(outpath,"CELLS_INFO_EXCEL"))
    label_feedback.config(text="1. Choose cell ID,\n2. Then choose cell property (Area, Perimeter, or Circularity."+
                          "\n3. Use scrollbar to explore results.")
    b_create.config(bg=button_color)
    start_flash([drop_1],"choose_cell", page6, flashers)
############################################

def slide_patch(value):  # value=frame number from patch_slider
           
    canvas_4.delete('all')
    canvas_5.delete('all')
    canvas_6.delete('all')
    canvas_8.delete('all')    
    
    for i in range(len(pedigree[chosen_1.get()])):
        if pedigree[chosen_1.get()][i][1] == int(value)-1:
            image_number = i+1
      
    patch=one_cell_patches[chosen_1.get()][image_number-1][0]
    frame_number=one_cell_patches[chosen_1.get()][0][1]
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    global im_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(patch_rgb)
    im_pil = im_pil.resize((382, 382), Image.ANTIALIAS)
    im_pil = ImageTk.PhotoImage(im_pil)
    canvas_6.create_image(0, 0, anchor=NW, image=im_pil)
    
    red_patch=red_patches[chosen_1.get()][image_number-1][0]
    global red_im_pil
    red_patch_rgb = cv2.cvtColor(red_patch, cv2.COLOR_BGR2RGB)
    red_im_pil = Image.fromarray(red_patch_rgb)
    red_im_pil = red_im_pil.resize((382, 382), Image.ANTIALIAS)
    red_im_pil = ImageTk.PhotoImage(red_im_pil)
    canvas_5.create_image(0, 0, anchor=NW, image=red_im_pil)
    
    plott_pil=plots[chosen_1.get()][chosen_2.get()][image_number-1][0]
    global pl_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pl_pil = Image.fromarray(plott_pil)
    pl_pil.thumbnail((382,382), Image.ANTIALIAS)
    #pl_pil = pl_pil.resize((382, 382), Image.ANTIALIAS)
    pl_pil = ImageTk.PhotoImage(pl_pil)
    canvas_8.create_image(0, 0, anchor=NW, image=pl_pil)
    
    bright_image= bright_images[int(value)-1]
    bright_image_rgb = cv2.cvtColor(bright_image, cv2.COLOR_BGR2RGB)
    #bright_image_rgb=bright_image
    global bright_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bright_pil = Image.fromarray(bright_image_rgb)
    bright_pil = bright_pil.resize((382, 382), Image.ANTIALIAS)
    bright_pil = ImageTk.PhotoImage(bright_pil)
    canvas_4.create_image(0, 0, anchor=NW, image=bright_pil)
    
    #patch_slider.set(value)
    patch_slider.config(label="Frame "+str(value))  
        
    l_centr.config(text="Centroid: " +
              str(pedigree[chosen_1.get()][image_number-1][3]))
    combination=col_dict[chosen_2.get()]
    
    l_area.config(text="Area: " +
               str(pedigree[chosen_1.get()][image_number-1][4]), fg=combination[0])
    l_perim.config(text="Perimeter: " +
               str(pedigree[chosen_1.get()][image_number-1][5]), fg=combination[1])
    l_circ.config(text="Circularity: " +
               str(pedigree[chosen_1.get()][image_number-1][6]), fg=combination[2])

######################################
def create_patch_slider(value):
  stop_flash("choose_cell", page6, flashers)
  drop_1.config(fg=result_color,bg="black")
  print("Entering create_patch_slider")
  chosen_2.set("Choose cell property")
  canvas_4.delete('all')
  canvas_5.delete('all')
  canvas_6.delete('all')
  canvas_8.delete('all')
    
  chosen_1.set(value)
  key=chosen_1.get()
  print("key=", key)
  drop_1.config( bg="black",fg = result_color,font=all_font,activebackground="red")
  if key!="Choose cell ID":
    global ffrom, tto   
    ffrom, tto = pedigree[key][0][1]+1, pedigree[key][-1][1]+1
    print("ffrom=", ffrom)
    print("tto=", tto)
    global patch_slider
    #patch_slider = Scale(sub10, from_=ffrom, to=tto, orient=HORIZONTAL,
                         #troughcolor="blue", command=slide_patch, length=380)
    patch_slider=Scale(frame10_page6,from_=ffrom,to=tto,orient=HORIZONTAL,troughcolor="#513B1C",label="Frame "+str(ffrom), command=slide_patch,
                 activebackground="red", bg=label_color,showvalue=0, font=all_font, length=380)
    patch_slider.grid(row=0, column=0, sticky="e")   

    patch_slider.set(ffrom)
  start_flash([drop_2],"choose_property", page6, flashers)    
###########################################################     
def display_first_patch(value):  # value=cell name from dropdown menu
    #per_cell_dict=pedigree
    
  stop_flash("choose_property", page6, flashers)
  drop_2.config(fg=result_color,bg="black")  
  canvas_4.delete('all')
  canvas_5.delete('all')
  canvas_6.delete('all')
  canvas_8.delete('all')
    
  cell_property=chosen_2.get()
  if cell_property!="Choose cell property":
    drop_2.config( bg="black",fg = result_color,font=all_font,activebackground="red")
    patch_slider.set(ffrom)
    patch=one_cell_patches[chosen_1.get()][0][0]
    frame_number=one_cell_patches[chosen_1.get()][0][1]
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    global im_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(patch_rgb)
    im_pil = im_pil.resize((382, 382), Image.ANTIALIAS)
    im_pil = ImageTk.PhotoImage(im_pil)
    canvas_6.create_image(0, 0, anchor=NW, image=im_pil)
    
    
    
    red_patch = red_patches[chosen_1.get()][0][0]
    red_patch_rgb = cv2.cvtColor(red_patch, cv2.COLOR_BGR2RGB)
    global red_im_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    red_im_pil = Image.fromarray(red_patch_rgb)
    red_im_pil = red_im_pil.resize((382, 382), Image.ANTIALIAS)
    red_im_pil = ImageTk.PhotoImage(red_im_pil)
    canvas_5.create_image(0, 0, anchor=NW, image=red_im_pil)
    
    #cell_property=chosen_2.get()
    #if cell_property!="Choose cell property":
    plott_pil=plots[chosen_1.get()][chosen_2.get()][0][0]
    global pl_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pl_pil = Image.fromarray(plott_pil)
    pl_pil.thumbnail((382,382), Image.ANTIALIAS)
    #pl_pil = pl_pil.resize((382, 382), Image.ANTIALIAS)
    pl_pil = ImageTk.PhotoImage(pl_pil)
    canvas_8.create_image(0, 0, anchor=NW, image=pl_pil)
    
    
    bright_image= bright_images[frame_number-1]
    bright_image_rgb = cv2.cvtColor(bright_image, cv2.COLOR_BGR2RGB)
    #bright_image_rgb=bright_image
    global bright_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bright_pil = Image.fromarray(bright_image_rgb)
    bright_pil = bright_pil.resize((382, 382), Image.ANTIALIAS)
    bright_pil = ImageTk.PhotoImage(bright_pil)
    canvas_4.create_image(0, 0, anchor=NW, image=bright_pil)       
    
    global col_dict
    col_dict={"Area":["red", "yellow", "yellow"],"Perimeter":["yellow", "red", "yellow"],"Circularity":["yellow", "yellow", "red"]}
    l_centr.config(text="Centroid: " + str(pedigree[chosen_1.get()][0][3]))
    combination=col_dict[chosen_2.get()]
    l_area.config(text="Area: " + str(pedigree[chosen_1.get()][0][4]), fg=combination[0])
    l_perim.config(text="Perimeter: " + str(pedigree[chosen_1.get()][0][5]), fg=combination[1])
    l_circ.config(text="Circularity: " + str(pedigree[chosen_1.get()][0][6]), fg=combination[2])
    
    

global drop_1,drop_2
drop_1 = OptionMenu(frame3_page6, chosen_1, *options_cells,  command= create_patch_slider)
drop_1.grid(row=3, column=0, padx=200)
drop_1.config(bg = label_color,font=all_font,activebackground="red")
drop_1["menu"].config(bg=label_color,activebackground="red")



options_properties = ["Area", "Perimeter", "Circularity"]
drop_2 = OptionMenu(frame3_page6, chosen_2, *options_properties, command=display_first_patch)
drop_2.grid(row=3, column=1, padx=200)
drop_2.config(bg = label_color, font=all_font,activebackground="red")
drop_2["menu"].config(bg=label_color,activebackground="red")

label_feedback = tk.Label(frame2_page6, justify=tk.LEFT,text="Welcome to Step 4 of the pipeline!!!!\n\nIf you create results for the 1st time, press Create.\nOtherwise, press Retrieve."+
              "\nWhen menue opens click on the INPUT movie.",bg="black", fg="yellow", font=all_font, width=50, height=5)

label_feedback.grid(row=0, column=1, padx=300, sticky="n")


b_create = tk.Button(frame2_page6, text=" Create",
                bg=button_color, font=all_font,command=lambda: Thread(target=create_results).start())
b_create.grid(row=0, column=0,sticky="n", pady=(10,0), padx=20)


b_retrieve = tk.Button(frame2_page6, text="Retrieve",
               bg=button_color, font=all_font, activebackground="red",command=lambda:Thread(target= retrieve).start())
b_retrieve.grid(row=1, column=0,sticky="n", pady=(0,30), padx=20)

start_flash([b_retrieve, b_create],"begin", page6, flashers)
#############################  sub3 #################
l_centr = tk.Label(frame9_page6, text="Centroid:",bg = "black", fg="yellow" , font=all_font)
l_centr.grid(row=0, column=0, pady=2)

l_area = tk.Label(frame9_page6, text="Area:", bg = "black", fg="yellow",font=all_font)
l_area.grid(row=1, column=0, pady=2)

l_perim = tk.Label(frame9_page6, text="Perimeter:", bg = "black", fg="yellow",font=all_font)
l_perim.grid(row=2, column=0, pady=2)

l_circ = tk.Label(frame9_page6, text="Circularity:", bg = "black", fg="yellow",font=all_font)
l_circ.grid(row=3, column=0,pady=(0,70))
###################################################################
locations=[frame3_page1,frame8_page2,frame13_page3,frame11_page4,frame8_page5,frame11_page6]
x_back,x_exit,x_next=700,750,800


for i in range(6):
    location=locations[i]
    if i==5:
        x_back,x_exit=150,200
    Button(location, text="Exit",bg="orange",font=all_font, command=win.destroy).place(x=x_exit,y=0)
    #Button(location, text="Exit",bg="orange",font=all_font, command=win.destroy).grid(row=0,column=1)
    if i<5:
       Button(location, text="Next",bg="orange",font=all_font, command=lambda:go_to_page(page_number.get()+1)).place(x=x_next,y=0)
    if i>0:
       Button(location, text="Back",bg="orange",font=all_font, command=lambda:go_to_page(page_number.get()-1)).place(x=x_back,y=0)

#########################################################################


win.mainloop()

