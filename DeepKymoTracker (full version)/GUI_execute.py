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
#import tifffile as tiff
#import imagecodecs
import math
import shutil

#############################################################################
win= tk.Tk()

win.geometry('%dx%d+%d+%d' % (1530, 2000, 0, 0))
ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen


#win.geometry('1530x2000')

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
#################################

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
        if ii==1:
           activate_buttons(all_buttons_page2,[button_choose_folder])
        if ii==2:
           activate_buttons(all_buttons_page3,[button_select]) 
        if ii==3:
            activate_buttons(all_buttons_page4,[button_load])
        if ii==4:
            activate_buttons(all_buttons_page5,[button_load_p5])
          
    #print("page_number exiting go_to_page=", num) 
################################################      
pages=[]
for i in range(6):
    page=tk.Toplevel(master=win)
    #page.geometry('1530x2000')
    page.geometry('%dx%d+%d+%d' % (1530, 2000, 0, 0))
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
global sorted_aphanumeric,extract_movie_name,save_images_page2,process_tif, calculate_n_digits_in_name,display_image_p2_fix_missing
from helper_functions_page2 import sorted_aphanumeric,extract_movie_name,save_images_page2,process_tif,calculate_n_digits_in_name,create_name_dictionary,display_image_p2_fix_missing
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
   all_buttons_page2.append(movies_menu)
   update_flash([movies_menu])  
   button_choose_folder.config(bg=button_color)
   activate_buttons(all_buttons_page2,[movies_menu]) 
#######################################
def display_frame_count(text_new,ii, count):# print frame count dynamically while loading
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
          #a = tiff.imread(old_name)
          #a = (old_name)
          c, n_bright_slices=process_tif(old_name)
          bright_images.append(c)
          global photo_bright
          photo_bright=turn_image_into_tkinter(c, canvas_size_p2,[])
          canvas_bright_p2.create_image(0,0,anchor=NW,image=photo_bright)
          ##############                  
          text_br="\n Brightfield channel: Slices = "+str(n_bright_slices)+",  Number of frames =   "
          br_count=display_frame_count(text_br,i_br, br_count)
          #print("br_count=", br_count)
        elif ("_w2FITC_" in filename) or ("_w3Multi600_" in filename):# process fluorescent          
          i_fl+=1
          instruct_var_p2.set("Processing fluorescent frames...")              
          fluor_names.append(filename)
          fl_name_p2.set("Original name:   "+str(filename))
          old_name=os.path.join(path,filename)
          #b = tiff.imread(old_name)
          #b = Image.open(old_name)
          b,n_fluor_slices=process_tif(old_name)
          fluor_images.append(b)
          global photo_fluor
          photo_fluor=turn_image_into_tkinter(b, canvas_size_p2,[])
          canvas_fluor_p2.create_image(0,0,anchor=NW,image=photo_fluor)
          #text_fl="\n  Number of fluorescent frames:  "
          text_fl="\n Fluorescent channel: Slices = "+str(n_fluor_slices)+",  Number of frames =   "
          fl_count=display_frame_count(text_fl,i_fl, fl_count)               
        elif ("_w3TRITC_" in filename):# process red channel
          i_red+=1
          instruct_var_p2.set("Processing red frames...")
          red_names.append(filename)
          red_name_p2.set("Original name:   "+str(filename))
          old_name=os.path.join(path,filename)         
          #r = tiff.imread(old_name)
          #r = Image.open(old_name)          
          r,n_red_slices=process_tif(old_name)         
          red_images.append(r)
          global photo_red
          photo_red=turn_image_into_tkinter(r, canvas_size_p2,[])
          canvas_red_p2.create_image(0,0,anchor=NW,image=photo_red)
          ###############################
          #text_red="\n  Number of red frames:  "
          text_red="\n          Red channel: Slices = "+str(n_red_slices)+",     Number of frames =   "
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
    frame_slider=Scale(frame6_page2,from_=1,to=max_number_of_frames,orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p2, length=300, showvalue=0)
    frame_slider.pack() 
    frame_slider.set(1)
    slide_p2("1")
    movies_menu.config(bg="black", fg="cyan")   
    instruct_var_p2.set("All frames have been processed.\nNow, you can scroll through them by using slider.\n\nAfter you are finished, press Button 3 to save the processed movie.")
    activate_buttons(all_buttons_page2,[button_save_movie])       
###############################
def slide_p2(value):# display image even when it is missing (in this case it is black)
    #print("value=", value)
    canvas_bright_p2.delete("all")
    canvas_fluor_p2.delete("all")
    canvas_red_p2.delete("all")
    image_number=int(value)    
    frame_slider.config(label="Frame "+str(value))
    ###########################################       
    br_image, old_br_name,new_br_name=display_image_p2_fix_missing(value, bright_dictionary,"ch02", n_digits,canvas_size_p2)         
    global br_tk  
    br_tk=turn_image_into_tkinter(br_image, canvas_size_p2,[])     
    canvas_bright_p2.create_image(0,0, anchor=NW, image=br_tk)   
    br_name_p2.set("Original name:   "+old_br_name+"\nNew name:   "+new_br_name)    
    ################################    
    fl_image, old_fl_name, new_fl_name=display_image_p2_fix_missing( value, fluor_dictionary,"ch00", n_digits,canvas_size_p2)     
    global fl_tk
    fl_tk=turn_image_into_tkinter(fl_image, canvas_size_p2,[])       
    canvas_fluor_p2.create_image(0,0, anchor=NW, image=fl_tk)    
    fl_name_p2.set("Original name:   "+old_fl_name+"\nNew name:   "+new_fl_name)    
    ###############################################
    red_image, old_red_name, new_red_name=display_image_p2_fix_missing(value, red_dictionary,"ch01", n_digits,canvas_size_p2)          
    global red_tk  
    red_tk=turn_image_into_tkinter(red_image, canvas_size_p2,[])     
    canvas_red_p2.create_image(0,0, anchor=NW, image=red_tk)                   
    red_name_p2.set("Original name:   "+old_red_name+"\nNew name:   "+new_red_name)
############################################################
l_page_name=tk.Label(frame1_page2,text= "STEP 1: EXTRACT MOVIE FROM FOLDER", bg="yellow", fg="red", font=("Times", "24")).pack()
button_choose_folder=tk.Button(frame3_page2,text="1. Choose folder with movies",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=lambda: explore_folder())
button_choose_folder.grid(row=0,column=0, padx=100,pady=20)
button_save_movie=tk.Button(frame11_page2,text="3. Save processed movie",bg='#9ACD32',activebackground="red",font=all_font , command=lambda: [save_images_page2(movie_name,feedback_var_p2,bright_names,fluor_names,red_names, bright_images, fluor_images, red_images, instruct_var_p2),\
        update_flash([]) ])
button_save_movie.pack()
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
###################### 
global all_buttons_page2
all_buttons_page2=[button_choose_folder,button_save_movie]
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
global   load_image_names,cut_all, draw_circles_p3, update_feedback_text,cut_well_in_manual_shift
from interface_functions import   cut_well_from_image, calculate_angle, cut_all,cut_well_in_manual_shift
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
    global n_digits
    base =os.path.basename(fluor_names_sorted[-1])
    name =os.path.splitext(base)[0]
    index_t =name.find("_t")
    index_ch=name.find("_ch")
    n_digits = index_ch-index_t-2
             
    global list_of_red_frame_numbers
    list_of_red_frame_numbers =extract_red_frame_numbers(red_names_sorted)
    #print("list_of_red_frame_numbers=", list_of_red_frame_numbers) 
    
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
    photo_clicked=turn_image_into_tkinter(clicked_bright, canvas_size_p3,[])
    
    canvas_left.create_image(0,0, anchor=NW, image=photo_clicked)
    canvas_left.bind("<Button-1>",measure_intensities)
    instruct_var_p3.set("Now, click on the dark border of the well(s) 2-3 times to measure intensities.\nThen click Button 2."
                    "\nThe thresholded image will appear in the window to the right.")    
    update_flash([])
    activate_buttons(all_buttons_page3,[])
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
        activate_buttons(all_buttons_page3,[button_threshold]) 
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
    thr_image=turn_image_into_tkinter(thresh, canvas_size_p3,[])    
    canvas_mid.create_image(0,0, anchor=NW, image=thr_image)
    threshold_slider.config(variable=low,label="Threshold = "+str(low))    
    instruct_var_p3.set("The borders of wells should become SOLID white line, WITHOUT INTERRUPTIONS."
                       "\nImprove thresholded image if necessary\nby sliding the bar below to change threshold."
                       "\nFinally, click on the well of interest.")
    update_flash([threshold_slider])
    activate_buttons(all_buttons_page3,[threshold_slider])    
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
    thr_image=turn_image_into_tkinter(thresh, canvas_size_p3,[])    
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
    
    #print("first_box=", first_box)    
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
    closing_2=turn_image_into_tkinter(closing_1, canvas_size_p3,[])   
    canvas_right.create_image(0,0, anchor=NW, image=closing_2)    
    ######## here it draws red rect in fluorescent image of canvas_left
    im_copy=clicked_bright.copy()# 
    global photo_im_red,M_first,rows,cols
    im_red=cv2.cvtColor(im_copy,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(im_red,[first_box],0,(0,0,255),5)    
    photo_im_red=turn_image_into_tkinter(im_red, canvas_size_p3,[])   
    canvas_left.create_image(0,0, anchor=NW, image=photo_im_red)    
    rows,cols = clicked_bright.shape 
    M_first = cv2.getRotationMatrix2D((int(round(cols/2)),int(round(rows/2))),angle,1)   
    
    instruct_var_p3.set("Check that the well has been detected correctly: a red frame should appear around the well.\nIf it is not correct go back to sliding bar."
                       "\nFinally, push Button 3 to check the result.")
    update_flash([button_cut_well, threshold_slider])
    activate_buttons(all_buttons_page3,[button_cut_well, threshold_slider ])          
######################################################
def cut_first_well():# cut well in the first image and display it in canvas_mid 
 instruct_var_p3.set("It is important to manually correct shift in Frame 1. Push Button 4 and drag the image with mouse to eliminate the shift."
                       "\nFinally, push Button 5 to check the results.")
 global canvas_mid 
 canvas_mid.delete("all")
 
#################### draw temp image (binary) to rotate it and find rect_new
 #print("first box=", first_box)
 temp=np.zeros(clicked_bright.shape, np.uint8)
 cv2.drawContours(temp,[first_box],0,255,-1)
 dst = cv2.warpAffine(temp,M_first,(cols,rows))
####################  4. calculate its borders   
 _,contours_new, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt_new=contours_new[0]
 rect_new = cv2.minAreaRect(cnt_new)             
 box_final = cv2.boxPoints(rect_new)# horisontal well    
 box_final = np.int0(np.round(box_final))
 #print("first box_final=", box_final)
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
 final_s=turn_image_into_tkinter(cut_bright, canvas_size_p3,[]) 
 finalImage_small=canvas_mid.create_image(0,0, anchor=NW, image=final_s)
 #########################
 
 global delta_x, delta_y
 delta_x, delta_y=0,0
 canvas_mid.unbind("<Button-1>")
 update_flash([button_first_shift_edit])
 activate_buttons(all_buttons_page3,[button_first_shift_edit ])   
######################################################
def drag_image(event, canvas,imageFinal):# drag image with mouse
    global x_img,y_img, points, x_last,y_last,dx,dy, delta_x,delta_y    
    x, y = event.x, event.y   
    points.append([x,y])
    if len(points)==1:
      print("TOUCHED THE MOUSE BUTTON")             
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

######################################################
def edit_first_frame_shift():  
    global popup_mid, canvas_popup_mid
    
    popup_mid = tk.Toplevel(master=page3,  bg=bg_color)
    popup_mid.geometry('%dx%d+%d+%d' % (popup_size_p3, popup_size_p3+50, 0, 0))
    frame1 = tk.Frame(master=popup_mid, width=popup_size_p3, height=popup_size_p3)
    frame1.pack()
    frame2 = tk.Frame(master=popup_mid, width=popup_size_p3, height=50)
    frame2.pack()
    canvas_popup_mid = Canvas(frame1, height=popup_size_p3, width=popup_size_p3, bg=bg_color)
    canvas_popup_mid.pack(anchor='nw', fill='both', expand=True)
    def close_and_flash():
        update_flash([button_bright])
        activate_buttons(all_buttons_page3,[button_bright])
        popup_mid.destroy()
    global button_close
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=close_and_flash)
    button_close.pack()
   
    global x_img,y_img, points, x_last,y_last,dx,dy, x0,y0, br_image, x1,y1, delta_x,delta_y
    x0,y0=x_min_first, y_min_first# x0,y0- image coord system; x1,y1 - popup canvas coord system
    x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))
   
    x_img,y_img, x_last,y_last,dx,dy=  0,0,x1,y1,0,0
    delta_x, delta_y=int(round((x_last-x1)*image_size_p3[0]/popup_image_size_p3)),int(round((y_last-y1)*image_size_p3[1]/popup_image_size_p3))
    #can_delta_x,can_delta_y=x_last-x1,y_last-y1    
    points=[]
    global new_name
    head, tail=os.path.split(my_path)
    new_name=os.path.join(my_destin,tail)
    ###################################
    final_bright, rot_bright=cut_well_in_manual_shift(clicked_bright,x0+delta_x,y0+delta_y,well_size, M_first, cols, rows)    
    br_image=rot_bright   
    global image1,imageFinal   
    canvas_popup_mid.delete("all")
    image1=turn_image_into_tkinter(br_image, popup_image_size_p3,[])
    imageFinal_big = canvas_popup_mid.create_image(-x1, -y1, image = image1,anchor='nw')
    ##################################################   
    canvas_popup_mid.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_mid, imageFinal_big))   
    canvas_popup_mid.bind("<ButtonRelease>", lambda event: cut_and_save_patch(event,canvas_popup_mid, canvas_mid))    
    update_flash([button_close])    
##################################################

def cut_and_save_patch(event, canvas_big, canvas_small):
    print("RELEASED MOUSE")
    global points, br_image, new_name,x_last, y_last #, x0,y0
    
    xx,yy=int(round(x_last*image_size_p3[0]/popup_image_size_p3)),int(round(y_last*image_size_p3[1]/popup_image_size_p3))    
    patch=br_image[yy:yy+well_size, xx:xx+well_size]
    patch_1=patch.copy()       
    cv2.imwrite(new_name, patch)# save in INPUT folder
    global tk_patch, image2 
    tk_patch=turn_image_into_tkinter(patch, popup_size_p3,[])      
    canvas_big.delete("all")
    canvas_big.create_image(0,0, image = tk_patch,anchor='nw')

    image2=turn_image_into_tkinter(patch_1, canvas_size_p3,[])    
    canvas_small.create_image(0, 0, image = image2,anchor='nw')
    points=[]
##################################

#####################  
def edit_current_frame_shift():# Button 6a. Edit well shift in current frame"
    button_fluor.config(bg="red")
    frame_number=frame_pop_slider.get()
    print("current frame_number=", frame_number)
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
    image1=turn_image_into_tkinter(br_image, size,[])      
    imageFinal= canvas_popup_right.create_image(-x1, -y1, image = image1,anchor='nw')
    ##################################################
    #canvas_popup_right.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_right, imageFinal_big))
    #canvas_popup_right.bind("<ButtonRelease>", lambda event: cut_and_save_current(event,canvas_popup_right, canvas_right))
    button_fluor.config(bg=bg_color)
##########################################
#######################
def start_editing_frames():#   
    global popup_right, canvas_popup_right, l_popup_canvas    
    popup_right = tk.Toplevel(master=page3,  bg=bg_color)
    popup_right.geometry('%dx%d+%d+%d' % (popup_size_p3, popup_size_p3+210, 0, 0))
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
        activate_buttons(all_buttons_page3,[button_fluor])        
        popup_right.destroy()
        popup_right=None
       
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command= destroy_popup)
    button_close.pack()
    
    #first_tk_pop=turn_image_into_tkinter(first, popup_size_p3,[])
    #canvas_popup_right.create_image(0,0, anchor=NW, image=first_tk_pop)
    l_popup_canvas.config(text=os.path.basename(bright_names_sorted[0]))
    update_flash([button_current_edit])
    #############################################
    points=[]
    global image1, new_name, imageFinal
    new_name=new_br_names[frame_slider.get()-1]
    br_image= rotated_images[frame_slider.get()-1]    
    size=int(round(image_size_p3[0]*popup_size_p3/well_size))   
    image1=turn_image_into_tkinter(br_image, size,[])      
    imageFinal = canvas_popup_right.create_image(-x1, -y1, image = image1,anchor='nw')
    canvas_popup_right.bind('<B1-Motion>', lambda event: drag_image( event,canvas_popup_right, imageFinal))
    canvas_popup_right.bind("<ButtonRelease>", lambda event: cut_and_save_current(event,canvas_popup_right, canvas_right))           
 ###########################################################
######## "<ButtonRelease>"
def cut_and_save_current(event, canvas_big, canvas_small):
    print("INSIDE CUT_AND_SAVE_CURRENT")
    # cut and save bright well in INPUT folder
    global points, br_image, new_name, x0,y0, x_last, y_last
    xx,yy=int(round(x_last*image_size_p3[0]/popup_image_size_p3)),int(round(y_last*image_size_p3[1]/popup_image_size_p3))    
    patch=br_image[yy:yy+well_size, xx:xx+well_size]
    cv2.imwrite(new_name, patch)# save in INPUT folder
   
    ###############################################
    # modify rotation_matrices for current frame    
    new_x_min, new_y_min=x_last,y_last
    current_frame_number=frame_pop_slider.get()
    print("current_frame_number=", current_frame_number)
    item=rotation_matrices[current_frame_number-1]
    #print("item=", item)
    M,x_min,y_min,row,cols, rotation_indicator=item[0],item[1],item[2],item[3],item[4], item[5]
    new_item=(M, xx,yy,rows,cols, rotation_indicator)
    #print("new_item=", new_item)
    rotation_matrices[current_frame_number-1]=new_item
    #######################################
    #  display modified frame in both canvases
    global tk_patch, image2 
    tk_patch=turn_image_into_tkinter(patch, popup_size_p3,[])      
    canvas_big.delete("all")
    canvas_big.create_image(0,0, image = tk_patch,anchor='nw')
    patch_1=patch.copy()
    image2=turn_image_into_tkinter(patch_1, canvas_size_p3,[])    
    canvas_small.create_image(0, 0, image = image2,anchor='nw')
    points=[] 
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
    final_bright_tk=turn_image_into_tkinter(final_bright, canvas_size_p3,[])
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
        first_tk=turn_image_into_tkinter(first, canvas_size_p3,[])
  global frame_slider    
  frame_slider=Scale(frame11_page3,from_=1,to=len(bright_names_sorted),orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(1), command=slide_p3, length=250, showvalue=0)
  frame_slider.pack()
  frame_slider.set(1)
  #######################
  global  bright_dictionary_p2
  
  bright_dictionary_p2=create_name_dictionary_p4(new_br_names)
  
  threshold_slider.config(bg=label_color) 
  instruct_var_p3.set("Scroll through frames to ensure that the well fits completely into each frame.\nIf you want to corect shift in some frames, push Button 6 to launch editing window."
                 "\nOtherwise, push Button 7 to apply to ALL FLUORESCENT images")
  button_bright.config(bg=button_color)
  update_flash([button_shift_edit])
  activate_buttons(all_buttons_page3,[button_shift_edit ])          
  canvas_right.delete("all")
  canvas_right.create_image(0,0, anchor=NW, image=first_tk)
  l_right_canvas.config(text=os.path.basename(bright_names_sorted[0]))           
