import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, Canvas
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
#import pygame
import gc
import pickle
from threading import Thread
from functools import partial
import copy
import tifffile as tiff
#import imagecodecs
import math
import shutil

#############################################################################
win= tk.Tk()

#w = 800 # width for the Tk root
#h = 650 # height for the Tk root


ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
#x = (ws/2) - (w/2)
#y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
#win.geometry('%dx%d+%d+%d' % (1530, 2000, x, y))
win.geometry('1530x2000')

bg_color,all_font,button_color,result_color,label_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA"

win.config(bg=bg_color)
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: PROCESS MULTIPAGE TIFF", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING","PAGE 5: CORRECT SEGMENTATION", "PAGE 6: VISUALISE RESULTS"]
global page_number, software_folder
software_folder = os.getcwd()
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
global  turn_image_into_tkinter, CustomThread, flash
from interface_functions import turn_image_into_tkinter,CustomThread,flash


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

###############################################
cwd = os.getcwd()
im=Image.open(os.path.join(cwd,"logo.tif"))
im=im.resize((500,500))
img = ImageTk.PhotoImage(im)
# Create a Label Widget to display the text or Image
logo_label = Label(frame2_page1, image = img, bg="brown")
logo_label.grid(row=0, column=2,rowspan=5, padx=5, pady=(100,0))

###########################################################################
############################   PAGE 2 : EXTRACT MOVIE FROM FOLDER  ##############################
###############################################################################
page2=pages[1]
global  canvas_size_p2
canvas_size_p2=400

frame1_page2 = tk.Frame(master=page2, width=1530, height=50, bg=bg_color)
frame1_page2.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame2_page2.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame3_page2.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame4_page2 = tk.Frame(master=page2, width=canvas_size_p2, height=canvas_size_p2, bg=bg_color)
frame4_page2.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W)

frame5_page2 = tk.Frame(master=page2, width=canvas_size_p2, height=canvas_size_p2, bg=bg_color)
frame5_page2.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W)

frame9_page2 = tk.Frame(master=page2, width=canvas_size_p2, height=canvas_size_p2, bg=bg_color)
frame9_page2.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W)