#########################
global frame_pop_slider
frame_pop_slider=None
######################### scroll through all images
def slide_p3(value): 
       image_number = int(value)# without 0 digits on slider
       frame_slider.config(label="Frame "+str(value))
       image_number_zfill=str(value).zfill(n_digits)       
       ##############################################         
       canvas_right.delete("all")           
       ###########################################
       global br_final
       ####################################
       br_path=new_br_names[image_number-1]
       br_final, br_name=display_image_p4_fix_missing(image_number_zfill,bright_dictionary_p2, canvas_size_p3)                           
       canvas_right.create_image(0,0, anchor=NW, image=br_final)      
       l_right_canvas.config(text=br_name)
       ##############################################
       if new_fl_names:
          canvas_mid.delete("all")
          global fl_final
          fl_path=new_fl_names[image_number-1]          
          fl_final, fl_name=display_image_p4_fix_missing(image_number_zfill,fluor_dictionary_p2, canvas_size_p3)                           
          canvas_mid.create_image(0,0, anchor=NW, image=fl_final)      
          l_mid_canvas.config(text=fl_name)
       ##############################################
       if new_red_names:
          canvas_left.delete("all")
          global red_final
          red_path=new_red_names[image_number-1]         
          red_final, red_name=display_image_p4_fix_missing(image_number_zfill,red_dictionary_p2, canvas_size_p3)                           
          canvas_left.create_image(0,0, anchor=NW, image=red_final)      
          l_left_canvas.config(text=red_name)
       if popup_right:
          canvas_popup_right.delete("all") 
          item=rotation_matrices[image_number-1]
          x_min,y_min=item[1],item[2]       
          global x_img,y_img, points, x_last,y_last,dx,dy, rotated_images, x0,y0, br_image
          x0,y0=x_min, y_min
          x1,y1=int(round(x0*popup_size_p3/well_size)),int(round(y0*popup_size_p3/well_size))   
          x_img,y_img, x_last,y_last,dx,dy=  0,0,x1,y1,0,0
          points=[]             
          global image1, new_name, imageFinal
          new_name=new_br_names[image_number-1]
          br_image= rotated_images[image_number-1]    
          size=int(round(image_size_p3[0]*popup_size_p3/well_size))   
          image1=turn_image_into_tkinter(br_image, size,[])      
          imageFinal = canvas_popup_right.create_image(-x1, -y1, image = image1,anchor='nw')
          ####################################
          #br_image_copy=cv2.imread(br_path,0)
          frame_pop_slider.config(label="Frame "+str(value))
          #global br_popup  
          #br_popup=turn_image_into_tkinter(br_image_copy, popup_size_p3,[])     
          #canvas_popup_right.create_image(0,0, anchor=NW, image=br_popup)
          l_popup_canvas.config(text=os.path.basename(bright_names_sorted[image_number-1]))
##################### activate editing frame shift for current frame in canvas_right
  
def cut_fluor_wells():#cut fluor and red wells
 instruct_var_p3.set("Processing fluorescent and red frames....") 
 update_flash([])
 
 button_fluor.config(bg="red")
 progressbar_fluor = ttk.Progressbar(frame10_page3, orient='horizontal',mode='determinate',length=280)
 progressbar_fluor.pack()
 
 #list_of_red_frame_numbers =extract_red_frame_numbers(red_names_sorted)
 #print("list_of_red_frame_numbers=", list_of_red_frame_numbers)    
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
    final_fluor_tk=turn_image_into_tkinter(final_fluor, canvas_size_p3,[])
    canvas_mid.delete("all")
    canvas_mid.create_image(0,0, anchor=NW, image=final_fluor_tk)
    l_mid_canvas.config(text=os.path.basename(fluor_name))
    ###############################
    if k+1 in list_of_red_frame_numbers:
      index=list_of_red_frame_numbers.index(k+1)
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
    final_red_tk=turn_image_into_tkinter(final_red, canvas_size_p3,[])
    canvas_left.delete("all")
    canvas_left.create_image(0,0, anchor=NW, image=final_red_tk)
    l_left_canvas.config(text=red_text)
    #print("new_red_names=", new_red_names)
 #######################
    
 global  red_dictionary_p2,fluor_dictionary_p2
 red_dictionary_p2=create_name_dictionary_p4( new_red_names)
 fluor_dictionary_p2=create_name_dictionary_p4( new_fl_names)
      
 canvas_left.delete("all")
 canvas_mid.delete("all")
 canvas_right.delete("all")
 frame_slider.set(1)
 slide_p3(1)
 feedback_dict["dest"]=my_destin# print destination folder in feedback panel
 feedback_text=update_feedback_text(feedback_dict)
 feedback_var_p3.set(feedback_text)
 instruct_var_p3.set("Finished!\nThe input movie has been created and stored in folder\n "+str(my_destin)+
                 "\nNow, you are ready to proceed to STEP 3 of the pipeline.")               
 button_fluor.config(bg=button_color)
 activate_buttons(all_buttons_page3,[]) 
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
button_cut_well=tk.Button(frame4_page3,text="3. Cut well",bg=button_color,activebackground="red",font=all_font, command=lambda: cut_first_well())
button_cut_well.grid(row=1, column=0,padx=10) 

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
global all_buttons_page3
all_buttons_page3=[button_select,button_threshold,button_cut_well,
        button_first_shift_edit,button_bright,button_shift_edit, threshold_slider, button_fluor]
###########################################################################
######### PAGE 4 :STEP-3:  EXECUTE AND CORRECT TRACKING ##############################
###############################################################################
page4=pages[3]
page4.config(bg=bg_color)
global canvas_size_p4
canvas_size_p4 =382
 

frame1_page4 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame1_page4.grid(row=0, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

frame2_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg=bg_color)
frame2_page4.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg=bg_color)
frame3_page4.grid(row=1, column=1, rowspan=1, columnspan=5, sticky=W+E+N+S)

frame5_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame5_page4.grid(row=2, column=0, rowspan=1, columnspan=1)

frame6_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg="blue")
frame6_page4.grid(row=2, column=1, rowspan=1, columnspan=1)

frame7_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame7_page4.grid(row=2, column=2, rowspan=1, columnspan=1)

frame8_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame8_page4.grid(row=3, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame9_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg=bg_color)
frame9_page4.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame10_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg=bg_color)
frame10_page4.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame12_page4 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame12_page4.grid(row=4, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)


frame11_page4 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame11_page4.grid(row=5, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

canvas_previous = Canvas(frame5_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_previous.pack(anchor='nw', fill='both', expand=True)
canvas_current = Canvas(frame6_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_current.pack(anchor='nw', fill='both', expand=True)
global canvas_lineage_exec
canvas_lineage_exec = Canvas(frame7_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
#canvas_lineage.grid(row=0,column=0)
#canvas_lineage_exec.pack(anchor='nw', fill='both', expand=True)
canvas_lineage_exec.pack(anchor='nw')
#canvas_lineage_exec.config(width=canvas_size_p4+100)
########################### These labels do not change

title_label = tk.Label(frame1_page4, text="STEP 3: EXECUTE AND CORRECT TRACKING",
              bg="yellow", fg="red", font=("Times", "24")).pack()
#title_label.grid(row=0, column=1, padx=2, sticky="n")

label_previous = tk.Label(frame8_page4, text="Previous Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_previous.grid(row=0, column=5, padx=100)

label_current = tk.Label(frame9_page4, text="Current Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
#label_current.grid(row=0, column=0,padx=100)
label_current.pack()


label_curr_frame_name = tk.Label(frame9_page4, text="           ", bg="black", fg="cyan", font='TkDefaultFont 10 bold' )
#label_curr_frame_name.grid(row=1, column=0,padx=100)
label_curr_frame_name.pack()

label_lineage = tk.Label(frame10_page4, text="Lineage", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_lineage.grid(row=0, column=0, padx=100)

###################################################
zero_image = Image.new('RGB', (canvas_size_p4, canvas_size_p4))
zero_image = ImageTk.PhotoImage(zero_image)
global lineage_images_tk, output_images, lineage_images_cv2, output_names
lineage_images_tk, output_images, lineage_images_cv2, output_names=[], [zero_image],[], ["             "]

################################
global popup_monitor
popup_monitor=None
global popup_window_size
popup_window_size=800
#####################################
global fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names, red_images, red_names
fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names, red_images, red_names=None,None,None, None, None,None, None   
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
###############################################
global fully_tracked_indicator
fully_tracked_indicator="no"
global update_feedback_text_p4
from preprocess import update_feedback_text_p4
global instruct_var_p4,feedback_var_p4,feedback_dict_p4
instruct_var_p4,feedback_var_p4=StringVar(), StringVar()
feedback_dict_p4={"movie name":" ","frame size":" ","cell diameter":" ","patch size":" ","number in frame 1":" ","max number":" ", "fluor frames":" ","bright frames":" ","red frames":" ","number of processed":" "}
feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
feedback_var_p4.set(feedback_text_p4)

feedback_label_p4=tk.Label(frame1_page4,textvariable=feedback_var_p4 ,bg="black", fg=result_color, font=all_font, height=5)
feedback_label_p4.pack(fill=BOTH)   

instruct_var_p4.set(" Step 3 allows you to track and manually correct tracking errors if necessary. \n\nTo choose raw movie , press Button 1."
                    "\nThen, navigate to your INPUT_MOVIE and click on it. ")
##################################
global manual_IDs,manual_centroids,mother_name,  daughter_indicators 
manual_IDs,  manual_centroids, mother_name, daughter_indicators=[], [], None, []
#################
def activate_buttons(all_buttons_list,active_buttons_list):
    for button in all_buttons_list:
        if button in active_buttons_list:
            button.config(state=NORMAL)                        
        else:
            button.config(state=DISABLED)
#######################
def load_helper_functions():
    os.chdir(software_folder)
    global predict_first_frame, create_output_folders,\
        detect_division, update_dictionary_after_division, check_division_frame_number, predict_tracking, predict_tracking_general, backup_track, predict_first_frame, segment_and_clean,\
         plot_frame, create_first_color_dictionary,\
        create_pedigree, create_output_movie, load_weights, extract_lineage,\
        create_lineage_image_one_frame, extract_file_name, load_clip, update_lineage,force_manual_IDs,create_lineage_for_Lorenzo,sorted_aphanumeric,update_color_dictionary,update_naive_names_list,update_xs_after_new_cells,\
        load_full_raw_movie,create_models,extract_output_images,create_name_dictionary_p4,display_image_p4_fix_missing,removeLeadingZeros,rename_file, show_3_canvases,update_changeable_params_history,extract_changeable_params_history,update_xs_after_division

    from preprocess import create_output_folders, load_weights, extract_file_name,load_clip,load_full_raw_movie,create_models,removeLeadingZeros
    

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_division_frame_number)

    from functions import (predict_tracking_general,  backup_track, predict_first_frame, segment_and_clean,
                           hungarian, predict_tracking,force_manual_IDs)
    
    from plot import plot_frame, create_first_color_dictionary,update_color_dictionary,update_naive_names_list,update_xs_after_new_cells, rename_file,update_xs_after_division
    from postprocess import   create_output_movie,  create_lineage_image_one_frame,sorted_aphanumeric
    from keras.models import model_from_json
    from print_excel import print_excel_files,extract_lineage,update_lineage, extract_const_movie_parameters,update_changeable_params_history,extract_changeable_params_history
    from interface_functions import extract_output_images,create_name_dictionary_p4,display_image_p4_fix_missing, show_3_canvases
    from keras.optimizers import Adam
###########################################    
global models, models_directory,tracker,segmentor,refiner
from helpers_for_PAGE_4 import load_models_p5

models_directory = os.path.join(software_folder, "TRAINED MODELS")
models,tracker,segmentor,refiner=[], None, None, None

load_helper_functions()
models,models_directory=create_models(software_folder)

if segmentor==None and refiner==None:      
        software_folder = os.getcwd() 
        segmentor, refiner= load_models_p5(software_folder)
        #dialog_label_5.config(text="Loaded models")
#######################


############ click Button 1 and explore if OUTPUT exists or not
############### If yes, ask whether user wants to continue or start all over again
################ by creating a popup option menu
def initiate_tracking_page():
     button_load.configure(background = 'red')
     global my_dir, input_movie_folder
     my_dir = filedialog.askdirectory()# input movie folder
     #input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\n")
     #################################
     feedback_dict_p4["movie name"]=str(my_dir)     
     input_movie_folder = os.path.basename(my_dir)
     global outpath
     #load_helper_functions()
     outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
     global init_image,last_image, frame_size, num_frames,  all_names_fluor
     all_names_fluor=[]
     number_of_brights, number_of_reds=0,0
     #output_names=[None]     
     for filename in sorted_aphanumeric(os.listdir(my_dir)):   
        if filename.endswith("ch00.tif"):
            instruct_var_p4.set("Loading input movie ...")                           
            full_name_fluor = os.path.join(my_dir, filename)
            all_names_fluor.append(full_name_fluor)
        if filename.endswith("ch02.tif"):
             number_of_brights+=1
        if filename.endswith("ch01.tif"):
             number_of_reds+=1
      
     #print("len(output_names) before=", len(output_names))
     feedback_dict_p4["fluor frames"]=str(len(all_names_fluor))
     feedback_dict_p4["bright frames"]=str( number_of_brights)
     feedback_dict_p4["red frames"]=str( number_of_reds)
     global full_core_fluor_name, n_digits, first_frame_number, start_empty_file_name, frame_size
     full_core_fluor_name, n_digits, first_frame_number= extract_file_name(all_names_fluor[0])
     
     init_image=cv2.imread(all_names_fluor[0],0)
     last_image=cv2.imread(all_names_fluor[-1 ],0)
     frame_size=init_image[0].shape[0]
     num_frames=len(all_names_fluor)
     global lin_image_widths
     lin_image_widths=[num_frames]
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
          output_fluor_folder=os.path.join(outpath,"FLUORESCENT_MOVIE_RESULTS")
          if  len(os.listdir( output_fluor_folder))==0:# 2. if OUTPUT is empty
              print("OUTPUT exists but empty")
              shutil.rmtree(outpath)# delete OUPUT if it exists
              os.mkdir(outpath)# create OUTPUT folder and start tracking from Frame 1
              del all_names_fluor              
              prepare_for_first_go()
          else:# 2. if OUTPUT is not empty
            print("OUTPUT exists but non-empty")
            #output_fluor_folder= os.path.join(outpath, "FLUORESCENT_MOVIE_RESULTS")
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
                  global output_names_fluor
                  output_names_fluor=[]
                  for filename in sorted_aphanumeric(os.listdir(output_fluor_folder)):   
                    if filename.endswith("ch00.tif"):
                     #feedback_label.configure(text="Loading input movie ...")                      
                     output_name_fluor = os.path.join(output_fluor_folder, filename)
                     output_names_fluor.append(output_name_fluor)
                  feedback_dict_p4["number of processed"]=str(len(output_names_fluor))
                 
                  print("len(output_names_fluor)=",len(output_names_fluor))
                  ####################
                  ####################
                  from preprocess import create_output_folders
                  global out_folders
                  out_folders = create_output_folders(outpath)# creates names only  
    
                  global true_cell_radius, patch_size,basic_naive_names,  xs, full_core_bright_name,curr_frame_cell_names,flag,edit_id_indicator, \
                  base_colours,colour_counter,colour_dictionary,basic_naive_names, contrast_value, dict_of_divisions,naive_names_counter,number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta
                  true_cell_radius, edit_id_indicator=IntVar(),StringVar()
   
                  (frame_size, true_cell_radius_pickle, patch_size,basic_naive_names,
                  num_frames, full_core_fluor_name, n_digits, full_core_bright_name, first_frame_number,
                  base_colours, contrast_value, number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta)= extract_const_movie_parameters(outpath)
                  
    
                  true_cell_radius.set(true_cell_radius_pickle)
                  ###################################

                   ########################################################
                  #cell_info_label.config(text= "FRAME SIZE: "+str(frame_size)+"x"+str(frame_size)+
                           #"\nCELL DIAMETER:= "+str(2*true_cell_radius.get())+"\nPATCH SIZE= "+str(2*patch_size)+" x "+str(2*patch_size))
                  #############################################
                  #################################
                  feedback_dict_p4["cell diameter"]=str(2*true_cell_radius.get())
                  feedback_dict_p4["frame size"]=str(frame_size)+"x"+str(frame_size)
                  feedback_dict_p4["patch size"]=str(2*patch_size)+" x "+str(2*patch_size)
                  feedback_dict_p4["initial number of cells"]=str(number_in_first_frame)
                  #feedback_dict_p4["max number"]=str(basic_naive_names)
                  
                  feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
                  feedback_var_p4.set(feedback_text_p4)
     ###################################
                 
                  
                  lineage_per_frame = extract_lineage(outpath)
                  last_frame_cell_dict=lineage_per_frame[-1]
                  n_cells=len(last_frame_cell_dict)    
                  internal_cell_names=list(last_frame_cell_dict.keys())
    
                  global coords, start_frame
                  start_frame=last_frame_cell_dict[internal_cell_names[0]][12]+1    
                  coords=last_frame_cell_dict[internal_cell_names[0]][14]
                  ##############################
                  global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
                  dict_of_divisions,naive_names_counter, changable_params_history
                  xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,naive_names_counter,lin_image_widths,changable_params_history= extract_changeable_params_history(outpath, -1)
                  edit_id_indicator.set(edit_id_indicator_pickle)
                                    
                 
                  global output_images,lineage_images_tk, output_names,lineage_images_cv2    
                  output_images,lineage_images_tk, output_names,lineage_images_cv2=extract_output_images(out_folders[1],os.path.join(out_folders[4],"LINEAGE_IMAGES"),canvas_size_p4, output_images,output_names, lin_image_widths)
             
                  global  previous_lineage_image, lineage_image_width
                  previous_lineage_image=lineage_images_cv2[-1]     
                  #canvas_lineage_width=previous_lineage_image.shape[1]*canvas_size_p4/previous_lineage_image.shape[0]
                  canvas_lineage_width=canvas_size_p4+90*(len(lin_image_widths)-1)   
                  print("canvas_lineage_width=", canvas_lineage_width)
                  canvas_lineage_exec.config(width=canvas_lineage_width)
                  #######################################################
                  #################################################
                  if len(all_names_fluor)>len(output_names_fluor):
                     print("partly tracked")
                     instruct_var_p4.set("The movie has been partially tracked. \nPress OK to view the processed frames.")
                     button_load.configure(background = button_color)
                     global popup_partly_tracked, button_retrieve
                     #########################
                     popup_partly_tracked = tk.Toplevel(master=page4, bg=label_color)
                     w,h = 400,150                      
                     x,y = (ws/2) - (w/2),(hs/2) - (h/2)                     
                     popup_partly_tracked.geometry('%dx%d+%d+%d' % (w, h, x, y))
                     label_popup = tk.Label(popup_partly_tracked, text="The movie has been partially tracked. \nPress OK to view the processed frames.",width=400, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
                     label_popup.pack()                     
                     button_retrieve = Button(popup_partly_tracked, text="OK",
                     bg=button_color,font='TkDefaultFont 14 bold', command=lambda:[retrieve_unfinished_movie(), update_flash([button_execute]), popup_partly_tracked.destroy() ])
                     button_retrieve.pack()
                     update_flash([ button_retrieve])
                     ########################################
        
                  else:
                     print("fully tracked")
                     button_load.configure(background = button_color)
                     #button_execute.configure(bg=button_color)
                     global fully_tracked_indicator
                     fully_tracked_indicator="yes"
                     instruct_var_p4.set("The movie has been fully tracked. \nPress OK to view the processed frames.")
                     #############################################################
                     def close_fully_popup():                     
                                         
                      display_first_frame()
                      instruct_var_p4.set("The movie has been fully tracked.\nUse slide bar to check results."\
                                          "\nIf you need to edit tracking errors, stop the slide bar on the frame of interest and choose one of the options under Edit tools."\
                                              "\nIf you are happy with the results,press Exit or Next to proceed to segmentation correction.")
                     ################################################
                     global popup_fully_tracked, button_ok
                     popup_fully_tracked = tk.Toplevel(master=page4, bg=label_color)
                     w,h = 400,150                      
                     x,y = (ws/2) - (w/2),(hs/2) - (h/2)                     
                     popup_fully_tracked.geometry('%dx%d+%d+%d' % (w, h, x, y))
                     label_popup = tk.Label(popup_fully_tracked, text="The movie has been fully tracked. \nPress OK to view the processed frames.",width=400, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
                     label_popup.pack()                                          
                     button_ok = Button(popup_fully_tracked, text=" OK",font='TkDefaultFont 14 bold', bg=button_color, command=lambda:[retrieve_unfinished_movie(), close_fully_popup(),  popup_fully_tracked.destroy() ])
                    
                     button_ok.pack()
                     update_flash([button_ok])
            else:# 3. if RESULT_FLUOR does not exist
                 print("RESULT_FLUORESCENT does not exist")
                 shutil.rmtree(outpath)# delete OUPUT if it exists
                 os.mkdir(outpath)# create OUTPUT folder and start tracking from Frame 1
                 prepare_for_first_go()

#############################################################
 
def prepare_for_first_go():
    feedback_dict_p4["number of processed"]="0"
    instruct_var_p4.set("Input mivie is loaded. Setting up parameters of the movie in progress...")
    ##########
    
    #########
    global popup_first_preview, canvas_popup_fluor_p4,canvas_popup_bright_p4,canvas_popup_red_p4
    popup_first_preview = tk.Toplevel(master=page4, bg=bg_color)
    popup_first_preview.title("PAGE 4 POPUP WINDOW: SETTING CONSTANT PARAMETERS OF INPUT MOVIE")                 
    popup_first_preview.geometry('%dx%d+%d+%d' % (1530, 2000-160, 0, 160))
    #popup_first_preview = tk.Toplevel(master=page4, width=1528, height=50, bg="blue")
    
    frame1 = tk.Frame(master=popup_first_preview , width=1528, height=50, bg=bg_color)
    frame1.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame2 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame3 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame3.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame4 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame4.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame5 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame5.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame6 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame6.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame7 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
    frame7.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame8 = tk.Frame(master=popup_first_preview , width=1528, height=50,bg=bg_color)
    frame8.grid(row=3, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame9 = tk.Frame(master=popup_first_preview , width=1528, height=50,bg=bg_color)
    frame9.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    ###########################################
    #l_feedback=tk.Label(frame1,text= "Input movie: ", bg="black", fg="cyan", font=("Times", "12"))
    #l_feedback.pack()
    
    global  canvas_left_pop, canvas_mid_pop, canvas_right_pop 
    canvas_left_pop = Canvas(frame2, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_left_pop.pack(anchor='nw', fill='both', expand=True)
    canvas_mid_pop = Canvas(frame3, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_mid_pop.pack(anchor='nw', fill='both', expand=True)
    canvas_right_pop = Canvas(frame4, bg="green", height=canvas_size_p4, width=canvas_size_p4)
    canvas_right_pop.pack(anchor='nw',  expand=True)
    
    l_bright=tk.Label(frame5,text= "Bright ", bg="black", fg="cyan", font=("Times", "12"))
    l_fluor=tk.Label(frame6,text= "Fluor ", bg="black", fg="cyan", font=("Times", "12"))
    l_red=tk.Label(frame7,text= "Red ", bg="black", fg="cyan", font=("Times", "12"))
    l_bright.pack(),l_fluor.pack(),l_red.pack()
    ################################################
    
    ##########################################################
    global  button_contrast,button_cell_radius,  button_assign_positions,  pop_slider, button_close 
    button_contrast = Button(frame5, text="2a. Enhance image contrast",font='TkDefaultFont 10 bold', bg=button_color, command=lambda:[create_contrast_popup(),instruct_var_p4.set("Adjusting contrast....")])
    button_contrast.pack()
    
    button_cell_radius = Button(frame6, text="2b. Measure cell size",font='TkDefaultFont 10 bold', bg=button_color, command=create_cell_measure_popup)
    button_cell_radius.pack()
    
    
    button_assign_positions = Button(frame7, text="2c. Assign initial cell positions",font='TkDefaultFont 10 bold', bg=button_color, command=create_assign_cell_positions_popup)
    button_assign_positions.pack()
    
    #button_count_cells = Button(frame7, text="2d. Count max number of cells",font='TkDefaultFont 10 bold', bg=button_color, command=start_counting_cells)
    #button_count_cells.pack()
    
    button_close = Button(frame9, text=" Close this window",font='TkDefaultFont 10 bold', bg=button_color, command=close_popup_canvas)
    button_close.pack()
    
    global first_go_buttons
    first_go_buttons=[button_load,button_contrast,button_cell_radius,  button_assign_positions]
    activate_buttons(first_go_buttons,[button_contrast])
    

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
       br_tk, br_name=display_image_p4_fix_missing(image_number_zfill, bright_dictionary,"ch02", canvas_size_p4)              
       canvas_left_pop.create_image(0,0, anchor=NW, image=br_tk)
       l_bright.config(text= "Bright \n"+br_name)
       #br_name_p2.set("Original name:   "+old_br_name+"\nNew name:   "+new_br_name)    
       ################################    
       fl_tk, fl_name=display_image_p4_fix_missing(image_number_zfill, fluor_dictionary,"ch00", canvas_size_p4)     
             
       canvas_mid_pop.create_image(0,0, anchor=NW, image=fl_tk)
       l_fluor.config(text= "Fluor \n"+fl_name)
       #fl_name_p2.set("Original name:   "+old_fl_name+"\nNew name:   "+new_fl_name)    
       ###############################################
       red_tk, red_name=display_image_p4_fix_missing(image_number_zfill, red_dictionary,"ch01",canvas_size_p4)          
           
       canvas_right_pop.create_image(0,0, anchor=NW, image=red_tk)
       l_red.config(text= "Red \n"+red_name)                   
       #red_name_p2.set("Original name:   "+old_red_name+"\nNew name:  
       ################################# 
    
    pop_slider = Scale(frame6, from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1, orient=HORIZONTAL, troughcolor="green", command=slide_frames_pop, length=370)      
    pop_slider.pack()
    #view_slider.config(from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1)      
    slide_frames_pop(first_frame_number)
    #instruct_var_p4.set("Loading input movie ...")
    #instruct_label = tk.Label(frame8, text=" Welcome to STEP 3 of the pipeline! \n\nTo choose input movie you want to track, press Button 1. ",fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
    #instruct_label.grid(row=1, column=0,columnspan=4, sticky=W)
    global instruct_label_popup_p4
    instruct_label_popup_p4=tk.Label(frame8,text="Input movie is loaded. Now, you need to set up some parametres using Buttons 2a,2b,2c and 2d consequetively. Start with Button 2a." ,bg="black", fg="yellow", font=all_font,width=10, height=5)
    instruct_label_popup_p4.pack(fill=BOTH) 
    #button_close = Button(frame9, text=" Close this window",font='TkDefaultFont 10 bold', bg=button_color, command=close_popup_canvas)
    #button_close.pack()
    ###########################################   
    global  full_core_bright_name, out_folders,full_core_red_name
       
    out_folders = create_output_folders(outpath)  
    full_core_bright_name, _, _= extract_file_name(all_names_bright[0])
    ############################## DEBUG
    if len(all_names_red)!=0:
        full_core_red_name, _, _= extract_file_name(all_names_red[0])
    else:
        full_core_red_name="0"
    ##############################################
    ###########################################
    print("n_digits=", n_digits)   
    ########### load the first clip         
    #global fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names                 
    #fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(0,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number)
    global   previous_lineage_image, lineage_image_size
    #number_of_added_new_cells=0     
    #frame_size=fluor_images[0].shape[0]
    #cell_info_label.config(text= "FRAME SIZE:"+str(frame_size)+"x"+str(frame_size), fg="#00FFFF", bg="black")
    #################################    
    feedback_dict_p4["frame size"]=str(frame_size)+"x"+str(frame_size)
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4)
     ###################################
    print("frame_size_before=", frame_size)
    if num_frames<=382:
        lineage_image_size=num_frames#this is the size of lineage image
    else:
        lineage_image_size=num_frames
    previous_lineage_image =np.zeros((lineage_image_size, lineage_image_size,3), dtype="uint8") 
    #feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))   
    button_load.configure(background =button_color)
    global start_frame
    start_frame=first_frame_number
    print("start_frame inside prepare for first_go=", start_frame)   
    update_flash([button_contrast])
    global contrast_value
    contrast_value="0"

#######################################
global retrieve_unfinished_movie
def retrieve_unfinished_movie():# in retrieve mode
    print("I am inside retrieve function")
    instruct_var_p4.set("Loading unfinished movie ..."),   
    update_flash([button_execute])                
    display_first_frame()
    instruct_var_p4.set("Use slide bar to check the results.\n To continue tracking, push Button 3."\
                        "\nTo correct tracking errors, stop the slider at the frame of interest and go to Edit tools." \
                        "\nNOTE: tracking will start from the last frame, not the one you stopped the slider at.")
    #input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1))           
    #feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))
    
###########################################
button_load = Button(frame1_page4, text="1. Click to open file menu and then select input movie folder",
               bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=initiate_tracking_page).start(), update_flash([]), feedback_label_p4.configure(text="Loading input movie ...") ])
button_load.pack()
#button_load.grid(row=2, column=0, padx=10, pady=20)

################################
######### measure cell radius in cell_measure_popup window (Bitton 2b)
############################
def draw_first_circles(event):# draw green circles to measure cell diameter
    rad=scaled_cell_radius.get()
    circle=canvas_for_radius.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline = "red",width = 2)
    centres.append([int(round(event.x)), int(round(event.y))])
    circles.append(circle)
    if len(circles)==1:
           update_flash([radius_slider])
           activate_buttons(radius_popup_buttons,[radius_slider]) 
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
       new_circle=canvas_for_radius.create_oval(centres[k][0]-scaled_cell_radius,centres[k][1]-scaled_cell_radius,centres[k][0]+scaled_cell_radius,centres[k][1]+scaled_cell_radius,outline = "red",width = 2) 
       #canvas.create_oval(event.x-value,event.y-value,event.x+value,event.y+value,outline = "red",width = 2)
       #coords.append([event.x, event.y])
       new_circles.append(new_circle)
       if len(new_circles)==1:
             update_flash([button_save_radius])
             activate_buttons(radius_popup_buttons,[button_save_radius, radius_slider])
  circles=new_circles
###################################################
def save_cell_radius():
    global patch_size, bordersize
    update_flash([button_assign_positions])
    patch_size=int(round(true_cell_radius.get()*2.4))# it is actually HALF on the square side
    bordersize=patch_size 
    #patch_size=int(round(true_cell_radius.get()*2.4))
    instruct_label_popup_p4.configure(text="Cell diameter has been measured. \nNow, go to Button 2c to assign initial cells` positions.")     
    activate_buttons(radius_popup_buttons,[ button_assign_positions]) 
    popup_for_radius.destroy()
    #cell_info_label.config(text= "FRAME SIZE: "+str(frame_size)+"x"+str(frame_size)+
                           #"\nCELL DIAMETER:= "+str(2*true_cell_radius.get())+"\nPATCH SIZE= "+str(2*patch_size)+" x "+str(2*patch_size),
                           #fg="#00FFFF", bg="black")
     #################################    
    feedback_dict_p4["cell diameter"]=str(2*true_cell_radius.get())
    feedback_dict_p4["patch size"]=str(2*patch_size)+" x "+str(2*patch_size)
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4)
     ###################################
 
#####################################
def create_cell_measure_popup():
    update_flash([])
    global popup_for_radius, canvas_for_radius, photo_image
    instruct_label_popup_p4.configure(text="Measuring cell diameter is in progress....")     
    #global cliplimit
    #cliplimit=IntVar()
    #cliplimit.set(0.)
    popup_for_radius = tk.Toplevel(master=popup_first_preview, bg=bg_color)
    popup_for_radius.title("PAGE 4 POPUP WINDOW: MEASURE CELL DIAMETER")       
    popup_for_radius.geometry('%dx%d+%d+%d' % (popup_window_size, popup_window_size+200, 0, 0))
    frame1 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=popup_window_size)
    frame1.pack()
    frame2 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=50, bg=bg_color)
    frame2.pack()

    canvas_for_radius = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg=bg_color)
    canvas_for_radius.pack(anchor='nw', fill='both', expand=True)
    #######################################
    if contrast_value!="0":
           global init_image              
           clahe = cv2.createCLAHE(clipLimit=float(contrast_value))
           init_image=clahe.apply(last_image)
    else:
        init_image=last_image
               
    photo_image=turn_image_into_tkinter(init_image,popup_window_size,[])     
    canvas_for_radius.create_image(0,0, anchor=NW, image=photo_image)

    global centres, circles,scaled_cell_radius, true_cell_radius
    centres, circles,scaled_cell_radius, true_cell_radius =[],[],IntVar(),IntVar()

    scaled_cell_radius.set(20)
    true_cell_radius.set(int(round(scaled_cell_radius.get()*frame_size/popup_window_size)))
    print("initial_true_radius=",true_cell_radius.get())
    global radius_slider, button_save_radius   
    radius_slider=Scale(frame2,from_=1,to=100,orient=HORIZONTAL,troughcolor="green",activebackground="red",label="Cell radius = "+str(int(true_cell_radius.get())),variable=scaled_cell_radius, command=change_radius, length=150, showvalue=0)
    radius_slider.pack()
    radius_label_p4=tk.Label(frame2,text="To measure cell radius, left click on a cell (make sure to click on the centroid) and then \nuse the slide bar to change radius.\nThe cell should be entirely enclosed inside green circle."\
                             "\nTo check,you can also click on all cells in frame",bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)
    radius_label_p4.pack(fill=BOTH) 
    
    button_save_radius=tk.Button(frame2,text="Save",activebackground="red", command=save_cell_radius, bg=button_color)
    button_save_radius.pack()    
    canvas_for_radius.bind("<Button-1>",draw_first_circles)
       
    global radius_popup_buttons
    radius_popup_buttons=[button_cell_radius, button_save_radius,radius_slider,button_assign_positions ]
    activate_buttons(radius_popup_buttons,[ button_cell_radius])    
###############################################
################### adjust contrast if necessary in contrast_popup (Button 2a)  
####################################### #
def create_contrast_popup():    
    global popup_contrast, canvas_contrast, photo_image, number_of_contrast_changes
    number_of_contrast_changes=[]
    global cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_contrast = tk.Toplevel(master= popup_first_preview, bg=bg_color)
    popup_contrast.title("PAGE 4 POPUP WINDOW: ADJUST CONTRAST") 
    popup_contrast.geometry('%dx%d+%d+%d' % (popup_window_size, popup_window_size+200, 0, 0))
    
    frame1 = tk.Frame(master=popup_contrast, width=popup_window_size, height=popup_window_size, bg=bg_color)
    frame1.pack()
    frame2 = tk.Frame(master=popup_contrast, width=popup_window_size, height=50, bg=bg_color)
    frame2.pack()

    canvas_contrast = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg="black")
    canvas_contrast.pack(anchor='nw', fill='both', expand=True)
   
    photo_image=turn_image_into_tkinter(init_image,popup_window_size,[])     
    canvas_contrast.create_image(0,0, anchor=NW, image=photo_image)    
    global contrast_slider, button_save_contrast    
    contrast_slider=Scale(frame2,from_=0,to=100,orient=HORIZONTAL,troughcolor="#513B1C",variable=cliplimit,activebackground="red",label="Cliplimit = " +str(int(cliplimit.get())),command=change_contrast, length=150, showvalue=0)
    contrast_slider.pack()
    
    contrast_label_p4=tk.Label(frame2,text="To adjust contrast, use the slide bar. \nThen click Save." ,bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)
    contrast_label_p4.pack(fill=BOTH)
    instruct_label_popup_p4.configure(text="Adjusting contrast in progress...")
    #instruct_var_p4.set("Adjusting contrast....")
    button_save_contrast=tk.Button(frame2,text="Save",activebackground="red", command=save_contrast, bg=button_color)
    button_save_contrast.pack()       
    update_flash([contrast_slider])
    
    global contrast_popup_buttons
    contrast_popup_buttons=[button_contrast, button_save_contrast,button_cell_radius ]
    activate_buttons(contrast_popup_buttons,[ button_contrast])
        
###################################
def change_contrast(value):
    number_of_contrast_changes.append(value)
    if len(number_of_contrast_changes)==1:
        update_flash([button_save_contrast])
        activate_buttons(contrast_popup_buttons,[ button_save_contrast])
    canvas_contrast.delete("all")
    contrast_slider.config(label="Cliplimit =  "+ value)
    init_image_copy=init_image.copy()
    global contrast_value
    if value!="0":      
      contrast_value=value
      #contrast_indicator.set("yes") 
      clahe = cv2.createCLAHE(clipLimit=float(value))
      cl=clahe.apply(init_image_copy)      
      result=cl
    else:     
      result=init_image
      contrast_value="0"
      #contrast_indicator.set("yes")           
    global photo_image_contrast
    photo_image_contrast=turn_image_into_tkinter(result,popup_window_size,[])     
    canvas_contrast.create_image(0,0, anchor=NW, image=photo_image_contrast)
###############################
def save_contrast():
    ind=cliplimit.get()
    print("ind = ", ind)
    update_flash([button_cell_radius])
    button_save_contrast.config(bg=button_color)
    activate_buttons(contrast_popup_buttons,[ button_cell_radius])
    instruct_label_popup_p4.configure(text="Contrast has been adjusted. \nNow, go to Button 2b to measure cell diameter.")     
    popup_contrast.destroy()  
################### Assign initial cell positions in assign_cell_positions_popup (Button 2c)

##################################
global create_assign_cell_positions_popup
def create_assign_cell_positions_popup():
    instruct_label_popup_p4.configure(text="Assigning initial cells` positions is in progress....")     
    global  manual_init_positions
    manual_init_positions =[]
    #instruct_var_p4.set("Waiting for manual assignment of cell positions in Frame 1 ...")
    #feedback_label_p4.configure(text="Waiting for manual assignment of cell positions in Frame 1 ...")
    button_contrast.configure(bg=button_color, fg="black")
    global popup_assign_pos,  cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_assign_pos = tk.Toplevel(master=popup_first_preview, bg=bg_color)
    popup_assign_pos.title("PAGE 4 POPUP WINDOW: ASSIGN INITIAL CELL POSITIONS") 
    popup_assign_pos.geometry('%dx%d+%d+%d' % (popup_window_size, popup_window_size+400, 0, 0))
    
     
    sub2 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=popup_window_size, bg=bg_color)
    #sub2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    sub2.pack()
    global canvas_assign_pos
    
    print("manual_init_positions inside create assign=",manual_init_positions)
    canvas_assign_pos = Canvas(sub2,  height=popup_window_size, width=popup_window_size,bg=bg_color)
    canvas_assign_pos.pack(anchor='nw', fill='both', expand=True)
    canvas_assign_pos.bind("<Button-1>", click_position)
    
      
    sub3 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=300, bg=bg_color)
    #sub3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    sub3.pack()
    ass_pos_label_p4=tk.Label(sub3,text="This is Frame 1 of the input movie.\nTo assign positions of cells of interest, click on centroids."\
                              "\nThen, click Save.",bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)
    ass_pos_label_p4.pack(fill=BOTH) 
    global button_save_init_positions, photo_image
    button_save_init_positions = Button(sub3, text="Save", bg=button_color,activebackground="red", command= close_assign_window)
    button_save_init_positions.pack()
    #update_flash([button_save_init_positions])    
    canvas_assign_pos.create_image(0, 0, anchor=NW, image=photo_image_contrast)
    
    global positions_popup_buttons, button_close
    positions_popup_buttons=[button_assign_positions, button_save_init_positions, button_close ]
    activate_buttons(positions_popup_buttons,[ button_assign_positions])
    #global counting_buttons
    #counting_buttons=[button_count_cells, button_close] 
    #activate_buttons(counting_buttons,[ button_count_cells])