frame6_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame6_page2.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame11_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame11_page2.grid(row=5, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame12_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame12_page2.grid(row=6, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame7_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame7_page2.grid(row=7, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame10_page2 = tk.Frame(master=page2, width=1530, height=30, bg=bg_color)
frame10_page2.grid(row=8, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame8_page2 = tk.Frame(master=page2, width=1530, height=50, bg=bg_color)
frame8_page2.grid(row=9, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
######################################################
canvas_fluor_p2 = Canvas(frame5_page2, bg=bg_color, height=canvas_size_p2, width=canvas_size_p2)
canvas_fluor_p2.pack(anchor='nw')
canvas_bright_p2= Canvas(frame4_page2, bg=bg_color, height=canvas_size_p2, width=canvas_size_p2)
canvas_bright_p2.pack(anchor='nw')
canvas_red_p2= Canvas(frame9_page2, bg=bg_color, height=canvas_size_p2, width=canvas_size_p2)
canvas_red_p2.pack(anchor='nw')
#####################################################
global progressbar_page2
s = ttk.Style()
s.theme_use('clam')
s.configure("bar.Horizontal.TProgressbar", troughcolor=bg_color, 
                bordercolor="green", background="green", lightcolor="green", 
                darkcolor="black")
progressbar_page2 = ttk.Progressbar(frame3_page2,style="bar.Horizontal.TProgressbar",orient='horizontal',mode='determinate',length=280)
progressbar_page2.grid(row=0, column=1, padx=150, pady=20)
########################################
global menu_variable, feedback_var_p2, instruct_var_p2,fl_name_p2,br_name_p2, red_name_p2
menu_variable, feedback_var_p2,instruct_var_p2,fl_name_p2, br_name_p2,red_name_p2=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
menu_variable.set("2. Select movie name:")
feedback_var_p2.set("\n\n\n\n")
instruct_var_p2.set("")
instruct_var_p2.set("STEP 1 is designed to help you extract a cell movie from a folder containing numerous movies taken by spinning desk or epi."+
                    "\nThe file names should contain _w2FITC_ or_w3Multi600_(for fluorescent channel), _w1BF_ (for brightfield channel), and _w3TRITC_ (for red channel).\nThe program extracts all frames of chosen movie from folder, process them and change file names slightly."+
                    " \nTo begin, click Button 1 to open file menu, then navigate to the folder containing movies and click on it.")
fl_name_p2.set("           "),br_name_p2.set("           "),red_name_p2.set("           ")
######################################
global  load_image_names,create_name_dictionary
global sorted_aphanumeric,extract_movie_name,save_images_page2,process_tif, calculate_n_digits_in_name,display_image_p2
from helper_functions_page2 import sorted_aphanumeric,extract_movie_name,save_images_page2,process_tif,calculate_n_digits_in_name,display_image_p2,create_name_dictionary
#######################################
def explore_folder():# check which movies are inside the folder and create menu with their names
   update_flash([])  
   button_choose_folder.config(bg="red")
   names=[]
   global path
   path=filedialog.askdirectory()#
   feedback_var_p2.set("Chosen folder: " +str(path))
   instruct_var_p2.set("Exploring  folder: " +str(path) +" . . .")
   #l_result.config(text="Folder: " +str(path))
   for filename in os.listdir(path):
      if "thumb" not in filename and filename.endswith(".TIF"):
         index_s,index_t=filename.find("_s"),filename.find("_t")
         exact_name =filename[index_s+1:index_t]
         if exact_name not in names:
           names.append(exact_name)

   movie_names_int =[int(x[1:]) for x in names]
   movie_names_int.sort()
   movie_names =["s"+str(y) for y in movie_names_int]
   instruct_var_p2.set("Movies discovered inside this folder:\n"+str(movie_names)+\
                     "\n\nSelect a movie of interest from the dropdown menu. The extraction of the movie will start automatically.")  
   global movies_menu
   feedback_var_p2.set(feedback_var_p2.get()+"\nAll movies in this folder:  "+str(movie_names))
   movies_menu = OptionMenu(frame3_page2,menu_variable, *movie_names, command=create_movie_for_display)
   movies_menu.grid(row=0, column=2, padx=100,pady=20)
   movies_menu.config(bg=button_color, font=all_font, activebackground="red")
   movies_menu.config(width=20)
   movies_menu["menu"].config(bg=label_color,activebackground="red") 
   update_flash([movies_menu])  
   button_choose_folder.config(bg=button_color)
#######################################
def display_frame_count(text_new,ii, count):# print frame count while loading
     shift=0
     previous_text=feedback_var_p2.get()     
     if ii!=1 and ii!=0:                 
            if len(count)<len(str(ii)):
                shift=1          
            remaining_text=previous_text[:-(len(str(ii))+len(text_new)-shift)]
     else:
              remaining_text=previous_text
     feedback_var_p2.set(remaining_text+text_new+str(ii))
     count=str(ii)
     return count
################################
def load_and_process_page2(path,total_number_of_frames,movie_name):
  bright_images, fluor_names,  red_names=[],[],[] 
  bright_images, fluor_images, red_images=[],[],[]
    
  global br_name_p2, frame3_page2,instruct_var_p2,progressbar_page2 
  
  i_total,i_fl, i_red, i_br=0,0,0,0
  br_count, fl_count,red_count="0","0","0"
          
  for filename in sorted_aphanumeric(os.listdir(path)):
   if "thumb" not in filename and filename.endswith(".TIF"):
     index_s,index_t=filename.find("_s"),filename.find("_t")
     exact_name =filename[index_s+1:index_t]     
     if exact_name==movie_name:
        i_total+=1        
        progressbar_page2["value"]=(i_total+1)/(total_number_of_frames)*100        
        time.sleep(0.02)
        frame3_page2.update_idletasks()       
        if "_w1BF_" in filename:          
          instruct_var_p2.set("Processing brightfiled frames...")
          i_br+=1          
          bright_names.append(filename)
          br_name_p2.set("Original name:   "+str(filename))
          old_name=os.path.join(path,filename)
          a = tiff.imread(old_name)
          c=process_tif(a)
          bright_images.append(c)
          global photo_bright
          photo_bright=turn_image_into_tkinter(c, canvas_size_p2)
          canvas_bright_p2.create_image(0,0,anchor=NW,image=photo_bright)
          ##############                  
          text_br="\n  Number of brightfield frames:  "
          br_count=display_frame_count(text_br,i_br, br_count)
          print("br_count=", br_count)
        elif ("_w2FITC_" in filename) or ("_w3Multi600_" in filename):# process fluorescent          
          i_fl+=1
          instruct_var_p2.set("Processing fluorescent frames...")              
          fluor_names.append(filename)
          fl_name_p2.set("Original name:   "+str(filename))
          old_name=os.path.join(path,filename)
          b = tiff.imread(old_name)         
          b=process_tif(b)
          fluor_images.append(b)
          global photo_fluor
          photo_fluor=turn_image_into_tkinter(b, canvas_size_p2)
          canvas_fluor_p2.create_image(0,0,anchor=NW,image=photo_fluor)
          text_fl="\n  Number of fluorescent frames:  "
          fl_count=display_frame_count(text_fl,i_fl, fl_count)               
        elif ("_w3TRITC_" in filename):# process red channel
          i_red+=1
          instruct_var_p2.set("Processing red frames...")
          red_names.append(filename)
          red_name_p2.set("Original name:   "+str(filename))
          old_name=os.path.join(path,filename)         
          r = tiff.imread(old_name)          
          r=process_tif(r)         
          red_images.append(r)
          global photo_red
          photo_red=turn_image_into_tkinter(r, canvas_size_p2)
          canvas_red_p2.create_image(0,0,anchor=NW,image=photo_red)
          ###############################
          text_red="\n  Number of red frames:  "
          red_count=display_frame_count(text_red,i_red, red_count)
  if len(bright_names)==0:     
      text_br="\n  Number of bright frames:  "
      br_count=display_frame_count(text_br,i_br, br_count)
  if len(fluor_names)==0:     
      text_fluor="\n  Number of fluorescent frames:  "
      fluor_count=display_frame_count(text_fluor,i_fl, fl_count)
  if len(red_names)==0:     
      text_red="\n  Number of red frames:  "
      red_count=display_frame_count(text_red,i_red, red_count)
  ####### create dictionaries for frame display when scrolling
  global  bright_dictionary,red_dictionary,fluor_dictionary
  red_dictionary=create_name_dictionary(red_names, red_images)
  bright_dictionary=create_name_dictionary(bright_names, bright_images)
  fluor_dictionary=create_name_dictionary(fluor_names, fluor_images)
  all_names=[bright_names,fluor_names,red_names]#
  all_images=[bright_images,fluor_images,red_images]# find channel with maximum number of frames
  all_lengths=[len(bright_names),len(fluor_names),len(red_names)]
  global max_number_of_frames 
  max_number_of_frames =max(all_lengths)
  p=all_lengths.index(max_number_of_frames)  
  size=str(all_images[p][0].shape[0])
  feedback_var_p2.set(feedback_var_p2.get()+"\nFrame size:  "+ size +" x " + size)     
  global n_digits
  n_digits=calculate_n_digits_in_name(all_names[p][-1])  
  return fluor_images,bright_images,red_images, fluor_names, bright_names, red_names
##################################
def create_movie_for_display(value):
    update_flash([])    
    global movies_menu    
    movies_menu.config(bg="red")
    global movie_name
    movie_name=value
    feedback_var_p2.set(feedback_var_p2.get()+"\nChosen movie:  "+str(movie_name))   
    total_number_of_frames=0
    for filename in sorted_aphanumeric(os.listdir(path)):# count total number of frames for progress bar
      if "thumb" not in filename and filename.endswith(".TIF"):
        index_s,index_t=filename.find("_s"),filename.find("_t")
        exact_name =filename[index_s+1:index_t]     
        if exact_name==movie_name:
           total_number_of_frames+=1
    ######## load the whole movie
    global fluor_images, bright_images,red_images,fluor_names, bright_names, red_names    
    fluor_images, bright_images,red_images,fluor_names, bright_names, red_names=load_and_process_page2(path,total_number_of_frames,movie_name)   
    global frame_slider
    frame_slider=Scale(frame6_page2,from_=1,to=max_number_of_frames,orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p2, length=150, showvalue=0)
    frame_slider.pack() 
    frame_slider.set(1)
    slide_p2("1")
    movies_menu.config(bg="black", fg="cyan")   
    instruct_var_p2.set("All frames have been processed.\nNow, you can scroll through them by using slider.\n\nAfter you are finished, press Button 3 to save the processed movie.")      
###############################
def slide_p2(value):# display image even when it is missing (in this case it is black)
    print("value=", value)
    canvas_bright_p2.delete("all")
    canvas_fluor_p2.delete("all")
    canvas_red_p2.delete("all")
    image_number=int(value)    
    frame_slider.config(label="Frame "+str(value))
    ###########################################       
    br_image, old_br_name,new_br_name=display_image_p2(value, bright_dictionary,"ch02", n_digits,canvas_size_p2)         
    global br_tk  
    br_tk=turn_image_into_tkinter(br_image, canvas_size_p2)     
    canvas_bright_p2.create_image(0,0, anchor=NW, image=br_tk)   
    br_name_p2.set("Original name:   "+old_br_name+"\nNew name:   "+new_br_name)    
    ################################    
    fl_image, old_fl_name, new_fl_name=display_image_p2( value, fluor_dictionary,"ch00", n_digits,canvas_size_p2)     
    global fl_tk
    fl_tk=turn_image_into_tkinter(fl_image, canvas_size_p2)       
    canvas_fluor_p2.create_image(0,0, anchor=NW, image=fl_tk)    
    fl_name_p2.set("Original name:   "+old_fl_name+"\nNew name:   "+new_fl_name)    
    ###############################################
    red_image, old_red_name, new_red_name=display_image_p2(value, red_dictionary,"ch01", n_digits,canvas_size_p2)          
    global red_tk  
    red_tk=turn_image_into_tkinter(red_image, canvas_size_p2)     
    canvas_red_p2.create_image(0,0, anchor=NW, image=red_tk)                   
    red_name_p2.set("Original name:   "+old_red_name+"\nNew name:   "+new_red_name)
############################################################
################## buttons and labels page 2 ############
l_page_name=tk.Label(frame1_page2,text= "STEP 1: EXTRACT MOVIE FROM FOLDER", bg="yellow", fg="red", font=("Times", "24")).pack()
button_choose_folder=tk.Button(frame3_page2,text="1. Choose folder with movies",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=lambda: explore_folder())
button_choose_folder.grid(row=0,column=0, padx=100,pady=20)
button_save_movie=tk.Button(frame11_page2,text="3. Save processed movie",bg='#9ACD32',activebackground="red",font=all_font , command=lambda: [save_images_page2(movie_name,feedback_var_p2,bright_names,fluor_names,red_names, bright_images, fluor_images, red_images, instruct_var_p2), update_flash([])]).pack()
l_instr_name_p2=tk.Label(frame7_page2,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="red").pack() 
l_feedback_p2=tk.Label(frame2_page2,textvariable=feedback_var_p2,bg="black", fg=result_color, font=all_font, height=8)
l_feedback_p2.pack(fill=BOTH) 
l_instruct_p2=tk.Label(frame7_page2,textvariable=instruct_var_p2 ,bg="black", fg="yellow", font=all_font, height=5)
l_instruct_p2.pack(fill=BOTH)  
l_fluor_announce_p2=tk.Label(frame5_page2,text="Fluorescent" ,bg=label_color, font=all_font).pack() 
l_bright_announce_p2=tk.Label(frame4_page2,text="Brightfield" ,bg=label_color, font=all_font).pack() 
l_red_announce_p2=tk.Label(frame9_page2,text="Red" ,bg=label_color, font=all_font).pack() 
l_fluor_name_p2=tk.Label(frame5_page2,textvariable=fl_name_p2,bg="black", fg=result_color, font=all_font, height=2).pack() 
l_bright_name_p2=tk.Label(frame4_page2,textvariable=br_name_p2 ,bg="black", fg=result_color, font=all_font, height=2).pack() 
l_red_name_p2=tk.Label(frame9_page2,textvariable=red_name_p2,bg="black", fg=result_color, font=all_font, height=2).pack() 

###########################################################################
############################   PAGE 3 : CUT WELL  ##############################
###############################################################################
page3=pages[2]
global  canvas_size_p3
canvas_size_p3=400

frame1_page3 = tk.Frame(master=page3, width=1528, height=50, bg=bg_color)
frame1_page3.grid(row=0, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame2_page3 = tk.Frame(master=page3, width=1528, height=50, bg=bg_color)
frame2_page3.grid(row=1, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame3_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame3_page3.grid(row=2,column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame4_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame4_page3.grid(row=2, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame5_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame5_page3.grid(row=2, column=2,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame6_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame6_page3.grid(row=3,column=0,rowspan = 1, columnspan = 1,sticky = W)

frame7_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame7_page3.grid(row=3, column=1,rowspan = 1, columnspan = 1,sticky = W)

frame8_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame8_page3.grid(row=3, column=2,rowspan = 1, columnspan = 1,sticky = W)

frame9_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=100, bg=bg_color)
frame9_page3.grid(row=4, column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame10_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=100, bg=bg_color)
frame10_page3.grid(row=4, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame11_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=100, bg=bg_color)
frame11_page3.grid(row=4, column=2,rowspan = 1, columnspan = 2,sticky = W+E+N+S)

frame12_page3 = tk.Frame(master=page3, width=1530, height=30, bg=bg_color)
frame12_page3.grid(row=5, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame13_page3 = tk.Frame(master=page3, width=1530, height=30, bg=bg_color)
frame13_page3.grid(row=6, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame14_page3 = tk.Frame(master=page3, width=1530, height=30, bg=bg_color)
frame14_page3.grid(row=7, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame15_page3 = tk.Frame(master=page3, width=1530, height=100, bg=bg_color)
frame15_page3.grid(row=8, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)
###############################################
global canvas_left, canvas_mid, canvas_right
canvas_left = Canvas(frame6_page3, bg=bg_color, height=canvas_size_p3, width=canvas_size_p3)
canvas_left.pack(anchor='nw', fill='both', expand=True)
canvas_mid = Canvas(frame7_page3, bg=bg_color, height=canvas_size_p3, width=canvas_size_p3)
canvas_mid.pack(anchor='nw', fill='both', expand=True)
canvas_right = Canvas(frame8_page3, bg=bg_color, height=canvas_size_p3, width=canvas_size_p3)
canvas_right.pack(anchor='nw', fill='both', expand=True)
###################################################
global popup_mid, popup_right,popup_size_p3
popup_mid, popup_right, popup_size_p3=None, None, 800
#################################################
global low,high 
low,high=0,255

global red_point_coords,intensities,bright_names,green_blob
red_point_coords,intensities,bright_names=[],[], []

green_blob=canvas_mid.create_oval(100-1,100+1,100+1,100+1,outline = "black",fill = "black",width = 2)
##############################################
global   load_image_names,cut_all, draw_circles_p3, update_feedback_text
from interface_functions import   cut_well_from_image, calculate_angle, cut_all
from preprocess import load_image_names, extract_file_name,extract_red_frame_numbers,update_feedback_text
#######################################################
global instruct_var_p3,feedback_var_p3, feedback_dict
instruct_var_p3,feedback_var_p3=StringVar(), StringVar()
feedback_dict={"s":" ","im":" ","fl":" ","br":" ","red":" ","w":" ", "dest":" "}
feedback_text=update_feedback_text(feedback_dict)
feedback_var_p3.set(feedback_text)
instruct_var_p3.set(" Step 2 allows you to cut out a well of interest out of initial cell movie. \n\nTo choose raw movie , press Button 1."
                    "\nThen, navigate to your raw movie, open it and click on ANY BRIGHT field image")
##############################################
def select_one_bright():# load all frames,display clicked bright frame    
    global my_path, my_destin, bright_names_sorted,fluor_names_sorted, red_names_sorted,clicked_number 
    my_path=filedialog.askopenfilename()
    l_left_canvas.config(text=os.path.basename(my_path))    
    movie_dir=os.path.dirname(my_path)
    feedback_dict["s"]=movie_dir
    
    bright_names_sorted,fluor_names_sorted, red_names_sorted =load_image_names(movie_dir)
    feedback_dict["fl"],feedback_dict["br"],feedback_dict["red"]=str(len(fluor_names_sorted)),str(len(bright_names_sorted)),str(len(red_names_sorted))
       
    my_destin=os.path.join(os.getcwd() ,"INPUT_MOVIE "+os.path.basename(movie_dir))
      
    if not os.path.exists(my_destin):
      os.mkdir(my_destin)
    else:# delete previous version of INPUT_MOVIE_...
           shutil.rmtree(my_destin)
           os.mkdir(my_destin)    
    global photo_clicked# the same image in PIL (for display)
    global clicked_bright# the image in opencv (as array, for measuring intensities)
    global image_size_p3
    clicked_bright=cv2.imread(my_path,0)# 0 is very important!!!!
    image_size_p3=clicked_bright.shape

    feedback_dict["im"]= str(image_size_p3[0])+" x "+str(image_size_p3[1])
    
    feedback_text=update_feedback_text(feedback_dict)
    feedback_var_p3.set(feedback_text)
    photo_clicked=turn_image_into_tkinter(clicked_bright, canvas_size_p3)
    
    canvas_left.create_image(0,0, anchor=NW, image=photo_clicked)
    canvas_left.bind("<Button-1>",measure_intensities)
    instruct_var_p3.set("Now, click on the dark border of the well(s) 2-3 times to measure intensities.\nThen click Button 2."
                    "\nThe thresholded image will appear in the window to the right.")    
    update_flash([])    
####################################################
def measure_intensities(event):# draw red circles on well borders to measure intensities
    global red_point_coords
    global intensities
    canvas_left.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,outline = "red",fill = "red",width = 2)
    red_point_coords.append([event.x, event.y])    
    intensity=clicked_bright[int(event.y*image_size_p3[1]/canvas_size_p3),int(image_size_p3[0]/canvas_size_p3)]
    intensities.append(intensity)
    if len(red_point_coords)==2:
        update_flash([button_threshold])
###################################################################
def apply_thresh():# threshold the clicked image (aftre measuring well border intensities)
    global lower,low, high , thresh,thr_image   
    canvas_left.delete("all")
    canvas_mid.delete("all")
    canvas_right.delete("all")
    canvas_left.create_image(0,0, anchor=NW, image=photo_clicked)   
    low, high=min(intensities), max(intensities)    
    ret,thresh = cv2.threshold(clicked_bright,low,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold (it is now from 130 to 255)   
    thresh[thresh!=0]=255
    thr_image=turn_image_into_tkinter(thresh, canvas_size_p3)    
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image)
    threshold_slider.config(variable=low,label="Threshold = "+str(low))    
    instruct_var_p3.set("The borders of wells should become SOLID white line, WITHOUT INTERRUPTIONS."
                       "\nImprove thresholded image if necessary\nby sliding the bar below to change threshold."
                       "\nFinally, click on the well of interest.")
    update_flash([threshold_slider])    
    canvas_mid.bind("<Button-1>", choose_well)
    l_mid_canvas.config(text=os.path.basename(my_path))
    threshold_slider.set(low)
############################################################
def change_threshold(value): # change threshold     
    low=float(value)
    global thresh,thr_image
    ret,thresh = cv2.threshold(clicked_bright,low,high,cv2.THRESH_BINARY_INV)# here you can adjust threshold   
    thresh[thresh!=0]=255
    threshold_slider.config(label="Threshold = "+str(value))
    thr_image=turn_image_into_tkinter(thresh, canvas_size_p3)    
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image)    
######################## respond to upper_thresh slider and thresh image accordingly 
global  seeds
seeds=[]
#################################### 
def choose_well(event):# click on the well of interest, get green circle and red rectangle  
    global green_blob
    canvas_mid.delete(green_blob)
    global seed, seeds    
    green_blob=canvas_mid.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,outline = "green",fill = "green",width = 5)
    seed=(int(event.x*thresh.shape[1]/canvas_size_p3), int(event.y*thresh.shape[0]/canvas_size_p3))
    seeds.append(seed)    
    im_thr=thresh.copy()
    mask=None
    fill_image=cv2.floodFill(im_thr, mask, seed, 255,flags=8)# here you define the centre of the well (there are 4 in total)
    fill_image = thresh | im_thr
    fill_image-=thresh   
    closing = cv2.morphologyEx(fill_image, cv2.MORPH_CLOSE, (5,5))    
    _,contours, hierarchy = cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    cnt=contours[0]    
    global first_rect,first_x0, first_box, angle  
    first_rect = cv2.minAreaRect(cnt)
    angle, first_box=calculate_angle(first_rect)
    print("first_box=", first_box)    
    first_x0=first_box[0][0]    
    global  well_size, popup_image_size_p3   
    x0,y0,x1,y1,x2,y2,x3,y3=first_box[0][0],first_box[0][1],first_box[1][0],first_box[1][1],\
                            first_box[2][0],first_box[2][1],first_box[3][0],first_box[3][1]    
    size_1=math.sqrt(((x1-x0)**2+(y1-y0)**2))
    size_2=math.sqrt(((x2-x1)**2+(y2-y1)**2))
    well_size=int(round(max(size_1,size_2)))
    popup_image_size_p3=int(round(image_size_p3[0]*popup_size_p3/well_size))
    feedback_dict["w"]= str(well_size)+" x "+str(well_size)
    feedback_text=update_feedback_text(feedback_dict)
    feedback_var_p3.set(feedback_text)
    global closing_2
    closing_1=cv2.cvtColor(closing,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(closing_1,[first_box],0,(0,0,255),5)# draw red rect around detected well 
    closing_2=turn_image_into_tkinter(closing_1, canvas_size_p3)   
    canvas_right.create_image(0,0, anchor=NW, image=closing_2)    
    ######## here it draws red rect in fluorescent image of canvas_left
    im_copy=clicked_bright.copy()# 
    global photo_im_red,M_first,rows,cols
    im_red=cv2.cvtColor(im_copy,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(im_red,[first_box],0,(0,0,255),5)    
    photo_im_red=turn_image_into_tkinter(im_red, canvas_size_p3)   
    canvas_left.create_image(0,0, anchor=NW, image=photo_im_red)    
    rows,cols = clicked_bright.shape 
    M_first = cv2.getRotationMatrix2D((int(round(cols/2)),int(round(rows/2))),angle,1)   
    
    instruct_var_p3.set("Check that the well has been detected correctly: a red frame should appear around the well.\nIf it is not correct go back to sliding bar."
                       "\nFinally, push Button 3 to check the result.")
    update_flash([button_display_p3])        
######################################################
def cut_first_well():# cut well in the first image and display it in canvas_mid 
 instruct_var_p3.set("It is important to manually correct shift in Frame 1. Push Button 4 and drag the image with mouse to eliminate the shift."
                       "\nFinally, push Button 5 to check the results.")
 global canvas_mid 
 canvas_mid.delete("all")
 
#################### draw temp image (binary) to rotate it and find rect_new
 print("first box=", first_box)
 temp=np.zeros(clicked_bright.shape, np.uint8)
 cv2.drawContours(temp,[first_box],0,255,-1)
 dst = cv2.warpAffine(temp,M_first,(cols,rows))
####################  4. calculate its borders   
 _,contours_new, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt_new=contours_new[0]
 rect_new = cv2.minAreaRect(cnt_new)             
 box_final = cv2.boxPoints(rect_new)# horisontal well    
 box_final = np.int0(np.round(box_final))
 print("first box_final=", box_final)
 xs=[box_final[k][0] for k in range(4)]
 ys=[box_final[k][1] for k in range(4)]
 global x_min_first, y_min_first, x0,y0,x1,y1
 x_min_first, y_min_first=min(xs),min(ys)
 ###########################
 x0,y0=x_min_first, y_min_first# x0,y0- image coord system; x1,y1 - popup canvas coord system
 x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))
 #############################
 global rot_bright
 rot_bright = cv2.warpAffine(clicked_bright,M_first,(cols,rows))
 global cut_bright
 cut_bright=rot_bright[y_min_first:y_min_first+well_size, x_min_first:x_min_first+well_size]
 global final_s, finalImage_small, final_fake
 final_s=turn_image_into_tkinter(cut_bright, canvas_size_p3) 
 finalImage_small=canvas_mid.create_image(0,0, anchor=NW, image=final_s)
 #########################
 #seeds=[]
 
 global delta_x, delta_y
 delta_x, delta_y=0,0
 canvas_mid.unbind("<Button-1>")
 update_flash([button_first_shift_edit]) 
######################################################
def drag_image(event, canvas,imageFinal):# drag image with mouse
    global x_img,y_img, points, x_last,y_last,dx,dy, delta_x,delta_y    
    x, y = event.x, event.y   
    points.append([x,y])             
    if len(points)>1:
         dx, dy=x-x_img,y-y_img
         canvas.move(imageFinal, dx,dy)
         canvas.update()
         x_last-=dx
         y_last-=dy                
    x_img = x
    y_img = y
    delta_x, delta_y=int(round((x_last-x1)*image_size_p3[0]/popup_image_size_p3)),int(round((y_last-y1)*image_size_p3[1]/popup_image_size_p3))    
##############################
def edit_frame_shift(label):  
    global popup_mid, canvas_popup_mid
    
    popup_mid = tk.Toplevel(master=page3, width=popup_size_p3, height=popup_size_p3)
    frame1 = tk.Frame(master=popup_mid, width=popup_size_p3, height=popup_size_p3)
    frame1.pack()
    frame2 = tk.Frame(master=popup_mid, width=popup_size_p3, height=50)
    frame2.pack()
    canvas_popup_mid = Canvas(frame1, height=popup_size_p3, width=popup_size_p3, bg=bg_color)
    canvas_popup_mid.pack(anchor='nw', fill='both', expand=True)
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=lambda:   popup_mid.destroy())
    button_close.pack()
   
    global x_img,y_img, points, x_last,y_last,dx,dy, br_image, delta_x,delta_y
    #x0,y0=x_min_first, y_min_first# x0,y0- image coord system; x1,y1 - popup canvas coord system
    #x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))
    delta_x, delta_y=x_last-x0*well_size/popup_size_p3,y_last-y0*well_size/popup_size_p3
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x1,y1,0,0
    print("x1,y1=", x1,y1)
    points=[]
    global new_name
    head, tail=os.path.split(my_path)
    new_name=os.path.join(my_destin,tail)
   
    final_bright,M,x_min,y_min, rows, cols, rot_indicator, rot_bright=cut_well_from_image(clicked_bright,seed,well_size,first_x0, delta_x, delta_y, first_rect)
    br_image=rot_bright
   
    global image1,imageFinal_big   
    size=int(round(image_size_p3[0]*popup_size_p3/well_size))   
    image1=turn_image_into_tkinter(br_image, size)
    imageFinal_big = canvas_popup_mid.create_image(-x1, -y1, image = image1,anchor='nw')
    ##################################################   
    canvas_popup_mid.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_mid, imageFinal_big))   
    canvas_popup_mid.bind("<ButtonRelease>", lambda event: cut_and_save_patch(event,canvas_popup_mid, canvas_mid))    
######################################################
def edit_first_frame_shift():  
    global popup_mid, canvas_popup_mid
    
    popup_mid = tk.Toplevel(master=page3, width=popup_size_p3, height=popup_size_p3, bg=bg_color)
    frame1 = tk.Frame(master=popup_mid, width=popup_size_p3, height=popup_size_p3)
    frame1.pack()
    frame2 = tk.Frame(master=popup_mid, width=popup_size_p3, height=50)
    frame2.pack()
    canvas_popup_mid = Canvas(frame1, height=popup_size_p3, width=popup_size_p3, bg=bg_color)
    canvas_popup_mid.pack(anchor='nw', fill='both', expand=True)
    def close_and_flash():
        update_flash([button_bright])
        popup_mid.destroy()
    global button_close
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=close_and_flash)
    button_close.pack()
   
    global x_img,y_img, points, x_last,y_last,dx,dy, x0,y0, br_image, x1,y1, delta_x,delta_y
    x0,y0=x_min_first, y_min_first# x0,y0- image coord system; x1,y1 - popup canvas coord system
    x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))
   
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x1,y1,0,0
    delta_x, delta_y=int(round((x_last-x1)*image_size_p3[0]/popup_image_size_p3)),int(round((y_last-y1)*image_size_p3[1]/popup_image_size_p3))
    can_delta_x,can_delta_y=x_last-x1,y_last-y1
    
    points=[]
    global new_name
    head, tail=os.path.split(my_path)
    new_name=os.path.join(my_destin,tail)   
    final_bright,M,x_min,y_min, rows, cols, rot_indicator, rot_bright=cut_well_from_image(clicked_bright,seed,well_size,first_x0, delta_x, delta_y, first_rect)
    br_image=rot_bright
   
    global image1,imageFinal   
    canvas_popup_mid.delete("all")
    image1=turn_image_into_tkinter(br_image, popup_image_size_p3)
    imageFinal_big = canvas_popup_mid.create_image(-x1, -y1, image = image1,anchor='nw')
    ##################################################   
    canvas_popup_mid.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_mid, imageFinal_big))   
    canvas_popup_mid.bind("<ButtonRelease>", lambda event: cut_and_save_patch(event,canvas_popup_mid, canvas_mid))    
    update_flash([button_close])    
############################################
def cut_and_save_patch(event, canvas_big, canvas_small):
    global points, br_image, new_name, x0,y0, x_last, y_last
    
    xx,yy=int(round(x_last*image_size_p3[0]/popup_image_size_p3)),int(round(y_last*image_size_p3[1]/popup_image_size_p3))    
    patch=br_image[yy:yy+well_size, xx:xx+well_size]
    patch_1=patch.copy()       
    cv2.imwrite(new_name, patch)
    global tk_patch, image2 
    tk_patch=turn_image_into_tkinter(patch, popup_size_p3)      
    canvas_big.delete("all")
    canvas_big.create_image(0,0, image = tk_patch,anchor='nw')

    image2=turn_image_into_tkinter(patch_1, canvas_size_p3)    
    canvas_small.create_image(0, 0, image = image2,anchor='nw')
    points=[]
##########################################
def start_editing_frames():  
    global popup_right, canvas_popup_right, l_popup_canvas    
    popup_right = tk.Toplevel(master=page3, width=popup_size_p3, height=popup_size_p3, bg=bg_color)
    frame3 = tk.Frame(master=popup_right, width=popup_size_p3, height=50)
    frame3.pack()
    frame1 = tk.Frame(master=popup_right, width=popup_size_p3, height=popup_size_p3, bg=bg_color)
    frame1.pack()
    frame2 = tk.Frame(master=popup_right, width=popup_size_p3, height=50, bg=bg_color)
    frame2.pack()
    canvas_popup_right = Canvas(frame1, height=popup_size_p3, width=popup_size_p3, bg="black")
    canvas_popup_right.pack(anchor='nw', fill='both', expand=True)
     
    button_current_edit=tk.Button(frame3,text="6a. Edit well shift in current frame",bg=button_color,activebackground="red",font=all_font, command=edit_current_frame_shift)
    button_current_edit.pack()
    
    l_popup_canvas=tk.Label(frame2,text= "bright frame", bg="black", fg="cyan", font=("Times", "12"))
    l_popup_canvas.pack()  
    
    global frame_pop_slider, first_tk_pop    
    frame_pop_slider=Scale(frame2,from_=1,to=len(bright_names_sorted),orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p3, length=250, showvalue=0)
    frame_pop_slider.pack()
    frame_pop_slider.set(frame_slider.get())
    
    l_instruct_popup=tk.Label(frame2,text="Scroll through frames to ensure that the well fits completely into each frame.\nIf it does not push Button 6a and correct shift in the current frame.Do it for as many frames as necessary."
                 "\nFinally, close the popup window" ,bg="black", fg="yellow", font=all_font, height=5)
    l_instruct_popup.pack(fill=BOTH)  
    def destroy_popup():
        global popup_right
        update_flash([button_fluor]) 
        popup_right.destroy()
        popup_right=None
       
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command= destroy_popup)
    button_close.pack()
    
    first_tk_pop=turn_image_into_tkinter(first, popup_size_p3)
    canvas_popup_right.create_image(0,0, anchor=NW, image=first_tk_pop)
    l_popup_canvas.config(text=os.path.basename(bright_names_sorted[0]))
    update_flash([button_current_edit])           
###########################################################
def edit_current_frame_shift():
    button_fluor.config(bg="red")
    frame_number=frame_pop_slider.get()
    print("frame_number=", frame_number)
    frame_slider.set(frame_number)
    item=rotation_matrices[frame_number-1]
    x_min,y_min=item[1],item[2]
      
    global x_img,y_img, points, x_last,y_last,dx,dy, rotated_images, x0,y0, br_image
    x0,y0=x_min, y_min
    x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))
   
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x1,y1,0,0
    points=[]    
    br_image= rotated_images[frame_number-1]
    ####################################################
    global image1, new_name, imageFinal
    new_name=new_br_names[frame_number-1]
        
    size=int(round(image_size_p3[0]*popup_size_p3/well_size))
   
    image1=turn_image_into_tkinter(br_image, size)      
    imageFinal_big = canvas_popup_right.create_image(-x1, -y1, image = image1,anchor='nw')
    ##################################################
    canvas_popup_right.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_right, imageFinal_big))
    canvas_popup_right.bind("<ButtonRelease>", lambda event: cut_and_save_patch(event,canvas_popup_right, canvas_right))
    button_fluor.config(bg=bg_color)
##########################################
def cut_and_save_current(event):
    global points, br_image, new_name, x0,y0, x_last, y_last
    
    points=[]   
    patch=br_image[y_last:y_last+well_size, x_last:x_last+well_size]
    
    new_x_min, new_y_min=x_last,y_last
    current_frame_number=frame_slider.get()
    item=rotation_matrices[current_frame_number-1]
    M,x_min,y_min,row,cols, rotation_indicator=item[0],item[1],item[2],item[3],item[4], item[5]
    new_item=(M, x_last,y_last,rows,cols, rotation_indicator)
    rotation_matrices[current_frame_number-1]=new_item
               
    cv2.imwrite(new_name, patch)
    global corrected_patch
    corrected_patch=turn_image_into_tkinter(patch, canvas_size_p3)      
    canvas_right.delete("all")
    canvas_right.create_image(0,0, image = corrected_patch,anchor='nw')
###################################### 
global new_fl_names, new_red_names
new_fl_names,new_red_names= None, None
#################################   
def cut_bright_wells():# Button 5. Apply to all bright
  update_flash([])
  button_bright.config(bg="red")
  instruct_var_p3.set("Processing bright field frames....")  
  global rotation_matrices,new_br_names, rotated_images, boxes, final_boxes
  rotation_matrices, new_br_names, rotated_images=[],[],[]
  boxes, final_boxes=[],[]

  for k in range(len(bright_names_sorted)): 
    bright_name=bright_names_sorted[k]
    l_right_canvas.config(text=os.path.basename(bright_name))
    bright_image=cv2.imread(bright_name,-1)  
    final_bright,M,x_min,y_min, rows, cols, rot_indicator, rot_bright=cut_well_from_image(bright_image,seed,well_size,first_x0, delta_x, delta_y, first_rect)
    #print("final_bright.shape,final_bright.dtype=",final_bright.shape,final_bright.dtype)
    final_bright_tk=turn_image_into_tkinter(final_bright, canvas_size_p3)
    canvas_right.delete("all")
    canvas_right.create_image(0,0, anchor=NW, image=final_bright_tk)
    rotation_matrices.append((M,x_min,y_min, rows, cols, rot_indicator))
    
    rotated_images.append(rot_bright)    
    head, tail=os.path.split(bright_name)   
    new_br_name=os.path.join(my_destin,tail)
    new_br_names.append(new_br_name)       
    cv2.imwrite(new_br_name, final_bright)
    if k==0:
        global first_tk, first
        first=final_bright       
        first_tk=turn_image_into_tkinter(first, canvas_size_p3)
  global frame_slider    
  frame_slider=Scale(frame11_page3,from_=1,to=len(bright_names_sorted),orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p3, length=250, showvalue=0)
  frame_slider.pack()
  frame_slider.set(1)
  
  threshold_slider.config(bg=label_color) 
  instruct_var_p3.set("Scroll through frames to ensure that the well fits completely into each frame.\nIf you want to corect shift in some frames, push Button 6 to launch editing window."
                 "\nOtherwise, push Button 7 to apply to ALL FLUORESCENT images")
  button_bright.config(bg=button_color)
  update_flash([button_shift_edit])  
  canvas_right.delete("all")
  canvas_right.create_image(0,0, anchor=NW, image=first_tk)
  l_right_canvas.config(text=os.path.basename(bright_names_sorted[0]))           
#########################
global frame_pop_slider
frame_pop_slider=None
######################### scroll through all images
def slide_p3(value):
    canvas_right.delete("all")
    image_number=int(value)
    print("slider value = ", value)    
    frame_slider.config(label="Frame "+str(value))       
    br_image=cv2.imread(new_br_names[image_number-1])
    global br_final  
    br_final=turn_image_into_tkinter(br_image, canvas_size_p3)     
    canvas_right.create_image(0,0, anchor=NW, image=br_final)
    l_right_canvas.config(text=os.path.basename(bright_names_sorted[image_number-1]))
    if new_fl_names: 
      fl_image=cv2.imread(new_fl_names[image_number-1])
      global fl_final
      fl_final=turn_image_into_tkinter(fl_image, canvas_size_p3)       
      canvas_mid.create_image(0,0, anchor=NW, image=fl_final)
      l_mid_canvas.config(text=os.path.basename(fluor_names_sorted[image_number-1]))
    if new_red_names:
      red_image=cv2.imread(new_red_names[image_number-1])
      global red_final
      red_final=turn_image_into_tkinter(red_image, canvas_size_p3)       
      canvas_left.create_image(0,0, anchor=NW, image=red_final)
      l_left_canvas.config(text=os.path.basename(red_names_sorted[image_number-1]))
    if popup_right:
      br_image_copy=br_image.copy()
      frame_pop_slider.config(label="Frame "+str(value))
      global br_popup  
      br_popup=turn_image_into_tkinter(br_image_copy, popup_size_p3)     
      canvas_popup_right.create_image(0,0, anchor=NW, image=br_popup)
      l_popup_canvas.config(text=os.path.basename(bright_names_sorted[image_number-1]))
##################### activate editing frame shift for current frame in canvas_right
  
def cut_fluor_wells():#cut fluor and red wells
 instruct_var_p3.set("Processing fluorescent and red frames....") 
 update_flash([])
 
 button_fluor.config(bg="red")
 progressbar_fluor = ttk.Progressbar(frame10_page3, orient='horizontal',mode='determinate',length=280)
 progressbar_fluor.pack()
 
 list_of_red_frame_numbers =extract_red_frame_numbers(red_names_sorted)
 print("list_of_red_frame_numbers=", list_of_red_frame_numbers)    
 global rotation_matrices,new_fl_names,new_red_names, first_tk_fl
 
 new_fl_names, new_red_names = [], []
 for k in range(len(fluor_names_sorted)):   
    info=rotation_matrices[k] 
    M,x_min,y_min,rows, cols, rot_indicator=info[0], info[1],info[2],info[3],info[4], info[5]    
    
    fluor_name=fluor_names_sorted[k]   
    fluor_image=cv2.imread(fluor_name,-1)        
    rot_fluor = cv2.warpAffine(fluor_image,M,(cols,rows))      
    cut_fluor=rot_fluor[y_min:y_min+well_size,x_min:x_min+well_size]
    if rot_indicator=="yes":
        final_fluor = cv2.rotate(cut_fluor, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        final_fluor=cut_fluor
    head, tail=os.path.split(fluor_name)
    new_fl_name=os.path.join(my_destin,tail)
    new_fl_names.append(new_fl_name)   
    cv2.imwrite(new_fl_name, final_fluor)
    final_fluor_tk=turn_image_into_tkinter(final_fluor, canvas_size_p3)
    canvas_mid.delete("all")
    canvas_mid.create_image(0,0, anchor=NW, image=final_fluor_tk)
    l_mid_canvas.config(text=os.path.basename(fluor_name))
    ###############################
    if k in list_of_red_frame_numbers:
      index=list_of_red_frame_numbers.index(k)
      red_name=red_names_sorted[index]
      red_text=os.path.basename(red_name)
      red_image=cv2.imread(red_name,-1)
      rot_red = cv2.warpAffine(red_image,M,(cols,rows))
      cut_red=rot_red[y_min:y_min+well_size,x_min:x_min+well_size]    
      if rot_indicator=="yes":       
        final_red = cv2.rotate(cut_red, cv2.ROTATE_90_COUNTERCLOCKWISE)
      else:      
        final_red=cut_red
      head, tail=os.path.split(red_name)
      new_red_name=os.path.join(my_destin,tail)
      new_red_names.append(new_red_name)   
      cv2.imwrite(new_red_name, final_red)      
    else:
      final_red=np.zeros((image_size_p3[1],image_size_p3[0]), np.uint8)
      red_text=" No image available"
    final_red_tk=turn_image_into_tkinter(final_red, canvas_size_p3)
    canvas_left.delete("all")
    canvas_left.create_image(0,0, anchor=NW, image=final_red_tk)
    l_left_canvas.config(text=red_text)   
 frame_slider.set(1)
 
 feedback_dict["dest"]=my_destin# print destination folder in feedback panel
 feedback_text=update_feedback_text(feedback_dict)
 feedback_var_p3.set(feedback_text)
 instruct_var_p3.set("Finished!\nThe input movie has been created and stored in folder\n "+str(my_destin)+
                 "\nNow, you are ready to proceed to STEP 3 of the pipeline.")               
 button_fluor.config(bg=button_color) 
##################################################
l_title=tk.Label(frame1_page3,text= "STEP-2: CUT WELL", bg="yellow", fg="red", font=("Times", "24")).pack()

l_feedback_p3=tk.Label(frame2_page3,textvariable=feedback_var_p3 ,bg="black", fg=result_color, font=all_font, height=5)
l_feedback_p3.pack(fill=BOTH)   

l_instr_name_p3=tk.Label(frame13_page3,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="red").pack()
l_instruct_p3=tk.Label(frame14_page3,textvariable=instruct_var_p3 ,bg="black", fg="yellow", font=all_font, height=5)
l_instruct_p3.pack(fill=BOTH)   
############################################################
l_left_canvas=tk.Label(frame9_page3,text= "         ", bg="black", fg="cyan", font=("Times", "12"))
l_left_canvas.pack()
l_mid_canvas=tk.Label(frame10_page3,text= "         ", bg="black", fg="cyan", font=("Times", "12"))
l_mid_canvas.pack()
l_right_canvas=tk.Label(frame11_page3,text= "          ", bg="black", fg="cyan", font=("Times", "12"))
l_right_canvas.pack()    
####################################
threshold_slider=Scale(frame4_page3, from_=0,to=255,orient=HORIZONTAL,variable=low,length=150,bg=label_color,	
    showvalue=0,troughcolor="#513B1C",label="Threshold = "+str(None), command=change_threshold,
    activebackground="red", font=all_font)
threshold_slider.grid(row=0, column=0,padx=10,pady=5)
#######################################################
button_select=tk.Button(frame3_page3 ,text="1. Go to raw movie",bg='#9ACD32', font='TkDefaultFont 10 bold' ,activebackground="red", command=select_one_bright)
button_select.pack()

button_threshold=tk.Button(frame3_page3,text="2. Apply initial threshold",bg=button_color,activebackground="red", font=all_font, command=lambda: apply_thresh())
button_threshold.pack()
###############################################
button_display_p3=tk.Button(frame4_page3,text="3. Cut well",bg=button_color,activebackground="red",font=all_font, command=lambda: cut_first_well())
button_display_p3.grid(row=1, column=0,padx=10) 

button_first_shift_edit=tk.Button(frame4_page3,text="4. Edit well shift in Frame 1",bg=button_color,activebackground="red",font=all_font, command=lambda:edit_first_frame_shift())
button_first_shift_edit.grid(row=2, column=0,padx=10,pady=5)

global button_bright
button_bright=tk.Button(frame5_page3,text="5. Apply to all bright",bg=button_color,activebackground="red",font=all_font, justify=LEFT,command=lambda:Thread(target=cut_bright_wells).start())
button_bright.grid(row=0, column=0,padx=10)
####################################################################
button_shift_edit=tk.Button(frame5_page3,text="6. Start editing frames",bg=button_color,activebackground="red",font=all_font, command=start_editing_frames)
button_shift_edit.grid(row=2, column=0,padx=10,pady=(10,10))
button_fluor=tk.Button(frame12_page3,text="7. Apply to all fluorescent and red",bg=button_color,activebackground="red",font=all_font, command=lambda: Thread(target=cut_fluor_wells).start())
button_fluor.pack()
###########################################################################
######### PAGE 4 :STEP-3:  EXECUTE AND CORRECT TRACKING ##############################
###############################################################################
page4=pages[3]
page4.config(bg=bg_color)
canvas_size_p4 =382
lineage_extension_for_new_cells=80

frame1_page4 = tk.Frame(master=page4, width=1528, height=50, bg="blue")
frame1_page4.grid(row=0, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

frame2_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg="yellow")
frame2_page4.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg="green")
frame3_page4.grid(row=1, column=1, rowspan=1, columnspan=5, sticky=W+E+N+S)