################ draw red spots in popup canvas in response to mouse click
def click_position(event):
    #print("manual_init_positions inside click_position=",manual_init_positions)
    canvas_assign_pos.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    #print("manual_init_positions second time=",manual_init_positions)
    manual_init_positions.append([event.x/popup_window_size*frame_size, event.y/popup_window_size*frame_size])
    if len(manual_init_positions)==1:
        update_flash([button_save_init_positions])
        activate_buttons(positions_popup_buttons,[ button_save_init_positions]) 
    #cell_numbers_label.config(text="NUMBER OF CELLS IN FRAME 1 = "+str(len(manual_init_positions)))
    feedback_dict_p4["initial number of cells"]=str(len(manual_init_positions))
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4)
##################################
def close_assign_window():
     update_flash([button_close])
     instruct_label_popup_p4.configure(text="Initial cells` positions in Frame 1 have been assigned. Now, go to Button 2d to assign maximum number of cells in input movie.")
     activate_buttons(positions_popup_buttons,[ button_close]) 
     popup_assign_pos.destroy()
############################    
def close_popup_canvas(): # save initial positions of cells in Frame 1                    
      global coords, manual_init_positions, coords_very_first, number_in_first_frame    
      
      coords_very_first=manual_init_positions
      number_in_first_frame=len(coords_very_first)
      global colour_dictionary, new_naive_names, colour_counter, base_colours, basic_naive_names, xs, init_delta,naive_names_counter
          
      colour_dictionary, new_naive_names, base_colours, colour_counter, basic_naive_names, xs, init_delta,naive_names_counter= create_first_color_dictionary(
         len(manual_init_positions), num_frames)
      print("xs=", xs)
      N_cells=len(manual_init_positions)      
      global curr_frame_cell_names, flag,  edit_id_indicator
      curr_frame_cell_names = new_naive_names# names of cell in the current frame
      flag="manual centroids"
      edit_id_indicator.set("yes")
      coords = np.zeros((N_cells, 2))      
      print("curr_frame_cell_names=", curr_frame_cell_names)     
      
      for i in range(N_cells):
        coords[i] = manual_init_positions[i]
      record_const_movie_parameters()  
      print("coords=", coords)
      button_contrast.configure(text =str(len(coords))+ " cells" ,background="black", fg="#00FFFF")
      #instruct_label_popup_p4.configure(text="Initial cells` positions in Frame 1 have been assigned. Now, go to Button 2d to assign maximum number of cells in input movie.") 
      instruct_var_p4.set("The parameters of the input movie have been set up.\n\nTo start execution, press Button 3.")
      #feedback_label_p4.config(text="The positions of cells in Frame 1 has been saved.\n\nTo start execution, press Button 3.")
      
      update_flash([button_execute])
      global all_buttons_page4
      activate_buttons(all_buttons_page4,[button_execute])
     
      popup_first_preview.destroy()


####################################################
############################################  
global curr_frame_cell_names, variable_stop, manual_division_indicator, mother_number, edit_id_indicator
curr_frame_cell_names, variable_stop, manual_division_indicator, mother_number, edit_id_indicator=[], "Do not stop", StringVar(), IntVar(),StringVar()
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
def cut_lineage(internal_start_frame): # after editing
    lineage_per_frame_p4=extract_lineage(outpath)
    print("CUT_LINEAGE")
    #print("len(lineage_per_frame_p4) BEFORE=", len(lineage_per_frame_p4))
    del lineage_per_frame_p4[(internal_start_frame)-1:]# was -1
    #print("len(lineage_per_frame_p4) AFTER=", len(lineage_per_frame_p4))   
    update_lineage(lineage_per_frame_p4,outpath,'wb')# "wb" means delete previous lineage and write a new one
    global output_images,lineage_images_tk,lineage_images_cv2, output_names    
   
    del lineage_images_cv2[(internal_start_frame-1):] 
    del lineage_images_tk[(internal_start_frame-1):]
    del output_images[(internal_start_frame):]# was start_frame:
    del output_names[(internal_start_frame):]
    del changeable_params_history[(internal_start_frame-1):]
    update_changeable_params_history(changeable_params_history,outpath, "wb")
        
    folders_to_truncate=[os.path.join("HELPERS_(NOT_FOR_USER)","MASKS"),"FLUORESCENT_MOVIE_RESULTS",os.path.join("HELPERS_(NOT_FOR_USER)","LINEAGE_IMAGES"),os.path.join("HELPERS_(NOT_FOR_USER)","CLEANED_PATCHES"), "BRIGHT_MOVIE_RESULTS"]
    for folder in folders_to_truncate:
        #print("folder=", folder)
        full_path_to_folder=os.path.join(outpath,folder)
        for filename in os.listdir(full_path_to_folder):
            #print("filename=", filename)
            index_t=filename.index("_t")
            #print("index_t=", index_t)
            number=int(filename[index_t+2:-9])
            if number>=start_frame:
               full_name=os.path.join(full_path_to_folder, filename)
               os.remove(full_name)

###########################################################
def clear_memory_of_previous_clip(fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names,red_images, red_names ):
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
 if red_names:
     del red_names
 if red_images:
     del red_images
     
#############################################
def record_const_movie_parameters():# record cell_size and other parameters in pickle file to be used at Step 4 and in retrieve mode
    list_of_const_movie_params=[frame_size, true_cell_radius.get(), patch_size,basic_naive_names,
                          num_frames, full_core_fluor_name, n_digits,full_core_bright_name, first_frame_number,
                          base_colours, contrast_value, number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta]
    const_parameters_path=os.path.join(outpath,"constant_movie_parameters.pkl")  
    with open(const_parameters_path, 'wb') as f:
        for i in range(len(list_of_const_movie_params)):
           pickle.dump(list_of_const_movie_params[i], f,protocol=pickle.HIGHEST_PROTOCOL)

###########################################


import time
########################################################
def execute():
 activate_buttons(all_buttons_page4,[button_execute])
 button_execute.configure(background = 'red') 
 instruct_var_p4.set("Execution in progress...")
 global start_frame
 print("START_FRAME inside execute=", start_frame)
 start_time=time.time()
 label_curr_frame_name.config(text=start_empty_file_name)
 label_current.configure(text="Current frame:  ", fg="black")
 print("xs in EXECUTE=",xs) 
 try:
   
    cell_radius=true_cell_radius.get()   
    canvas_previous.delete("all")
    canvas_current.delete("all")
    canvas_lineage_exec.delete("all")
      
    #label_edit.configure(text=" ")    
    #feedback_label.config(text="Wait, loading models ...", fg="yellow")
    global lineage_images_tk, output_images, lineage_per_frame_p4, previous_lineage_image, lineage_images_cv2 
    print("previous_lineage_image.shape IN EXEC=",previous_lineage_image.shape)    
    if lineage_per_frame_p4:
        del lineage_per_frame_p4
    
    global variable_stop,  tracker, segmentor, refiner# this variable allows to stop the loop (controlled by Stop button)     
    global coords, curr_frame_cell_names, count,  cells, old_number_of_cells, edit_id_indicator,kk, lin_image_widths
    #label_edit.configure(text="curr_frame_cell_names:\n " + str(curr_frame_cell_names), bg="black")
    print("lin_image_widths INSIDE EXECUTE=", lin_image_widths)     
    N_cells = coords.shape[0]
    division_indicator=0
    centroids_for_benchmarking=[coords]
    n =num_frames  
    #k = start_frame  # the first frame of clip 
    first_number_in_clip=start_frame    
    kk = 0  # the number of frame within clip    
    clear_memory_of_models(tracker, segmentor, refiner)
    tracker, segmentor, refiner=load_weights(models)    
    #feedback_label.config(text="Execution is about to begin ...")
    update_flash([button_pause])
    activate_buttons(all_buttons_page4,[button_pause])
    
    print("num_frames=", num_frames)
    print("first_frame_number=", first_frame_number)
    last_frame_number=num_frames+first_frame_number-1
    print("last_frame_number=", last_frame_number)
    # n=last_frame_number
    while  first_number_in_clip <= last_frame_number:    
    #while k < n:
        print("Inside  k -loop=")
                
        global fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names,red_names, red_images 
        clear_memory_of_previous_clip(fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names,red_images, red_names)
        fluor_images,fluor_images_compressed,bright_images,fluor_names,br_names,red_names, red_images  =load_clip( first_number_in_clip,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number, full_core_red_name,red_dictionary)
        
        clip_centr = predict_tracking_general(
                coords, fluor_images, fluor_images_compressed, fluor_names,  first_number_in_clip,  tracker,last_frame_number, cell_radius, frame_size)
        print("TRACKING PREDICTED FOR CLIP BEGINNING WITH FRAME  ", first_number_in_clip)
        print("curr_frame_cell_names=",curr_frame_cell_names)        
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
                dict_of_divisions, cells, count, coords,curr_frame_cell_names, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, first_number_in_clip+kk, edit_id_indicator, mother_number, out_folders, cell_radius, frame_size, colour_dictionary, patch_size, "first cleaning", bordersize)
          
            print("cell names after segmentation=", list(cells.keys()))
            print("curr_frame_cell_names after segmentation=",curr_frame_cell_names) 
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
                       cut_patch, cells, curr_frame_cell_names, count, division_indicator, coords, frame_size, colour_dictionary,bordersize, patch_size)
                   
               if division_indicator == 1 and mother_8_name != []:                   
                   dict_of_divisions[mother_8_name] = first_number_in_clip+kk
                   #print("mother_cell_name =", mother_8_name)                  
                   #print("8-figure division detected in frame ", first_number_in_clip+kk)                 
            #################################################### 
                      
            if manual_division_indicator.get()=="yes":
                 manual_division_indicator.set("no")
            #record_const_movie_parameters()
            print("curr_frame_cell_names after division=",curr_frame_cell_names) 
            update_changeable_params_history([[xs,curr_frame_cell_names,flag,edit_id_indicator.get(),colour_counter,colour_dictionary,dict_of_divisions,naive_names_counter, lin_image_widths]],outpath, 'ab')
            update_lineage([cells],outpath,'ab')# concatenates {cells}  to pickle 
            #eedback_label.config(text="Execution in progress: \nFrame "+ str(first_number_in_clip+kk)+"\n - If you need to stop for editing, press Button 3a."
                            #"\n - Otherwise, wait until execution is finished.")
            #label_current.configure(text="Current frame: " +str(first_frame_number+k+kk+1), fg="red")           
            N_cells = len(cells)
            print("cells after division detector=", list(cells.keys()))
            #print("n_digits_inside execute=", n_digits)
            print("previous_lineage_image.shape =", previous_lineage_image.shape)
            current_lineage_image=create_lineage_image_one_frame(cells, previous_lineage_image, xs, first_number_in_clip+kk, first_frame_number)
            print("current_lineage_image.shape =", current_lineage_image.shape)
            #print("fluor_names inside exeute=", fluor_names)
            coords, destin_fluor = plot_frame(cells, clip_centr, first_number_in_clip, kk,
                                fluor_images, fluor_names, out_folders, coords, coords, bright_images, br_names, frame_size , n_digits, first_frame_number, contrast_value, current_lineage_image,patch_size, red_images, red_names, bordersize)          
            
                      
            image_seg=destin_fluor# for displaying dynamically on unterface
            photo_image_seg=turn_image_into_tkinter(image_seg, canvas_size_p4,[])
            #canvas_current.create_image(0,0,anchor=NW,image=photo_image_seg)
            output_images.append(photo_image_seg)
            output_name=rename_file(out_folders[1],fluor_names[kk])
            output_name_base=os.path.split(output_name)[1]          
            output_names.append(output_name_base)
            #output_names.append(rename_file(out_folders[3],fluor_names[kk]))         
            image_lin=current_lineage_image
            image_lin_copy=copy.deepcopy(image_lin)         
            lineage_images_cv2.append(image_lin_copy)
            previous_lineage_image=current_lineage_image# need it for the next lineage image
            print("len(lineage_images_cv2) inside execute=",len(lineage_images_cv2))
            print("image_lin.shape=",image_lin.shape)
            #global photo_image_lin                       
            photo_image_lin=turn_image_into_tkinter(image_lin, canvas_size_p4, lin_image_widths)
            #canvas_lineage.create_image(0,0,anchor=NW,image=photo_image_lin)          
            lineage_images_tk.append(photo_image_lin)
            #input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\nTOTAL NUMBER OF FRAMES: "+str(num_frames)+"\nNUMBER OF TRACKED FRAMES:  " +str(len(output_names)-1)) 
            feedback_dict_p4["number of processed"]=str(len(output_names)-1)
            feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
            feedback_var_p4.set(feedback_text_p4)
            centroids_for_benchmarking.append(coords)            
            
            #print("set view_slider at ",first_frame_number+k+kk)
            
            if  first_number_in_clip == start_frame and kk==0:
            #if  k == start_frame-1 and kk==0:
                 view_slider.config(from_=first_frame_number,to=first_frame_number+len(all_names_fluor)-1)
            
            view_slider.set(first_number_in_clip+kk)# show images dinamically
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
       feedback_label_p4.config(text="Stopped due to error", fg="#DF0101", font='TkDefaultFont 10 bold')      
       #start_frame=k+kk+1            
       print("Stopped due to error!!!!!")
       tk.messagebox.showerror('Error',traceback.format_exc())
       update_flash([])     
 if variable_stop=="Stop":
     print("MANAGED TO BREAK OUT OF CLIP LOOP")
     feedback_label_p4.config(text="You stopped execution manually. \nPress Button 4 to check results." )
     variable_stop="Do not stop"
 else:
     feedback_label_p4.config(text="Execution finished! \nPress Button 4 to check results." )
     finish_time=time.time()
    
     execution_time=finish_time-start_time
     print("execution_time=", execution_time)
 button_execute.configure(background = button_color)
 button_pause.configure(background = button_color)
 update_flash([button_display])
 activate_buttons(all_buttons_page4,[button_display])
 print("dict_of_divisions after execution =", dict_of_divisions) 
###############################################
def stop_execution_manually():
    print("STOPPED MANUALLY!!!!")
    instruct_var_p4.set("You stopped execution. \nTo see all the processed frames,  push button 4. Display result.")
    button_execute.configure(background = button_color)
    global variable_stop
    variable_stop = "Stop"
    button_pause.configure(background = "red")
    #activate_buttons(all_buttons_page4,[button_display])
    #print("START_FRAME after pushing pause=", start_frame)
    print("dict_of_divisions after execution inside stop_exec_manually=", dict_of_divisions)
#################################################################    
button_pause = Button(frame2_page4, text="3a. Pause ",activebackground="red",
               bg='#9ACD32', font='TkDefaultFont 10 bold', command=stop_execution_manually)
button_pause.grid(row=0, column=2, padx=10, pady=20)  
#############################
def slide_frames(value):# view_slider (main screen)
    #print("len(lineage_images) inside SLIDE_FRAMES=",len(lineage_images))
    image_number = int(value)
    #print("image_number inside slide_frames=", image_number)    
    internal_image_number=image_number-first_frame_number+1    
    label_curr_frame_name.config(text=output_names[image_number-first_frame_number+1])
    label_current.configure(text="Current frame: " +str(image_number), fg="black")     
    show_3_canvases(canvas_previous,canvas_current,canvas_lineage_exec,output_images,lineage_images_tk,image_number, first_frame_number)
##############################################
global view_slider# main screen
view_slider = Scale(frame9_page4, from_=1, to=1, orient=HORIZONTAL, troughcolor="green", command=slide_frames, length=370)      
#view_slider.grid(row=6, column=0, pady=5)
view_slider.pack() 
###########################################
def display_first_frame():# display all frames after pushing button "Display result"
    update_flash([])
    button_display.config(bg="red")
    button_execute.configure(bg=button_color)
    global fully_tracked_indicator
    if fully_tracked_indicator=="yes":
           activate_buttons(all_buttons_page4,[R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell ])
    else:
          activate_buttons(all_buttons_page4,[R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell, button_execute ])  
    view_slider.config(from_=first_frame_number,to=len(output_images)+first_frame_number-2)   
    view_slider.set(str(first_frame_number))  
    slide_frames(first_frame_number)
    
    global  lineage_per_frame_p4
    lineage_per_frame_p4=extract_lineage(outpath)
    print("len(lineage_per_frame_p4)=", len(lineage_per_frame_p4))
    # creates and saves per cell pedigree in pickle file, but then it is deleted when you push button "Execute"  
    #pedigree = create_pedigree(lineage_per_frame_p4, outpath, frame_size) 
    #instruct_var_p4.set("You stopped execution. \nTo see all the processed frames,  push button 4. Display result.")    
    instruct_var_p4.set("Check results by sliding the bar under Current Frame."
                    "\n - If you need to edit, stop the slide bar at the frame of interest and go for one of the options under Edit tools."
                    "\n - If you are happy with the result, press Button 3. Execute to continue tracking.")       
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
    ############################################
    cell_number_in_mask=int(mask_image[int(event.y/canvas_size_p4*frame_size),int(event.x/canvas_size_p4*frame_size)])
    cell_number=int(math.log(round(cell_number_in_mask),2)) 
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
    instruct_var_p4.set("Cells chosen in Previous Frame:\n " + str(cell_names_external) +"\n")  
########################
def get_centroids_manually(event):
    if popup_monitor!=None:
          popup_monitor.deiconify()
    canvas_current.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    manual_centroids.append([event.x/canvas_size_p4*frame_size, event.y/canvas_size_p4*frame_size])   
    instruct_var_p4.set("Centroids assigned in Current Frame:\n " + str(manual_centroids))
######################################
def start_editing_IDs():
    button_save_id.grid(row=3, column=0, columnspan=1)
    R_edit_ID.configure(background = 'red')
    activate_buttons(all_buttons_page4,[button_save_id])
    update_flash([button_save_id])
    if popup_monitor!=None:
          popup_monitor.deiconify()
    #instruct_label_p4.configure(text="Click on the cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on the same cell in Current Frame \nMake sure you click on the centroid!")
  
    instruct_var_p4.set("First, click on the cell of interest in Previous Frame.\n"
                "Then, click on its desired position in Current Frame.Make sure you click as close to the centroid as possible!\n You can repeat it MULTIPLE TIMES.\nFinally, save edits by pressing button Save ID edits.")    
    global manual_centroids, manual_IDs, cell_names_external
    manual_centroids, manual_IDs, cell_names_external, daughter_indicators=[],[], [],[] 
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    update_flash([button_save_id])   
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
    global previous_lineage_image
    previous_lineage_image=lineage_images_cv2[start_frame_internal-2]
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(outpath, start_frame_internal)
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
    instruct_var_p4.set(" ID edits  for frame  " +str(start_frame)+"  have been saved.\nPress Button 3 to resume execution.")
 
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
    activate_buttons(all_buttons_page4,[button_execute])
    
    label_current.configure( text="Current frame", fg="black" )
    button_save_id.configure(background = '#9ACD32')
    button_pause.configure(background = button_color)
    button_display.configure(bg=button_color)
    #button_save_division.configure(background = '#9ACD32')
    instruct_label_p4.config(text="You finished editing IDs in Frame " +str(start_frame)+".\n To resume tracking, press Button 3." )
    print("dict_of_divisions after stop_editing_IDs =", dict_of_divisions)
    if  popup_monitor!=None: 
       popup_monitor.destroy()
###################################################
def start_editing_division():
    R_edit_division.configure(background = 'red')
    activate_buttons(all_buttons_page4,[ button_save_division])
    button_save_division.grid(row=3, column=1, columnspan=1)
    update_flash([button_save_division]) 
    
    #instruct_label_p4.set("Click on mother cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on daughter cells in Current Frame \nMake sure you click on centroids!")
    print("started manual division editing.....")
    global mother_number
    mother_number=None 
    instruct_var_p4.set("First, click on mother cell in Previous Frame.\n"
               "Then, click on daughter cells in Current Frame. Make sure you click as close to the daughter cells` centroids as possible!\nYou can do it ONLY ONCE.\n Finally, save by pressing button Save division edits.")    
    global manual_centroids, manual_IDs,cell_names_external, daughter_indicators
    manual_centroids, manual_IDs, cell_names_external, daughter_indicators=[],[],[],[]
    
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    
    R_edit_ID.configure(background = '#9ACD32')
   