frame5_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg="orange")
frame5_page4.grid(row=2, column=0, rowspan=1, columnspan=1)

frame6_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg="white")
frame6_page4.grid(row=2, column=1, rowspan=1, columnspan=1)

frame7_page4 = tk.Frame(master=page4, width=canvas_size_p4+lineage_extension_for_new_cells, height=canvas_size_p4, bg="red")
frame7_page4.grid(row=2, column=2, rowspan=1, columnspan=1)

frame8_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg="blue")
frame8_page4.grid(row=3, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame9_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg="magenta")
frame9_page4.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame10_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg="grey")
frame10_page4.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame11_page4 = tk.Frame(master=page4, width=1528, height=50, bg="yellow")
frame11_page4.grid(row=4, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

canvas_previous = Canvas(frame5_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_previous.pack(anchor='nw', fill='both', expand=True)
canvas_current = Canvas(frame6_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_current.pack(anchor='nw', fill='both', expand=True)
########################### These labels do not change

title_label = tk.Label(frame1_page4, text="STEP 3: EXECUTE AND CORRECT TRACKING",
              bg="yellow", fg="red", font=("Times", "24"))
title_label.grid(row=0, column=1, padx=2, sticky="n")
label_previous = tk.Label(frame8_page4, text="Previous Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_previous.grid(row=0, column=5, padx=100)

label_current = tk.Label(frame9_page4, text="Current Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_current.grid(row=0, column=0,padx=100)


label_curr_frame_name = tk.Label(frame9_page4, text="           ", bg="black", fg="cyan", font='TkDefaultFont 10 bold' )
label_curr_frame_name.grid(row=1, column=0,padx=100)

label_lineage = tk.Label(frame10_page4, text="Lineage", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_lineage.grid(row=0, column=0, padx=100)
################################
canvas_lineage = Canvas(frame7_page4, bg="green", height=canvas_size_p4, width=canvas_size_p4+lineage_extension_for_new_cells)
canvas_lineage.grid(row=0,column=0)
###################################################
zero_image = Image.new('RGB', (canvas_size_p4, canvas_size_p4))
zero_image = ImageTk.PhotoImage(zero_image)
global lineage_images, output_images, lineage_images_cv2, output_names
lineage_images, output_images, lineage_images_cv2, output_names=[], [zero_image],[], ["             "]

################################
global popup_monitor
popup_monitor=None
global popup_window_size
popup_window_size=800
#####################################
global fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names
fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names=None,None,None, None, None  
global  lineage_per_frame_p4,start_frame,dict_of_divisions,  cells, changeable_params_history
lineage_per_frame_p4,start_frame,dict_of_divisions, cells,changeable_params_history = None,1, {},{},[]
global  count, pedigree, flag
pedigree,flag= None ," "
count = np.zeros((100), dtype="uint8")# for division


global my_dir
my_dir= ''


global per_cell_dict
per_cell_dict = {}
global clicked# used in radio buttons for editing,indicates which canvas is used for IDs extraction, value = "Current" or "Previous"
clicked = StringVar()
clicked.set(" ")

##################################
global manual_IDs,manual_centroids,mother_name,  daughter_indicators 
manual_IDs,  manual_centroids, mother_name, daughter_indicators=[], [], None, []
#################
def load_helper_functions():
    os.chdir(software_folder)
    global predict_first_frame, create_output_folders,\
        detect_division, update_dictionary_after_division, check_division_frame_number, predict_tracking, predict_tracking_general, backup_track, predict_first_frame, segment_and_clean,\
        create_previous_frame, plot_frame, create_first_color_dictionary,\
        create_pedigree, create_output_movie, load_weights, extract_lineage,create_dictionary_of_xs,\
        create_lineage_image_one_frame, extract_file_name, load_clip, update_lineage,force_manual_IDs,create_lineage_for_Lorenzo,sorted_aphanumeric,update_color_dictionary,update_naive_names_list,update_xs,\
        load_full_raw_movie,create_models,extract_output_images,create_name_dictionary_p4,display_image_p4,removeLeadingZeros,rename_file, show_3_canvases,update_changeable_params_history,extract_changeable_params_history

    from preprocess import create_output_folders, load_weights, extract_file_name,load_clip,load_full_raw_movie,create_models,removeLeadingZeros
    

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_division_frame_number)

    from functions import (predict_tracking_general,  backup_track, predict_first_frame, segment_and_clean,
                           hungarian, create_previous_frame, predict_tracking,force_manual_IDs)
    
    from plot import plot_frame, create_first_color_dictionary,update_color_dictionary,update_naive_names_list,update_xs, rename_file
    from postprocess import create_pedigree,  create_output_movie, create_dictionary_of_xs, create_lineage_image_one_frame,sorted_aphanumeric
    from keras.models import model_from_json
    from extract_lineage_for_Lorenzo import create_lineage_for_Lorenzo,extract_lineage,update_lineage, extract_const_movie_parameters,update_changeable_params_history,extract_changeable_params_history
    from interface_functions import extract_output_images,create_name_dictionary_p4,display_image_p4, show_3_canvases
    from keras.optimizers import Adam
###########################################    
global models, models_directory,tracker,segmentor,refiner


models_directory = os.path.join(software_folder, "TRAINED MODELS")
models,tracker,segmentor,refiner=[], None, None, None

load_helper_functions()
models,models_directory=create_models(software_folder)
#######################


############ click Button 1 and explore if OUTPUT exists or not
############### If yes, ask whether user wants to continue or start all over again
################ by creating a popup option menu
def initiate_tracking_page():
     #print("manual_init_positions in initiate=",manual_init_posiitons)
     #button_load.configure(background = 'red')
     global my_dir, input_movie_folder
     my_dir = filedialog.askdirectory()# input movie folder
     input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\n")
     input_movie_folder = os.path.basename(my_dir)
     global outpath
     #load_helper_functions()
     outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
     global init_image,last_image, frame_size, num_frames,  all_names_fluor
     all_names_fluor=[]
     #output_names=[None]     
     for filename in sorted_aphanumeric(os.listdir(my_dir)):   
        if filename.endswith("ch00.tif"):
            feedback_label.configure(text="Loading input movie ...")
            #output_name=filename 
            #output_names.append(output_names)                     
            full_name_fluor = os.path.join(my_dir, filename)
            all_names_fluor.append(full_name_fluor)
     #print("len(output_names) before=", len(output_names))
     
     global full_core_fluor_name, n_digits, first_frame_number, start_empty_file_name, frame_size
     full_core_fluor_name, n_digits, first_frame_number= extract_file_name(all_names_fluor[0])
     
     init_image=cv2.imread(all_names_fluor[0],0)
     last_image=cv2.imread(all_names_fluor[-1 ],0)
     frame_size=init_image[0].shape[0]
     num_frames=len(all_names_fluor)
     start_empty_file_name = " "# to make label look beautiful
     for i in range(len(all_names_fluor[0])):
          start_empty_file_name += " "
     label_curr_frame_name.config(text=start_empty_file_name)
     # check if OUTPUT exists:
     if not os.path.exists(outpath) :# 1. if OUTPUT does not exist       
          os.mkdir(outpath)
          print("OUTPUT does not exist")
          del all_names_fluor
          
          prepare_for_first_go()
     else:# 1. if OUTPUT exists
          if  len(os.listdir(outpath))==0:# 2. if OUTPUT is empty
              print("OUTPUT exists but empty")
              shutil.rmtree(outpath)# delete OUPUT if it exists
              os.mkdir(outpath)# create OUTPUT folder and start tracking from Frame 1
              del all_names_fluor              
              prepare_for_first_go()
          else:# 2. if OUTPUT is not empty
            print("OUTPUT exists but non-empty")
            output_fluor_folder= os.path.join(outpath, "RESULT_FLUORESCENT")
            if os.path.exists(output_fluor_folder):# 3. if RESULT_FLUOR exists
               print("RESULT_FLUOR exists")
               if  len(os.listdir(output_fluor_folder))==0:# 4.if RESULT_FLUOR is empty
                   print("RESULT_FLUOR exists but empty")
                   shutil.rmtree(outpath)# delete OUPUT if it exists
                   os.mkdir(outpath)# create OUTPUT folder and start tracking from Frame 1
                   del all_names_fluor
                   prepare_for_first_go()
               else:# 4. RESULT_FLUOR is not empty, i.e. movie has been processed (partly or fully)
                  print("RESULT_FLUOR is not empty")
                
                  output_names_fluor=[]
                  for filename in sorted_aphanumeric(os.listdir(output_fluor_folder)):   
                    if filename.endswith("ch00.tif"):
                     #feedback_label.configure(text="Loading input movie ...")                      
                     output_name_fluor = os.path.join(output_fluor_folder, filename)
                     output_names_fluor.append(output_name_fluor)
                     
                  print("len(output_names_fluor)=",len(output_names_fluor))
                  ####################
                  ####################
                  from preprocess import create_output_folders
                  global out_folders
                  out_folders = create_output_folders(outpath)# creates names only  
    
                  global true_cell_radius, patch_size,max_number_of_cells,  xs, full_core_bright_name,curr_frame_cell_names,flag,edit_id_indicator, \
                  base_colours,colour_counter,colour_dictionary,unused_naive_names, contrast_value, dict_of_divisions,number_of_added_new_cells
                  true_cell_radius, edit_id_indicator=IntVar(),StringVar()
   
                  (frame_size, true_cell_radius_pickle, patch_size,max_number_of_cells,
                  num_frames, full_core_fluor_name, n_digits, full_core_bright_name, first_frame_number,
                  base_colours, contrast_value)= extract_const_movie_parameters(outpath)
                  
    
                  true_cell_radius.set(true_cell_radius_pickle)
                  ###################################
                  """
                  global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
                  dict_of_divisions,number_of_added_new_cells
                  list_of_ch_movie_params=extract_changeable_params_history(outpath)
                  xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells= extract_changeable_params_history(outpath)
                  edit_id_indicator.set(edit_id_indicator_pickle)
                  """
                  ########################################################
                  cell_info_label.config(text= "FRAME SIZE: "+str(frame_size)+"x"+str(frame_size)+
                           "\nCELL DIAMETER:= "+str(2*true_cell_radius.get())+"\nPATCH SIZE= "+str(2*patch_size)+" x "+str(2*patch_size))
                  #############################################
                  lineage_per_frame = extract_lineage(outpath)
                  last_frame_cell_dict=lineage_per_frame[-1]
                  n_cells=len(last_frame_cell_dict)    
                  internal_cell_names=list(last_frame_cell_dict.keys())
    
                  global coords, start_frame
                  start_frame=last_frame_cell_dict[internal_cell_names[0]][12]+1    
                  coords=last_frame_cell_dict[internal_cell_names[0]][14]
    
                  global output_images,lineage_images, output_names,lineage_images_cv2    
                  output_images,lineage_images, output_names,lineage_images_cv2=extract_output_images(out_folders[3],out_folders[5],canvas_size_p4, output_images,output_names)
    
                  global  previous_lineage_image, lineage_image_size
                  previous_lineage_image=lineage_images_cv2[-1]     
                  lineage_image_size=previous_lineage_image.shape[0]
                  #######################################################
                  #################################################
                  if len(all_names_fluor)>len(output_names_fluor):
                     print("partly tracked")
                     global popup_partly_tracked, button_retrieve    
                     popup_partly_tracked = tk.Toplevel(master=page4, width=200, height=50, bg="red")
                     label_popup = tk.Label(popup_partly_tracked, text="Partly tracked",width=100, height=20, bg="black", fg="yellow", font='TkDefaultFont 10 bold' )
                     label_popup.pack()
                     #button_retrieve = Button(popup_partly_tracked, text="Retrieve unfinished movie",
                     #bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=retrieve_unfinished_movie).start(), update_flash([]), feedback_label.configure(text="Loading unfinished movie ..."),popup_partly_tracked.destroy() ])
                     button_retrieve = Button(popup_partly_tracked, text="Retrieve unfinished movie",
                     bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[retrieve_unfinished_movie(), update_flash([]), feedback_label.configure(text="Loading unfinished movie ..."),popup_partly_tracked.destroy() ])
                     button_retrieve.pack()
                     
                     #button_close = Button(popup_partly_tracked, text=" Close",font='TkDefaultFont 10 bold', bg=button_color, command=popup_partly_tracked.destroy())
                     #button_close.pack()
        
                  else:
                     print("fully tracked")
                     def close_fully_popup():
                      popup_fully_tracked.destroy()                      
                      display_first_frame()
                                        
                     global popup_fully_tracked    
                     popup_fully_tracked = tk.Toplevel(master=page4, bg="blue")
                     w,h = 200,50                      
                     x,y = (ws/2) - (w/2),(hs/2) - (h/2)                     
                     popup_fully_tracked.geometry('%dx%d+%d+%d' % (w, h, x, y))
                     label_popup = tk.Label(popup_fully_tracked, text="Fully tracked",bg="black", fg="yellow", font='TkDefaultFont 10 bold' )
                     label_popup.pack()
                     button_ok = Button(popup_fully_tracked, text=" OK",font='TkDefaultFont 10 bold', bg=button_color, command=close_fully_popup)
                     button_ok.pack()
                     input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1))  
            else:# 3. if RESULT_FLUOR does not exist
                 print("RESULT_FLUORESCENT does not exist")
                 shutil.rmtree(outpath)# delete OUPUT if it exists
                 os.mkdir(outpath)# create OUTPUT folder and start tracking from Frame 1
                 prepare_for_first_go()

#############################################################
 
def prepare_for_first_go():
    
    global popup_first_preview, canvas_popup_fluor_p4,canvas_popup_bright_p4,canvas_popup_red_p4    
    popup_first_preview = tk.Toplevel(master=page4, width=1528, height=50, bg="blue")
    
    frame1 = tk.Frame(master=popup_first_preview , width=1528, height=50, bg="orange")
    frame1.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame2 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="yellow")
    frame2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame3 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="white")
    frame3.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame4 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="green")
    frame4.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame5 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="red")
    frame5.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame6 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="blue")
    frame6.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame7 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg="grey")
    frame7.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame8 = tk.Frame(master=popup_first_preview , width=1528, height=50,bg="yellow")
    frame8.grid(row=3, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame9 = tk.Frame(master=popup_first_preview , width=1528, height=50,bg="white")
    frame9.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    ###########################################
    l_feedback=tk.Label(frame1,text= "Input movie: ", bg="black", fg="cyan", font=("Times", "12"))
    l_feedback.pack()
    
    global  canvas_left_pop, canvas_mid_pop, canvas_right_pop 
    canvas_left_pop = Canvas(frame2, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_left_pop.pack(anchor='nw', fill='both', expand=True)
    canvas_mid_pop = Canvas(frame3, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_mid_pop.pack(anchor='nw', fill='both', expand=True)
    canvas_right_pop = Canvas(frame4, bg="green", height=canvas_size_p4, width=canvas_size_p4)
    canvas_right_pop.pack(anchor='nw', fill='both', expand=True)
    
    l_bright=tk.Label(frame5,text= "Bright ", bg="black", fg="cyan", font=("Times", "12"))
    l_fluor=tk.Label(frame6,text= "Fluor ", bg="black", fg="cyan", font=("Times", "12"))
    l_red=tk.Label(frame7,text= "Red ", bg="black", fg="cyan", font=("Times", "12"))
    l_bright.pack(),l_fluor.pack(),l_red.pack()
    global  button_contrast,button_cell_radius,  button_assign_positions,  pop_slider,button_count_cells 
    button_contrast = Button(frame5, text="2a. Enhance image contrast",font='TkDefaultFont 10 bold', bg=button_color, command=create_contrast_popup)
    button_contrast.pack()
    
    button_cell_radius = Button(frame6, text="2b. Measure cell size",font='TkDefaultFont 10 bold', bg=button_color, command=create_cell_measure_popup)
    button_cell_radius.pack()
    
    
    button_assign_positions = Button(frame7, text="2c. Assign initial cell positions",font='TkDefaultFont 10 bold', bg=button_color, command=create_assign_cell_positions_popup)
    button_assign_positions.pack()
###################################################
          
    def click_cells_to_count(event):     
      canvas_mid_pop.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
      clicked_cells.append([event.x, event.y])
      global max_number_of_cells
      max_number_of_cells=len(clicked_cells)
      if max_number_of_cells==1:
          update_flash([button_close])
      print("max_number_of_cells=",max_number_of_cells)
      cell_numbers_label.config(text="# CELLS IN FRAME 1 = "+str(len(manual_init_positions))+
                                '\nMAX # CELLS IN A FRAME = '+str(max_number_of_cells))
########################################################    
    def start_counting_cells():
        print(" I am inside start_counting_cells")
        update_flash([])
        button_count_cells.config(bg="red")
        canvas_mid_pop.bind("<Button-1>",click_cells_to_count)
        global clicked_cells
        clicked_cells=[]
###########################################        
    button_count_cells = Button(frame7, text="2d. Count max number of cells",font='TkDefaultFont 10 bold', bg=button_color, command=start_counting_cells)
    button_count_cells.pack()
    
    global  all_names_fluor,all_names_bright,all_names_red
        
    all_names_fluor, all_names_bright,all_names_red=load_full_raw_movie(my_dir)
    print("len(all_names_fluor)=", len(all_names_fluor))
    print("len(all_names_bright)=", len(all_names_bright))
    print("len(all_names_red)=", len(all_names_red))
    #####################
    
    #######################
    global  bright_dictionary,red_dictionary,fluor_dictionary
    red_dictionary=create_name_dictionary_p4(all_names_red)
    bright_dictionary=create_name_dictionary_p4(all_names_bright)
    fluor_dictionary=create_name_dictionary_p4(all_names_fluor)
    #print("fluor_dictionary=", fluor_dictionary)   
    ############################
    global slide_frames_pop    
    def slide_frames_pop(value): 
       image_number = int(value)
       image_number_zfill=str(value).zfill(n_digits)
       print("image_number=", image_number)
       print("image_number_zfill=", image_number_zfill)
       #show_3_channels(canvas_left_pop,canvas_mid_pop,canvas_right_pop, all_names_fluor,all_names_bright,all_names_red,canvas_size_p4,image_number)
       
       canvas_left_pop.delete("all")
       canvas_mid_pop.delete("all")
       canvas_right_pop.delete("all")
       image_number=int(value)    
       #frame_slider.config(label="Frame "+str(value))
       ###########################################
       global br_tk,fl_tk,red_tk        
       br_tk, br_name=display_image_p4(image_number_zfill, bright_dictionary,"ch02", canvas_size_p4)              
       canvas_left_pop.create_image(0,0, anchor=NW, image=br_tk)
       l_bright.config(text= "Bright \n"+br_name)
       #br_name_p2.set("Original name:   "+old_br_name+"\nNew name:   "+new_br_name)    
       ################################    
       fl_tk, fl_name=display_image_p4(image_number_zfill, fluor_dictionary,"ch00", canvas_size_p4)     
             
       canvas_mid_pop.create_image(0,0, anchor=NW, image=fl_tk)
       l_fluor.config(text= "Fluor \n"+fl_name)
       #fl_name_p2.set("Original name:   "+old_fl_name+"\nNew name:   "+new_fl_name)    
       ###############################################
       red_tk, red_name=display_image_p4(image_number_zfill, red_dictionary,"ch01",canvas_size_p4)          
           
       canvas_right_pop.create_image(0,0, anchor=NW, image=red_tk)
       l_red.config(text= "Red \n"+red_name)                   
       #red_name_p2.set("Original name:   "+old_red_name+"\nNew name:  
       ################################# 
    
    pop_slider = Scale(frame6, from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1, orient=HORIZONTAL, troughcolor="green", command=slide_frames_pop, length=370)      
    pop_slider.pack()
    #view_slider.config(from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1)      
    slide_frames_pop(first_frame_number)
    instruct_label = tk.Label(frame8, text=" Welcome to STEP 3 of the pipeline! \n\nTo choose input movie you want to track, press Button 1. ",fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
    instruct_label.grid(row=1, column=0,columnspan=4, sticky=W)
    
    button_close = Button(frame9, text=" Close initial popup",font='TkDefaultFont 10 bold', bg=button_color, command=close_popup_canvas)
    button_close.pack()
    ###########################################   
    global  full_core_bright_name, out_folders#, output_names
    
    #view_slider.config(to=num_frames)       
    input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1)) 
    #input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nNUMBER OF FRAMES: "+str(num_frames))    
    out_folders = create_output_folders(outpath)
    #output_names=[None]    
    full_core_bright_name, _, _= extract_file_name(all_names_bright[0])
    print("n_digits=", n_digits)   
    ########### load the first clip         
    #global fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names                 
    #fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(0,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number)
    global   previous_lineage_image, lineage_image_size, number_of_added_new_cells
    number_of_added_new_cells=0     
    #frame_size=fluor_images[0].shape[0]
    cell_info_label.config(text= "FRAME SIZE:"+str(frame_size)+"x"+str(frame_size), fg="#00FFFF", bg="black")
    print("frame_size_before=", frame_size)
    if num_frames<=382:
        lineage_image_size=num_frames#this is the size of lineage image
    else:
        lineage_image_size=num_frames
    previous_lineage_image =np.zeros((lineage_image_size, lineage_image_size+200,3), dtype="uint8") 
    feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))   
    button_load.configure(background =button_color)
    global start_frame
    start_frame=first_frame_number
    print("start_frame inside prepare for first_go=", start_frame)   
    update_flash([button_contrast])
#######################################
global retrieve_unfinished_movie
def retrieve_unfinished_movie():# in retrieve mode
    print("I am inside retrieve function")
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
    dict_of_divisions,number_of_added_new_cells,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history= extract_changeable_params_history(outpath, -1)
    edit_id_indicator.set(edit_id_indicator_pickle)
    ########################################################
    update_flash([button_execute])                
    display_first_frame()
    input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1))           
    feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))
    
###########################################
button_load = Button(frame1_page4, text="1. Click to open file menu and then select input movie folder",
               bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=initiate_tracking_page).start(), update_flash([]), feedback_label.configure(text="Loading input movie ...") ])
button_load.grid(row=2, column=0, padx=10, pady=20)

################################
######### measure cell radius in cell_measure_popup window (Bitton 2b)
############################
def draw_first_circles(event):# draw green circles to measure cell diameter
    rad=scaled_cell_radius.get()
    circle=canvas_for_radius.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline = "green",width = 2)
    centres.append([int(round(event.x)), int(round(event.y))])
    circles.append(circle)
    if len(circles)==1:
           update_flash([radius_slider])
##############################################              
def change_radius(value):# change cell radius manually  
  new_circles=[]  
  scaled_cell_radius=int(value)
  true_cell_radius.set(int(round(scaled_cell_radius*frame_size/popup_window_size)))
  radius_slider.config(label="Cell radius =  "+str(true_cell_radius.get())) 
  #radius_slider.set(cell_radius)
  global circles
  for k in range(len(centres)):
       canvas_for_radius.delete(circles[k])
       new_circle=canvas_for_radius.create_oval(centres[k][0]-scaled_cell_radius,centres[k][1]-scaled_cell_radius,centres[k][0]+scaled_cell_radius,centres[k][1]+scaled_cell_radius,outline = "green",width = 2) 
       #canvas.create_oval(event.x-value,event.y-value,event.x+value,event.y+value,outline = "red",width = 2)
       #coords.append([event.x, event.y])
       new_circles.append(new_circle)
       if len(new_circles)==1:
             update_flash([button_save_radius])       
  circles=new_circles
###################################################
def save_cell_radius():
    global patch_size
    update_flash([button_assign_positions])
    patch_size=int(round(true_cell_radius.get()*2.4))
    #patch_size=int(round(true_cell_radius.get()*2.4))
    print("cell_radius, patch_size=", true_cell_radius.get(), patch_size)
    popup_for_radius.destroy()
    cell_info_label.config(text= "FRAME SIZE: "+str(frame_size)+"x"+str(frame_size)+
                           "\nCELL DIAMETER:= "+str(2*true_cell_radius.get())+"\nPATCH SIZE= "+str(2*patch_size)+" x "+str(2*patch_size),
                           fg="#00FFFF", bg="black")
    
    #return true_cell_radius, patch_size
#################################
#######################################
def record_const_movie_parameters():# record cell_size and other parameters in pickle file to be used at Step 4 and in retrieve mode
    list_of_const_movie_params=[frame_size, true_cell_radius.get(), patch_size,max_number_of_cells,
                          num_frames, full_core_fluor_name, n_digits,full_core_bright_name, first_frame_number,
                          base_colours, contrast_value]
    const_parameters_path=os.path.join(outpath,"constant_movie_parameters.pkl")  
    with open(const_parameters_path, 'wb') as f:
        for i in range(len(list_of_const_movie_params)):
           pickle.dump(list_of_const_movie_params[i], f,protocol=pickle.HIGHEST_PROTOCOL)
#####################################
def create_cell_measure_popup():
    update_flash([])
    global popup_for_radius, canvas_for_radius, photo_image
    #global cliplimit
    #cliplimit=IntVar()
    #cliplimit.set(0.)
    popup_for_radius = tk.Toplevel(master=popup_first_preview, width=popup_window_size, height=popup_window_size)
    frame1 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=popup_window_size)
    frame1.pack()
    frame2 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=50)
    frame2.pack()

    canvas_for_radius = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg="black")
    canvas_for_radius.pack(anchor='nw', fill='both', expand=True)
    #######################################
    if contrast_value!="0":
           global last_image              
           clahe = cv2.createCLAHE(clipLimit=float(contrast_value))
           init_image=clahe.apply(last_image)
               
    photo_image=turn_image_into_tkinter(init_image,popup_window_size)     
    canvas_for_radius.create_image(0,0, anchor=NW, image=photo_image)

    global centres, circles,scaled_cell_radius, true_cell_radius
    centres, circles,scaled_cell_radius, true_cell_radius =[],[],IntVar(),IntVar()

    scaled_cell_radius.set(20)
    true_cell_radius.set(int(round(scaled_cell_radius.get()*frame_size/popup_window_size)))
    print("initial_true_radius=",true_cell_radius.get())
    global radius_slider, button_save_radius   
    radius_slider=Scale(frame2,from_=1,to=100,orient=HORIZONTAL,troughcolor="#513B1C",activebackground="red",label="Cell radius = "+str(int(true_cell_radius.get())),variable=scaled_cell_radius, command=change_radius, length=150, showvalue=0)
    radius_slider.pack()
    
    button_save_radius=tk.Button(frame2,text="Save",activebackground="red", command=save_cell_radius)
    button_save_radius.pack()    
    canvas_for_radius.bind("<Button-1>",draw_first_circles)    
###############################################
################### adjust contrast if necessary in contrast_popup (Button 2a)  
########################################
global contrast_value
contrast_value=StringVar()
contrast_value.set("0")

def save_contrast():
    ind=cliplimit.get()
    print("ind = ", ind)
    update_flash([button_cell_radius])
    button_save_contrast.config(bg=button_color)     
    popup_contrast.destroy()    