########################################
def stop_editing_division():
    print("INSIDE STOP_EDITING_DIVISION")
   
    R_edit_division.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>")
    global  mask_prev_frame
    
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())
    
    print("frame number from slider=",start_frame)
    start_frame_internal=start_frame-first_frame_number+1
    print("internal_frame_number=", start_frame_internal)
    global previous_lineage_image
    previous_lineage_image=lineage_images_cv2[start_frame_internal-2]
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(outpath, start_frame_internal)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    
    print("curr_frame_cell_names before=",curr_frame_cell_names)
    edit_id_indicator.set(edit_id_indicator_pickle)
   
    ########################################################
    keys=list(lineage_per_frame_p4[start_frame_internal-1].keys())# from previous frame was -2   
     
    coords_old=lineage_per_frame_p4[start_frame_internal-1][keys[0]][14] 
    global manual_IDs, mother_number, mother_name    
    manual_division_indicator.set("yes")
    mother_number=manual_IDs[0] 
    print("mother_number=", mother_number)
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage_per_frame_p4[start_frame_internal-2][mother_name_internal][11]
    mother_color=lineage_per_frame_p4[start_frame_internal-2][mother_name_internal][15]
    print("mother_name=", mother_name)                                    
    daughter_1_number=mother_number
    daughter_2_number=len(coords_old)    
    daughter_1_name=mother_name+"0"
    daughter_2_name=mother_name+"1"
    daughter_names=[ daughter_1_name, daughter_2_name]
    xs=update_xs_after_division(xs,daughter_1_name,daughter_2_name, mother_name,init_delta)
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,daughter_names,base_colours, colour_counter)
   
    curr_frame_cell_names[mother_number]=daughter_1_name
    curr_frame_cell_names.append(daughter_2_name)  
    coords_daughter_1=manual_centroids[0]
    coords_daughter_2=manual_centroids[1]
    print("curr_frame_cell_names after=",curr_frame_cell_names)
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
    button_display.configure(background = button_color)
    
    R_edit_division.configure(background = '#9ACD32')
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You finished editing missed division in Frame  "+str(start_frame)+" .\n To resume execution, press Button 3." ) 
############################################
def add_new_cell():
  instruct_var_p4.set("To add a new cell/cells, click on their cetroids in Current Frame./Once finished, click Save added cells.")
  R_add_new_cell.configure(background="red")
  button_save_added_cell.grid(row=3, column=2, columnspan=1)
  update_flash([button_save_added_cell])
  activate_buttons(all_buttons_page4,[button_save_added_cell])  
  global colour
  colour_init=[0,0,255]
  colour="#%02x%02x%02x" % tuple(colour_init)
  canvas_current.bind("<Button-1>", get_centroids_manually)  
  global manual_centroids
  manual_centroids=[]
  cv2.imwrite(r"C:\Users\helina\Desktop\prevous_image_in_add.tif", previous_lineage_image)
###############################################
def save_added_cell():   
    global start_frame    
    start_frame=int(view_slider.get())   
    internal_start_frame=start_frame-first_frame_number+1
    
    keys=list(lineage_per_frame_p4[internal_start_frame-1].keys())      
    b = np.array(manual_centroids)
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(outpath, internal_start_frame)
    #edit_id_indicator.set(edit_id_indicator_pickle)
    edit_id_indicator.set(edit_id_indicator_pickle)
     
    ########################################################
    global coords,  previous_lineage_image
    previous_lineage_image=lineage_images_cv2[internal_start_frame-2]
    coords_old=coords
    coords=np.concatenate((coords_old, b), axis=0)     
    number_of_now_added_cells=len(manual_centroids)
    #print("number_of_added_cells=", number_of_now_added_cells)
    global  base_colours, delta, naive_names_counter
    #######
    new_naive_names,naive_names_counter=update_naive_names_list(basic_naive_names, number_of_now_added_cells,naive_names_counter)
    #print("new_naive_names before", new_naive_names)
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)    
    curr_frame_cell_names+=new_naive_names
    #number_of_processed_cells=number_in_first_frame+number_of_added_new_cells+len(dict_of_divisions)
    #print("number_of_processed_cells=",number_of_processed_cells)
    #number_of_remaining_cells=max_number_of_cells-number_of_processed_cells
    #print("number_of_remaining_cells=",number_of_remaining_cells)
    # change previous lineage image by adding new cells    
    xs, previous_lineage_image,lin_image_widths=update_xs_after_new_cells(xs,new_naive_names, previous_lineage_image, canvas_lineage_exec, canvas_size_p4, init_delta,lin_image_widths)
    print("previous_lineage_image.shape AFTER CREATION=",previous_lineage_image.shape)
    
    number_of_added_new_cells+=number_of_now_added_cells        
    #lineage_images_cv2[internal_start_frame-1]=previous_lineage_image
    lineage_images_cv2[internal_start_frame-2]=previous_lineage_image     
    instruct_var_p4.set("Added cells:\n " + str(new_naive_names))
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage_exec.delete('all')
  
    
    #print("dict_of_divisios before save_added=", dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}
    #print("dict_of_divisios after save_added=", dict_of_divisions)    
    cut_lineage(internal_start_frame)
   
    update_flash([button_execute])
    button_pause.configure(background = button_color)
    button_display.configure(background = button_color)
    R_add_new_cell.configure(background=button_color)
    button_save_added_cell.grid_forget()
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You added new cells in Frame "+str(start_frame)+"  .\nTo resume tracking, push Button 3.")
#####################################
def remove_died_cell():
  R_remove_dead_cell.configure(background="red")
  button_save_removed_cell.grid(row=3, column=3, columnspan=1)
  update_flash([button_save_removed_cell])
  activate_buttons(all_buttons_page4,[button_save_removed_cell])
  canvas_current.bind("<Button-1>", get_cell_IDs_manually) 
  global manual_IDs,cell_names_external, daughter_indicators
  manual_IDs, cell_names_external, daughter_indicators=[],[],[]
  instruct_var_p4.set("To remove a cell/cells, click on them in Current Frame.\nOnce finished,click Save removed cells. ")  
###########################################
def save_removed_cell():
    instruct_var_p4.set("Deleted cells:\n " + str(cell_names_external))
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())   
    internal_start_frame=start_frame-first_frame_number+1    
    ###############################
    global previous_lineage_image
    previous_lineage_image=lineage_images_cv2[internal_start_frame-2]
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(outpath, internal_start_frame)
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
    button_display.configure(background = button_color)
    R_remove_dead_cell.configure(background=button_color)
    button_save_removed_cell.grid_forget()
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You deleted cells in Frame  "+str(start_frame)+"  /nTo resume tracking, push Button 3.")
##########################################

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
               bg='#9ACD32', activebackground="red",command=lambda:[threading.Thread(target=execute).start(), update_flash([]), button_display.configure(bg=button_color)])               
button_execute.grid(row=0, column=0, pady=20)
#global button_display
button_display = Button(frame2_page4, text="4. Display result", font='TkDefaultFont 10 bold', 
               bg='#9ACD32',activebackground="red", command=lambda: [display_first_frame(), update_flash([])])
button_display.grid(row=2, column=0, padx=20)

################################################

l_instr_name_p4=tk.Label(frame9_page4,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="red").pack()
instruct_label_p4=tk.Label(frame12_page4,textvariable=instruct_var_p4 ,bg="black", fg="yellow", font=all_font, height=5)
instruct_label_p4.pack(fill=BOTH)
 
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

#button_magnify = Button(frame8_page4, text="7. Magnify current frame",activebackground="red", font=all_font, 
              #bg=button_color, command=lambda:magnify_current_frame())
#button_magnify.grid(row=1, column=5, padx=100)

global R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell
edit_label_name=tk.Label(frame3_page4,text="Edit tools",bg=label_color,  font=("Times", "14")). grid(row=0, column=2, pady=5, padx=30)
R_edit_ID = Radiobutton(frame3_page4, text="Edit IDs", value="Previous", font=all_font, variable=clicked, command=lambda:start_editing_IDs(), background=button_color, activebackground="red")
R_edit_ID.grid(row=1, column=0, pady=10, padx=10)

R_edit_division = Radiobutton(frame3_page4, text="Edit division",background=button_color, font=all_font,
                 value="Previous", activebackground="red",variable=clicked,  command=lambda:start_editing_division())
R_edit_division.grid(row=1, column=1, pady=10, padx=10)

R_add_new_cell = Radiobutton(frame3_page4, text="Add new cell", value="Previous", font=all_font, variable=clicked, command=lambda:add_new_cell(), background=button_color, activebackground="red")
R_add_new_cell.grid(row=1, column=2, pady=10, padx=10)

R_remove_dead_cell = Radiobutton(frame3_page4, text="Remove dead cell",background=button_color, font=all_font,
                 value="Current", activebackground="red",variable=clicked, command=remove_died_cell)    
R_remove_dead_cell.grid(row=1, column=3,pady=10, padx=10)
################################################
global all_buttons_page4
#label_edit = tk.Label(frame3_page4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow", width=50, height=4)
all_buttons_page4=[button_load,button_execute, button_pause,button_display,\
                   R_edit_ID,R_edit_division, R_add_new_cell,R_remove_dead_cell,\
                   button_save_id,button_save_division,button_save_added_cell,button_save_removed_cell]

###########################################################################
############################## PAGE-5 (STEP-4): CORRECT SEGMENTATION #######
#############################################################################
page5=pages[4]
page5.title("PAGE 5. CORRECT SEGMENTATION")
page5.config(bg=bg_color)
from helpers_for_PAGE_4 import delete_contour_with_specific_colour,update_frame_dictionary_after_manual_segm_correction, load_models_p5, load_tracked_movie_p5, make_contour_red
from plot import paste_patch, prepare_contours,paste_benchmark_patch,create_name_for_cleaned_patch

from interface_functions import turn_image_into_tkinter,display_both_channels, show_2_canvases
from postprocess import create_output_movie
from print_excel import print_excel_files, extract_const_movie_parameters
from functions import  clean_manual_patch, segment_manual_patch,segment_one_cell_at_a_time,create_intensity_dictionary,remove_cell_from_mask
############ LAYOUT

page5.geometry('1530x2000')
#bg_color,all_font,button_color,result_color,label_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA"

global window_p5_size
window_p5_size =600


frame1_page5 = tk.Frame(master=page5, width=1528, height=5, bg=bg_color)
frame1_page5.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page5 = tk.Frame(master=page5, width=1528, height=50, bg=bg_color)
frame2_page5.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page5 = tk.Frame(master=page5, width=1528, height=30, bg=bg_color)
frame3_page5.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
################################################
frame3a_page5 = tk.Frame(master=page5, width=window_p5_size, height=30, bg=bg_color)
frame3a_page5.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
frame3b_page5 = tk.Frame(master=page5, width=window_p5_size, height=30, bg=bg_color)
frame3b_page5.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
frame3c_page5 = tk.Frame(master=page5, width=window_p5_size, height=30, bg=bg_color)
frame3c_page5.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)


############################################

#frame4_page5 = tk.Frame(master=page5, width=1528, height=50, bg="grey")
#frame4_page5.grid(row=4, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)
############################################################################
frame5_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size, bg=bg_color)
frame5_page5.grid(row=4, column=0,rowspan=1,columnspan=1, sticky=W)

frame6_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size , bg=bg_color)
frame6_page5.grid(row=4, column=1,rowspan=1,columnspan=1, sticky=W)

frame7_page5 = tk.Frame(master=page5, width=100 , height=window_p5_size , bg=bg_color)
frame7_page5.grid(row=4,column=2,rowspan=1,columnspan=1, sticky=W)
#################################################################
frame7c_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame7c_page5.grid(row=5, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

frame7b_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame7b_page5.grid(row=6, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

frame7a_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame7a_page5.grid(row=7, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

###################################################

frame8_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame8_page5.grid(row=8, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

######### POPULATE WITH WIDGETS

global canvas_fluor_p5
canvas_fluor_p5 = Canvas(frame6_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_fluor_p5.pack(anchor='nw', fill='both', expand=True)
label_fluor_name=tk.Label(frame6_page5, text="                       ",
              bg="black", fg="cyan", font=all_font)
label_fluor_name.pack()
global canvas_bright_p5
canvas_bright_p5 = Canvas(frame5_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_bright_p5.pack(anchor='nw', fill='both', expand=True)
label_bright_name=tk.Label(frame5_page5, text="                  ",
              bg="black", fg="cyan", font=all_font)
label_bright_name.pack()

l_title = tk.Label(frame1_page5, text="STEP 4: CORRECT SEGMENTATION",
              bg="yellow", fg="red", font=("Times", "24"))
l_title.grid(row=0, column=3, padx=500, sticky="n")

feedback_label_5 = tk.Label(frame2_page5, text="Movie:      \nFluorescent frames:    Bright frames:       Red frames:       \nFrame size:       Cell diameter: ",
                          fg="cyan",bg="black", font='TkDefaultFont 10 bold', width=200,height=3)
feedback_label_5.grid(row=0, column=0, sticky="w")

dialog_label_5 = tk.Label(frame7a_page5, text="Step-4 allows you to manually correct segmentation in a tracked movie."
                          "\nTo load a tracked movie, click Button 1 and navigate to OUTPUT_MOVIE_[specific movie name]",
                          fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=200,height=4)
dialog_label_5.grid(row=0, column=0, sticky="w")
##########################################
#global list_of_modified_frames, points
#global refiner, segmentor
#refiner, segmentor=None, None
#list_of_modified_frames, points=[], []
###########################################
l_instr_name_p5=tk.Label(frame7b_page5,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="red").pack()
###################################################
number_of_slides_p5=[]# for slide_bar flashing
def slide_frames_p5(value):
    number_of_slides_p5.append(value)
    #if len(number_of_slides_p5)==1:
        #update_flash([])
        #activate_buttons(all_buttons_page5,[button_final_movie])
    image_number = int(value)
    print(" image_number=", image_number)
    #global internal_frame_number_p5
    internal_frame_number_for_slider=image_number-first_frame_number_p5
    print(" internal_frame_number=", internal_frame_number_for_slider)
    #label_fluor_name.config(text=os.path.basename(path_filled_fluors[image_number-1]))
    label_fluor_name.config(text=os.path.basename(path_filled_fluors[internal_frame_number_for_slider]))
     
    label_bright_name.config(text=os.path.basename(path_filled_brights[internal_frame_number_for_slider])) 
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,internal_frame_number_for_slider, window_p5_size) 
############################# load all mecessary images
def choose_and_load_tracked_movie():
    global edits_indicator
    edits_indicator="no"
    global button_load_p5
    update_flash([])
    button_load_p5.configure(background = 'red')
    global output_dir, input_dir,software_folder
    output_dir = filedialog.askdirectory()
          
    head_tail=os.path.split(output_dir)
    head =head_tail[0]
    tail =head_tail[1]
    input_movie_name=tail[7:]
    input_dir  =os.path.join(head,input_movie_name)    
    global path_filled_brights,path_filled_fluors,path_filled_reds,path_masks
    global empty_fluors, empty_brights, empty_reds,filled_fluors, filled_brights,filled_reds, masks
    global lineage_per_frame_p5
    dialog_label_5.config(text="loading tracked movie...")
    path_filled_brights,path_filled_fluors,path_filled_reds,path_masks, empty_fluors, empty_brights, empty_reds,filled_fluors, filled_brights,filled_reds, masks, lineage_per_frame_p5=load_tracked_movie_p5(input_dir,output_dir)
    global frame_p5_size,cell_radius_p5,patch_size_p5,full_core_red_name, first_frame_number_p5,red_dictionary, bordersize   
    #############
    frame_p5_size, cell_radius_p5, patch_size_p5,max_number_of_cells,\
           num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number_p5,\
           base_colours,contrast_value,number_cells_in_first_frame,full_core_red_name,red_dictionary, bordersize, delta=extract_const_movie_parameters(output_dir)
    #################################
    global resize_coeff, new_shape
    resize_coeff=window_p5_size /frame_p5_size
    global  image_origin_x,image_origin_y, factor_in, factor_out,factor,zoom_coeff,delta_x,delta_y, cell_center_visual_x, cell_center_visual_y# for zooming
    delta_x, delta_y=0,0
    factor_in, factor_out, factor=1,1,1
    image_origin_x,image_origin_y=0,0
    zoom_coeff=1
    new_shape=window_p5_size
    cell_center_visual_x,cell_center_visual_y=300,300
    ############################
    print("frame_p5_size=",frame_p5_size)
    feedback_label_5.configure(text="Movie : "+input_dir+"\nFluorescent frames: "+str(num_frames)+\
                               "   Bright frames: "+str(len(filled_brights))+"   Red frames:"+str(len(filled_reds))+\
                                   "\nFrame size = "+ str(frame_p5_size)+" x "+str(frame_p5_size)+"   Cell diameter = "+str(cell_radius_p5*2))
   
    global photo_filled_fluors, photo_filled_brights
    dialog_label_5.config(text="Preparing images for display...")
    photo_filled_fluors=[ turn_image_into_tkinter(filled_fluors[i], window_p5_size,[]) for i in range(len(masks))]
    dialog_label_5.config(text="Prepared 50 % of images for display")
    photo_filled_brights=[ turn_image_into_tkinter(filled_brights[i], window_p5_size,[]) for i in range(len(masks))]
    dialog_label_5.config(text="To check segmentation in each frame, use the slide bar below."
                            "\nIf manual correction is needed in a ceartain frame, stop the slider and push button 2.")
      
    global canvas_fluor_p5, canvas_bright_p5
    image_number=1    
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,image_number, window_p5_size)        
    #view_slider_p5.configure(to=len(masks))
    view_slider_p5.configure(from_=first_frame_number_p5,to=first_frame_number_p5+len(masks)-1)
    ################################################
    button_load_p5.configure(background = button_color)
    update_flash([view_slider_p5])
    activate_buttons(all_buttons_page5,[view_slider_p5, button_final_movie])
    ######################### new addtion for click_one_cell
    global mode_variable,zoom_status# used in radio buttons for editing,indicates which canvas is used for IDs extraction, value = "Current" or "Previous"
    mode_variable,zoom_status = StringVar(),StringVar()
    mode_variable.set(" ") 
    zoom_status.set("off")
    activate_fast_edit_mode()
    global previous_frame_number, previous_cell_number
    previous_frame_number, previous_cell_number=-2, -2
    print("previous_frame_number=",previous_frame_number)
    canvas_fluor_p5.unbind_all("<Button-3>")   
    canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)
    global oval,oval_x,oval_y
    oval_x,oval_y=1,1
    oval=canvas_fluor_p5.create_oval(oval_x-1, oval_y-1, oval_x+1,
                          oval_y+1, outline="magenta",  width=1)
    global points
    points=[]
    """
    global segmentor, refiner
    if segmentor==None and refiner==None:      
        software_folder = os.getcwd() 
        segmentor, refiner= load_models_p5(software_folder)
        dialog_label_5.config(text="Loaded models")
    """             
###########################################
def activate_fast_edit_mode():#enter fast segmentation mode
   button_activate_fast_edit_mode.configure(background = 'red')
   button_activate_slow_edit_mode.configure(background = button_color)   
   dialog_label_5.config(text="\nIn the right image, right-click on the cell you want to correct.")
             
   canvas_fluor_p5.unbind_all("<Button-1>")
   #canvas_fluor_p5.unbind_all("<Button-1>")   
   canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)
   mode_variable.set("fast")
   print("mode_variable=", mode_variable)
#########################################################
##############################################
def activate_hand_drawing_mode_for_one_cell():
    
    dialog_label_5.config(text="Draw the contour of the cell with the left mouse. Warning:  Be careful not to draw on neughbouring close cells!\n If you want to undo right-click the mouse anywhere in the image.\nOnce you are finished, push Button 4b.")    
    
    global cell_contour_fl, cell_contour_br,points, mask_hand, points_for_original# for the clicked cel
    cell_contour_fl=[]
    cell_contour_br=[]
    points, points_for_original=[],[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
###########################################
#######################################################  
def activate_slow_edit_mode():
    mode_variable.set("slow")
    button_activate_slow_edit_mode.configure(background = 'red')
    button_activate_fast_edit_mode.configure(background = button_color)
    dialog_label_5.config(text="Right-click on the cell you want to correct. Its contours should disappear.")
    #update_flash([button_activate_hand_drawing_mode_for_one_cell])
    ########################## delete contour of the clicked ce;;
    global canvas_fluor_p5,canvas_bright_p5
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<B1-Motion>")
    canvas_fluor_p5.unbind_all( "<ButtonPress-1>")
    canvas_fluor_p5.unbind_all("token<ButtonRelease-1>")
    #canvas_fluor_p5.bind("<B1-Motion>", drag)
    canvas_fluor_p5.unbind_all("<MouseWheel>")
    canvas_fluor_p5.bind("<Button-1>", get_x_and_y)    
    #canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse, add="+")
    canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse) 
            
    activate_hand_drawing_mode_for_one_cell()       
    ################################
    # delete contour of the hit cell
    global   filled_fluor, filled_bright, filled_red, empty_fluor, empty_bright, empty_red, cell_color, photo_fluor,photo_bright, filled_fluor_copy, filled_bright_copy
    global final_mask,cell_number_in_frame,intensity_dictionary_for_frame
    print("cell-color=", cell_color)
    print("cell_number inside activate slow mode=", cell_number_in_frame)
    
    filled_fluor_copy=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
    filled_bright_copy=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
    #filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color)
    
    filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
    filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
    filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color)
    
    final_mask=remove_cell_from_mask(cell_number_in_frame, final_mask, intensity_dictionary_for_frame)
    # display frames with erased cell    
    cv2.imwrite("C:\\Users\\helina\\Desktop\\filled_fluor.tif", filled_fluor)  
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y)
    global oval_x,oval_y, factor# create magenta oval on clicked cell
    oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
    #oval=canvas_fluor_p5.create_oval(oval_x-3, oval_y-3, oval_x+3,
                      #oval_y+3, outline="magenta", fill="magenta", width=2)