#########################################
def create_contrast_popup():
    #window_size=800
    global popup_contrast, canvas_contrast, photo_image, number_of_contrast_changes
    number_of_contrast_changes=[]
    global cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_contrast = tk.Toplevel(master= popup_first_preview , width=popup_window_size, height=popup_window_size)
    frame1 = tk.Frame(master=popup_contrast, width=popup_window_size, height=popup_window_size)
    frame1.pack()
    frame2 = tk.Frame(master=popup_contrast, width=popup_window_size, height=50)
    frame2.pack()

    canvas_contrast = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg="black")
    canvas_contrast.pack(anchor='nw', fill='both', expand=True)
   
    photo_image=turn_image_into_tkinter(init_image,popup_window_size)     
    canvas_contrast.create_image(0,0, anchor=NW, image=photo_image)    
    global contrast_slider, button_save_contrast    
    contrast_slider=Scale(frame2,from_=0,to=100,orient=HORIZONTAL,troughcolor="#513B1C",variable=cliplimit,activebackground="red",label="Cliplimit = " +str(int(cliplimit.get())),command=change_contrast, length=150, showvalue=0)
    contrast_slider.pack()
    
    button_save_contrast=tk.Button(frame2,text="Save",activebackground="red", command=save_contrast)
    button_save_contrast.pack()    
    update_flash([contrast_slider])    
###################################
def change_contrast(value):
    number_of_contrast_changes.append(value)
    if len(number_of_contrast_changes)==1:
        update_flash([button_save_contrast])
    canvas_contrast.delete("all")
    contrast_slider.config(label="Cliplimit =  "+ value)
    init_image_copy=init_image.copy()   
    if value!="0":
      global contrast_value
      contrast_value=value
      #contrast_indicator.set("yes") 
      clahe = cv2.createCLAHE(clipLimit=float(value))
      cl=clahe.apply(init_image_copy)      
      result=cl
    else:     
      result=init_image
      #contrast_indicator.set("yes")           
    global photo_image_contrast
    photo_image_contrast=turn_image_into_tkinter(result,popup_window_size)     
    canvas_contrast.create_image(0,0, anchor=NW, image=photo_image_contrast)
###############################
################### Assign initial cell positions in assign_cell_positions_popup (Button 2c)

##################################
global create_assign_cell_positions_popup
def create_assign_cell_positions_popup():
    #update_flash([])
    global  manual_init_positions
    manual_init_positions =[]
    feedback_label.configure(text="Waiting for manual assignment of cell positions in Frame 1 ...")
    button_contrast.configure(bg=button_color, fg="black")
    global popup_assign_pos,  cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_assign_pos = tk.Toplevel(master=popup_first_preview, width=popup_window_size, height=popup_window_size)
    sub1 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=50, bg="#A52A2A")
    sub1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    global label_click_popup
    label_click_popup = tk.Label(
        sub1, text="Click on each cell with the left button of the mouse,\nthen save", bg="black",fg="yellow", font='TkDefaultFont 10 bold')
    label_click_popup.pack()
     
    sub2 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=popup_window_size, bg="#A52A2A")
    sub2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

    global canvas_assign_pos
    
    print("manual_init_positions inside create assign=",manual_init_positions)
    canvas_assign_pos = Canvas(sub2, bg='black', height=popup_window_size, width=popup_window_size)
    canvas_assign_pos.pack(anchor='nw', fill='both', expand=True)
    canvas_assign_pos.bind("<Button-1>", click_position)
    
      
    sub3 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=50, bg="#A52A2A")
    sub3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    global button_save_init_positions, photo_image
    button_save_init_positions = Button(sub3, text="Save", bg=button_color,activebackground="red", command= close_assign_window)
    button_save_init_positions.pack()
    #update_flash([button_save_init_positions])    
    canvas_assign_pos.create_image(0, 0, anchor=NW, image=photo_image_contrast)
################ draw red spots in popup canvas in response to mouse click
def click_position(event):
    #print("manual_init_positions inside click_position=",manual_init_positions)
    canvas_assign_pos.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    #print("manual_init_positions second time=",manual_init_positions)
    manual_init_positions.append([event.x/popup_window_size*frame_size, event.y/popup_window_size*frame_size])
    if len(manual_init_positions)==1:
        update_flash([button_save_init_positions])
    cell_numbers_label.config(text="NUMBER OF CELLS IN FRAME 1 = "+str(len(manual_init_positions)))
    
##################################
def close_assign_window():
     update_flash([button_count_cells]) 
     popup_assign_pos.destroy()  
############################    
def close_popup_canvas(): # save initial positions of cells in Frame 1                    
      global coords, manual_init_positiona, coords_very_first    
      
      coords_very_first=manual_init_positions
      global colour_dictionary, new_naive_names, colour_counter, base_colours, unused_naive_names, xs
          
      colour_dictionary, new_naive_names, base_colours, colour_counter, unused_naive_names,xs= create_first_color_dictionary(
        max_number_of_cells, len(manual_init_positions), num_frames)
      #print("colour_counter=",colour_counter)
      #print("colour_dictionary=",colour_dictionary)
      #print("new_naive_names=",new_naive_names)
      #print("unused_naive_names=",unused_naive_names)
      #print("max_number_of_cells=",max_number_of_cells)
      #print("xs=", xs)
      #global xs
      #xs=create_dictionary_of_xs(new_naive_names, coords_very_first, num_frames, max_number_of_cells)   
      N_cells=len(manual_init_positions)      
      global curr_frame_cell_names, flag,  edit_id_indicator
      curr_frame_cell_names = new_naive_names# names of cell in the current frame
      flag="manual centroids"
      edit_id_indicator.set("yes")
      coords = np.zeros((N_cells, 2))
      #print("xs=", xs)
       #print("template_names=", template_names)
      print("curr_frame_cell_names=", curr_frame_cell_names)
     
     
      
      #prev_frame = np.zeros((frame_size, frame_size), dtype="float64")
     
      for i in range(N_cells):
        coords[i] = manual_init_positions[i]
        
      print("coords=", coords)
      button_contrast.configure(text =str(len(coords))+ " cells" ,background="black", fg="#00FFFF")
      feedback_label.config(text="The positions of cells in Frame 1 has been saved.\n\nTo start execution, press Button 3.")
      #stop_flash("save", popup, flashers)
      update_flash([button_execute])
     
      popup_first_preview.destroy()

####################################################
############################################  
global curr_frame_cell_names, variable_stop, manual_division_indicator, mother_number, edit_id_indicator
curr_frame_cell_names, variable_stop, manual_division_indicator, mother_number, edit_id_indicator=StringVar(), "Do not stop", StringVar(), IntVar(),StringVar()
manual_division_indicator.set("no")
edit_id_indicator.set("no")
#############################################################

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
def cut_lineage(start_frame_internal): # after pausing
    lineage_per_frame_p4=extract_lineage(outpath)
    print("len(lineage_per_frame_p4) BEFORE=", len(lineage_per_frame_p4))
    del lineage_per_frame_p4[(start_frame_internal)-1:]# was -1
    print("len(lineage_per_frame_p4) AFTER=", len(lineage_per_frame_p4))   
    update_lineage(lineage_per_frame_p4,outpath,'wb')# "wb" means delete previous lineage and write a new one
    global output_images,lineage_images,lineage_images_cv2, output_names    
    #del output_images[(start_frame):]# was start_frame:
    #del output_names[(start_frame):]
    print("start_frame_internal=", start_frame_internal)
    print("len(output_images)=",len(output_images))
    print("len(output_names)=",len(output_names)) 
    global previous_lineage_image
    print("len(lineage_images_cv2) before cut lineage=",len(lineage_images_cv2))   
    previous_lineage_image=lineage_images_cv2[start_frame_internal-2]

    del lineage_images_cv2[(start_frame_internal-1):] 
    del lineage_images[(start_frame_internal-1):]
    del output_images[(start_frame_internal):]# was start_frame:
    del output_names[(start_frame_internal):]
    del changeable_params_history[(start_frame_internal-1):]
    update_changeable_params_history(changeable_params_history,outpath, "wb")
    
    print("len(lineage_images_cv2) after cut=",len(lineage_images_cv2))
    """          
    global dict_of_divisions 
    print("dict_of_divisios before cut_lineage=", dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}
    print("dict_of_divisios after cut_lineage=", dict_of_divisions)
    """
    folders_to_truncate=["MASKS","RESULT_FLUORESCENT","LINEAGE_IMAGES","CLEANED_PATCHES", "RESULT_BRIGHT"]
    for folder in folders_to_truncate:
        full_path_to_folder=os.path.join(outpath,folder)
        for filename in os.listdir(full_path_to_folder):
            index_t=filename.index("_t")
            number=int(filename[index_t+2:-9])
            if number>=start_frame:
               full_name=os.path.join(full_path_to_folder, filename)
               os.remove(full_name)

###########################################################
def clear_memory_of_previous_clip(fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names ):
 if fluor_images:
     del fluor_images
 if fluor_images_compressed:
     del fluor_images_compressed
 if bright_images:
     del bright_images
 if fluor_names:
     del fluor_names
 if br_names:
     del br_names     
#############################################


import time
########################################################
def execute(): 
 global start_frame
 print("START_FRAME inside execute=", start_frame)
 start_time=time.time()
 label_curr_frame_name.config(text=start_empty_file_name)
 label_current.configure(text="Current frame:  ", fg="black") 
 try:
    cell_radius=true_cell_radius.get()   
    canvas_previous.delete("all")
    canvas_current.delete("all")
    canvas_lineage.delete("all")
    button_execute.configure(background = 'red')   
    label_edit.configure(text=" ")    
    feedback_label.config(text="Wait, loading models ...", fg="yellow")
    global lineage_images, output_images, lineage_per_frame_p4, previous_lineage_image, lineage_images_cv2     
    if lineage_per_frame_p4:
        del lineage_per_frame_p4
    
    global variable_stop,  tracker, segmentor, refiner# this variable allows to stop the loop (controlled by Stop button)     
    global coords, curr_frame_cell_names, count,  cells, old_number_of_cells, edit_id_indicator,kk
    label_edit.configure(text="curr_frame_cell_names:\n " + str(curr_frame_cell_names), bg="black")     
    N_cells = coords.shape[0]
    division_indicator=0
    centroids_for_benchmarking=[coords]
    n =num_frames  
    #k = start_frame  # the first frame of clip 
    first_number_in_clip=start_frame    
    kk = 0  # the number of frame within clip    
    clear_memory_of_models(tracker, segmentor, refiner)
    tracker, segmentor, refiner=load_weights(models)    
    feedback_label.config(text="Execution is about to begin ...")
    update_flash([button_pause])
    
    print("num_frames=", num_frames)
    print("first_frame_number=", first_frame_number)
    last_frame_number=num_frames+first_frame_number-1
    print("last_frame_number=", last_frame_number)
    # n=last_frame_number
    while  first_number_in_clip <= last_frame_number:    
    #while k < n:
        print("Inside  k -loop=")
                
        global fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names
        clear_memory_of_previous_clip(fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names)
        fluor_images,fluor_images_compressed,bright_images,fluor_names,br_names =load_clip( first_number_in_clip,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number)
        
        clip_centr = predict_tracking_general(
                coords, fluor_images, fluor_images_compressed, fluor_names,  first_number_in_clip, out_folders[0], tracker,last_frame_number, cell_radius, frame_size)
        print("TRACKING PREDICTED FOR CLIP BEGINNING WITH FRAME  ", first_number_in_clip)
                
        for kk in range(len(clip_centr)):# it is actually 4 (number of frames in clip)
            current_frame_number=first_number_in_clip+kk
            cv2.imwrite(r"C:\Users\helina\Desktop\previous\previous_frame_%s.tif" % ( current_frame_number), previous_lineage_image)            
            print("FRAME NUMBER = ",  current_frame_number)# segmenting all the 4 frames in the clip            
            #print("edit_id_indicator.get()=",edit_id_indicator.get())
            if  edit_id_indicator.get()=="yes" and kk==0:
                clip_centr=force_manual_IDs(clip_centr,coords,kk)
                edit_id_indicator.set("no")
            else:
                clip_centr =  backup_track(
                   clip_centr, coords, kk, cell_radius)  # correct too big jumps
                      
            tracked_centroids=clip_centr[kk]              
            empty_fluor = fluor_images[kk]         
            empty_bright = bright_images[kk]                        
            count, cells, coords,  curr_frame_cell_names, olds = segment_and_clean(
                dict_of_divisions, cells, count, coords,curr_frame_cell_names, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, first_number_in_clip+kk, edit_id_indicator, mother_number, out_folders, cell_radius, frame_size, colour_dictionary, patch_size, "first cleaning")
          
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
                   cells, count, first_number_in_clip, kk)             
               if (np.any(count == 2) or np.any(count == 1)):                  
                   if mother_8_name != []:
                       count = check_division_frame_number(
                           count, cells, dict_of_divisions, mother_8_name, first_number_in_clip+kk)                      
               if np.any(count == 2):
                 
                   
                   cells, curr_frame_cell_names, count, division_indicator, coords = update_dictionary_after_division(
                       cut_patch, cells, curr_frame_cell_names, count, division_indicator, coords, frame_size, colour_dictionary)
               if division_indicator == 1 and mother_8_name != []:                   
                   dict_of_divisions[mother_8_name] = first_number_in_clip+kk
                   #print("mother_cell_name =", mother_8_name)                  
                   #print("8-figure division detected in frame ", first_number_in_clip+kk)                 
            #################################################### 
                      
            if manual_division_indicator.get()=="yes":
                 manual_division_indicator.set("no")
            record_const_movie_parameters()
            update_changeable_params_history([[xs,curr_frame_cell_names,flag,edit_id_indicator.get(),colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells]],outpath, 'ab')
            update_lineage([cells],outpath,'ab')# concatenates {cells}  to pickle 
            feedback_label.config(text="Execution in progress: \nFrame "+ str(first_number_in_clip+kk)+"\n - If you need to stop for editing, press Button 3a."
                            "\n - Otherwise, wait until execution is finished.")
            #label_current.configure(text="Current frame: " +str(first_frame_number+k+kk+1), fg="red")           
            N_cells = len(cells)
            print("cells after division detector=", list(cells.keys()))
            #print("n_digits_inside execute=", n_digits)
           
            current_lineage_image=create_lineage_image_one_frame(cells, previous_lineage_image, xs, first_number_in_clip+kk, first_frame_number)
            print("current_lineage_image.shape =", current_lineage_image.shape)
            #print("fluor_names inside exeute=", fluor_names)
            coords, destin_fluor = plot_frame(cells, clip_centr, first_number_in_clip, kk,
                                fluor_images, fluor_names, out_folders, coords, coords, bright_images, br_names, frame_size , n_digits, first_frame_number, contrast_value, current_lineage_image,patch_size)          
            
                      
            image_seg=destin_fluor
            photo_image_seg=turn_image_into_tkinter(image_seg, canvas_size_p4)
            #canvas_current.create_image(0,0,anchor=NW,image=photo_image_seg)
            output_images.append(photo_image_seg)
            output_name=rename_file(out_folders[3],fluor_names[kk])
            output_name_base=os.path.split(output_name)[1]          
            output_names.append(output_name_base)
            #output_names.append(rename_file(out_folders[3],fluor_names[kk]))         
            image_lin=current_lineage_image
            image_lin_copy=copy.deepcopy(image_lin)         
            lineage_images_cv2.append(image_lin_copy)
            previous_lineage_image=current_lineage_image# need it for the next lineage image
            print("len(lineage_images_cv2) inside execute=",len(lineage_images_cv2))
            print("image_lin.shape=",image_lin.shape)                       
            photo_image_lin=turn_image_into_tkinter(image_lin, canvas_size_p4)
            #canvas_lineage.create_image(0,0,anchor=NW,image=photo_image_lin)          
            lineage_images.append(photo_image_lin)
            input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1)) 
            centroids_for_benchmarking.append(coords)            
            
            #print("set view_slider at ",first_frame_number+k+kk)
            
            if  first_number_in_clip == start_frame and kk==0:
            #if  k == start_frame-1 and kk==0:
                 view_slider.config(from_=first_frame_number,to=first_frame_number+len(all_names_fluor)-1)
            
            view_slider.set(first_number_in_clip+kk)
            slide_frames(view_slider.get())
            print("set view_slider at ",first_number_in_clip+kk)
            if variable_stop=="Stop":              
               start_frame=current_frame_number+1
               print("current_frame_number after stop=", current_frame_number)
               print("new start frame after stop=", start_frame)                                                                              
               break                  
            if (division_indicator == 1):
                print("division occured in frame ", first_number_in_clip+kk)              
                dict_of_divisions[existing_cell_names[-1][:-1]] = first_number_in_clip+kk
                break 
            
       
        print("BROKE OUT OF BIG LOOP")
        if variable_stop=="Stop":
            #first_number_in_clip = first_number_in_clip+kk
            N_cells = coords.shape[0]
            break
        else:            
            if (division_indicator == 1):
              first_number_in_clip = first_number_in_clip+kk
              N_cells = coords.shape[0]            
            else:
              first_number_in_clip += 4                
             
 except:
       feedback_label.config(text="Stopped due to error", fg="#DF0101", font='TkDefaultFont 10 bold')      
       #start_frame=k+kk+1            
       print("Stopped due to error!!!!!")
       tk.messagebox.showerror('Error',traceback.format_exc())
       update_flash([])     
 if variable_stop=="Stop":
     print("MANAGED TO BREAK OUT OF CLIP LOOP")
     feedback_label.config(text="You stopped execution manually. \nPress Button 4 to check results." )
     variable_stop="Do not stop"
 else:
     feedback_label.config(text="Execution finished! \nPress Button 4 to check results." )
     finish_time=time.time()
     execution_time=finish_time-start_time
     print("execution_time=", execution_time)
 button_execute.configure(background = button_color)
 update_flash([button_display])
 button_pause.configure(background = "red")
 print("dict_of_divisions after execution =", dict_of_divisions) 