#############################################
def right_click_one_cell(event):# extract info about clicked celland take action
    mode=mode_variable.get()# after right-clicking cell, extract mode, frame_number and cell_number
    global frame_number, previous_frame_number, previous_cell_number, canvas_fluor_p5, canvas_bright_p5
    global clicked_cell_position_marker, cell_number_in_frame, filled_fluor, filled_bright, filled_red
    global oval, cell_color, cell_ID
    global oval_x_init,oval_y_init, oval_x,oval_y
    ############################################
    global edits_indicator, internal_frame_number_p5
    edits_indicator="yes"
    #############################################
    global all_buttons_page5,button_activate_fast_edit_mode,button_activate_slow_edit_mode,start_zoom_button
    activate_buttons(all_buttons_page5,[button_activate_fast_edit_mode,button_activate_slow_edit_mode,start_zoom_button])
    ##############################################    
    frame_number=view_slider_p5.get()    
    
    ###################################################
    print("mode=", mode)    
    if mode=="fast":# the fast editing (by clicking)   
       if frame_number!=previous_frame_number:# if you are in a new frame
          if previous_frame_number!=-2:# at least 1 frame is edited already
             print("entered new frame in fast mode")         
             print("internal_frame_number inside right_click=", internal_frame_number_p5)
             save_edits_for_frame()# save ed, i.e. not edited yet
             #frame_number=view_slider_p5.get()    
             #internal_frame_number_p5=frame_number-first_frame_number_p5
             print("internal_frame_number_p5 INSIDE RIGHT_CLICK=",internal_frame_number_p5)    
          ################# first of all, get frame info          
          else:# if this is the very 1st frame
              print("in the very first frame, fast mode")
             
          previous_cell_number=-2# if you are in a new frame
          previous_frame_number=frame_number
          #internal_frame_number=frame_number-first_frame_number_p5
          #internal_frame_number=frame_number-1
          internal_frame_number_p5=frame_number-first_frame_number_p5
          print("internal_frame_number_p5 INSIDE RIGHT_CLICK=",internal_frame_number_p5)    
          get_frame_info(internal_frame_number_p5)
       else:# if it is still the same frame
            print("in the same frame, fast mode")    
    ##########################################      
       clicked_cell_position_marker=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]# position marker in image of original size!!!
       print("clicked_cell_position_marker=",clicked_cell_position_marker)
       print("internal_frame_number NO ZOOM =", internal_frame_number_p5)
       mask=masks[internal_frame_number_p5]
       #cell_number=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]-1
       ##################################################
       cell_number_in_mask=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]
       #cell_number_for_mask=round(cell_number_scaled)# for plotting masks (visualisation purpose only)
       cell_number_in_frame=int(math.log(round(cell_number_in_mask),2)) 
       
       ###################################################
       print("cell_number_in_mask, cell_number_in_frame", cell_number_in_mask, cell_number_in_frame)
       
    ##################################################    
       if cell_number_in_frame!=-1:# if you hit a cell body, not background (accidentally)
          if cell_number_in_frame!=previous_cell_number:# you clicked on a new cell, same frame, fast mode
                     print("clicked on new cell, fast mode")                                            
                     #saving previous cell
                     canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
                     print("cells_in_current_frame_sorted=",cells_in_current_frame_sorted)
                     cell_color=cells_in_current_frame_sorted[cell_number_in_frame][1]
                     cell_ID=cells_in_current_frame_sorted[cell_number_in_frame][0]
                     ########################################
                     #global init_x,init_y# create magenta oval on clicked cell
                     oval_x_init,oval_y_init=event.x,event.y# coordinates in window
                     oval_x,oval_y=oval_x_init,oval_y_init
                     #oval_x,oval_y =clicked_cell_position_marker[0],clicked_cell_position_marker[1]
                     print("oval_x-init, oval_y_init=",oval_x, oval_y)
                     #oval=canvas_fluor_p5.create_oval(oval_x-5, oval_y-5, oval_x+5,
                          #oval_y+5, outline="magenta",  width=1)
                     global red_color,filled_fluor_copy,filled_bright_copy,filled_red_copy
                     #global red_color
                     red_color= [0,0,255,255]
                     filled_fluor_copy,filled_bright_copy,filled_red_copy=filled_fluor.copy(),filled_bright.copy(),filled_red.copy()                    
                     filled_fluor_copy=make_contour_red(filled_fluor_copy, empty_fluor,cell_color)
                     filled_bright_copy=make_contour_red(filled_bright_copy, empty_bright,cell_color)
                     filled_red_copy=make_contour_red(filled_red_copy, empty_red,cell_color)
                     
                     #global 
                     #final_mask=remove_cell_from_mask(cell_number_in_frame, final_mask, intensity_dictionary_for_frame)
                     #### display  current frame with modified cell    
                     global photo_fluor, photo_bright
                     canvas_bright_p5.delete("all")
                     canvas_fluor_p5.delete("all")
                     #global photo_fluor_copy, photo_bright_copy
                     canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y)
                     #canvas_fluor_p5.delete(oval)      
                     oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
                                     
                     #previous_cell_number=cell_number
          else:# if you hit cell with the same number, but in different frame
              #if frame_number!=previous_frame_number:
                    #previous_cell_number=-2
                    print("previous_cell_number=", previous_cell_number)
                    print("the same with the same numvber")
                    save_one_edited_cell()
          previous_cell_number=cell_number_in_frame          
       else:# you hit background, i.e. cell_number=-1
              print("clicked on  background, fast mode")         
              print("do nothing")
      
    ######################################
    if mode=="slow":# the slow editing (by hand-drawing)     
         print("slow mode")
         #global frame_number, frame_indicator, cell_indicator,internal_frame_number
         #frame_number=view_slider_p5.get()
       
         if frame_number!=previous_frame_number:# if you are in a new frame
            if previous_frame_number!=-2:
                print("entered new frame")
                #cell_indicator=-2
                save_edits_for_frame()          
            else:
               print("have not started editing yet")
            previous_cell_number=-2
            previous_frame_number=frame_number
            #internal_frame_number=frame_number-first_frame_number_p5
            #internal_frame_number=frame_number-1
            internal_frame_number_p5=frame_number-first_frame_number_p5
            print("internal_frame_number_p5 INSIDE SLOW=",internal_frame_number_p5)    
            get_frame_info(internal_frame_number_p5)
         else:# if it is still the same frame
              print("in the same frame")
         ##################################################       
          #clicked_cell_positon_marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
         #clicked_cell_positon_marker=[int(round((event.x/zoom_coeff-image_origin_x)/(resize_coeff))),int(round((event.y/zoom_coeff-image_origin_y)/(resize_coeff)))]
         clicked_cell_position_marker=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]
         print("clicked_cel_position_marker=", clicked_cell_position_marker)
         print("internal_frame_number ZOOM=",internal_frame_number_p5)
         mask=masks[internal_frame_number_p5]
         #cell_number=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]-1
         #cell_number_scaled=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]
         #cell_number=int(math.log(cell_number_scaled*1000000,2)) 
         #############################
         # it is mask, not final_mask - very important!!!
         cell_number_in_mask=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]
         print("cell_number-in_mask=", cell_number_in_mask)
         if cell_number_in_mask==0:# if you clicked on background
             erase_line()  
         else:
             cell_number_in_frame=int(math.log(round(cell_number_in_mask),2))          
         ##################################                                
             if cell_number_in_frame!= previous_cell_number:# you clicked on a new cell
                     print("clicked on new cell")
                     ###############################
                     if  previous_cell_number!=-2:                     
                           #save_hand_drawing_for_one_cell()
                           save_one_edited_cell()
                     #########################################
                     #global oval, cell_color, cell_ID
                     canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
                     cell_color=cells_in_current_frame_sorted[cell_number_in_frame][1]
                     cell_ID=cells_in_current_frame_sorted[cell_number_in_frame][0]
                     ########################################
                     #final_mask[final_mask==cell_number_for_mask]=0# erase clicked cell from mask
                     final_mask=remove_cell_from_mask(cell_number_in_frame, final_mask, intensity_dictionary_for_frame)
                     #global photo_fluor, photo_bright, canvas_bright_p5  
                     #global  filled_fluor, filled_bright, colour_four_channel, filled_red         
                     filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
                     filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
                     filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color) 
                     # display frames with erased cell    
                     canvas_bright,canvas_fluor,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y)
                     canvas_fluor_p5.delete(oval)      
                     #global init_x,init_y# create magenta oval on clicked cell
                     oval_x,oval_y=event.x,event.y
                     oval=canvas_fluor_p5.create_oval(oval_x-5, oval_y-5, oval_x+5,
                       oval_y+5, outline="magenta", width=1)
                     cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\filled_fluor_after_click.tif", filled_fluor)
                     dialog_label_5.config(text="To be able to start hand drawing, push Button 4a.")   
                     ###########################################
                     activate_hand_drawing_mode_for_one_cell()
                     ##############################################                    
             else:# you clicked on the same cell,slow mode
                     print("clicked on  same cell")
                     #save_hand_drawing_for_one_cell()
                     save_one_edited_cell()
                     activate_fast_edit_mode()                     
         previous_cell_number=cell_number_in_frame
        
################################################

def get_x_and_y(event):
    global lasx,lasy
    lasx,lasy=event.x,event.y         
#########################################
############################################    
def draw_with_mouse(event):
    global coeff
    global lasx,lasy, line_fl, line_br 
    xx,yy=event.x,event.y
    line_fl=canvas_fluor_p5.create_line((lasx,lasy,xx,yy), fill="red", width=5)
    get_x_and_y(event)
    line_br=canvas_bright_p5.create_line((lasx,lasy,xx,yy), fill="red", width=5)
    cell_contour_fl.append(line_fl)
    cell_contour_br.append(line_br)   
    #lasx,lasy=event.x,event.y
    #points.append([[int(round(lasx/window_p5_size*frame_p5_size)),int(round(lasy/window_p5_size*frame_p5_size))]])
    points.append([[int(round(lasx/zoom_coeff-image_origin_x)),int(round(lasy/zoom_coeff-image_origin_y))]])
    points_for_original.append([[int(round((lasx-image_origin_x)/resize_coeff)),int(round((lasy-image_origin_y)/resize_coeff))]])
    #clicked_cell_position_marker=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]
###################################   
def erase_line():# in case you are not happy with your hand contour and want to delete it
    global cell_contour_fl, cell_contour_br, points,mask_hand, final_mask, points_for_original
    for i in range(len(cell_contour_fl)):        
         canvas_fluor_p5.delete(cell_contour_fl[i])
         canvas_bright_p5.delete(cell_contour_br[i])   
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    cell_number_in_mask=2**cell_number_in_frame
    final_mask[final_mask==cell_number_in_mask]=0
    points, points_for_original=[],[]
    cell_contour_fl, cell_contour_br=[],[]
    
############  ZOOMING FUNCTIONS ##########
###############################################
###############################################
def start_zoom():
    zoom_status.set("on")
    activate_buttons(all_buttons_page5,[button_activate_fast_edit_mode,button_activate_slow_edit_mode,start_pan_button])
    #button_activate_fast_edit_mode.configure(background =button_color)
    global my_image_fl, my_image_br, points, canvas_fluor_p5, canvas_bright_p5,photo_fluor, photo_bright, internal_frame_number,x0,y0
    points=[]
    frame_number=view_slider_p5.get()
    internal_frame_number_p5=frame_number-first_frame_number_p5
    ##########

    canvas_fluor_p5.delete("all")
    canvas_bright_p5.delete("all")
    ####################################
    global oval_x,oval_y,cell_center_visual_x,cell_center_visual_y
    print("cell_centre_visual_x,cell_center_visual_y START_ZOOM=",cell_center_visual_x,cell_center_visual_y)
    ####### place cell of interest in the center of window when start zooming
    x0, y0=clicked_cell_position_marker[0],clicked_cell_position_marker[1]#x0, y0 - for original photo  
    image_origin_x,image_origin_y= cell_center_visual_x-oval_x, cell_center_visual_y-oval_y
    #x0, y0=(300-image_origin_x)/zoom_coeff,(300-image_origin_y)/zoom_coeff#x0, y0 - for original photo
    #################################
    
    print("x0, yo=", x0, y0)
    print(" image_origin_x,image_origin_y=",  image_origin_x,image_origin_y)
       
    oval_x,oval_y= cell_center_visual_x, cell_center_visual_y
    canvas_bright_p5,canvas_fluor_p5, photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y)
    #oval_x,oval_y= (oval_x+image_origin_x)/zoom_coeff,(oval_y+image_origin_y)/zoom_coeff
       
    oval=canvas_fluor_p5.create_oval(oval_x-5, oval_y-5, oval_x+5,
                       oval_y+5, outline="magenta", width=1)    
    canvas_fluor_p5.bind('<MouseWheel>', wheel)
##############################################
def start_pan():
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.bind( "<ButtonPress-1>", drag_start)
    canvas_fluor_p5.bind("token<ButtonRelease-1>", drag_stop)
    canvas_fluor_p5.bind("<B1-Motion>", drag)
    activate_buttons(all_buttons_page5,[stop_pan_button])
#######################################
def stop_pan():
    canvas_fluor_p5.unbind_all("<Button-1>")  
    canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)
    activate_buttons(all_buttons_page5,[button_activate_fast_edit_mode,button_activate_slow_edit_mode])   
###############################################               
def drag_start(event):
        # start drag of an object
        # record the item`s location
        global x,y
        x = event.x
        y = event.y
#############################################
def drag_stop(event):
        """End drag of an object"""
        # reset the drag information 
        global x,y
        x = 0
        y = 0
################################################
def drag(event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        global x,y,image_origin_x, image_origin_y, cell_center_visual_x, cell_center_visual_y, oval, oval_x,oval_y
        delta_x = event.x - x
        delta_y = event.y - y
        print("delta_x, delta_y=", delta_x, delta_y)
       
        # record the new position
        x = event.x
        y= event.y
        # recalculater center of image_resized after dragging

        image_origin_x+=delta_x
        image_origin_y+=delta_y
        canvas_fluor_p5.delete("all")
        print("image_origin_x, image_origin_y after drag=", image_origin_x, image_origin_y)
        """
        x0, y0=(300-image_origin_x)/zoom_coeff,(300-image_origin_y)/zoom_coeff#x0, y0 - for original photo
        print("x0, y0=", x0, y0)
        """
        image_object=canvas_fluor_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_fluor)
        canvas_bright_p5.delete("all")
        canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
       
        print("bbox after dragging=", canvas_fluor_p5.bbox(image_object))
        cell_center_visual_x+=delta_x
        cell_center_visual_y+=delta_y 
        #global init_x,init_y# create magenta oval on clicked cell
        oval_x+=delta_x
        oval_y+=delta_y
        oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
##################################
def wheel(event):
        ''' Zoom with mouse wheel '''
        global  photo_fluor, my_image_fl,photo_bright, my_image_fl_resized, x0, y0,image_object, factor_in, factor_out, zoom_coeff, image_origin_x, image_origin_y, resize_coeff, new_shape 
        global oval_x_init, oval_y_init, oval_x,oval_y, factor
        if  event.delta == -120:  # scroll down
          factor_out*=0.8
          factor_in*=0.8
                  
          my_image_fl_resized=filled_fluor_copy.copy()
          my_image_fl_resized= cv2.resize(my_image_fl_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_fl_resized = cv2.resize(my_image_fl_resized,(int(my_image_fl_resized.shape[0] * factor_out ), int(my_image_fl_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)      
              
          my_image_br_resized=filled_bright_copy.copy()
          my_image_br_resized= cv2.resize(my_image_br_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)
          my_image_br_resized = cv2.resize(my_image_br_resized,(int(my_image_br_resized.shape[0] * factor_out ), int(my_image_br_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)   
          new_shape=my_image_fl_resized.shape[0]
   
          #############################################################         
        
          x0_new_out, y0_new_out=oval_x_init*factor_out,oval_y_init*factor_out
          photo_fluor =  turn_image_into_tkinter(my_image_fl_resized,new_shape)
          photo_bright =  turn_image_into_tkinter(my_image_br_resized,new_shape)            
          image_origin_x, image_origin_y= cell_center_visual_x-x0_new_out, cell_center_visual_y-y0_new_out
          canvas_fluor_p5.delete("all")
          canvas_bright_p5.delete("all")
          image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=photo_fluor)
          canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
          resize_coeff=new_shape/frame_p5_size
          zoom_coeff=new_shape/window_p5_size
          oval_x, oval_y= cell_center_visual_x, cell_center_visual_y
         
          factor=factor_out
          oval=canvas_fluor_p5.create_oval(oval_x-5*factor_out, oval_y-5*factor_out, oval_x+5*factor_out,
                       oval_y+5*factor_out, outline="magenta", width=1)
        if   event.delta == 120:  # scroll up
          factor_in*=1.2
          factor_out*=1.2
              
          my_image_fl_resized=filled_fluor_copy.copy()
          my_image_fl_resized= cv2.resize(my_image_fl_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_fl_resized = cv2.resize(my_image_fl_resized,(int(my_image_fl_resized.shape[0] * factor_out ), int(my_image_fl_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)      
         
       
          my_image_br_resized=filled_bright_copy.copy()
          my_image_br_resized= cv2.resize(my_image_br_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
          my_image_br_resized = cv2.resize(my_image_br_resized,(int(my_image_br_resized.shape[0] * factor_out ), int(my_image_br_resized.shape[1] * factor_out)), cv2.INTER_LINEAR)  
          #################################################
          new_shape=my_image_fl_resized.shape[0]
          #x0_new_in, y0_new_in=x0*factor_in,y0*factor_in
          x0_new_in, y0_new_in=oval_x_init*factor_in,oval_y_init*factor_in
          photo_fluor =  turn_image_into_tkinter(my_image_fl_resized,new_shape,[])
          photo_bright =  turn_image_into_tkinter(my_image_br_resized,new_shape,[])            
          canvas_fluor_p5.delete("all")
          canvas_bright_p5.delete("all")
          image_origin_x, image_origin_y= cell_center_visual_x-x0_new_in, cell_center_visual_y-y0_new_in
          image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=photo_fluor)
          canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
          zoom_coeff=new_shape/window_p5_size
          resize_coeff=new_shape/frame_p5_size
          #oval_x, oval_y=300-oval_x*factor_out,300-oval_y*factor_out 
          #new_oval_x,new_oval_y= x0*factor_in+image_origin_x,y0*factor_in+image_origin_y
          oval_x,oval_y= cell_center_visual_x, cell_center_visual_y
          oval=canvas_fluor_p5.create_oval(oval_x-5*factor_in, oval_y-5*factor_in, oval_x+5*factor_in,
                       oval_y+5*factor_in, outline="magenta", width=1)        
          factor=factor_in
        
###############################################
def start_drawing():    
    canvas_fluor_p5.unbind("all")
    #canvas.bind("<Button-1>", savePosn)
    canvas_fluor_p5.bind("<Button-1>",  get_x_and_y)
    canvas_fluor_p5.bind("<B1-Motion>", addLine)
    global points, points_for_original
    points=[]
    points_for_original=[]
##################################
#####################################################
def stop_zoom():
    #activate_slow_edit_mode()
    print("inside stop_zoom")
    global my_image_resized, tk_image, my_image, points, canvas_fluor_p5,canvas_bright_p5,photo_fluor, photo_bright
    canvas_fluor_p5.delete("all")
    canvas_bright_p5.delete("all")
    if points:# if you did hand drawing
      ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)#
      print("my_image_resized.shape=", my_image_resized.shape)
      cv2.drawContours(my_image_resized,[ctr],0,(255,255,255),2)
      ctr_origin = np.array(points_for_original).reshape((-1,1,2)).astype(np.int32)#
      cv2.drawContours(my_image,[ctr_origin],0,(255,255,255),2)
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_origin.tif", my_image)
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_zoom_resized.tif", my_image_resized)
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,0,0)
    #tk_image =  turn_image_into_tkinter(my_image_resized,window_p5_size)
    #canvas_fluor_p5.create_image(0,0, anchor="nw", image=tk_image)
    canvas_fluor_p5.unbind("all")
    global resize_coeff, new_shape
    resize_coeff=window_p5_size /frame_p5_size
    global  image_origin_x,image_origin_y, factor_in, factor_out,factor,zoom_coeff,delta_x,delta_y
    delta_x, delta_y=0,0
    factor_in, factor_out, factor=1,1,1
    image_origin_x,image_origin_y=0,0
    zoom_coeff=1
    new_shape=window_p5_size
    mode_variable.set("fast")
    oval=canvas_fluor_p5.create_oval(oval_x_init-5*factor, oval_y_init-5*factor, oval_x_init+5*factor,
                       oval_y_init+5*factor, outline="magenta", width=1)
    zoom_status.set("off")

    global cell_center_visual_x,cell_center_visual_y
    print("cell_centre_visual_x,cell_center_visual_y BEFORE=",cell_center_visual_x,cell_center_visual_y)
    cell_center_visual_x,cell_center_visual_y=300,300
    print("cell_centre_visual_x,cell_center_visual_y AFTER=",cell_center_visual_x,cell_center_visual_y)
################################################
def save_one_edited_cell():
    activate_buttons(all_buttons_page5,[view_slider_p5, button_final_movie])
    #button_activate_hand_drawing_mode_for_one_cell.configure(background = button_color)
    update_flash([view_slider_p5])
    button_activate_slow_edit_mode.configure(background = button_color) 
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, points, filled_fluor, filled_bright, filled_red
    if len(points)!=0:# if it was hand drawing    
       ctr = np.array(points_for_original).reshape((-1,1,2)).astype(np.int32)# turn drawn points into contour (ctr)
       #ctr = np.array(points).reshape((-1,1,2)).astype(np.int8)# turn drawn points into contour (ctr)
       cell_number_in_mask=2**cell_number_in_frame
       #print("cell_number_in_frame in SAVE_ONE_CELL=", cell_number_in_frame)
       #print("cell_number_in_mask in SAVE_ONE_CEWLL=", cell_number_in_mask)
       #final_mask[final_mask==cell_number+1]=0
       global final_mask
       #final_mask=remove_cell_from_mask(cell_number_in_frame, final_mask, intensity_dictionary_for_frame)
       #final_mask[final_mask==cell_number_scaled]=0
       # mask_hand - here you hand-draw new contour
       mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
      
       cv2.drawContours(mask_hand,[ctr],0,(255,255,255),-1)
       #print("np.max(mask_hand)=",np.max(mask_hand))
       
       #################################
       mask_hand_uint64= mask_hand.astype(np.uint64)
       #print("np.max(mask_hand) before=",np.max(mask_hand_uint64))
       mask_hand_uint64[mask_hand_uint64==255]=cell_number_in_mask
       #print("np.max(mask_hand) after=",np.max(mask_hand_uint64))
       #final_mask[mask_hand==255]=cell_number+1
       
       #final_mask[mask_hand==255]=cell_number_scaled
       final_mask+=mask_hand_uint64
       #print("np.max(final_mask)=",np.max(final_mask))
       #final_mask[mask_hand==255]=cell_indicator+1
       ######### need to get segmented_frame and segmented_patch here to pass to modified_cell_IDs                     
       segmented_frame= np.zeros((frame_p5_size+2*bordersize,frame_p5_size+2*bordersize),dtype="uint8")
       cv2.drawContours(segmented_frame,[ctr] , 0, 255, -1)
       im2, contours, hierarchy = cv2.findContours(segmented_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
       cell_contour=contours[0]                                
       M = cv2.moments(cell_contour) 
       if M["m00"]==0.:
          M["m00"]=0.001
       new_cX = np.round(M["m10"] / M["m00"],2)
       new_cY = np.round(M["m01"] / M["m00"],2)
       new_base=cv2.copyMakeBorder(segmented_frame , top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )
       a_new,b_new,c_new,d_new=int(round(new_cX))+bordersize-patch_size_p5,int(round(new_cX))+bordersize+ patch_size_p5,int(round(new_cY))+bordersize-patch_size_p5,int(round(new_cY))+bordersize+patch_size_p5           
       segmented_patch = new_base[c_new:d_new, a_new:b_new]
       #modified_cell_IDs[hand_cell_number]=[segmented_frame, final_mask, segmented_patch]
       #modified_cell_IDs[cell_number]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], cell_color, cell_ID]
       modified_cell_IDs[previous_cell_number]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], cell_color, cell_ID]  
       #########################################
       global oval
       canvas_fluor_p5.delete(oval)
       cv2.drawContours(filled_fluor,[ctr] , 0, cell_color, 1)
       cv2.drawContours(filled_bright,[ctr] , 0, cell_color, 1)
       cv2.drawContours(filled_red,[ctr] , 0, cell_color, 1)
       canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y)
       oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor,oval_x+5*factor,
                       oval_y+5*factor, outline="magenta",  width=1)             
       points=[]          
       dialog_label_5.config(text="If you want to hand draw  another cell, push Button 4 once again.\n If you are finished with the current frame, press Button 6."
                          "\nIf you are finished with the whole movie, press Button 7.")
    else:# if it was fast editing
        
      filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)     
      filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
      filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color)      
      filled_fluor,debug_fluor_image=paste_patch(filled_fluor,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)      
      filled_bright, debug_bright_image=paste_patch(filled_bright,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)
      filled_red, debug_red_image=paste_patch(filled_red,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)
            
      #### display  current frame with modified cell    
      #global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, oval     
      canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y)
      canvas_fluor_p5.delete(oval)      
      oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
    print("zoom_status=", zoom_status.get())
    if zoom_status.get()=="on":
          stop_zoom()
    
                    
#################################################
           

#############################################
def edit_by_clicking(event):
      number_of_clicks=[]# this is for flashing only
      #global segmentor, refiner     
      global manually_clicked_centroid, final_mask, a,b,c,d 
      #manually_clicked_centroid=[event.x/window_p5_size*frame_p5_size,event.y/window_p5_size*frame_p5_size]
      #manually_clicked_centroid=[int(round((event.x/zoom_coeff-image_origin_x)/(resize_coeff))),int(round((event.y/zoom_coeff-image_origin_y)/(resize_coeff)))]
      manually_clicked_centroid=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]
      #print("manually_clicked_centroid=", manually_clicked_centroid)
      #print("clicked_cell_positon_marker=", clicked_cell_position_marker)
      #print("centroid[0].dtype=",centroid[0].dtype)
      dialog_label_5.config(text=str(manually_clicked_centroid))
      number_of_clicks.append(manually_clicked_centroid)
      if len(number_of_clicks)==1:# it is only for flashing
          #update_flash([button_save_frame])
          print("update_flash")
      segmented_frame, segmented_patch,a,b,c,d, final_mask, new_centroid=segment_one_cell_at_a_time(segmentor, refiner,empty_fluor,empty_bright,manually_clicked_centroid, cell_radius_p5, frame_p5_size, patch_size_p5, clicked_cell_position_marker,final_mask,cell_number_in_frame, bordersize)
      ############## modify mask for frame
      new_cX, new_cY=new_centroid[0],new_centroid[1]
      mask_with_current_cell=paste_benchmark_patch(segmented_patch,a,b,c,d,cell_number_in_frame, frame_p5_size, bordersize)
      #print("cell_number_in_frame=", cell_number_in_frame)
      #print("np.max(mask_with_current_cell)=",np.max(mask_with_current_cell))
      cell_number_in_mask=2**cell_number_in_frame
      #final_mask[final_mask==cell_number_in_mask]=0
      final_mask=remove_cell_from_mask(cell_number_in_frame, final_mask, intensity_dictionary_for_frame)
      #final_mask[final_mask==cell_number+1]=0# delete previous contour of cell
      final_mask+=mask_with_current_cell# insert current contour of cell
      cv2.imwrite(r"C:\Users\helina\Desktop\segmented_patch.tif",segmented_patch)
      #final_mask_debug= final_mask.astype(np.uint8)
      #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_inside_edit.tif",final_mask_debug*200)
      ################### modify fluor, bright and red current frame
      global patch_with_contours
      patch_with_contours=prepare_contours(segmented_patch)    
      global filled_fluor_copy, filled_bright_copy, filled_red_copy
      ### here a very important dictionary of modified cells is created multiple times
      modified_cell_IDs[cell_number_in_frame]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], cell_color, cell_ID]      
      dialog_label_5.config(text="If you are unable to achieve good segmentation by just clicking, start hand drawing mode by pushing Button 4.")     
      
      filled_fluor_copy=delete_contour_with_specific_colour(filled_fluor_copy, empty_fluor,red_color)     
      filled_bright_copy=delete_contour_with_specific_colour(filled_bright_copy, empty_bright,red_color)
      filled_red_copy=delete_contour_with_specific_colour(filled_red_copy, empty_red,red_color)      
      filled_fluor_copy,debug_fluor_image=paste_patch(filled_fluor_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)      
      filled_bright_copy, debug_bright_image=paste_patch(filled_bright_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)
      filled_red_copy, debug_red_image=paste_patch(filled_red_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)
            
      #### display  current frame with modified cell    
      global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, oval     
      canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y)
      canvas_fluor_p5.delete(oval)      
      oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
                
#################################################

###################################################
def get_frame_info(internal_frame_number_p5):# for manual segmentation correction    
    print("frame_number inside get_frame_info=", frame_number)
    #internal_frame_number=frame_number-first_frame_number_p5
    print("internal_frame_number INSIDE GET_FRAME_INFO=", internal_frame_number_p5)
    global frame_dictionary
    frame_dictionary=lineage_per_frame_p5[internal_frame_number_p5]
    keys=list(frame_dictionary.keys())
    global intensity_dictionary_for_frame
    intensity_dictionary_for_frame=create_intensity_dictionary(len(keys))
    print("intensity_dictionary_for_frame inside get_frame_info=",  intensity_dictionary_for_frame)
    debug_frame_number=frame_dictionary["cell_0"][12]
    print("debug_frame_number=",debug_frame_number)
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
    modified_cell_IDs={}
    global mask, empty_fluor, empty_bright, empty_red
    mask=masks[internal_frame_number_p5]
    empty_fluor=empty_fluors[internal_frame_number_p5]
    empty_bright=empty_brights[internal_frame_number_p5]
    empty_red=empty_reds[internal_frame_number_p5]
    ###################################
    
    global path_filled_bright, path_filled_fluor,path_filled_red,path_mask
    path_filled_bright, path_filled_fluor,path_filled_red,path_mask= path_filled_brights[internal_frame_number_p5],path_filled_fluors[internal_frame_number_p5],path_filled_reds[internal_frame_number_p5],path_masks[internal_frame_number_p5]
    global final_mask,filled_fluor,filled_bright, filled_red
    filled_fluor=filled_fluors[internal_frame_number_p5]
    filled_bright=filled_brights[internal_frame_number_p5]
    filled_red=filled_reds[internal_frame_number_p5]
    final_mask=copy.deepcopy(mask)
      
    update_flash([])
    
    #button_frame_info.configure(background = "red")
    #global oval# create invisible magenta oval
    #oval= canvas_fluor_p5.create_oval(5-3, 5-3, 5+3,
                      # 5+3, outline="magenta", fill="magenta", width=2)  