###############################################
def stop_execution_manually():
    print("STOPPED MANUALLY!!!!")
    button_execute.configure(background = button_color)
    global variable_stop
    variable_stop = "Stop"
    button_pause.configure(background = "red")
    #print("START_FRAME after pushing pause=", start_frame)
    print("dict_of_divisions after execution inside stop_exec_manually=", dict_of_divisions)
#################################################################    
button_pause = Button(frame2_page4, text="3a. Pause ",activebackground="red",
               bg='#9ACD32', font='TkDefaultFont 10 bold', command=stop_execution_manually)
button_pause.grid(row=0, column=2, padx=10, pady=20)  
#############################
def slide_frames(value):# view_slider (main screen)

    image_number = int(value)
    #print("image_number inside slide_frames=", image_number)    
    internal_image_number=image_number-first_frame_number+1    
    label_curr_frame_name.config(text=output_names[image_number-first_frame_number+1])
    label_current.configure(text="Current frame: " +str(image_number), fg="black")     
    show_3_canvases(canvas_previous,canvas_current,canvas_lineage,output_images,lineage_images,image_number, first_frame_number)
##############################################
global view_slider# main screen
view_slider = Scale(frame9_page4, from_=1, to=1, orient=HORIZONTAL, troughcolor="green", command=slide_frames, length=370)      
view_slider.grid(row=6, column=0, pady=5) 
###########################################
def display_first_frame():# display all frames after pushing button "Display result"
    view_slider.config(from_=first_frame_number,to=len(output_images)+first_frame_number-2)   
    view_slider.set(str(first_frame_number))  
    slide_frames(first_frame_number)
    
    global pedigree, lineage_per_frame_p4
    lineage_per_frame_p4=extract_lineage(outpath)
    print("len(lineage_per_frame_p4)=", len(lineage_per_frame_p4))
    # creates and saves per cell pedigree in pickle file, but then it is deleted when you push button "Execute"  
    pedigree = create_pedigree(lineage_per_frame_p4, outpath, frame_size) 
        
    feedback_label.config(text="Check results by sliding the bar under Current Frame."
                    "\n - If you need to edit cell IDs, press Button 5."
                    "\n - If you need to edit missed division, press Button 6."
                    "\n - If you are happy with the result press Button 7 to create lineage movie.")       
###########3#######################
def get_cell_IDs_manually(event):# gets cell ID from previous frame during editing
    if popup_monitor!=None:
          popup_monitor.deiconify()
    canvas_indicator=clicked.get()
    print("canvas_indicator=", canvas_indicator)
    if canvas_indicator=="Previous":
        canvas_IDs=canvas_previous# click on previos frame to get IDs
        shift=2
    else:
        canvas_IDs=canvas_current# click on current frame to get IDs
        shift=1
    global manual_IDs, cell_names_external, daughter_indicators
    print("len(lineage_per_frame_p4)=",len(lineage_per_frame_p4))
    frame=int(view_slider.get())
    print("frame number from slider=",frame)
    internal_frame_number=frame-first_frame_number+1
    print("internal_frame_number=", internal_frame_number)
    
    keys=list(lineage_per_frame_p4[internal_frame_number-shift].keys())#was -2  
    mask_image=lineage_per_frame_p4[internal_frame_number-shift][keys[0]][13]
    
    
    #keys=list(lineage_per_frame_p4[int(view_slider.get())-shift].keys())#was -2  
    #mask_image=lineage_per_frame_p4[int(view_slider.get())-shift][keys[0]][13]
    
    #previous_resized =cv2.resize(previous_image, (window_size,window_size), interpolation = cv2.INTER_AREA)  
    #cell_number=int(previous_resized[event.y,event.x])-1
    cell_number=int(mask_image[int(event.y/canvas_size_p4*frame_size),int(event.x/canvas_size_p4*frame_size)]-1)
    print("cell_number=", cell_number)
    manual_IDs.append(cell_number)
    print("manual_IDs=", manual_IDs)     
    cell_name_internal="cell_"+ str(cell_number) 
    cell_name_external=lineage_per_frame_p4[internal_frame_number-shift][cell_name_internal][11]# was -1
    daughter_ind=lineage_per_frame_p4[internal_frame_number-shift][cell_name_internal][16]# was -1
    daughter_indicators.append(daughter_ind)
    
    print("daughter_indicators=", daughter_indicators)
    print("cell_name_external=", cell_name_external)
    cell_names_external.append(cell_name_external)    
    colour_four_channel=colour_dictionary[cell_name_external]    
    colour_three_channel=colour_four_channel[:-1]
    colour_three_channel.reverse()    
    global colour
    colour="#%02x%02x%02x" % tuple(colour_three_channel)
    canvas_IDs.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    label_edit.configure(text="Cells chosen in Previous Frame:\n " + str(cell_names_external) +"\n", bg="black")  
########################
def get_centroids_manually(event):
    if popup_monitor!=None:
          popup_monitor.deiconify()
    canvas_current.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    manual_centroids.append([event.x/canvas_size_p4*frame_size, event.y/canvas_size_p4*frame_size])   
    label_edit.configure(text="Centroids assigned:\n " + str(manual_centroids) +"\n""Centroids assigned in Current Frame:\n " + str(manual_centroids), bg="black")
######################################
def start_editing_IDs():
    button_save_id.grid(row=3, column=0, columnspan=1)
    update_flash([button_save_id])
    if popup_monitor!=None:
          popup_monitor.deiconify()
    label_edit.configure(text="Click on the cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on the same cell in Current Frame \nMake sure you click on the centroid!")
  
    feedback_label.configure(text="First, click on the cell of interest in Previous Frame.\n"
               "Then, click on its desired position in Current Frame.\n You can repeat it MULTIPLE TIMES.\nFinally, save edits by pressing 5a.Save ID edits.")    
    global manual_centroids, manual_IDs, cell_names_external
    manual_centroids, manual_IDs, cell_names_external, daughter_indicators=[],[], [],[] 
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    update_flash([button_save_id])
    
    R_edit_division.configure(background = '#9ACD32')
    R_edit_ID.configure(background = 'red')
    print("dict_of_divisions after start_editing_IDs =", dict_of_divisions) 
####################################################
def stop_editing_IDs():
    
    R_edit_ID.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>") 
    global start_frame, lineage_per_frame_p4, edit_id_indicator
  
    
    start_frame=int(view_slider.get())
    print("start_frame=", start_frame)
    start_frame_internal=start_frame-first_frame_number+1
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
    dict_of_divisions,number_of_added_new_cells,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history= extract_changeable_params_history(outpath, start_frame_internal)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    edit_id_indicator.set("yes")
    ########################################################
    keys=list(lineage_per_frame_p4[start_frame_internal-1].keys())   
    coords_old=lineage_per_frame_p4[start_frame_internal-1][keys[0]][14]
    print("coords_old=", coords_old)
    
    for i in range(len(manual_centroids)):
        coords_old[manual_IDs[i]]=manual_centroids[i] 
    #############
    global coords
    coords=coords_old 
    print("coords=", coords)
    global mask_current    
    mask_current=lineage_per_frame_p4[start_frame_internal-1][keys[0]][13]    
    feedback_label.config(text="")
 
    text1=[lineage_per_frame_p4[start_frame_internal-2][key][11] for key in keys]
    print("text1=",text1)
    numbers=[lineage_per_frame_p4[start_frame_internal-2][key][17] for key in keys]
    print("numbers=",numbers)
    w=list(zip(numbers,text1))
    ww=sorted(w,key=lambda student:student[0])
    ress = list(zip(*ww))
    curr_frame_cell_names =list(ress[1])
               
    cut_lineage(start_frame_internal)
    
    print("dict_of_divisios before edit_IDs=", dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}
    print("dict_of_divisios after edit_IDs=", dict_of_divisions)
    ##############################
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    update_flash([button_execute])
    button_save_id.grid_forget()
    
    label_current.configure( text="Current frame", fg="black" )
    button_save_id.configure(background = '#9ACD32')
    button_pause.configure(background = button_color)
    #button_save_division.configure(background = '#9ACD32')
    feedback_label.config(text="You finished editing IDs.\n To resume execution, press Button 3." )
    print("dict_of_divisions after stop_editing_IDs =", dict_of_divisions)
    if  popup_monitor!=None: 
       popup_monitor.destroy()
###################################################
def start_editing_division():
    R_edit_division.configure(background = 'red')
    button_save_division.grid(row=3, column=1, columnspan=1)
    update_flash([button_save_division]) 
    
    label_edit.configure(text="Click on mother cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on daughter cells in Current Frame \nMake sure you click on centroids!")
    print("started manual division editing.....")
    global mother_number
    mother_number=None 
    feedback_label.configure(text="First, click on mother cell in Previous Frame.\n"
               "Then, click on daughter cells in Current Frame.\nYou can do it ONLY ONCE.\n Finally, save by pressing 6a. Save division edits.")    
    global manual_centroids, manual_IDs,cell_names_external, daughter_indicators
    manual_centroids, manual_IDs, cell_names_external, daughter_indicators=[],[],[],[]
    
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    
    R_edit_ID.configure(background = '#9ACD32')
   
########################################
def stop_editing_division():
    R_edit_division.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>")
    global  mask_prev_frame
    
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())
    
    print("frame number from slider=",start_frame)
    start_frame_internal=start_frame-first_frame_number+1
    print("internal_frame_number=", start_frame_internal)
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
    dict_of_divisions,number_of_added_new_cells,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history= extract_changeable_params_history(outpath, start_frame_internal)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    edit_id_indicator.set(edit_id_indicator_pickle)
    curr_frame_cell_names=[] 
    ########################################################
    keys=list(lineage_per_frame_p4[start_frame_internal-1].keys())# from previous frame was -2   
    mask_prev_frame=lineage_per_frame_p4[start_frame_internal-1][keys[0]][13]# prev_frame-1 is not a mistake!!! was -1
   
    coords_old=lineage_per_frame_p4[start_frame_internal-1][keys[0]][14] 
    global manual_IDs, mother_number, mother_name    
    manual_division_indicator.set("yes")
    mother_number=manual_IDs[0] 
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage_per_frame_p4[start_frame_internal-2][mother_name_internal][11]
    mother_color=lineage_per_frame_p4[start_frame_internal-2][mother_name_internal][15]
                                        
    daughter_1_number=mother_number
    daughter_2_number=len(coords_old)    
    daughter_1_name=mother_name+"0"
    daughter_2_name=mother_name+"1"
    new_cell_names=[ daughter_1_name, daughter_2_name]
   
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_cell_names,base_colours, colour_counter)    
    
    all_cell_numbers=[]# from prev_frame, for creating daughter names
    m=int(np.max(mask_prev_frame))
    for i in range(1,m+1):
      if np.any(mask_prev_frame==i):
          all_cell_numbers.append(i-1)     
    all_cell_numbers_sorted =sorted(all_cell_numbers)
    dict_keys=list(lineage_per_frame_p4[start_frame_internal-2].keys()) # in case there are overlaps in previous frame after segmentation
    for num in all_cell_numbers_sorted:
        cell_key="cell_"+str(num)
        if cell_key in dict_keys:
            true_cell_name=lineage_per_frame_p4[start_frame_internal-2][cell_key][11] 
            curr_frame_cell_names.append(true_cell_name)
    
    curr_frame_cell_names[mother_number]=daughter_1_name
    curr_frame_cell_names.append(daughter_2_name)  
    coords_daughter_1=manual_centroids[0]
    coords_daughter_2=manual_centroids[1]
    print("curr_frame_cell_names=",curr_frame_cell_names)
    coords_old[mother_number]=coords_daughter_1    
    coords_old=np.concatenate((coords_old,np.array(coords_daughter_2).reshape((1,2))))    
    global  coords
    coords=coords_old 
        
    dict_of_divisions[mother_name] = start_frame    
    cut_lineage(start_frame_internal)    
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    #view_slider.grid_remove()
    label_current.configure( text="Current frame", fg="black" )
    update_flash([button_execute])
    button_save_division.grid_forget()
    button_pause.configure(background = button_color)
    #stop_flash("save_division", page4, flashers)
    R_edit_division.configure(background = '#9ACD32')
    feedback_label.config(text="You finished editing missed division.\n To resume execution, press Button 3." ) 
############################################
def add_new_cell():
  button_save_added_cell.grid(row=3, column=2, columnspan=1)
  update_flash([button_save_added_cell])  
  global colour
  colour_init=[0,0,255]
  colour="#%02x%02x%02x" % tuple(colour_init)
  canvas_current.bind("<Button-1>", get_centroids_manually)  
  global manual_centroids
  manual_centroids=[] 
###############################################
def save_added_cell():   
    global start_frame    
    start_frame=int(view_slider.get())   
    internal_start_frame=start_frame-first_frame_number+1
    
    keys=list(lineage_per_frame_p4[internal_start_frame-1].keys())      
    b = np.array(manual_centroids)
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
    dict_of_divisions,number_of_added_new_cells,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history= extract_changeable_params_history(outpath, internal_start_frame)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    edit_id_indicator.set(edit_id_indicator_pickle)
     
    ########################################################
    global coords,  previous_lineage_image   
    coords_old=coords
    coords=np.concatenate((coords_old, b), axis=0)     
    number_of_now_added_cells=len(manual_centroids)
    #print("number_of_added_cells=", number_of_now_added_cells)
    global  base_colours
    #######
    new_naive_names, unused_naive_names=update_naive_names_list(unused_naive_names, number_of_now_added_cells)
    #print("new_naive_names before", new_naive_names)
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)    
    curr_frame_cell_names+=new_naive_names    
    xs=update_xs(xs,new_naive_names, num_frames,  lineage_image_size, number_of_added_new_cells)
    number_of_added_new_cells+=number_of_now_added_cells          
    lineage_images_cv2[internal_start_frame-1]=previous_lineage_image     
    label_edit.configure(text="Added cells:\n " + str(new_naive_names), bg="black")
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
  
    
    #print("dict_of_divisios before save_added=", dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}
    #print("dict_of_divisios after save_added=", dict_of_divisions)    
    cut_lineage(internal_start_frame)
   
    update_flash([button_execute])
    button_pause.configure(background = button_color)
    button_save_added_cell.grid_forget()
#####################################
def remove_died_cell():   
  button_save_removed_cell.grid(row=3, column=3, columnspan=1)
  update_flash([button_save_removed_cell])
  canvas_current.bind("<Button-1>", get_cell_IDs_manually) 
  global manual_IDs,cell_names_external, daughter_indicators
  manual_IDs, cell_names_external, daughter_indicators=[],[],[]  
###########################################
def save_removed_cell():
    label_edit.configure(text="Deleted cells:\n " + str(cell_names_external), bg="black")
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())   
    internal_start_frame=start_frame-first_frame_number+1    
    ###############################
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,\
    dict_of_divisions,number_of_added_new_cells,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,unused_naive_names,dict_of_divisions,number_of_added_new_cells,changeable_params_history= extract_changeable_params_history(outpath, internal_start_frame)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    edit_id_indicator.set(edit_id_indicator_pickle)
     
    ########################################################
    keys=list(lineage_per_frame_p4[internal_start_frame-1].keys())   
    coords_old=lineage_per_frame_p4[internal_start_frame-1][keys[0]][14]    
    print("manual_IDs=", manual_IDs)
    print("cell_names_external=", cell_names_external)
    #print(" daughter_indicators inside remove_cells", daughter_indicators)
    if "daughter-1" in daughter_indicators or "daughter-2"in daughter_indicators:
        
        dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val < start_frame}
       
    global coords
    print("curr_frame_cell_names BEFORE=", curr_frame_cell_names)
    n=len(manual_IDs)
    for i in range(n):# i=0,1,2,3,...,n manual IDs
        int_number=manual_IDs[i]
        ext_name=cell_names_external[i]# luckily, they are in the same order
        curr_frame_cell_names.remove(ext_name)
    coords=np.delete(coords_old, (manual_IDs), axis=0)
    print("curr_frame_cell_names AFTER", curr_frame_cell_names)
           
    cut_lineage(internal_start_frame)
    
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    R_remove_dead_cell.config(bg=button_color)
    update_flash([button_execute])
    button_pause.configure(background = button_color)
    button_save_removed_cell.grid_forget()
##########################################
def magnify_current_frame():

    current_frame_number= view_slider.get()
    global popup_monitor, popup_window_size
    popup_window_size=800
    popup_monitor = tk.Toplevel(master=page4, width=popup_window_size, height=popup_window_size)
    x_offset = popup_monitor.winfo_x()
    #y_offset = popup_monitor.winfo_y()
    x_offset, y_offset = popup_monitor.winfo_x() + 1000, popup_monitor.winfo_y()
    
    popup_monitor.geometry(f"+{x_offset}+{y_offset}")
    print("x_offset=", x_offset,"y_offset=", y_offset)

    ###############################
    sub1_big = tk.Frame(master=popup_monitor, width=popup_window_size, height=40, bg="green")
    sub1_big.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
     
    label_choose_channel = tk.Label(sub1_big, text="Choose channel ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow")
    label_choose_channel.grid(row=0, column=0, padx=100)
    global RR1, RR2
    RR1 = Radiobutton(sub1_big, text="Fluorescent", value="Fluor", font=all_font, variable=clicked, command=show_channel, background=button_color, activebackground="red")
    RR1.grid(row=0, column=1, pady=10, padx=10)
    RR2 = Radiobutton(sub1_big, text="Bright",background=button_color, font='TkDefaultFont 10 bold',
                 value="Bright", activebackground="red",variable=clicked, command=show_channel)
    
    RR2.grid(row=0, column=2,pady=10, padx=10)
    #################################################     
    sub2_big = tk.Frame(master=popup_monitor, width=popup_window_size, height=popup_window_size, bg="#A52A2A")
    sub2_big.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    global  canvas_popup_current
    canvas_popup_current = Canvas(sub2_big, bg='black', height=popup_window_size, width=popup_window_size)
    canvas_popup_current.pack(anchor='nw', fill='both', expand=True)
    #################################################
    sub3_big = tk.Frame(master=popup_monitor, width=popup_window_size, height=40, bg="yellow")
    sub3_big.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
     
    label_big_current_frame = tk.Label(sub3_big, text="Current frame: "+str(current_frame_number), font='TkDefaultFont 10 bold',  bg="black", fg="yellow")
    label_big_current_frame.grid(row=0, column=0, padx=300)
    
    fluor_name=full_core_fluor_name+str(current_frame_number+first_frame_number).zfill(n_digits)+"_ch00.tif"       
    image=cv2.imread(fluor_name, -1)
    global photo
    photo=turn_image_into_tkinter(image, 800)
    canvas_popup_current.create_image(0, 0, anchor=NW, image=photo)
    RR1.configure(bg="black", fg="#00FFFF")
#######################################
def show_channel():# switcvh between fluorescent and bright channels in magnified window of current frame
    global photo
    current_frame_number=view_slider.get()
    value=clicked.get()
    if value=="Fluor":
        fluor_name=full_core_fluor_name+str(current_frame_number+first_frame_number).zfill(n_digits)+"_ch00.tif"       
        image=cv2.imread(fluor_name, -1)
        RR2.configure(bg=button_color, fg="black")
        RR1.configure(bg="black", fg="#00FFFF")
    else:
        bright_name=full_core_bright_name+str(current_frame_number+first_frame_number).zfill(n_digits)+"_ch02.tif"
        image=cv2.imread(bright_name, -1)
        RR1.configure(bg=button_color, fg="black")
        RR2.configure(bg="black", fg="#00FFFF")
    photo=turn_image_into_tkinter(image, 800)
    canvas_popup_current.create_image(0, 0, anchor=NW, image=photo)
    
################### Buttons and labels Page 4####################

button_execute = Button(frame2_page4, text="3. Execute", font='TkDefaultFont 10 bold', 
               bg='#9ACD32', activebackground="red",command=lambda:[threading.Thread(target=execute).start(), update_flash([])])               
button_execute.grid(row=0, column=0, pady=20)

button_display = Button(frame2_page4, text="4. Display result", font='TkDefaultFont 10 bold', 
               bg='#9ACD32',activebackground="red", command=lambda: [display_first_frame(), update_flash([])])
button_display.grid(row=2, column=0, padx=20)

feedback_label = tk.Label(frame1_page4, text=" Welcome to STEP 3 of the pipeline! \n\nTo choose input movie you want to track, press Button 1. ",fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
feedback_label.grid(row=1, column=0,columnspan=4, sticky=W)

input_info_label = tk.Label(frame1_page4, text=my_dir, bg="black", fg="cyan")
input_info_label.grid(row=2, column=1, padx=2)

cell_info_label = tk.Label(frame1_page4, text=my_dir,fg="#00FFFF", bg="black")
cell_info_label.grid(row=2, column=2, padx=2)

cell_numbers_label = tk.Label(frame1_page4, text=my_dir,fg="#00FFFF", bg="black")
cell_numbers_label.grid(row=2, column=3, padx=2)
#progressbar = ttk.Progressbar(
    #frame9_page4, orient='horizontal', mode='determinate', length=100)
button_save_id = Button(frame3_page4, text="Save ID edits", activebackground="red",font=all_font, 
              bg=button_color, command=lambda:stop_editing_IDs())
button_save_id.grid(row=3, column=0)
button_save_id.grid_forget()

button_save_division = Button(frame3_page4, text="Save division edits",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:stop_editing_division())
button_save_division.grid(row=3, column=1, columnspan=1)
button_save_division.grid_forget()

button_save_added_cell = Button(frame3_page4, text="Save added cell",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:save_added_cell())
button_save_added_cell.grid(row=3, column=2, columnspan=1)
button_save_added_cell.grid_forget()

button_save_removed_cell = Button(frame3_page4, text="Save removed cell",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:save_removed_cell())
button_save_removed_cell.grid(row=3, column=3, columnspan=1)
button_save_removed_cell.grid_forget()

button_magnify = Button(frame8_page4, text="7. Magnify current frame",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:magnify_current_frame())
button_magnify.grid(row=1, column=5, padx=100)

global R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell
R_edit_ID = Radiobutton(frame3_page4, text="Edit IDs", value="Previous", font=all_font, variable=clicked, command=lambda:start_editing_IDs(), background=button_color, activebackground="red")
R_edit_ID.grid(row=0, column=0, pady=10, padx=10)

R_edit_division = Radiobutton(frame3_page4, text="Edit division",background=button_color, font=all_font,
                 value="Previous", activebackground="red",variable=clicked,  command=lambda:start_editing_division())
R_edit_division.grid(row=0, column=1, pady=10, padx=10)

R_add_new_cell = Radiobutton(frame3_page4, text="Add new cell", value="Previous", font=all_font, variable=clicked, command=lambda:add_new_cell(), background=button_color, activebackground="red")
R_add_new_cell.grid(row=0, column=2, pady=10, padx=10)

R_remove_dead_cell = Radiobutton(frame3_page4, text="Remove dead cell",background=button_color, font=all_font,
                 value="Current", activebackground="red",variable=clicked, command=remove_died_cell)    
R_remove_dead_cell.grid(row=0, column=3,pady=10, padx=10)
################################################

label_edit = tk.Label(frame3_page4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow", width=50, height=4)


###########################################################################
############################## PAGE-5 (STEP-4): CORRECT SEGMENTATION #######
#############################################################################
page5=pages[4]
page5.title("4. CORRECT SEGMENTATION")
page5.config(bg=bg_color)
from helpers_for_PAGE_4 import delete_contour_with_specific_colour,update_lineage_after_manual_segm_correction, load_models_p5, load_tracked_movie
from plot import paste_patch, prepare_contours,paste_benchmark_patch

from interface_functions import turn_image_into_tkinter,display_both_channels, show_2_canvases
from postprocess import create_output_movie
from extract_lineage_for_Lorenzo import create_lineage_for_Lorenzo, extract_const_movie_parameters
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
#global button_load_p5
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
    global frame_p5_size,cell_radius_p5,patch_size_p5
    #frame_p5_size=int(empty_fluors[0].shape[0])
    #############
    list_of_movie_params=extract_movie_parameters(output_dir)
    frame_p5_size,cell_radius_p5,patch_size_p5= list_of_movie_params[0],list_of_movie_params[1],list_of_movie_params[2]
    #list_of_movie_params=[frame_size, true_cell_radius.get(), patch_size,max_number_of_cells]
    #global cell_radius_p5,patch_size_p5
    
    #if frame_p5_size==256:
        #cell_radius_p5, patch_size_p5=7, 16
    #else:
        #cell_radius_p5, patch_size_p5=20, 48
    ##########################
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
l_title = tk.Label(frame1_page6, text="STEP 5: VISUALISE RESULTS",
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
from extract_lineage_for_Lorenzo import extract_lineage,extract_const_movie_parameters


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
    global pedigree, frame_size_p6  
    lineage_per_frame=extract_lineage(outpath)
    list_of_movie_params=extract_movie_parameters(outpath)
    frame_size_p6=list_of_movie_params[0]
    pedigree = create_pedigree(lineage_per_frame, outpath,frame_size_p6)# pedigree is also saved in pickle file
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

#start_flash([b_retrieve, b_create],"begin", page6, flashers)
#############################  sub3 #################
l_centr = tk.Label(frame9_page6, text="Centroid:",bg = "black", fg="yellow" , font=all_font)
l_centr.grid(row=0, column=0, pady=2)

l_area = tk.Label(frame9_page6, text="Area:", bg = "black", fg="yellow",font=all_font)
l_area.grid(row=1, column=0, pady=2)

l_perim = tk.Label(frame9_page6, text="Perimeter:", bg = "black", fg="yellow",font=all_font)
l_perim.grid(row=2, column=0, pady=2)

l_circ = tk.Label(frame9_page6, text="Circularity:", bg = "black", fg="yellow",font=all_font)
l_circ.grid(row=3, column=0,pady=(0,70))
###########################################################
############## Navigation between pages: buttons Back, Exit, Next plus buttons on title page
#########################################################################
global update_flash
def update_flash(buttons):# buttons are those which will start flashing
    global flashers
    #print("len(flashers)=", len(flashers))
    if flashers!={}:# stop flashing all previous buttons
        keys=list(flashers.keys())
        for key in keys:
            #print("key=", key)
            if isinstance(key, str)==False:
              key.config(bg=button_color)# old buttons become green again
            win.after_cancel(flashers[key])
    flashers={}# delete all previous flashesr
    
    flashers_names =[]
    if len(buttons)!=0:# it can be buttons=[]; in this case, update_flash just stops flashing all previous buttons, without switching new ones
       for i in range(len(buttons)):
          #button_name = str(buttons[i])
          button_name = buttons[i]
          
          flashers_names.append(button_name)         
       flasher_name ="additional_flasher"# need it for flash function
       flashers_names.append(flasher_name) 
       colors =['#9ACD32' for k in range(len(buttons)+1)]    
       colors_combinations =[]
       for iii in range(len(colors)):
          colors_copy =copy.deepcopy(colors)
          old =colors_copy
          old[iii]="red"
          colors_combinations.append(old)
       flashers=flash(colors_combinations, buttons,flashers_names, win, flashers)
    #print("flashers_names after=", flashers_names)
##########################################################
def combine_funcs(*funcs):    
    def inner_combined_func(*args, **kwargs): 
        for f in funcs: 
            f(*args, **kwargs)     
    return inner_combined_func 
##################################################
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: EXTRACT MOVIE FROM FOLDER", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING", "PAGE 5: CORRECT SEGMENTATION","PAGE 6: VISUALISE RESULTS" ]
initial_buttons=[[button_choose_folder],[button_select],[button_load],[button_load_p5],[b_create,b_retrieve]]
page_numbers=[page1,page2,page3,page4,page5, page6]

######################## locations of buttons Back, Exit and Next
locations=[frame3_page1,frame8_page2,frame15_page3,frame11_page4,frame8_page5,frame11_page6]
x_back,x_exit,x_next=700,750,800

             
for i in range(0,6):
    
    if i==5:
       x_back,x_exit=150,200
    location=locations[i]               
    Button(location, text="Exit",bg="orange",font=all_font, command=win.destroy).place(x=x_exit,y=0)      
    
    if i>0:
      f_back=partial(go_to_page,i)
      if i==1:
          flash_buttons=[]
      else:
          flash_buttons=initial_buttons[i-2]
      g_back=partial(update_flash,flash_buttons) 
      Button(location, text="Back",bg="orange",font=all_font, command=combine_funcs(f_back,g_back)).place(x=x_back,y=0)
            
      Button(frame2_page1, text= "GO TO STEP %s" % (i),bg=button_color,font=all_font,command=combine_funcs(f_next,g_next)).grid(row=1+i,column=0,pady=5, padx=200)
      Label(frame2_page1, text= "STEP %s: " % (i)+ page_titles[i][7:],bg="black",fg="yellow",font=all_font).grid(row=1+i,column=1,pady=5, padx=5)
    if i<5:
       f_next=partial(go_to_page,i+2)
       g_next=partial(update_flash,initial_buttons[i]) 
       Button(location, text="Next",bg="orange",font=all_font, command=combine_funcs(f_next,g_next)).place(x=x_next,y=0)      
    



win.mainloop()