################################################################
def save_edits_for_frame(): #saves all eduts in current frame and modifies linage for this frame
    global   frame_dictionary
    #number_of_slides_p5=[]    
    update_flash([view_slider_p5])
    print("internal_frame_number inside save_edits_for_frame=", internal_frame_number_p5)
    #button_frame_info.configure(background = button_color)     
    #button_save_frame.configure(background = 'red')
    ###################################
    frame_dictionary= lineage_per_frame_p5[internal_frame_number_p5]
    debug_item=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]
    #cv2.imwrite(r"C:\Users\helina\Desktop\patch_before.tif",debug_item)
    modified_frame_dictionary=update_frame_dictionary_after_manual_segm_correction(final_mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,frame_p5_size, patch_size_p5, bordersize)    
    lineage_per_frame_p5[internal_frame_number_p5]=modified_frame_dictionary
    debug_item_after=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]
    #cv2.imwrite(r"C:\Users\helina\Desktop\patch_after.tif",debug_item_after)
    ##################################################    
    modified_cells_keys=list(modified_cell_IDs.keys())
    for key in  modified_cells_keys:
       print("key=", key)
       new_cX,new_cY=modified_cell_IDs[key][3][0],modified_cell_IDs[key][3][1]
       cell_ID, cell_color=modified_cell_IDs[key][5],modified_cell_IDs[key][4]
       cv2.putText(filled_bright,cell_ID,(int(new_cX)-5,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,0.7, cell_color,1)
       cv2.putText(filled_fluor,cell_ID,(int(new_cX)-5,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,0.7, cell_color,1)
       cv2.putText(filled_red,cell_ID,(int(new_cX)-5,int(new_cY)+5),cv2.FONT_HERSHEY_PLAIN,0.7, cell_color,1)
    cv2.imwrite(path_filled_bright, filled_bright )# rewrite BRIGHT_MOVIE_RESULTS
    cv2.imwrite(path_filled_fluor, filled_fluor)# rewrite FLEORESCENT_MOVIE_RESULTS
    cv2.imwrite(path_filled_red, filled_red )# rewrite RED_MOVIE_RESULTS
    destin_mask_for_plot=np.round(final_mask)
    destin_mask_for_plot = destin_mask_for_plot.astype(np.uint64)
    cv2.imwrite(path_mask, destin_mask_for_plot) # rewrite MASKS)
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_inside_save_frame.tif",final_mask)
    ################### rewrite CLEANED_PATCHES
    cell_numbers=list(modified_cell_IDs.keys())
    for cell_number in cell_numbers:
       patch_path=create_name_for_cleaned_patch(path_filled_brights[internal_frame_number_p5], cell_number)
       print("patch_path=", patch_path)
       patch=modified_cell_IDs[cell_number][2]
       cv2.imwrite(os.path.join(output_dir,"HELPERS_(NOT_FOR_USER)","CLEANED_PATCHES",patch_path), patch)          
    ############################################
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y)         
    global photo_filled_fluors, photo_filled_brights, filled_fluors, filled_brights# update frames on the screen
    photo_filled_fluors[ internal_frame_number_p5]=photo_fluor
    photo_filled_brights[ internal_frame_number_p5]=photo_bright
    filled_fluors[ internal_frame_number_p5]=filled_fluor
    filled_brights[ internal_frame_number_p5]=filled_bright
    filled_reds[ internal_frame_number_p5]=filled_red
    masks[ internal_frame_number_p5]=final_mask
    
    canvas_fluor_p5.delete(oval)
    #button_save_frame.configure(background = button_color)
    dialog_label_5.config(text="You have 3 oprions now:\n  - Go to the next frame ( by using the slide bar) \n - Finish editing the movie (by pushing Button 7)"
                            "\n - Leave it for some other time (by clicking  Exit or Next")
       
#######################################
def create_final_movie():# create final movie + pedigree_per_cell (simplified, i.e. only centroids and areas)
  dialog_label_5.config(text="Creating lineage and final movie...")
  global output_dir,frame_p5_size 
  print("output_dir=", output_dir)  
  if edits_indicator=="yes":
    mode=mode_variable.get()
    if mode=="slow":
        save_hand_drawing_for_one_cell()
        activate_fast_edit_mode()
    save_edits_for_frame()
             
  update_lineage(lineage_per_frame_p5,output_dir, 'wb')
  dialog_label_5.config(text="Lineage per cell is stored in" +str(output_dir))
    
  lineage_per_cell=print_excel_files(output_dir, frame_p5_size,lineage_per_frame_p5, bordersize,patch_size_p5)
  dialog_label_5.config(text="Lineage per cell is stored in" +str(output_dir)+
                          "Creating final movie...")
  create_output_movie(output_dir, frame_p5_size)       
  dialog_label_5.config(text="Lineage per cell is stored in  " +str(os.path.join(output_dir,"lineage_per_cell.pkl"))+
                          "\nFinal movie is in  " + str(os.path.join(output_dir,"lineage_movie.avi")))
############### widgets in Page 5

global button_load_p5,button_activate_fast_edit_mode, button_activate_slow_edit_mode,\
                   start_zoom_button, start_pan_button,stop_pan_button,\
                   button_final_movie,view_slider_p5
    
button_load_p5 = Button(frame3_page5, text="1. Click to open file menu and choose OUTPUT folder", command=lambda:threading.Thread(target=choose_and_load_tracked_movie).start(), bg=button_color, font=all_font,activebackground="orange")
button_load_p5.pack(pady=5)

edit_label_fast = tk.Label(frame3a_page5, text=" FAST edit mode: by clicking",
                          fg="black",bg=label_color, font='TkDefaultFont 10 bold').pack(pady=5)
   
button_activate_fast_edit_mode = Button(frame3a_page5, text="3. Activate fast mode", command=activate_fast_edit_mode,bg=button_color, font=all_font,activebackground="red")
button_activate_fast_edit_mode.pack(pady=5)

#########################################################
edit_label_slow = tk.Label(frame3b_page5, text=" SLOW edit mode: by hand drawing",
                          fg="black",bg=label_color, font='TkDefaultFont 10 bold').pack(pady=5)
button_activate_slow_edit_mode = Button(frame3b_page5, text="4. Activate slow mode",  command=activate_slow_edit_mode,bg=button_color, font=all_font,activebackground="red")
button_activate_slow_edit_mode.pack(side=tk.LEFT, padx=10,pady=5)

###########################################
start_zoom_button = tk.Button(frame3b_page5, text="Start zoom", command=start_zoom,bg=button_color, font=all_font,activebackground="red")
start_zoom_button.pack(side=tk.LEFT)
#stop_zoom_button = tk.Button(frame3b_page5, text="Stop zoom", command=stop_zoom,bg=button_color, font=all_font,activebackground="red")
#stop_zoom_button.pack(side=tk.LEFT)
start_pan_button = tk.Button(frame3b_page5, text="Start pan", command=start_pan,bg=button_color, font=all_font,activebackground="red")
start_pan_button.pack(side=tk.LEFT)
stop_pan_button = tk.Button(frame3b_page5, text="Stop pan", command=stop_pan,bg=button_color, font=all_font,activebackground="red")
stop_pan_button.pack(side=tk.LEFT)
#############################################

global button_final_movie
button_final_movie = Button(frame7_page5, text="7. Create final movie\n and \nExcel files", command=create_final_movie,bg=button_color, font=all_font,activebackground="red")
button_final_movie.pack(pady=5)    
##################################
global view_slider_p5
view_slider_p5 = Scale(frame7c_page5, from_=1, to=1,orient=HORIZONTAL, troughcolor="green", command=slide_frames_p5, length=370)      
view_slider_p5.pack(pady=5)    
############################################
global all_buttons_page5
#label_edit = tk.Label(frame3_page4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow", width=50, height=4)
all_buttons_page5=[button_load_p5,button_activate_fast_edit_mode, button_activate_slow_edit_mode,\
                   start_zoom_button, start_pan_button,stop_pan_button,\
                   button_final_movie,view_slider_p5]


################################################################################
#####################################   PAGE 6: VISUALIZE RESULTS  #########################
###########################################
page6=pages[5]
page6.title("5. VISUALISE RESULTS")
page6.config(bg=bg_color)
######################################
frame1_page6 = tk.Frame(master=page6, width=1528, height=50, bg=bg_color)
frame1_page6.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page6 = tk.Frame(master=page6, width=1528, height=30, bg="blue")
frame2_page6.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page6 = tk.Frame(master=page6, width=1528, height=50, bg="yellow")
frame3_page6.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
########################################################
frame4_page6 = tk.Frame(master=page6, width=382, height=382, bg="green")
frame4_page6.grid(row=3, column=0, rowspan=1, columnspan=1)

frame5_page6 = tk.Frame(master=page6, width=382, height=382, bg="magenta")
frame5_page6.grid(row=3, column=1, rowspan=1, columnspan=1)

frame6_page6 = tk.Frame(master=page6, width=382, height=382, bg="orange")
frame6_page6.grid(row=3, column=2, rowspan=1, columnspan=1)
##############################################################

frame8_page6 = tk.Frame(master=page6, width=382, height=250, bg="cyan")
frame8_page6.grid(row=4, column=0, rowspan=1, columnspan=1)

frame9_page6 = tk.Frame(master=page6, width=382, height=250, bg="white")
frame9_page6.grid(row=4, column=1, rowspan=1, columnspan=1)

frame10_page6 = tk.Frame(master=page6, width=382, height=250, bg="yellow")
frame10_page6.grid(row=4, column=2, rowspan=1, columnspan=1)

###################################################################
frame11_page6 = tk.Frame(master=page6, width=1528, height=20, bg="navy")
frame11_page6.grid(row=5, column=0, rowspan=1, columnspan=3)

frame12_page6 = tk.Frame(master=page6, width=1528, height=20, bg="orange")
frame12_page6.grid(row=6, column=0, rowspan=1, columnspan=3)

frame13_page6 = tk.Frame(master=page6, width=1528, height=20, bg="blue")
frame13_page6.grid(row=7, column=0, rowspan=1, columnspan=3)

######################################################
canvas_bright = Canvas(frame4_page6, bg="green", height=382, width=382)
canvas_bright.pack(anchor='nw', fill='both', expand=True)

label_file_name=tk.Label(frame4_page6, text="this is label file_name", bg="black", fg="cyan")
label_file_name.pack(anchor='nw', fill='both', expand=True)

canvas_lineage = Canvas(frame5_page6, bg="magenta", height=382, width=382)
canvas_lineage.pack(anchor='nw', fill='both', expand=True)

canvas_patch = Canvas(frame6_page6, bg="orange", height=382, width=382)
canvas_patch.grid(row=0,column=0)

canvas_graph = Canvas(frame8_page6, bg="cyan", height=250, width=382)
canvas_graph.pack(anchor='nw', fill='both', expand=True)
############################   sub1   ############################################
label_title = tk.Label(frame1_page6, text="STEP 5: VISUALISE RESULTS",
              bg="yellow", fg="red", font=("Times", "24"))
label_title.grid(row=0, column=3, padx=500, sticky="n")
label_instr_name_p6=tk.Label(frame11_page6,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="red").pack()
############################## sub2 #####################
options_cells = [""]
global cell_ID, cell_property
cell_ID, cell_property = StringVar(page6),StringVar(page6)
cell_ID.set("Choose cell ID")
cell_property.set("Choose cell property")
global ffrom
ffrom=1
##############################################################
global extract_info_from_file_name

from postprocess import (sorted_aphanumeric, change_dict,extract_info_from_file_name, plot_per_cell_info,
              load_and_prepare_result_images)
from print_excel import extract_lineage,extract_const_movie_parameters
from interface_functions import turn_image_into_tkinter
##########################################
def create_display_images_p6():# plot images necessary for display       
        label_instruct_p6.config(text="\nCreating results ...\n\n\n")   
        still_lineage=cv2.imread(os.path.join( outpath,"still_lineage.tif"), -1)
        plot_per_cell_info(pedigree, outpath, still_lineage,label_instruct_p6, progress_bar,first_frame_number_p6)
        load_display_images_p6()        
#######################################
def retrieve_display_images_p6():# If display iamges were created before, upload them
        print("INSIDE RETRIEVE")       
        label_instruct_p6.config(text="\nRetrieving results ...\n\n\n")          
        load_display_images_p6()
 ######################################################
def load_display_images_p6():# load images for display that have already been created before 
      global keys,menu_cell_ID, progress_bar   
      keys=list(pedigree.keys())
      print("keys=", keys)
      #############
      
      menu_cell_ID.destroy()
      menu_cell_ID = OptionMenu(frame3_page6, cell_ID, *keys,  command= create_patch_slider)
      menu_cell_ID.pack(side=RIGHT, padx=200)
      menu_cell_ID.config(bg = label_color,font=all_font,activebackground="red")
      menu_cell_ID["menu"].config(bg=label_color,activebackground="red")
      ############
        
      ####################
      global red_patches, one_cell_patches, plots, bright_names
      label_instruct_p6.config(text="\nLoading results ...\n\n\n") 
      red_patches, one_cell_patches, plots, bright_names=load_and_prepare_result_images(outpath, keys, progress_bar)
      label_feedback_p6.grid(row=0, column=1, padx=10)
      #l_loaded.config(text="Created results for movie:\n"+ os.path.join(software_folder, input_movie_folder))
      label_feedback_p6.config(text="MOVIE:  "+ os.path.join(software_folder, input_movie_folder)+
                    "\nNUMBER OF FRAMES: "+ str(num_frames)+"                   FRAME SIZE: "+str(frame_size_p6)+" x "+str(frame_size_p6)+ "\nCELLS: "+str(list_of_cell_names))
      label_instruct_p6.config(text="1. Choose cell ID,\n2. Then choose cell property (Area, Perimeter, or Circularity."+
                          "\n3. Use scrollbar to explore results.")
      button_create.config(bg=button_color)
      global col_dict
      col_dict={"Area":["red", "yellow", "yellow"],"Perimeter":["yellow", "red", "yellow"],"Circularity":["yellow", "yellow", "red"]}
      update_flash([menu_cell_ID])
#############################################
def upload_processed_movie():# look if display images exist. If so, load them, if not - create them first and then load them.
    update_flash([])
    global progress_bar
    button_create.config(bg="red")
    global my_dir,out_folders, outpath, software_folder, options_cells, menu_cell_ID,input_movie_folder    
    my_dir = filedialog.askdirectory()# input movie folder (full path) 
    input_movie_folder = os.path.basename(my_dir)
    software_folder = os.path.dirname(my_dir)     
    outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
    label_instruct_p6.config(text="\nCreating results ...\n\n\n")    
    ################### load lineage_per_cell and constant movie params
    global pedigree, frame_size_p6, first_frame_number_p6, num_frames, list_of_cell_names
    pedigree_path=os.path.join(outpath,"lineage_per_cell.pkl")
    with open(pedigree_path, 'rb') as handle:
         pedigree = pickle.load(handle)   
       
    frame_size_p6, true_cell_radius_pickle, patch_size,max_number_of_cells,\
           num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number_p6,\
           base_colours,contrast_value,number_cells_in_first_frame,full_core_red_name, red_dictionary_p5,bordersize_p5,delta_p5=extract_const_movie_parameters(outpath)
    #############################################
    list_of_cell_names =list(pedigree.keys())
    w,h = 400,150 
    cell_info_folder=os.path.join(outpath,"HELPERS_(NOT_FOR_USER)","VISUALISATION_HELPERS", "PLOTS")
    if  len(os.listdir(cell_info_folder))==0:# display images are not existent, need to be created
      print("CREATE")
      ############################
      global  popup_create_display_images
      popup_create_display_images = tk.Toplevel(master=page6, bg=label_color)                        
      popup_create_display_images.geometry('%dx%d+%d+%d' % (w, h, (ws/2) - (w/2), (hs/2) - (h/2)))
      label_create = tk.Label(popup_create_display_images, text="Display images have not been created yet.|It mught take long to create them. \nPress OK to start.",width=400, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
      label_create.pack()                     
      button_create_p6 = Button(popup_create_display_images, text="OK",
      #bg=button_color,font='TkDefaultFont 14 bold', command=lambda:[popup_create_display_images.destroy(),create_display_images_p6()  ])
      bg=button_color,font='TkDefaultFont 14 bold',command=lambda:[ popup_create_display_images.destroy(), Thread(target=create_display_images_p6).start()])
      button_create_p6.pack()      
      ###########################      
    else:
      print("RETRIEVE")# diplay images are already there, just upload them
      global  popup_retrieve_display_images      
      label_instruct_p6.config(text="\nRetrieving results ...\n\n\n")        
      ############################
      popup_retrieve_display_images = tk.Toplevel(master=page6, bg=label_color)                        
      popup_retrieve_display_images.geometry('%dx%d+%d+%d' % (400, 159, (ws/2) - (w/2), (hs/2) - (h/2)))
      label_retrieve = tk.Label(popup_retrieve_display_images, text="Display images are already.|It should not take long to load them. \nPress OK to proceed.",width=400, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
      label_retrieve.pack()                     
      button_retrieve_p6 = Button(popup_retrieve_display_images, text="OK",
      bg=button_color,font='TkDefaultFont 14 bold', command=lambda:[popup_retrieve_display_images.destroy(),Thread(target=retrieve_display_images_p6).start()])
      button_retrieve_p6.pack()      
############################################
def slide_patch(value):  # value=frame number from patch_slider          
    canvas_bright.delete('all')
    canvas_lineage.delete('all')
    canvas_patch.delete('all')
    canvas_graph.delete('all')    
    print("INSIDE SLIDE_PATCH")
    
    print("ffrom=", ffrom)
    print("int(value)=",int(value))
    #frame_number=one_cell_patches[cell_ID.get()][0][1]
    internal_frame_number=int(value)-ffrom
    print("internal_image_number=", internal_frame_number)
    print("one_cell_patches.keys()=",one_cell_patches.keys())
    patch=one_cell_patches[cell_ID.get()][internal_frame_number][0]
  
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    global im_pil
    im_pil=turn_image_into_tkinter(patch_rgb, 382,[])    
    canvas_patch.create_image(0, 0, anchor=NW, image=im_pil)
    
    red_patch=red_patches[cell_ID.get()][internal_frame_number][0]
    global red_im_pil
    red_patch_rgb = cv2.cvtColor(red_patch, cv2.COLOR_BGR2RGB)   
    red_im_pil=turn_image_into_tkinter(red_patch_rgb, 382,[])
    canvas_lineage.create_image(0, 0, anchor=NW, image=red_im_pil)
    
    plott_pil=plots[cell_ID.get()][cell_property.get()][ internal_frame_number][0]
    global pl_pil
    pl_pil = Image.fromarray(plott_pil)
    pl_pil.thumbnail((382,382), Image.ANTIALIAS)
    pl_pil = ImageTk.PhotoImage(pl_pil)
    canvas_graph.create_image(0, 0, anchor=NW, image=pl_pil)    
    ######################################
    bright_name=bright_names[ int(value)-first_frame_number_p6]
    label_file_name.configure(text=os.path.basename(bright_name))
    bright_image=cv2.imread(bright_name, -1)

    bright_image_rgb = cv2.cvtColor(bright_image, cv2.COLOR_BGR2RGB)
    global bright_pil  
    bright_pil=turn_image_into_tkinter(bright_image_rgb, 382,[])
    canvas_bright.create_image(0, 0, anchor=NW, image=bright_pil)
    
   
    patch_slider.config(label="Frame "+str(value))  
        
    label_centr.config(text="Centroid: " +
              str(pedigree[cell_ID.get()][ internal_frame_number][3]))
    combination=col_dict[cell_property.get()]
    
    label_area.config(text="Area: " +
               str(pedigree[cell_ID.get()][internal_frame_number][4]), fg=combination[0])
    label_perim.config(text="Perimeter: " +
               str(pedigree[cell_ID.get()][internal_frame_number][5]), fg=combination[1])
    label_circ.config(text="Circularity: " +
               str(pedigree[cell_ID.get()][internal_frame_number][6]), fg=combination[2])
###########################################
def create_patch_slider(value):
  update_flash([])
  menu_cell_ID.config(fg=result_color,bg="black")
  print("Entering create_patch_slider")
  cell_property.set("Choose cell property")
  canvas_bright.delete('all')
  canvas_lineage.delete('all')
  canvas_patch.delete('all')
  canvas_graph.delete('all')
    
  cell_ID.set(value)
  key=cell_ID.get()
  print("key=", key)
  menu_cell_ID.config( bg="black",fg = result_color,font=all_font,activebackground="red")
  if key!="Choose cell ID":
    global ffrom, tto
    ffrom=pedigree[key][0][1]
    tto = pedigree[key][-1][1]
    #ffrom, tto = pedigree[key][0][1], pedigree[key][-1][1]
    print("ffrom=", ffrom)
    print("tto=", tto)
    global patch_slider
    patch_slider.destroy()
    patch_slider=Scale(frame10_page6,from_=ffrom,to=tto,orient=HORIZONTAL,troughcolor="#513B1C",label="Frame "+str(ffrom), command=slide_patch,
                 activebackground="red", bg=label_color,showvalue=0, font=all_font, length=380)
    #patch_slider.grid(row=0, column=0, sticky="e")
    patch_slider.pack(padx=10)
    
  update_flash([menu_cell_property])    
###########################################################
def display_first_patch(value):
    ffrom_1=str(ffrom)
    print("ffrom_1=", ffrom_1)    
    slide_patch(ffrom_1)
    patch_slider.set(ffrom_1)
    menu_cell_property.config( bg="black",fg = result_color,font=all_font,activebackground="red")
    update_flash([patch_slider])
######################################################
button_create = tk.Button(frame3_page6, text=" Upload_processed_movie",
                bg=button_color, font=all_font,command=upload_processed_movie)
button_create.pack()
#########################
global progress_bar
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='green', background='green')
progress_bar=ttk.Progressbar(frame3_page6, style="red.Horizontal.TProgressbar", orient="horizontal",
                length=280, mode="determinate")
progress_bar.pack(side=LEFT, padx=120)



global menu_cell_ID,menu_cell_property
menu_cell_ID = OptionMenu(frame3_page6, cell_ID, *options_cells,  command= create_patch_slider)
menu_cell_ID.pack(side=LEFT, padx=200)
menu_cell_ID.config(bg = label_color,font=all_font,activebackground="red")
menu_cell_ID["menu"].config(bg=label_color,activebackground="red")

options_properties = ["Area", "Perimeter", "Circularity"]
menu_cell_property = OptionMenu(frame3_page6, cell_property, *options_properties, command=display_first_patch)
menu_cell_property.pack( side=LEFT, padx=170)
menu_cell_property.config(bg = label_color, font=all_font,activebackground="red")
menu_cell_property["menu"].config(bg=label_color,activebackground="red")
###################
label_feedback_p6 = tk.Label(frame2_page6, text="\n\n\n"+
              "\nWhen menue opens click on the INPUT movie.",bg="black", fg="cyan", font=all_font, width=200, height=3)
label_feedback_p6.grid(row=0, column=0, sticky="w")
label_instruct_p6 = tk.Label(frame12_page6, text="Welcome to Step 5 of the pipeline!!!!\n\nIf you create result",bg="black", fg="yellow", font=all_font, width=200, height=5)
label_instruct_p6.grid(row=0, column=0, sticky="w")
###################################################################

#############################  sub3 #################
label_centr = tk.Label(frame9_page6, text="Centroid:",bg = "black", fg="yellow" , font=all_font)
label_centr.grid(row=0, column=0, pady=2)

label_area = tk.Label(frame9_page6, text="Area:", bg = "black", fg="yellow",font=all_font)
label_area.grid(row=1, column=0, pady=2)

label_perim = tk.Label(frame9_page6, text="Perimeter:", bg = "black", fg="yellow",font=all_font)
label_perim.grid(row=2, column=0, pady=2)

label_circ = tk.Label(frame9_page6, text="Circularity:", bg = "black", fg="yellow",font=all_font)
label_circ.grid(row=3, column=0,pady=(0,70))
#################################################
global patch_slider
    
patch_slider=Scale(frame10_page6,from_=ffrom,to=ffrom,orient=HORIZONTAL,troughcolor="#513B1C",label="Frame "+str(ffrom), command=slide_patch,
                 activebackground="red", bg=label_color,showvalue=0, font=all_font, length=370)
#patch_slider.grid(row=0, column=0, sticky="e")
patch_slider.pack(padx=(0,10))   
######################### This is the end of Page-6 #############
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
initial_buttons=[[button_choose_folder],[button_select],[button_load],[button_load_p5],[button_create]]

page_numbers=[page1,page2,page3,page4,page5, page6]

######################## locations of buttons Back, Exit and Next
locations=[frame3_page1,frame8_page2,frame15_page3,frame11_page4,frame8_page5,frame13_page6]
x_back,x_exit,x_next=700,750,800

######## make initial_buttons on each page flash and create back, exit, next buttons             
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
          #if i==2:
            #activate_buttons(all_buttons_page5,[button_load_p5])
            #activate_buttons(all_buttons_page4,[button_load])
          
             
      g_back=partial(update_flash,flash_buttons) 
      Button(location, text="Back",bg="orange",font=all_font, command=combine_funcs(f_back,g_back)).place(x=x_back,y=0)
            
      Button(frame2_page1, text= "GO TO STEP %s" % (i),bg=button_color,font=all_font,command=combine_funcs(f_next,g_next)).grid(row=1+i,column=0,pady=5, padx=200)
      Label(frame2_page1, text= "STEP %s: " % (i)+ page_titles[i][7:],bg="black",fg="yellow",font=all_font).grid(row=1+i,column=1,pady=5, padx=5)
    if i<5:
       f_next=partial(go_to_page,i+2)
       g_next=partial(update_flash,initial_buttons[i]) 
       Button(location, text="Next",bg="orange",font=all_font, command=combine_funcs(f_next,g_next)).place(x=x_next,y=0)      
    



win.mainloop()

