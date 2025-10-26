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

bg_color,all_font,button_color,result_color,label_color, slide_trough_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA","#513B1C"

win.config(bg=bg_color)
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: PROCESS MULTIPAGE TIFF", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING","PAGE 5: CORRECT SEGMENTATION", "PAGE 6: VISUALISE RESULTS"]
global page_number, software_folder
source_code_folder = os.getcwd()
print("source_code_folder=",source_code_folder)
software_folder=os. path. dirname(source_code_folder)
print("software_folder=",software_folder)
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
        if ii==5:
            activate_buttons(all_buttons_page6,[button_upload_p6])   
          
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
   print("path=", path)
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
button_save_movie=tk.Button(frame11_page2,text="3. Save processed movie",bg='#9ACD32',activebackground="red",font=all_font , command=lambda: [save_images_page2(movie_name,feedback_var_p2,bright_names,fluor_names,red_names, bright_images, fluor_images, red_images, instruct_var_p2, software_folder),\
        update_flash([]) ])
button_save_movie.pack()
l_instr_name_p2=tk.Label(frame7_page2,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="white").pack() 
l_feedback_p2=tk.Label(frame2_page2,textvariable=feedback_var_p2,bg="black", fg=result_color, font=all_font, height=8)
l_feedback_p2.pack(fill=BOTH) 
l_instruct_p2=tk.Label(frame7_page2,textvariable=instruct_var_p2 ,bg="black", fg="yellow", font=all_font, height=5)
l_instruct_p2.pack(fill=BOTH)  
l_fluor_announce_p2=tk.Label(frame5_page2,text="Fluorescent" ,bg=label_color, font=all_font).pack() 
l_bright_announce_p2=tk.Label(frame4_page2,text="Brightfield" ,bg=label_color, font=all_font).pack() 
l_red_announce_p2=tk.Label(frame9_page2,text="Red" ,bg=label_color, font=all_font).pack() 
l_fluor_name_p2=tk.Label(frame5_page2,textvariable=fl_name_p2,bg="black", fg=result_color, font=all_font,width=50, height=2).pack() 
l_bright_name_p2=tk.Label(frame4_page2,textvariable=br_name_p2 ,bg="black", fg=result_color, font=all_font,width=50, height=2).pack() 
l_red_name_p2=tk.Label(frame9_page2,textvariable=red_name_p2,bg="black", fg=result_color, font=all_font,width=50, height=2).pack()
###################### 
global all_buttons_page2
all_buttons_page2=[button_choose_folder,button_save_movie]
###########################################################################
############################   PAGE 3 : CUT WELL  ##############################
###############################################################################
page3=pages[2]
global  canvas_size_p3
canvas_size_p3=400

frame1_page3 = tk.Frame(master=page3, width=1530, height=50, bg=bg_color)
frame1_page3.grid(row=0, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame2_page3 = tk.Frame(master=page3, width=1530, height=50, bg=bg_color)
frame2_page3.grid(row=1, column=0,rowspan = 1, columnspan = 3,sticky = W+E+N+S)

frame3_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame3_page3.grid(row=2,column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame4_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame4_page3.grid(row=2, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame5_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=30, bg=bg_color)
frame5_page3.grid(row=2, column=2,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame6_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame6_page3.grid(row=3,column=0,rowspan = 1, columnspan = 1,sticky =  W+E+N+S)

frame7_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame7_page3.grid(row=3, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame8_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=canvas_size_p3, bg=bg_color)
frame8_page3.grid(row=3, column=2,rowspan = 1, columnspan = 1,sticky =  W+E+N+S)

frame9_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=200, bg=bg_color)
frame9_page3.grid(row=4, column=0,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame10_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=200, bg=bg_color)
frame10_page3.grid(row=4, column=1,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

frame11_page3 = tk.Frame(master=page3, width=canvas_size_p3, height=200, bg=bg_color)
frame11_page3.grid(row=4, column=2,rowspan = 1, columnspan = 1,sticky = W+E+N+S)

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
canvas_left.pack()
canvas_mid = Canvas(frame7_page3, bg=bg_color, height=canvas_size_p3, width=canvas_size_p3)
canvas_mid.pack()
canvas_right = Canvas(frame8_page3, bg=bg_color, height=canvas_size_p3, width=canvas_size_p3)
canvas_right.pack()
###################################################
global popup_mid, popup_right,popup_canvas_size_p3
popup_mid, popup_right, popup_canvas_size_p3=None, None, 800
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
feedback_dict={"s":" ","im":" ","fl":" ","br":" ","red":" ","w":" ", "dest":" ", "first":" ", "last":" "}
feedback_text=update_feedback_text(feedback_dict)
feedback_var_p3.set(feedback_text)
instruct_var_p3.set(" Step 2 allows you to cut out a well of interest out of initial cell movie. \n\nTo choose raw movie , press Button 1."
                    "\nThen, navigate to your raw movie, open it and click on ANY BRIGHT field image")
##############################################
def prepare_file_name_for_show(old_name):
    name =os.path.basename(old_name)
    index_t =name.find("_t")        
    split_name =name[:index_t+1]+" \n"+name[index_t+1:]
    return split_name
##################################################

################################
def select_one_bright():# load all frames,display clicked bright frame    
    global my_path, my_destin, bright_names_sorted,fluor_names_sorted, red_names_sorted,clicked_number, first_filename_for_show 
    my_path =filedialog.askopenfilename()
    print("INSIDE SELECT_ONE_BRIGHT")
    print("my_path=", my_path)
    #############################################
    first_filename_for_show=prepare_file_name_for_show(my_path)
    print(" first_filename_for_show=", first_filename_for_show)
    l_left_canvas.config(text=first_filename_for_show)
    #l_left_canvas.config(text=os.path.basename(my_path)) 
    ####################################################    
    raw_movie_dir =os.path.dirname(my_path)
    print("raw_movie_dir =", raw_movie_dir )
    feedback_dict["s"]=raw_movie_dir
    
    bright_names_sorted,fluor_names_sorted, red_names_sorted =load_image_names(raw_movie_dir)
    
    
    feedback_dict["fl"],feedback_dict["br"],feedback_dict["red"]=str(len(fluor_names_sorted)),str(len(bright_names_sorted)),str(len(red_names_sorted))
    ##########################################
    global n_digits_p3,first_frame_number_p3
    full_core_fluor_name_p3, n_digits_p3, first_frame_number_p3= extract_file_name(fluor_names_sorted[0])
   
    feedback_dict["first"]=str(first_frame_number_p3)
    feedback_dict["last"]=str(first_frame_number_p3+len(fluor_names_sorted)-1)
    ###################################################         
    global list_of_red_frame_numbers
    list_of_red_frame_numbers =extract_red_frame_numbers(red_names_sorted)
    print("list_of_red_frame_numbers=", list_of_red_frame_numbers) 
    ##############################################    
   
    print("software_folder=", software_folder)
   
    raw_movie_norm = os.path.normpath(raw_movie_dir)
    check_list=raw_movie_norm.split(os.sep)
    if "DeepKymoTracker" in check_list:
            movie_name=check_list[-2]     
    else:
            movie_name=check_list[-1]
    print("movie_name =", movie_name )
    general_movie_folder_path =os.path.join(software_folder,"MOVIES",movie_name)
    print("general_movie_folder_path  =", general_movie_folder_path  )
    if not os.path.exists(general_movie_folder_path):
      os.mkdir(general_movie_folder_path)
    my_destin=os.path.join( general_movie_folder_path ,"ONE_WELL_MOVIE_"+movie_name)
    print("my_destin =", my_destin )
    if not os.path.exists(my_destin):
      os.mkdir(my_destin)
    #############################################
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
                    "\nThe thresholded image will appear in the middle window.")    
    update_flash([])
    activate_buttons(all_buttons_page3,[])
####################################################

#path_norm = os.path.normpath(path)
#comp_list=path_norm.split(os.sep)
################################################
def measure_intensities(event):# draw red circles on well borders to measure intensities
    global red_point_coords
    global intensities
    canvas_left.create_oval(event.x-2,event.y-2,event.x+2,event.y+2,outline = "red",fill = "red",width = 2)
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
                       "\nImprove thresholded image if necessary by using threshold slider."
                       "\nFinally, click on the well of interest.")
    update_flash([threshold_slider])
    activate_buttons(all_buttons_page3,[threshold_slider])    
    canvas_mid.bind("<Button-1>", choose_well)
    first_filename_for_show=prepare_file_name_for_show(my_path)
    l_mid_canvas.config(text=first_filename_for_show)
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
    print("INSIDE CHOOSE_WELL")
    canvas_mid.delete(green_blob)
    global seed, seeds    
    green_blob=canvas_mid.create_oval(event.x-1,event.y-1,event.x+1,event.y+1,outline = "green",fill = "green",width = 5)
    seed=(int(event.x*thresh.shape[1]/canvas_size_p3), int(event.y*thresh.shape[0]/canvas_size_p3))
    seeds.append(seed)    
    im_thr=thresh.copy()
    _,contours_before, hierarchy = cv2.findContours(im_thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print("len(contours_before)=", len(contours_before)) 
    mask=None
    fill_image=cv2.floodFill(im_thr, mask, seed, 255,flags=8)# here you define the centre of the well (there are 4 in total)
    fill_image = thresh | im_thr
    fill_image-=thresh   
    closing = cv2.morphologyEx(fill_image, cv2.MORPH_CLOSE, (5,5))    
    _,contours, hierarchy = cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    cnt=contours[0]
  
    print("len(contours)=", len(contours))    
    global first_rect,first_x0, first_box, angle  
    first_rect = cv2.minAreaRect(cnt)
    angle, first_box=calculate_angle(first_rect)      
    first_x0=first_box[0][0]    
    global  well_size, popup_image_size_p3   
    x0,y0,x1,y1,x2,y2,x3,y3=first_box[0][0],first_box[0][1],first_box[1][0],first_box[1][1],\
                            first_box[2][0],first_box[2][1],first_box[3][0],first_box[3][1]    
    size_1=math.sqrt(((x1-x0)**2+(y1-y0)**2))
    size_2=math.sqrt(((x2-x1)**2+(y2-y1)**2))
    well_size=int(round(max(size_1,size_2)))
    print("well_size=", well_size)
    popup_image_size_p3=int(round(image_size_p3[0]*popup_canvas_size_p3/well_size))  
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
 instruct_var_p3.set("It is important to manually correct shift in Frame 1. Push Button 4 to get a magnified version of the frame.")
 global canvas_mid 
 canvas_mid.delete("all") 
#################### draw temp image (binary) to rotate it and find rect_new
 temp=np.zeros(clicked_bright.shape, np.uint8)
 cv2.drawContours(temp,[first_box],0,255,-1)
 dst = cv2.warpAffine(temp,M_first,(cols,rows))
####################  4. calculate its borders   
 _,contours_new, hierarchy = cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 cnt_new=contours_new[0]
 rect_new = cv2.minAreaRect(cnt_new)             
 box_final = cv2.boxPoints(rect_new)# horisontal well    
 box_final = np.int0(np.round(box_final))
 xs=[box_final[k][0] for k in range(4)]
 ys=[box_final[k][1] for k in range(4)]
 global x_min_first, y_min_first, x0,y0,x1,y1
 x_min_first, y_min_first=min(xs),min(ys)
 ###########################
 x_min_popup,y_min_popup=int(round(x_min_first*popup_canvas_size_p3/well_size)),int(round(y_min_first*popup_canvas_size_p3/well_size))
 #############################
 global rot_bright
 rot_bright = cv2.warpAffine(clicked_bright,M_first,(cols,rows))
 global cut_bright
 cut_bright=rot_bright[y_min_first:y_min_first+well_size, x_min_first:x_min_first+well_size]
 global final_s, finalImage_small
 final_s=turn_image_into_tkinter(cut_bright, canvas_size_p3,[]) 
 finalImage_small=canvas_mid.create_image(0,0, anchor=NW, image=final_s) 
 canvas_mid.unbind("<Button-1>")
 update_flash([button_first_shift_edit])
 activate_buttons(all_buttons_page3,[button_first_shift_edit ])
 threshold_slider.config(troughcolor=slide_trough_color, bg=label_color)   
###############################################              
def drag_start_p2(event):              
        global x_mouse,y_mouse
        x_mouse = event.x
        y_mouse = event.y       
#############################################
def drag_image_p2(event,canvas,imageObject):        
        global x_mouse,y_mouse, x_last,y_last     
        dx = event.x - x_mouse
        dy = event.y - y_mouse
        canvas.move(imageObject, dx,dy)
        canvas.update()      
        # record the new position
        x_mouse = event.x
        y_mouse= event.y
        x_last-=dx
        y_last-=dy               
######################################################
def edit_first_frame_shift():  
    global popup_mid, canvas_popup_mid   
    popup_mid = tk.Toplevel(master=page3,  bg=bg_color)
    popup_mid.geometry('%dx%d+%d+%d' % (popup_canvas_size_p3, popup_canvas_size_p3+200, 0, 0))
    frame1 = tk.Frame(master=popup_mid, width=popup_canvas_size_p3, height=popup_canvas_size_p3)
    frame1.pack()
    frame2 = tk.Frame(master=popup_mid, width=popup_canvas_size_p3, height=50)
    frame2.pack()
    canvas_popup_mid = Canvas(frame1, height=popup_canvas_size_p3, width=popup_canvas_size_p3, bg=bg_color)
    canvas_popup_mid.pack(anchor='nw', fill='both', expand=True)
    ##########################################
    l_popup_first=tk.Label(frame1,text=first_filename_for_show, bg="black", fg="cyan", font=("Times", "12"))
    l_popup_first.pack(fill=BOTH)    
    l_instruct_popup_first=tk.Label(frame1,text="Correct well shift, if necessary, by dragging image with mouse. Once you have finished, click Close button.",
                 bg="black", fg="yellow", font=all_font, height=5)
    l_instruct_popup_first.pack(fill=BOTH)
        
    #######################################
    def close_and_flash():
        update_flash([button_bright])
        activate_buttons(all_buttons_page3,[button_bright])
        instruct_var_p3.set("Shift in Frame 1 has been saved.\nNow, push Button 5 to cut wells from ALL brightfield frames.")                     
        popup_mid.destroy()
        button_first_shift_edit.config(bg=button_color)
    global button_close
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command=close_and_flash)
    button_close.pack() 
   
    global  x_last,y_last, br_image,  x_min_popup, y_min_popup,delta_x,delta_y  
    x_min_popup, y_min_popup=int(round(x_min_first*popup_canvas_size_p3/well_size)),int(round(y_min_first*popup_canvas_size_p3/well_size))   
    x_last,y_last=  x_min_popup, y_min_popup
    delta_x, delta_y=0,0
       
    global new_name
    head, tail=os.path.split(my_path)
    new_name=os.path.join(my_destin,tail)
    ###################################
    final_bright, rot_bright=cut_well_in_manual_shift(clicked_bright,x_min_first,y_min_first,well_size, M_first, cols, rows)    
    br_image=rot_bright   
    global image1,imageFinal_big   
    canvas_popup_mid.delete("all")
    image1=turn_image_into_tkinter(br_image, popup_image_size_p3,[])
    imageFinal_big = canvas_popup_mid.create_image(- x_min_popup, - y_min_popup, image = image1,anchor='nw')
    ##################################################
    global drag_start_p2,drag_image,drag_stop_p2 , cut_and_save_patch
    canvas_popup_mid.unbind_all("<ButtonRelease-1>")
    canvas_popup_mid.bind( "<ButtonPress-1>", drag_start_p2)   
    canvas_popup_mid.bind("<ButtonRelease-1>", lambda event: cut_and_save_patch(event))
    canvas_popup_mid.bind("<B1-Motion>", lambda event: drag_image_p2( event,canvas_popup_mid, imageFinal_big))    
    update_flash([button_close])
    button_first_shift_edit.config(bg="red")    
##################################################
def cut_and_save_patch(event):
    global br_image, new_name,x_last, y_last,  x_min_popup, y_min_popup, delta_x, delta_y
    global canvas_mid, canvas_popup_mid
    xx,yy=int(round(x_last*image_size_p3[0]/popup_image_size_p3)),int(round(y_last*image_size_p3[1]/popup_image_size_p3))    
    patch=br_image[yy:yy+well_size, xx:xx+well_size]
    patch_1=patch.copy()       
    cv2.imwrite(new_name, patch)# save in INPUT folder
    global tk_patch, image2, imageFinal_big 
    tk_patch=turn_image_into_tkinter(patch, popup_canvas_size_p3,[])      
    canvas_popup_mid.delete("all")
    imageFinal_big=canvas_popup_mid.create_image(0,0, image = tk_patch,anchor='nw')

    image2=turn_image_into_tkinter(patch_1, canvas_size_p3,[])    
    canvas_mid.create_image(0, 0, image = image2,anchor='nw')
    # the whole point of correcting shift in Frame 1 was to obtain delta_x, delta_y
    # delta_x, delta_y take into account shift in Frame 1 when cutting all bright wells 
    delta_x, delta_y=int(round((x_last- x_min_popup)*image_size_p3[0]/popup_image_size_p3)),int(round((y_last- y_min_popup)*image_size_p3[1]/popup_image_size_p3))    
##################################
def cut_bright_wells():# Button 5. Apply to all bright
  update_flash([])
  button_bright.config(bg="red")
  instruct_var_p3.set("Processing bright field frames....")  
  global rotation_matrices,destin_br_names, rotated_images, boxes, final_boxes
  rotation_matrices, destin_br_names, rotated_images=[],[],[]
  boxes, final_boxes=[],[]

  for k in range(len(bright_names_sorted)):            
    progressbar_page3["value"]=(k+1)/(len(bright_names_sorted))*100        
    time.sleep(0.02)
    frame5_page3.update_idletasks()   
    bright_name=bright_names_sorted[k]
    bright_name_for_show=prepare_file_name_for_show(bright_name)
    l_right_canvas.config(text=bright_name_for_show)
    bright_image=cv2.imread(bright_name,-1)  
    final_bright,M,x_min,y_min, rows, cols, rot_indicator, rot_bright=cut_well_from_image(bright_image,seed,well_size,first_x0, delta_x, delta_y, first_rect)
    #print("final_bright.shape,final_bright.dtype=",final_bright.shape,final_bright.dtype)
    final_bright_tk=turn_image_into_tkinter(final_bright, canvas_size_p3,[])
    canvas_right.delete("all")
    canvas_right.create_image(0,0, anchor=NW, image=final_bright_tk)
    rotation_matrices.append((M,x_min,y_min, rows, cols, rot_indicator))
    
    rotated_images.append(rot_bright)    
    head, tail=os.path.split(bright_name)   
    destin_br_name=os.path.join(my_destin,tail)
    destin_br_names.append(destin_br_name)       
    cv2.imwrite(destin_br_name, final_bright)
    if k==0:
        global first_tk, first
        first=final_bright       
        first_tk=turn_image_into_tkinter(first, canvas_size_p3,[])
  global frame_slider    
  frame_slider=Scale(frame11_page3,from_=first_frame_number_p3,to=len(bright_names_sorted)+first_frame_number_p3-1,orient=HORIZONTAL,troughcolor=slide_trough_color,bg=label_color,font=all_font,activebackground="red",label="Frame "+str(first_frame_number_p3), command=slide_p3, length=canvas_size_p3, showvalue=0)
  frame_slider.pack(side=tk.TOP, pady=5)
  #######################
  global  bright_dictionary_p2 
  bright_dictionary_p2=create_name_dictionary_p4(destin_br_names)  
  threshold_slider.config(bg=label_color) 
  instruct_var_p3.set("Scroll through frames to ensure that the well fits completely into each frame.\nTo get a better view of each frame, push Button 6 to launch editing window.")
  button_bright.config(bg=button_color)
  update_flash([button_shift_edit])
  activate_buttons(all_buttons_page3,[button_shift_edit ])          
  canvas_right.delete("all")
  canvas_right.create_image(0,0, anchor=NW, image=first_tk)
  first_bright_name_for_show=prepare_file_name_for_show(bright_names_sorted[0])
  l_right_canvas.config(text=first_bright_name_for_show)           
##########################################
def start_editing_frames():#   
    global popup_right, canvas_popup_right, l_popup_canvas    
    popup_right = tk.Toplevel(master=page3,  bg=bg_color)
    popup_right.geometry('%dx%d+%d+%d' % (popup_canvas_size_p3, popup_canvas_size_p3+210, 0, 0))   
    frame1 = tk.Frame(master=popup_right, width=popup_canvas_size_p3, height=popup_canvas_size_p3, bg=bg_color)
    frame1.pack()
    frame2 = tk.Frame(master=popup_right, width=popup_canvas_size_p3, height=50, bg=bg_color)
    frame2.pack()
    canvas_popup_right = Canvas(frame1, height=popup_canvas_size_p3, width=popup_canvas_size_p3, bg="black")
    canvas_popup_right.pack(anchor='nw', fill='both', expand=True)
    
    l_popup_canvas=tk.Label(frame2,text= "bright frame", bg="black", fg="cyan", font=("Times", "12"))
    l_popup_canvas.pack()  
    
    global frame_pop_slider, first_tk_pop    
    frame_pop_slider=Scale(frame2,from_=first_frame_number_p3,to=len(bright_names_sorted)+first_frame_number_p3-1,orient=HORIZONTAL,troughcolor="#513B1C",bg=label_color,font=all_font,activebackground="red",label="Frame "+str(first_frame_number_p3), command=slide_p3, length=popup_canvas_size_p3, showvalue=0)
    frame_pop_slider.pack()
    frame_pop_slider.set(first_frame_number_p3)
    frame_slider.set(first_frame_number_p3)
    slide_p3(first_frame_number_p3)
    
    l_instruct_popup=tk.Label(frame2,text="Scroll through frames to ensure that the well fits completely into each frame.\nIf it does not, drag the image with the mouse to correct well shift in the current frame.Do it for as many frames as necessary."
                 "\nFinally, close the popup window" ,bg="black", fg="yellow", font=all_font, height=5)
    l_instruct_popup.pack(fill=BOTH)  
    def destroy_popup():
        global popup_right      
        progressbar_page3["value"]=0
        update_flash([button_fluor])
        popup_right.destroy()
        popup_right=None
        instruct_var_p3.set("Your manual corrections in all brightfield frames have been saved.\nNow, press Button 7 to cut the well from all fluorescent and red frames.")
        button_shift_edit.config(bg=button_color) 
        activate_buttons(all_buttons_page3,[button_fluor]) 
        
    button_close=tk.Button(frame2,text="Close",bg='#9ACD32',activebackground="red",font='TkDefaultFont 10 bold' , command= destroy_popup)
    button_close.pack()    
    l_popup_canvas.config(text=os.path.basename(bright_names_sorted[0]))
    
    global image1, new_name, imageFinal_curr
    new_name=destin_br_names[0]
    br_image= rotated_images[0]
    item=rotation_matrices[0]  
    M,x_min,y_min,row,cols, rotation_indicator=item[0],item[1],item[2],item[3],item[4], item[5]       
    x_min_popup, y_min_popup=int(round(x_min*popup_canvas_size_p3/well_size)),int(round(y_min*popup_canvas_size_p3/well_size))
    image1=turn_image_into_tkinter(br_image, popup_image_size_p3,[])      
    imageFinal_curr = canvas_popup_right.create_image(- x_min_popup, - y_min_popup, image = image1,anchor='nw')    
    canvas_popup_right.bind( "<ButtonPress-1>", drag_start_p2)
    canvas_popup_right.bind("<ButtonRelease-1>", lambda event: cut_and_save_current(event))   
    canvas_popup_right.bind("<B1-Motion>", lambda event: drag_image_p2( event,canvas_popup_right, imageFinal_curr))
    update_flash([])
    button_shift_edit.config(bg="red")           
 ###########################################################
def cut_and_save_current(event):#"<ButtonRelease>"   
    # cut and save bright well in INPUT folder
    global  br_image, new_name, x_last, y_last
    xx,yy=int(round(x_last*image_size_p3[0]/popup_image_size_p3)),int(round(y_last*image_size_p3[1]/popup_image_size_p3))    
    patch=br_image[yy:yy+well_size, xx:xx+well_size]
    cv2.imwrite(new_name, patch)# save in INPUT folder   
    ###############################################
    # modify and save rotation_matrix for current frame       
    current_frame_number=frame_pop_slider.get()
    print("current_frame_number=", current_frame_number)
    item=rotation_matrices[current_frame_number-1] 
    M,x_min,y_min,row,cols, rotation_indicator=item[0],item[1],item[2],item[3],item[4], item[5]
    new_item=(M, xx,yy,rows,cols, rotation_indicator)  
    rotation_matrices[current_frame_number-1]=new_item
    #######################################
    #  display modified frame in both canvases
    global tk_patch, image2, canvas_popup_right, canvas_right, imageFinal_curr 
    tk_patch=turn_image_into_tkinter(patch, popup_canvas_size_p3,[])      
    canvas_popup_right.delete("all")
    canvas_popup_right.create_image(0,0, image = tk_patch,anchor='nw')
    patch_1=patch.copy()
    image2=turn_image_into_tkinter(patch_1, canvas_size_p3,[])    
    imageFinal_curr=canvas_right.create_image(0, 0, image = image2,anchor='nw') 
###################################### 
global destin_fl_names, destin_red_names
destin_fl_names,destin_red_names= None, None
global frame_pop_slider
frame_pop_slider=None
######################### scroll through all images
def slide_p3(value): 
       image_number = int(value)# without 0 digits on slider
       frame_slider.config(label="Frame "+str(value))
       image_number_zfill=str(value).zfill(n_digits_p3)                    
       canvas_right.delete("all")
       ################################################                 
       global br_final      
       br_path=destin_br_names[image_number-first_frame_number_p3-1]
       br_final, br_name=display_image_p4_fix_missing(image_number_zfill,bright_dictionary_p2, canvas_size_p3)                           
       canvas_right.create_image(0,0, anchor=NW, image=br_final)
       br_name_for_show=prepare_file_name_for_show(br_name)
       l_right_canvas.config(text=br_name_for_show)
       ##############################################       
       if destin_fl_names:
          canvas_mid.delete("all")
          global fl_final
          #fl_path=new_fl_names[image_number-first_frame_number_p3]          
          fl_final, fl_name=display_image_p4_fix_missing(image_number_zfill,fluor_dictionary_p2, canvas_size_p3)                           
          canvas_mid.create_image(0,0, anchor=NW, image=fl_final)
          fl_name_for_show=prepare_file_name_for_show(fl_name)
          l_mid_canvas.config(text=fl_name_for_show)
       ##############################################
       if destin_red_names:
          canvas_left.delete("all")
          global red_final
          #red_path=new_red_names[image_number-first_frame_number_p3]         
          red_final, red_name=display_image_p4_fix_missing(image_number_zfill,red_dictionary_p2, canvas_size_p3)                           
          canvas_left.create_image(0,0, anchor=NW, image=red_final)
          red_name_for_show=prepare_file_name_for_show(red_name)
          l_left_canvas.config(text=red_name_for_show)
       if popup_right:
          canvas_popup_right.delete("all") 
          item=rotation_matrices[image_number-first_frame_number_p3]
          x_min,y_min=item[1],item[2]       
          global  x_last,y_last, rotated_images, br_image
          #x0,y0=x_min, y_min
          x_min_popup, y_min_popup=int(round(x_min*popup_canvas_size_p3/well_size)),int(round(y_min*popup_canvas_size_p3/well_size))   
          x_last,y_last=  x_min_popup, y_min_popup
          global image1, new_name, imageFinal_curr
          new_name=destin_br_names[image_number-first_frame_number_p3]
          br_image= rotated_images[image_number-first_frame_number_p3]             
          image1=turn_image_into_tkinter(br_image, popup_image_size_p3,[])      
          imageFinal_curr = canvas_popup_right.create_image(- x_min_popup, - y_min_popup, image = image1,anchor='nw')         
          frame_pop_slider.config(label="Frame "+str(value))         
          l_popup_canvas.config(text=os.path.basename(bright_names_sorted[image_number-first_frame_number_p3]))
##################### activate editing frame shift for current frame in canvas_right  
def cut_fluor_wells():#cut fluor and red wells
 instruct_var_p3.set("Processing fluorescent and red frames....") 
 update_flash([]) 
 button_fluor.config(bg="red")
 #progressbar_fluor = ttk.Progressbar(frame10_page3, orient='horizontal',mode='determinate',length=280)
 #progressbar_fluor.pack()
    
 global rotation_matrices,destin_fl_names,destin_red_names, first_tk_fl 
 destin_fl_names, destin_red_names = [], []
 for k in range(len(fluor_names_sorted)):
    progressbar_page3["value"]=(k+1)/(len(fluor_names_sorted))*100        
    time.sleep(0.02)
    frame5_page3.update_idletasks()  
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
    destin_fl_name=os.path.join(my_destin,tail)
    destin_fl_names.append(destin_fl_name)   
    cv2.imwrite(destin_fl_name, final_fluor)
    final_fluor_tk=turn_image_into_tkinter(final_fluor, canvas_size_p3,[])
    canvas_mid.delete("all")
    canvas_mid.create_image(0,0, anchor=NW, image=final_fluor_tk)
    l_mid_canvas.config(text=os.path.basename(fluor_name))
    ###############################
    if k+first_frame_number_p3 in list_of_red_frame_numbers:
      index=list_of_red_frame_numbers.index(k+first_frame_number_p3) 
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
      destin_red_name=os.path.join(my_destin,tail)
      destin_red_names.append(destin_red_name)   
      cv2.imwrite(destin_red_name, final_red)      
    else:
      final_red=np.zeros((image_size_p3[1],image_size_p3[0]), np.uint8)
      red_text=" No red images available"
    final_red_tk=turn_image_into_tkinter(final_red, canvas_size_p3,[])
    canvas_left.delete("all")
    canvas_left.create_image(0,0, anchor=NW, image=final_red_tk)
    l_left_canvas.config(text=red_text)       
 global  red_dictionary_p2,fluor_dictionary_p2
 red_dictionary_p2=create_name_dictionary_p4( destin_red_names)
 fluor_dictionary_p2=create_name_dictionary_p4( destin_fl_names)
      
 canvas_left.delete("all")
 canvas_mid.delete("all")
 canvas_right.delete("all")
 frame_slider.set(first_frame_number_p3)
 slide_p3(first_frame_number_p3)
 feedback_dict["dest"]=my_destin# print destination folder in feedback panel
 feedback_text=update_feedback_text(feedback_dict)
 feedback_var_p3.set(feedback_text)
 instruct_var_p3.set("Finished!\nThe input movie has been created and stored in folder\n "+str(my_destin)+
                 "\nNow, you are ready to proceed to STEP 3 of the pipeline.")               
 button_fluor.config(bg=button_color)
 activate_buttons(all_buttons_page3,[]) 
##################################################

l_title=tk.Label(frame1_page3,text= "STEP-2: CUT WELL", bg="yellow", fg="red", font=("Times", "24")).pack(pady=5)
l_feedback_p3=tk.Label(frame2_page3,textvariable=feedback_var_p3 ,bg="black", fg=result_color, font=all_font, height=5)
l_feedback_p3.pack(fill=BOTH)   
l_instr_name_p3=tk.Label(frame13_page3,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="white").pack()
l_instruct_p3=tk.Label(frame14_page3,textvariable=instruct_var_p3 ,bg="black", fg="yellow", font=all_font, height=5)
l_instruct_p3.pack(fill=BOTH)   
############################################################
l_left_canvas=tk.Label(frame9_page3,text= "         ", bg="black", fg="cyan", font=("Times", "12"), width=45, height=2)
l_left_canvas.pack(side=tk.TOP, fill=None, expand=False)
l_mid_canvas=tk.Label(frame10_page3,text= "         ", bg="black", fg="cyan", font=("Times", "12"), width=45, height=2)
l_mid_canvas.pack(side=tk.TOP, fill=None, expand=False)
l_right_canvas=tk.Label(frame11_page3,text= "          ", bg="black", fg="cyan", font=("Times", "12"), width=45, height=2)
l_right_canvas.pack(side=tk.TOP, fill=None, expand=False)    

#######################################################
button_select=tk.Button(frame3_page3 ,text="1. Go to raw movie",bg='#9ACD32', font='TkDefaultFont 10 bold' ,activebackground="red", command=select_one_bright)
button_select.pack(side=tk.TOP, pady=(20,10))

button_threshold=tk.Button(frame3_page3,text="2. Apply initial threshold",bg=button_color,activebackground="red", font=all_font, command=lambda: apply_thresh())
button_threshold.pack(side=tk.TOP, pady=(10,10))
###############################################
threshold_slider=Scale(frame4_page3, from_=0,to=255,orient=HORIZONTAL,variable=low,length=150,bg=label_color,	
    showvalue=0,troughcolor=slide_trough_color,label="Threshold = "+str(None), command=change_threshold,
    activebackground="red", font=all_font)
threshold_slider.pack(side=tk.TOP,pady=5)
button_cut_well=tk.Button(frame4_page3,text="3. Cut well",bg=button_color,activebackground="red",font=all_font, command=lambda: cut_first_well())
button_cut_well.pack(side=tk.TOP,pady=5) 
button_first_shift_edit=tk.Button(frame4_page3,text="4. Edit well shift in Frame 1",bg=button_color,activebackground="red",font=all_font, command=lambda:edit_first_frame_shift())
button_first_shift_edit.pack(side=tk.TOP,pady=5)
#####################################################
global progressbar_page3
s = ttk.Style()
s.theme_use('clam')
s.configure("bar.Horizontal.TProgressbar", troughcolor=bg_color, 
                bordercolor="green", background="green", lightcolor="green", 
                darkcolor="black")
progressbar_page3 = ttk.Progressbar(frame5_page3,style="bar.Horizontal.TProgressbar",orient='horizontal',mode='determinate',length=280)
progressbar_page3.pack(side=tk.TOP, pady=10)

global button_bright
button_bright=tk.Button(frame5_page3,text="5. Apply to all bright",bg=button_color,activebackground="red",font=all_font, justify=LEFT,command=lambda:Thread(target=cut_bright_wells).start())
button_bright.pack(side=tk.TOP, pady=10)
####################################################################
button_shift_edit=tk.Button(frame5_page3,text="6. Start editing frames",bg=button_color,activebackground="red",font=all_font, command=start_editing_frames)
button_shift_edit.pack(side=tk.TOP, pady=10)
button_fluor=tk.Button(frame12_page3,text="7. Apply to all fluorescent and red",bg=button_color,activebackground="red",font=all_font, command=lambda: Thread(target=cut_fluor_wells).start())
button_fluor.pack(pady=5)
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
 
frame1_page4 = tk.Frame(master=page4, width=1530, height=50, bg=bg_color)
frame1_page4.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg=bg_color)
frame2_page4.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
###########################################################
container_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30)
container_page4.grid(row=1, column=1, rowspan=1, columnspan=5, sticky=W+E+N+S)
container_page4.grid_rowconfigure(0, weight=1)
container_page4.grid_columnconfigure(0, weight=1)
###################################################
frame3a_page4 = tk.Frame(master=container_page4,width=canvas_size_p4, height=10, bg=bg_color)
frame3a_page4.pack(fill = BOTH,expand=True)

frame3b_page4 = tk.Frame(master=container_page4, width=canvas_size_p4, height=10, bg=label_color)
frame3b_page4.pack( fill = BOTH,expand=True)

frame3c_page4 = tk.Frame(master=container_page4,width=canvas_size_p4, height=10, bg=bg_color)
frame3c_page4.pack(fill = BOTH,expand=True)
###################################################################
frame4_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=30, bg=bg_color)
frame4_page4.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
############################################
frame5_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame5_page4.grid(row=2, column=0, rowspan=1, columnspan=1)

frame6_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame6_page4.grid(row=2, column=1, rowspan=1, columnspan=1)

frame7_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame7_page4.grid(row=2, column=2, rowspan=1, columnspan=1)
######################################################################
frame8_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=canvas_size_p4, bg=bg_color)
frame8_page4.grid(row=3, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame9_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg=bg_color)
frame9_page4.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
####### overlay is for disabling slide bar during execution
overlay = tk.Frame(master=page4, bg='', bd=0)  # transparent
overlay.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
overlay.grid_forget()
 
frame10_page4 = tk.Frame(master=page4, width=canvas_size_p4, height=1538, bg=bg_color)
frame10_page4.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
####################################################################################
frame12_page4 = tk.Frame(master=page4, width=1530, height=50, bg=bg_color)
frame12_page4.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

gap_frame_page4 = tk.Frame(master=page4, width=1530, height=5, bg=bg_color)
gap_frame_page4.grid(row=5, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame11_page4 = tk.Frame(master=page4, width=1530, height=50, bg=bg_color)
frame11_page4.grid(row=6, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
################################################################
canvas_previous = Canvas(frame5_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_previous.pack(anchor='nw')
canvas_current = Canvas(frame6_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_current.pack(anchor='nw')
global canvas_lineage_exec
canvas_lineage_exec = Canvas(frame7_page4, bg=bg_color, height=canvas_size_p4, width=canvas_size_p4)
canvas_lineage_exec.pack(anchor='nw')
########################### These labels do not change
title_label = tk.Label(frame1_page4, text="STEP 3: EXECUTE AND CORRECT TRACKING",
              bg="yellow", fg="red", font=("Times", "24")).pack()
label_previous = tk.Label(frame8_page4, text="Previous Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' ).pack()
label_current = tk.Label(frame9_page4, text="Current Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_current.pack()
label_lineage = tk.Label(frame10_page4, text="Lineage", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' ).pack()
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
feedback_dict_p4={"movie name":" ","frame size":" ","cell diameter":" ","patch size":" ","initial number of cells":" ","from":" ","to":" ", "fluor frames":" ","bright frames":" ","red frames":" ","number of processed":" "}
feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
feedback_var_p4.set(feedback_text_p4)

feedback_label_p4=tk.Label(frame1_page4,textvariable=feedback_var_p4 ,bg="black", fg=result_color, font=all_font, height=6)
feedback_label_p4.pack(fill=BOTH)   

instruct_var_p4.set(" Step 3 allows you to track and manually correct tracking errors if necessary. \n\nTo choose raw movie , press Button 1."
                    "\nThen, navigate to ONE_WELL_MOVIE_{your movie name}, click on it once and press Select Folder. ")
##################################
global manual_IDs,manual_centroids,mother_name,  daughter_indicators 
manual_IDs,  manual_centroids, mother_name, daughter_indicators=[], [], None, []
#################
def activate_buttons(all_buttons_list,active_buttons_list):
    for button in all_buttons_list:
        #print("all_buttons_list,active_buttons_list,",all_buttons_list,active_buttons_list)
        if button in active_buttons_list:
            #print("ACTIVE button=", button)
            button.config(state=NORMAL)                        
        else:
            button.config(state=DISABLED)
            #print("DISABLED button=", button)
#######################

##############################
def load_helper_functions():
    os.chdir(source_code_folder)
    global predict_first_frame, create_output_folders,\
        detect_division, update_dictionary_after_division, check_division_frame_number, predict_tracking, predict_tracking_general, backup_track, predict_first_frame, segment_and_clean,\
         plot_frame, create_first_color_dictionary,\
        create_pedigree, create_output_movie, load_weights, extract_lineage,\
        create_lineage_image_one_frame, extract_file_name, load_clip, update_lineage,force_manual_IDs,create_lineage_for_Lorenzo,sorted_aphanumeric,update_color_dictionary,update_naive_names_list,update_xs_after_new_cells,\
        load_full_raw_movie,create_models,extract_output_images,create_name_dictionary_p4,display_image_p4_fix_missing,removeLeadingZeros,rename_file, show_3_canvases,update_changeable_params_history,extract_changeable_params_history,update_xs_after_division,process_figure_8

    from preprocess import create_output_folders, load_weights, extract_file_name,load_clip,load_full_raw_movie,create_models,removeLeadingZeros
    

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_division_frame_number,process_figure_8)

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
load_helper_functions()
models_directory = os.path.join(software_folder, "TRAINED MODELS")
tracker= None
models,models_directory=create_models(software_folder)
segmentor, refiner= load_models_p5(software_folder)
#######################
############ click Button 1 and explore if OUTPUT exists or not
############### If yes, ask whether user wants to continue or start all over again
################ by creating a popup option menu
def initiate_tracking_page():
     button_load.configure(background = 'red')
     global my_dir, input_movie_folder, current_movie_dir
     my_dir = filedialog.askdirectory()# input movie folder
     #input_info_label.config(text= "INPUT MOVIE:"+ "\n"+str(my_dir)+"\n")
     print("my_dir=", my_dir)
     #################################
     feedback_dict_p4["movie name"]=str(my_dir)     
     input_movie_folder = os.path.basename(my_dir)
     current_movie_dir=os.path.dirname(my_dir)
     print("current_movie_dir=", current_movie_dir)
     current_movie_name=os.path.basename(current_movie_dir)
     print("current_movie_name=", current_movie_name)
     global outpath, helper_dir_p4
     #load_helper_functions()
     #outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
     outpath = os.path.join(current_movie_dir, "TRACKED_MOVIE_"+current_movie_name)
     #helper_dir_p4=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER")
     helper_dir_p4=os.path.join(outpath, "HELPER_FOLDERS_(NOT FOR USER)")
     global init_image,last_image, frame_size, num_frames,  all_names_fluor
     all_names_fluor=[]
     number_of_brights, number_of_reds=0,0
     input_movie_dir=os.path.join(current_movie_dir,"ONE_WELL_MOVIE_"+current_movie_name)     
     for filename in sorted_aphanumeric(os.listdir( input_movie_dir)):   
        if filename.endswith("ch00.tif"):
            instruct_var_p4.set("Loading input movie ...")                           
            full_name_fluor = os.path.join( input_movie_dir, filename)
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
     feedback_dict_p4["from"]=str(first_frame_number)
     feedback_dict_p4["to"]=str(first_frame_number+len(all_names_fluor))
                                  
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
          output_fluor_folder=os.path.join(outpath,"TRACKED_GREEN_FL_CHANNEL")
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
    
                  global true_cell_radius, true_patch_size,basic_naive_names,  xs, full_core_bright_name,curr_frame_cell_names,flag,edit_id_indicator, \
                  base_colours,colour_counter,colour_dictionary,basic_naive_names, contrast_value, dict_of_divisions,naive_names_counter,number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta
                  true_cell_radius, true_patch_size,edit_id_indicator=IntVar(),IntVar(),StringVar()
   
                  (frame_size, true_cell_radius_pickle, true_patch_size_pickle,basic_naive_names,
                  num_frames, full_core_fluor_name, n_digits, full_core_bright_name, first_frame_number,
                  base_colours, contrast_value, number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta)= extract_const_movie_parameters(helper_dir_p4)
                  
    
                  true_cell_radius.set(true_cell_radius_pickle)
                  true_patch_size.set(true_patch_size_pickle)
                  ###################################

                   ########################################################
                  #cell_info_label.config(text= "FRAME SIZE: "+str(frame_size)+"x"+str(frame_size)+
                           #"\nCELL DIAMETER:= "+str(2*true_cell_radius.get())+"\nPATCH SIZE= "+str(2*patch_size)+" x "+str(2*patch_size))
                  #############################################
                  #################################
                  feedback_dict_p4["cell diameter"]=str(2*true_cell_radius.get())
                  feedback_dict_p4["frame size"]=str(frame_size)+"x"+str(frame_size)
                  feedback_dict_p4["patch size"]=str(2*true_patch_size.get())+" x "+str(2*true_patch_size.get())
                  feedback_dict_p4["initial number of cells"]=str(number_in_first_frame)
                  #feedback_dict_p4["max number"]=str(basic_naive_names)
                  
                  feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
                  feedback_var_p4.set(feedback_text_p4)
     ###################################
                 
                  
                  lineage_per_frame = extract_lineage(helper_dir_p4)
                  last_frame_cell_dict=lineage_per_frame[-1]
                  n_cells=len(last_frame_cell_dict)    
                  internal_cell_names=list(last_frame_cell_dict.keys())
    
                  global coords, start_frame
                  start_frame=last_frame_cell_dict[internal_cell_names[0]][12]+1    
                  coords=last_frame_cell_dict[internal_cell_names[0]][14]
                  ##############################
                  global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
                  dict_of_divisions,naive_names_counter, changable_params_history
                  xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,naive_names_counter,lin_image_widths,changable_params_history= extract_changeable_params_history(helper_dir_p4, -1)
                  edit_id_indicator.set(edit_id_indicator_pickle)
                                    
                  print("lin_image_widths=", lin_image_widths)
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
    global int_popup_color
    popup_color, int_popup_color ="#7A8F79","#B09D23"
    #########
    global popup_first_preview, canvas_popup_fluor_p4,canvas_popup_bright_p4,canvas_popup_red_p4
    popup_first_preview = tk.Toplevel(master=page4, bg=popup_color )  
    popup_first_preview.overrideredirect(True)                 
    popup_first_preview.geometry('%dx%d+%d+%d' % (1530, 2000-1200, 8, 159))
       
    frame1 = tk.Frame(master=popup_first_preview , width=1530, height=10, bg=popup_color )
    frame1.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame2 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame2.grid(row=1, column=0, rowspan=1, columnspan=1)
    
    frame3 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame3.grid(row=1, column=1, rowspan=1, columnspan=1)
    
    frame4 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame4.grid(row=1, column=2, rowspan=1, columnspan=1)
    
    frame5 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame5.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame6 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame6.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame7 = tk.Frame(master=popup_first_preview , width=canvas_size_p4, height=canvas_size_p4, bg=popup_color)
    frame7.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
    
    frame8 = tk.Frame(master=popup_first_preview , width=1530, height=50,bg=popup_color)
    frame8.grid(row=3, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    
    frame9 = tk.Frame(master=popup_first_preview , width=1530, height=100,bg=popup_color)
    frame9.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
    ###########################################
    global  canvas_left_pop, canvas_mid_pop, canvas_right_pop 
    canvas_left_pop = Canvas(frame2, bg=popup_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_left_pop.pack(anchor='nw')
    canvas_mid_pop = Canvas(frame3, bg=popup_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_mid_pop.pack(anchor='nw')
    canvas_right_pop = Canvas(frame4, bg=popup_color, height=canvas_size_p4, width=canvas_size_p4)
    canvas_right_pop.pack(anchor='nw')
    
    l_bright=tk.Label(frame5,text= "BRIGHT ", bg="black", fg="cyan", font=("Times", "12"), width=48, height=3)
    l_fluor=tk.Label(frame6,text= "FLUOR ", bg="black", fg="cyan", font=("Times", "12"), width=48, height=3)
    l_red=tk.Label(frame7,text= "RED ", bg="black", fg="cyan", font=("Times", "12"), width=48, height=3)
    l_bright.pack(),l_fluor.pack(),l_red.pack()    
    ##########################################################
    global  button_contrast,button_cell_radius,  button_assign_positions,  pop_slider, button_close 
    button_contrast = Button(frame5, text="1a. Enhance image contrast",font='TkDefaultFont 10 bold', bg=button_color, command=lambda:[create_contrast_popup(),instruct_var_p4.set("Adjusting contrast....")])
    button_contrast.pack(pady=5)
    
    button_cell_radius = Button(frame6, text="1b. Measure cell size",font='TkDefaultFont 10 bold', bg=button_color, command=create_cell_measure_popup)
    button_cell_radius.pack(pady=5)
        
    button_assign_positions = Button(frame7, text="1c. Assign initial cell positions",font='TkDefaultFont 10 bold', bg=button_color, command=create_assign_cell_positions_popup)
    button_assign_positions.pack(pady=5)
            
    button_close = Button(frame9, text=" Close this window",font='TkDefaultFont 10 bold', bg=button_color, command=close_popup_canvas)
    button_close.pack(pady=30)
    
    global first_go_buttons
    first_go_buttons=[button_load,button_contrast,button_cell_radius,  button_assign_positions]
    activate_buttons(first_go_buttons,[button_contrast])
    
    global  all_names_fluor,all_names_bright,all_names_red
        
    all_names_fluor, all_names_bright,all_names_red=load_full_raw_movie(my_dir)     
    #######################
    global  bright_dictionary,red_dictionary,fluor_dictionary
    red_dictionary=create_name_dictionary_p4(all_names_red)
    bright_dictionary=create_name_dictionary_p4(all_names_bright)
    fluor_dictionary=create_name_dictionary_p4(all_names_fluor)     
    ############################
    global slide_frames_pop    
    def slide_frames_pop(value): 
       image_number = int(value)
       image_number_zfill=str(value).zfill(n_digits)       
       canvas_left_pop.delete("all")
       canvas_mid_pop.delete("all")
       canvas_right_pop.delete("all")
       image_number=int(value)          
       ###########################################
       global br_tk,fl_tk,red_tk        
       br_tk, br_name=display_image_p4_fix_missing(image_number_zfill, bright_dictionary, canvas_size_p4)              
       canvas_left_pop.create_image(0,0, anchor=NW, image=br_tk)
       br_name_for_show=prepare_file_name_for_show(br_name)    
       l_bright.config(text= "BRIGHT \n"+br_name_for_show)      
       ################################    
       fl_tk, fl_name=display_image_p4_fix_missing(image_number_zfill, fluor_dictionary, canvas_size_p4)                  
       canvas_mid_pop.create_image(0,0, anchor=NW, image=fl_tk)
       fl_name_for_show=prepare_file_name_for_show(fl_name) 
       l_fluor.config(text= "FLUOR \n"+fl_name_for_show)     
       ###############################################
       red_tk, red_name=display_image_p4_fix_missing(image_number_zfill, red_dictionary,canvas_size_p4)                     
       canvas_right_pop.create_image(0,0, anchor=NW, image=red_tk)
       red_name_for_show=prepare_file_name_for_show(red_name) 
       l_red.config(text= "RED \n"+red_name_for_show)                        
           
    pop_slider = Scale(frame6, from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1, orient=HORIZONTAL,bg=label_color, troughcolor="#513B1C", command=slide_frames_pop, length=500)      
    pop_slider.pack(pady=5)    
    slide_frames_pop(first_frame_number)
   
    global instruct_label_popup_p4
    instruct_label_popup_p4=tk.Label(frame8,text="Input movie is loaded.\nYou can scroll through frames using silde bar.\n Now, you need to set up some parameterss using Buttons 1a,1b, and 1c consequtively. \nStart with Button 1a." ,bg="black", fg="yellow", font=all_font,width=10, height=5)
    instruct_label_popup_p4.pack(fill=BOTH) 
      
    global  full_core_bright_name, out_folders,full_core_red_name       
    out_folders = create_output_folders(outpath)    
    full_core_bright_name, _, _= extract_file_name(all_names_bright[0])
    ############################## 
    if len(all_names_red)!=0:
        full_core_red_name, _, _= extract_file_name(all_names_red[0])
    else:
        full_core_red_name="0"
    ##############################################
    global   previous_lineage_image, lineage_image_size
    
    feedback_dict_p4["frame size"]=str(frame_size)+"x"+str(frame_size)
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4)
    lineage_image_size=num_frames
    
    previous_lineage_image =np.zeros((lineage_image_size, lineage_image_size,3), dtype="uint8")  
    button_load.configure(background =button_color)
    global start_frame
    start_frame=first_frame_number     
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
###########################################
button_load = Button(frame1_page4, text="1. Click to open file menu and then select input movie folder",
               bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=initiate_tracking_page).start(), update_flash([]), feedback_label_p4.configure(text="Loading input movie ...") ])
button_load.pack()
################################
################### adjust contrast if necessary in contrast_popup (Button 2a)  
####################################### #
def create_contrast_popup():    
    global popup_contrast, canvas_contrast, photo_image, number_of_contrast_changes
    number_of_contrast_changes=[]
    global cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_contrast = tk.Toplevel(master= popup_first_preview, bg=int_popup_color)    
    popup_contrast.overrideredirect(True)  
    popup_contrast.geometry('%dx%d+%d+%d' % (popup_window_size+30, popup_window_size+200, 0, 0))
    
    frame1 = tk.Frame(master=popup_contrast, width=popup_window_size, height=popup_window_size, bg=int_popup_color)
    frame1.pack()
    frame2 = tk.Frame(master=popup_contrast, width=popup_window_size, height=50, bg=int_popup_color)
    frame2.pack()

    canvas_contrast = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg="black")
    canvas_contrast.pack(anchor='nw', pady=10)
   
    photo_image=turn_image_into_tkinter(init_image,popup_window_size,[])     
    canvas_contrast.create_image(0,0, anchor=NW, image=photo_image)    
    global contrast_slider, button_save_contrast    
    contrast_slider=Scale(frame2,from_=0,to=100,orient=HORIZONTAL,bg=label_color,troughcolor="#513B1C",variable=cliplimit,activebackground="red",label="Cliplimit = " +str(int(cliplimit.get())),command=change_contrast, length=150, showvalue=0)
    contrast_slider.pack(pady=(0,10))
    
    contrast_label_p4=tk.Label(frame2,text="To adjust contrast, use the slide bar. \nThen click Save." ,bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)
    contrast_label_p4.pack(fill=BOTH)
    instruct_label_popup_p4.configure(text="Adjusting contrast in progress...")   
    button_save_contrast=tk.Button(frame2,text="Save",activebackground="red", command=save_contrast, bg=button_color)
    button_save_contrast.pack(pady=8)       
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
      clahe = cv2.createCLAHE(clipLimit=float(value))
      cl=clahe.apply(init_image_copy)      
      result=cl
    else:     
      result=init_image
      contrast_value="0"            
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
    instruct_label_popup_p4.configure(text="Contrast has been adjusted. \nNow, go to Button 1b to measure cell diameter.")     
    popup_contrast.destroy()
######### measure cell radius in cell_measure_popup window (Bitton 2b)
############################
def draw_new_circles(event):# draw red circles to measure cell diameter   
    global click_counter,scaled_patch_size
    click_counter+=1     
    frame_number_from_slider=str(measure_cell_slider.get())
    frame_number_measure=str(frame_number_from_slider).zfill(n_digits)
    rad=scaled_cell_radius.get()   
    p_size=scaled_patch_size.get()
        
    circle=canvas_for_radius.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline = "red",width = 2)     
    square=canvas_for_radius.create_rectangle(event.x-p_size,event.y-p_size , event.x+p_size,event.y+p_size ,width=2, outline="yellow")    
    frame_object_dictionary[frame_number_measure].append([int(round(event.x)), int(round(event.y))])  
    circles.append(circle)
    squares.append(square)
    if click_counter==1:
           update_flash([radius_slider])
           activate_buttons(radius_popup_buttons,[radius_slider, patch_size_slider,measure_cell_slider, button_save_radius])    
##############################################
def draw_previous_circles():   
    rad=scaled_cell_radius.get()
    pat=scaled_patch_size.get()
    
    global centres, circles, squares    
    canvas_for_radius.delete("all")
    canvas_for_radius.create_image(0,0, anchor=NW, image=fl_measure_tk)
    for k in range(len(centres)):            
       circle=canvas_for_radius.create_oval(centres[k][0]-rad,centres[k][1]-rad,centres[k][0]+rad,centres[k][1]+rad,outline = "red",width = 2)       
       square=canvas_for_radius.create_rectangle(centres[k][0]-pat,centres[k][1]-pat,centres[k][0]+pat,centres[k][1]+pat ,width=2, outline="yellow")
       circles.append(circle)
       squares.append(square)        
########################################
def change_patch_size(value): 
  frame_number_from_slider=str(measure_cell_slider.get())
  frame_number_measure=str(frame_number_from_slider).zfill(n_digits)
  centres=frame_object_dictionary[frame_number_measure]  
  scaled_patch_size=int(value)
  rad=scaled_cell_radius.get()
  if scaled_patch_size<2.4*rad:
      rad=int(round(scaled_patch_size/2.4))
      scaled_cell_radius.set(rad)
      true_cell_radius.set(int(round(rad*frame_size/popup_window_size)))
  true_patch_size.set(int(round(scaled_patch_size*frame_size/popup_window_size)))
  patch_size_slider.config(label="Patch size =  "+str(true_patch_size.get()*2))
  radius_slider.config(label="Cell diameter =  "+str(true_cell_radius.get()*2))   
  global  squares, circles
  for k in range(len(centres)):     
       old_square=squares[k]
       old_circle=circles[k]
       canvas_for_radius.delete(old_square)
       canvas_for_radius.delete(old_circle)
       new_square=canvas_for_radius.create_rectangle(centres[k][0]-scaled_patch_size,centres[k][1]-scaled_patch_size,centres[k][0]+scaled_patch_size,centres[k][1]+scaled_patch_size ,width=2, outline="yellow")
       new_circle=canvas_for_radius.create_oval(centres[k][0]-rad,centres[k][1]-rad,centres[k][0]+rad,centres[k][1]+rad,outline = "red",width = 2)       
       squares[k]=new_square
       circles[k]=new_circle           
###############################################              
def change_radius(value):# change cell radius manually 
  frame_number_from_slider=str(measure_cell_slider.get())
  frame_number_measure=str(frame_number_from_slider).zfill(n_digits)
  centres=frame_object_dictionary[frame_number_measure] 
  scaled_cell_radius=int(value)
  p_size=scaled_patch_size.get()
  if p_size<2.4*scaled_cell_radius:
        p_size=int(round(2.4*scaled_cell_radius))
        scaled_patch_size.set(p_size)
        true_patch_size.set(int(round(p_size*frame_size/popup_window_size)))
  true_cell_radius.set(int(round(scaled_cell_radius*frame_size/popup_window_size)))
  radius_slider.config(label="Cell diameter =  "+str(true_cell_radius.get()*2))
  patch_size_slider.config(label="Patch size =  "+str(true_patch_size.get()*2))
  global circles, squares
  for k in range(len(centres)):
       old_circle=circles[k]
       old_square=squares[k]
       canvas_for_radius.delete(old_circle)
       canvas_for_radius.delete(old_square)
       new_circle=canvas_for_radius.create_oval(centres[k][0]-scaled_cell_radius,centres[k][1]-scaled_cell_radius,centres[k][0]+scaled_cell_radius,centres[k][1]+scaled_cell_radius,outline = "red",width = 2)
       new_square=canvas_for_radius.create_rectangle(centres[k][0]-p_size,centres[k][1]-p_size,centres[k][0]+p_size,centres[k][1]+p_size,outline = "yellow",width = 2) 
       circles[k]=new_circle
       squares[k]=new_square                     
###################################################
def save_cell_radius():
    global true_patch_size, bordersize
    update_flash([button_assign_positions])
    bordersize=true_patch_size.get()   
    instruct_label_popup_p4.configure(text="Cell diameter has been measured. \nNow, go to Button 2c to assign initial cells` positions.")     
    activate_buttons(radius_popup_buttons,[ button_assign_positions]) 
    popup_for_radius.destroy()    
    ### #################################    
    feedback_dict_p4["cell diameter"]=str(2*true_cell_radius.get())
    feedback_dict_p4["patch size"]=str(2*true_patch_size.get())+" x "+str(2*true_patch_size.get())
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4) 
#####################################
def create_cell_measure_popup():
    update_flash([])
    global popup_for_radius, canvas_for_radius, photo_image
    instruct_label_popup_p4.configure(text="Measuring cell diameter is in progress....")         
    popup_for_radius = tk.Toplevel(master=popup_first_preview, bg=int_popup_color)
    popup_for_radius.title("PAGE 4 POPUP WINDOW: MEASURE CELL DIAMETER")
    popup_for_radius.overrideredirect(True)        
    popup_for_radius.geometry('%dx%d+%d+%d' % (popup_window_size+20, popup_window_size+235, 0, 0))
    frame1 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=popup_window_size,bg=int_popup_color)
    frame1.pack()
    frame2 = tk.Frame(master=popup_for_radius, width=popup_window_size, height=50, bg=int_popup_color)
    frame2.pack()

    canvas_for_radius = Canvas(frame1, height=popup_window_size, width=popup_window_size, bg=int_popup_color)
    canvas_for_radius.pack(anchor='nw', pady=10)
    #######################################
    if contrast_value!="0":
           global init_image              
           clahe = cv2.createCLAHE(clipLimit=float(contrast_value))
           init_image=clahe.apply(last_image)
    else:
        init_image=last_image
               
    photo_image=turn_image_into_tkinter(init_image,popup_window_size,[])     
    canvas_for_radius.create_image(0,0, anchor=NW, image=photo_image)

    global centres, circles,squares,scaled_cell_radius,scaled_patch_size, true_cell_radius,true_patch_size 
    centres, circles,squares,scaled_cell_radius, true_cell_radius,scaled_patch_size, true_patch_size =[],[],[],IntVar(),IntVar(),IntVar(),IntVar()

    scaled_cell_radius.set(20)
    init_p_size=int(round(20*2.4))
    scaled_patch_size.set(init_p_size)  
    true_cell_radius.set(int(round(scaled_cell_radius.get()*frame_size/popup_window_size)))    
    true_patch_size.set(int(round(scaled_patch_size.get()*frame_size/popup_window_size)))    
  
    global radius_slider, button_save_radius   
    radius_slider=Scale(frame2,from_=1,to=100,orient=HORIZONTAL,bg=label_color, troughcolor="#513B1C",activebackground="red",label="Cell diameter = "+str(int(true_cell_radius.get()*2)),variable=scaled_cell_radius, command=change_radius, length=150, showvalue=0)
   
    global patch_size_slider   
    patch_size_slider=Scale(frame2,from_=1,to=100,orient=HORIZONTAL,bg=label_color, troughcolor="#513B1C",activebackground="red",label="Patch size = "+str(int(true_patch_size.get()*2)),variable=scaled_patch_size, command=change_patch_size, length=150, showvalue=0)   
    #############################
    def slide_frames_measure_cell(value):       
       global image_number
       image_number = int(value)
       image_number_zfill=str(value).zfill(n_digits)       
       measure_cell_slider.config(label="Frame  "+str(image_number))
       canvas_for_radius.delete("all")              
       global fl_measure_tk                 
       fl_measure_tk, fl_name=display_image_p4_fix_missing(image_number_zfill, fluor_dictionary, popup_window_size)                  
       canvas_for_radius.create_image(0,0, anchor=NW, image=fl_measure_tk)   
       frame_number_measure=image_number_zfill     
       global circles,squares
       circles,squares=[],[]
       global centres
       centres=frame_object_dictionary[frame_number_measure]       
       if len(centres)!=0:          
           draw_previous_circles()           
    ######################################
    global frame_object_dictionary
    frame_object_dictionary={}
    keys=list(fluor_dictionary.keys())  
    for key in keys: 
        frame_object_dictionary[key]=[]   
    ##########################################
    global measure_cell_slider, button_save_radius
    measure_cell_slider = Scale(frame2, from_=first_frame_number, to=first_frame_number+len(all_names_fluor)-1,label="Frame  "+str(first_frame_number), orient=HORIZONTAL, bg=label_color, troughcolor="#513B1C", command=slide_frames_measure_cell, length=370,showvalue=0)         
    measure_cell_slider.set(first_frame_number)
    slide_frames_measure_cell(first_frame_number)
    ########################################################
    radius_label_p4=tk.Label(frame2,text="To measure cell radius, left-click on a cell (make sure to click on the centroid) and then \nuse slide bars to change radius\patch size.\nThe cell should be entirely enclosed inside patch."\
                             "\nTo check,you can also click on other cells in the current frame.\n Also, you can do it in other frames, too, using the slide bar",bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)    
    button_save_radius=tk.Button(frame2,text="Save",activebackground="red", command=save_cell_radius, bg=button_color)     
    canvas_for_radius.bind("<Button-1>",draw_new_circles)
    #################################
    button_save_radius.pack(side=tk.BOTTOM, pady=3)      
    radius_label_p4.pack(side=tk.BOTTOM)
    measure_cell_slider.pack(side=tk.TOP, pady=(0,2))
    radius_slider.pack(side=tk.LEFT,padx=(150,90), pady=2)
    patch_size_slider.pack(side=tk.LEFT, padx=(90,150), pady=2)  
    #################################
    global click_counter
    click_counter=0
    global radius_popup_buttons
    radius_popup_buttons=[ button_save_radius,radius_slider,patch_size_slider,measure_cell_slider,button_assign_positions ]
    activate_buttons(radius_popup_buttons,[measure_cell_slider ])    
###############################################    
################### Assign initial cell positions in assign_cell_positions_popup (Button 2c)
##################################
global create_assign_cell_positions_popup
def create_assign_cell_positions_popup():
    instruct_label_popup_p4.configure(text="Assigning initial cells` positions is in progress....")     
    global  manual_init_positions
    manual_init_positions =[]
    
    button_contrast.configure(bg=button_color, fg="black")
    global popup_assign_pos,  cliplimit
    cliplimit=IntVar()
    cliplimit.set(0.)
    popup_assign_pos = tk.Toplevel(master=popup_first_preview, bg=int_popup_color)   
    popup_assign_pos.overrideredirect(True)
    popup_assign_pos.geometry('%dx%d+%d+%d' % (popup_window_size+20, popup_window_size+170, 0, 0))
         
    sub2 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=popup_window_size, bg=int_popup_color)
    sub2.pack()
    
    global canvas_assign_pos  
    canvas_assign_pos = Canvas(sub2,  height=popup_window_size, width=popup_window_size,bg=int_popup_color)
    canvas_assign_pos.pack(anchor='nw', pady=10)
    canvas_assign_pos.bind("<Button-1>", click_position)
      
    sub3 = tk.Frame(master=popup_assign_pos, width=popup_window_size, height=300, bg=int_popup_color)   
    sub3.pack()
    ass_pos_label_p4=tk.Label(sub3,text="This is Frame 1 of the input movie.\nTo assign positions of cells of interest, left-click on their centroids."\
                              "\nThen, click Save.",bg="black", fg="yellow", font=all_font,width=popup_window_size, height=5)
    ass_pos_label_p4.pack(fill=BOTH) 
    global button_save_init_positions, photo_image
    button_save_init_positions = Button(sub3, text="Save", bg=button_color,activebackground="red", command= close_assign_window)
    button_save_init_positions.pack(pady=15)      
    canvas_assign_pos.create_image(0, 0, anchor=NW, image=photo_image_contrast)
    
    global positions_popup_buttons, button_close
    positions_popup_buttons=[button_assign_positions, button_save_init_positions, button_close ]
    activate_buttons(positions_popup_buttons,[ button_assign_positions])    
################ draw red spots in popup canvas in response to mouse click
def click_position(event):  
    canvas_assign_pos.create_oval(event.x-3, event.y-3, event.x+3,
                       event.y+3, outline="red", fill="red", width=2)   
    manual_init_positions.append([event.x/popup_window_size*frame_size, event.y/popup_window_size*frame_size])
    if len(manual_init_positions)==1:
        update_flash([button_save_init_positions])
        activate_buttons(positions_popup_buttons,[ button_save_init_positions])    
    feedback_dict_p4["initial number of cells"]=str(len(manual_init_positions))
    feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
    feedback_var_p4.set(feedback_text_p4)
##################################
def close_assign_window():
     update_flash([button_close])
     instruct_label_popup_p4.configure(text="Initial cells` positions in Frame 1 have been assigned.\nNow, everyting is ready for tracking.\nClose ths window")
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
      instruct_var_p4.set("The parameters of the input movie have been set up.\n\nTo start execution, press Button 2.")
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
    lineage_per_frame_p4=extract_lineage( helper_dir_p4)
    print("CUT_LINEAGE")
    #print("len(lineage_per_frame_p4) BEFORE=", len(lineage_per_frame_p4))
    del lineage_per_frame_p4[internal_start_frame:]# was -1
    #print("len(lineage_per_frame_p4) AFTER=", len(lineage_per_frame_p4))   
    update_lineage(lineage_per_frame_p4, helper_dir_p4,'wb')# "wb" means delete previous lineage and write a new one
    global output_images,lineage_images_tk,lineage_images_cv2, output_names    
   
    del lineage_images_cv2[internal_start_frame:] 
    del lineage_images_tk[internal_start_frame:]
    del output_images[(internal_start_frame+1):]# was start_frame:
    del output_names[(internal_start_frame+1):]
    del changeable_params_history[internal_start_frame:]
    update_changeable_params_history(changeable_params_history, helper_dir_p4, "wb")
        
    folders_to_truncate=[os.path.join("HELPER_FOLDERS_(NOT FOR USER)","MASKS"),"TRACKED_GREEN_FL_CHANNEL",os.path.join("HELPER_FOLDERS_(NOT FOR USER)","LINEAGE_IMAGES"),os.path.join("HELPER_FOLDERS_(NOT FOR USER)","CLEANED_PATCHES"), "TRACKED_BRIGHTFIELD_CHANNEL"]
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
    list_of_const_movie_params=[frame_size, true_cell_radius.get(), true_patch_size.get(),basic_naive_names,
                          num_frames, full_core_fluor_name, n_digits,full_core_bright_name, first_frame_number,
                          base_colours, contrast_value, number_in_first_frame,full_core_red_name, red_dictionary, bordersize, init_delta]
    const_parameters_path=os.path.join( helper_dir_p4,"constant_movie_parameters.pkl")  
    with open(const_parameters_path, 'wb') as f:
        for i in range(len(list_of_const_movie_params)):
           pickle.dump(list_of_const_movie_params[i], f,protocol=pickle.HIGHEST_PROTOCOL)

###########################################


import time
########################################################
def execute(): 
 activate_buttons(all_buttons_page4,[button_execute])
 button_execute.configure(background = 'red') 
 instruct_var_p4.set("Execution in progress...\nPress Button 2a if you need to pause the tracking.")
 global start_frame, xs, edit_id_indicator
 print("START_FRAME inside execute=", start_frame)
 start_time=time.time()
 label_curr_frame_name.config(text=start_empty_file_name)
 label_current.configure(text="Current frame:  ", fg="black")
 try:   
    cell_radius=true_cell_radius.get()
    patch_size=true_patch_size.get()
    canvas_previous.delete("all")
    canvas_current.delete("all")
    canvas_lineage_exec.delete("all")
          
    global lineage_images_tk, output_images, lineage_per_frame_p4, previous_lineage_image, lineage_images_cv2    
    if lineage_per_frame_p4:
        del lineage_per_frame_p4
    
    global variable_stop,  tracker, segmentor, refiner# this variable allows to stop the loop (controlled by Stop button)     
    global coords, curr_frame_cell_names, count,  cells, old_number_of_cells, edit_id_indicator,kk, lin_image_widths, colour_dictionary, colour_counter, dict_of_divisions,changeable_params_history, init_delta
    
    N_cells = coords.shape[0]
    division_indicator=0
    centroids_for_benchmarking=[coords]
    n =num_frames    
    first_number_in_clip=start_frame    
    kk = 0  # the number of frame within clip    
    clear_memory_of_models(tracker, segmentor, refiner)
    tracker, segmentor, refiner=load_weights(models)       
    update_flash([button_pause])
    activate_buttons(all_buttons_page4,[button_pause])        
    last_frame_number=num_frames+first_frame_number-1  
    while  first_number_in_clip <= last_frame_number:                            
        global fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names,red_names, red_images 
        clear_memory_of_previous_clip(fluor_images, fluor_images_compressed,bright_images, fluor_names, br_names,red_images, red_names)
        fluor_images,fluor_images_compressed,bright_images,fluor_names,br_names,red_names, red_images  =load_clip( first_number_in_clip,full_core_fluor_name,full_core_bright_name,n_digits, num_frames, first_frame_number, full_core_red_name,red_dictionary)
        
        clip_centr = predict_tracking_general(
                coords, fluor_images, fluor_images_compressed, fluor_names,  first_number_in_clip,  tracker,last_frame_number, cell_radius, frame_size)
        for kk in range(len(clip_centr)):# it is actually 4 (number of frames in clip)
            current_frame_number=first_number_in_clip+kk            
            print("FRAME NUMBER = ",  current_frame_number)# segmenting all the 4 frames in the clip                       
            if  edit_id_indicator.get()=="yes" and kk==0:
                clip_centr=force_manual_IDs(clip_centr,coords,kk)
                edit_id_indicator.set("no")
            else:
                clip_centr =  backup_track(
                   clip_centr, coords, kk, cell_radius)  # correct too big jumps
                      
            tracked_centroids=clip_centr[kk]              
            empty_fluor = fluor_images[kk]         
            empty_bright = bright_images[kk]                        
            cells, coords,  curr_frame_cell_names = segment_and_clean(
                dict_of_divisions, cells, coords,curr_frame_cell_names, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, first_number_in_clip+kk, edit_id_indicator, mother_number, out_folders, cell_radius, frame_size, colour_dictionary, patch_size, "first cleaning", bordersize)            
            ################## If manual division corrected took place          
            if manual_division_indicator.get()=="yes":
                print("INSIDE MANUAL_DIVISION")
                daughter_1_name=mother_name+"0"
                daughter_2_name=mother_name+"1"
                for key in cells.keys():
                    name=cells[key][11]
                    if name==daughter_1_name:                     
                        cells[key][16]="daughter-1"
                    if name==daughter_2_name:
                        cells[key][16]="daughter-2"                                                          
            else:# Division detector in action
               print("INSIDE AUTOMATIC_DIVISION")
               division_indicator = 0  
               count, cut_patch, mother_8_name,mother_8_number,mother_8_centroid = detect_division(
                   cells, count, first_number_in_clip, kk)
               if (np.any(count == 2) or np.any(count == 1)):                  
                   if mother_8_name != []:
                       count = check_division_frame_number(
                           count, cells, dict_of_divisions, mother_8_name, first_number_in_clip+kk)              
               #######################################################
               if np.any(count == 2):# confirmed automatic division detection
                   print("AUTOMATIC DIVISION !!!!")  
                   division_indicator=1
                   start_frame_internal=current_frame_number-first_frame_number                                                   
                   daughter_1_name =mother_8_name+"0"
                   daughter_2_name=mother_8_name+"1"                                                      
                   previous_lineage_image=lineage_images_cv2[start_frame_internal-1]                                     
                   edit_id_indicator.set("no")
                   manual_division_indicator.set("no")                                   
                   xs=update_xs_after_division(xs,daughter_1_name,daughter_2_name, mother_8_name,init_delta)                                                        
                   dict_of_divisions[mother_8_name] = first_number_in_clip+kk                      
                   cells,curr_frame_cell_names,count,coords,colour_dictionary, colour_counter=update_dictionary_after_division(cut_patch,\
                          cells,curr_frame_cell_names,count,coords, frame_size, colour_dictionary,bordersize, patch_size,base_colours, colour_counter)                  
                   #############################################################            
               if division_indicator == 1 and mother_8_name != []:
                   print("mother_8_cell_name =", mother_8_name)                  
                   print("8-figure division detected in frame ", first_number_in_clip+kk)                 
            # End of Division Detector            
            if manual_division_indicator.get()=="yes":
                 manual_division_indicator.set("no")                 
            update_changeable_params_history([[xs,curr_frame_cell_names,flag,edit_id_indicator.get(),colour_counter,colour_dictionary,dict_of_divisions,naive_names_counter, lin_image_widths]], helper_dir_p4, 'ab')
            update_lineage([cells], helper_dir_p4,'ab')# concatenates {cells}  to pickle
            keys=list(cells.keys())           
            ##############################            
            N_cells = len(cells)            
            current_lineage_image=create_lineage_image_one_frame(cells, previous_lineage_image, xs, first_number_in_clip+kk, first_frame_number)            
            coords, destin_fluor = plot_frame(cells, clip_centr, first_number_in_clip, kk,
                                fluor_images, fluor_names, out_folders, coords, coords, bright_images, br_names, frame_size , n_digits, first_frame_number, contrast_value, current_lineage_image,patch_size, red_images, red_names, bordersize)          
                                 
            image_seg=destin_fluor# for displaying dynamically on unterface
            photo_image_seg=turn_image_into_tkinter(image_seg, canvas_size_p4,[])
            output_images.append(photo_image_seg)
            output_name=rename_file(out_folders[1],fluor_names[kk])
            output_name_base=os.path.split(output_name)[1]          
            output_names.append(output_name_base)
            
            image_lin=current_lineage_image
            image_lin_copy=copy.deepcopy(image_lin)         
            lineage_images_cv2.append(image_lin_copy)
            previous_lineage_image=current_lineage_image# need it for the next lineage image                                
            photo_image_lin=turn_image_into_tkinter(image_lin, canvas_size_p4, lin_image_widths)           
            lineage_images_tk.append(photo_image_lin)           
            feedback_dict_p4["number of processed"]=str(len(output_names)-1)
            feedback_text_p4=update_feedback_text_p4(feedback_dict_p4)
            feedback_var_p4.set(feedback_text_p4)
            centroids_for_benchmarking.append(coords)                       
            if  first_number_in_clip == start_frame and kk==0:           
                 view_slider.config(from_=first_frame_number,to=first_frame_number+len(all_names_fluor)-1)
            
            view_slider.set(first_number_in_clip+kk)# show images dinamically
            win.update()
            slide_frames(view_slider.get())           
            if variable_stop=="Stop":              
               start_frame=current_frame_number+1                                                                              
               break                  
            if (division_indicator == 1):
                print("division occured in frame ", first_number_in_clip+kk)
                print("breaking out of small loop due to detected division")                              
                break                    
        print("END OF BIG LOOP")
        if variable_stop=="Stop":          
            N_cells = coords.shape[0]
            break
        else:            
            if (division_indicator == 1):
              first_number_in_clip = first_number_in_clip+kk+1
              N_cells = coords.shape[0]            
            else:
              first_number_in_clip += 4                
             
 except:
       feedback_label_p4.config(text="Stopped due to error", fg="#DF0101", font='TkDefaultFont 10 bold')                       
       print("Stopped due to error!!!!!")
       tk.messagebox.showerror('Error',traceback.format_exc())
       update_flash([])     
 if variable_stop=="Stop":
     print("EXECUTION STOPPED MANUALLY")
     feedback_label_p4.config(text="You stopped execution manually. \nPress Button 3 to check results." )
     variable_stop="Do not stop"
 else:
     feedback_label_p4.config(text="Execution finished! \nPress Button 3 to check results." )
     finish_time=time.time()    
     execution_time=finish_time-start_time
   
 button_execute.configure(background = button_color)
 button_pause.configure(background = button_color)
 update_flash([button_display])
 activate_buttons(all_buttons_page4,[button_display]) 
###############################################
def stop_execution_manually():
    print("STOPPED MANUALLY!!!!")
    instruct_var_p4.set("You stopped execution. \nTo see all the processed frames,  push button 4. Display result.")
    button_execute.configure(background = button_color)
    global variable_stop
    variable_stop = "Stop"
    button_pause.configure(background = "red")
#################################################################    
def slide_frames(value):# view_slider (main screen)  
    frame_number = int(value)      
    internal_frame_number=frame_number-first_frame_number+1# +1 is correct because of the previous image in Frame 1    
    curr_file_name=output_names[internal_frame_number]   
    curr_file_name_for_show=prepare_file_name_for_show(curr_file_name)    
    label_curr_frame_name.config(text=curr_file_name_for_show)
    label_current.configure(text="Current frame: " +str(frame_number), fg="black")     
    show_3_canvases(canvas_previous,canvas_current,canvas_lineage_exec,output_images,lineage_images_tk,frame_number, first_frame_number)
##############################################
def display_first_frame():# display all frames after pushing button "Display result"
    update_flash([])
    button_display.config(bg="red")
    button_execute.configure(bg=button_color)
    global fully_tracked_indicator
    if fully_tracked_indicator=="yes":
           activate_buttons(all_buttons_page4,[R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell,button_create_excel])
    else:
          activate_buttons(all_buttons_page4,[R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell,button_create_excel, button_execute ])  
    view_slider.config(from_=first_frame_number,to=len(output_images)+first_frame_number-2)   
    view_slider.set(str(first_frame_number))  
    slide_frames(first_frame_number)
    
    global  lineage_per_frame_p4
    lineage_per_frame_p4=extract_lineage(helper_dir_p4)   
    instruct_var_p4.set("Check results by sliding the bar under Current Frame."
                    "\n - If you need to edit, stop the slide bar at the frame of interest and go for one of the options under Edit tools."
                    "\n - If you are happy with the result, press Button 3. Execute to continue tracking.")       
###########3#######################
def get_cell_IDs_manually(event):# gets cell ID from previous frame during editing
    if popup_monitor!=None:
          popup_monitor.deiconify()
    canvas_indicator=clicked.get()  
    if canvas_indicator=="Previous":
        canvas_IDs=canvas_previous# click on previos frame to get IDs
        shift=1
    else:
        canvas_IDs=canvas_current# click on current frame to get IDs
        shift=0
    global manual_IDs, cell_names_external, daughter_indicators
  
    frame=int(view_slider.get())   
    internal_frame_number=frame-first_frame_number    
    keys=list(lineage_per_frame_p4[internal_frame_number-shift].keys())
    
    mask_image=lineage_per_frame_p4[internal_frame_number-shift][keys[0]][13]   
    cell_number_in_mask=int(mask_image[int(event.y/canvas_size_p4*frame_size),int(event.x/canvas_size_p4*frame_size)])
    cell_number=int(math.log(round(cell_number_in_mask),2))     
    manual_IDs.append(cell_number)
      
    cell_name_internal="cell_"+ str(cell_number) 
    cell_name_external=lineage_per_frame_p4[internal_frame_number-shift][cell_name_internal][11]# was -1
    daughter_ind=lineage_per_frame_p4[internal_frame_number-shift][cell_name_internal][16]# was -1
    daughter_indicators.append(daughter_ind)
    print("colour_dictionary=",colour_dictionary)
    cell_names_external.append(cell_name_external)    
    colour_four_channel=colour_dictionary[cell_name_external][0]    
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
    button_save_id.pack(side=tk.LEFT, padx=5)
    R_edit_ID.configure(background = 'red')
    activate_buttons(all_buttons_page4,[button_save_id])
    update_flash([button_save_id])
    if popup_monitor!=None:
          popup_monitor.deiconify()
   
    instruct_var_p4.set("First, click on the cell of interest in Previous Frame.\n"
                "Then, click on its desired position in Current Frame.Make sure you click as close to the centroid as possible!\n You can repeat it MULTIPLE TIMES.\nFinally, save edits by pressing button Save ID edits.")    
    global manual_centroids, manual_IDs, cell_names_external
    manual_centroids, manual_IDs, cell_names_external, daughter_indicators=[],[], [],[] 
    canvas_previous.bind("<Button-1>", get_cell_IDs_manually) 
    canvas_current.bind("<Button-1>", get_centroids_manually)
    update_flash([button_save_id])       
####################################################
def stop_editing_IDs():    
    R_edit_ID.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>") 
    global start_frame, lineage_per_frame_p4, edit_id_indicator
      
    start_frame=int(view_slider.get())  
    #start_frame_internal=start_frame-first_frame_number+1
    start_frame_internal=start_frame-first_frame_number
    ###################################
    global previous_lineage_image
    #previous_lineage_image=lineage_images_cv2[start_frame_internal-2]
    previous_lineage_image=lineage_images_cv2[start_frame_internal-1]
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(helper_dir_p4, start_frame_internal)   
    edit_id_indicator.set("yes")
    ########################################################
    #keys=list(lineage_per_frame_p4[start_frame_internal-1].keys())   
    #coords_old=lineage_per_frame_p4[start_frame_internal-1][keys[0]][14]   
    keys=list(lineage_per_frame_p4[start_frame_internal].keys())   
    coords_old=lineage_per_frame_p4[start_frame_internal][keys[0]][14]   
    for i in range(len(manual_centroids)):
        coords_old[manual_IDs[i]]=manual_centroids[i] 
    #############
    global coords
    coords=coords_old   
    global mask_current    
    mask_current=lineage_per_frame_p4[start_frame_internal][keys[0]][13]    
    instruct_var_p4.set(" ID edits  for frame  " +str(start_frame)+"  have been saved.\nPress Button 3 to resume execution.")
 
    text1=[lineage_per_frame_p4[start_frame_internal][key][11] for key in keys] 
    numbers=[lineage_per_frame_p4[start_frame_internal][key][17] for key in keys]
  
    w=list(zip(numbers,text1))
    ww=sorted(w,key=lambda student:student[0])
    ress = list(zip(*ww))
    curr_frame_cell_names =list(ress[1])
               
    cut_lineage(start_frame_internal)
         
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}
    ##############################
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    update_flash([button_execute])
    button_save_id.pack_forget()
    activate_buttons(all_buttons_page4,[button_execute])
    
    label_current.configure( text="Current frame", fg="black" )
    button_save_id.configure(background = '#9ACD32')
    button_pause.configure(background = button_color)
    button_display.configure(bg=button_color) 
    instruct_label_p4.config(text="You finished editing IDs in Frame " +str(start_frame)+".\n To resume tracking, press Button 3." )
  
    if  popup_monitor!=None: 
       popup_monitor.destroy()
###################################################
def start_editing_division():
    R_edit_division.configure(background = 'red')
    activate_buttons(all_buttons_page4,[ button_save_division])
    button_save_division.pack(side=tk.LEFT, padx=110)
    update_flash([button_save_division]) 
       
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
    R_edit_division.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>")
    global  mask_prev_frame
    
    global start_frame, lineage_per_frame_p4
    start_frame=int(view_slider.get())
    ####### assign start_frame   
    start_frame_internal=start_frame-first_frame_number
    ################### assign previous_lineage_image
    global previous_lineage_image
    previous_lineage_image=lineage_images_cv2[start_frame_internal-1]
    #############################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(helper_dir_p4, start_frame_internal)
    ######################## assign indicators  
    edit_id_indicator.set(edit_id_indicator_pickle)
    manual_division_indicator.set("yes")
    ###########################################
    keys=list(lineage_per_frame_p4[start_frame_internal].keys())# from previous frame was -2    
    global manual_IDs, mother_number, mother_name 
    ##########################################
    global coords
    coords_old=lineage_per_frame_p4[start_frame_internal][keys[0]][14] 
    coords_daughter_1=manual_centroids[0]
    coords_daughter_2=manual_centroids[1]  
    coords_old[mother_number]=coords_daughter_1    
    coords_old=np.concatenate((coords_old,np.array(coords_daughter_2).reshape((1,2))))    
    coords=coords_old 
    #########################################    
    mother_number=manual_IDs[0]   
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage_per_frame_p4[start_frame_internal-1][mother_name_internal][11]
    mother_color=lineage_per_frame_p4[start_frame_internal-1][mother_name_internal][15]                                     
    daughter_1_number=mother_number
    daughter_2_number=len(coords_old)    
    daughter_1_name=mother_name+"0"
    daughter_2_name=mother_name+"1"
    daughter_names=[ daughter_1_name, daughter_2_name]
    #################### change xs,colour_dictionary, colour_counter 
    xs=update_xs_after_division(xs,daughter_1_name,daughter_2_name, mother_name,init_delta)
    colour_dictionary, colour_counter =update_color_dictionary(colour_dictionary,daughter_names,base_colours, colour_counter)
    ############# change curr_frame_cell_names
    curr_frame_cell_names[mother_number]=daughter_1_name
    curr_frame_cell_names.append(daughter_2_name)  
    ######################### change coords(they are manual)
    
    ##################### change dict_of_divisions   
    dict_of_divisions[mother_name] = start_frame 
    ###################################################
    cut_lineage(start_frame_internal)    
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
  
    label_current.configure( text="Current frame", fg="black" )
    update_flash([button_execute])
    button_save_division.pack_forget()
    button_pause.configure(background = button_color)
    button_display.configure(background = button_color)
    
    R_edit_division.configure(background = '#9ACD32')
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You finished editing missed division in Frame  "+str(start_frame)+" .\n To resume execution, press Button 3." ) 
############################################
def add_new_cell():
  instruct_var_p4.set("To add a new cell/cells, click on their cetroids in Current Frame./Once finished, click Save added cells.")
  R_add_new_cell.configure(background="red")
  button_save_added_cell.pack(side=tk.LEFT, padx=250)
  update_flash([button_save_added_cell])
  activate_buttons(all_buttons_page4,[button_save_added_cell])  
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
    internal_start_frame=start_frame-first_frame_number    
    keys=list(lineage_per_frame_p4[internal_start_frame].keys())      
    b = np.array(manual_centroids)
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(helper_dir_p4, internal_start_frame)   
    edit_id_indicator.set(edit_id_indicator_pickle)     
    ########################################################
    global coords,  previous_lineage_image
    previous_lineage_image=lineage_images_cv2[internal_start_frame-1]
    coords_old=coords
    coords=np.concatenate((coords_old, b), axis=0)     
    number_of_now_added_cells=len(manual_centroids)   
    global  base_colours, delta, naive_names_counter
    #######
    new_naive_names,naive_names_counter=update_naive_names_list(basic_naive_names, number_of_now_added_cells,naive_names_counter)    
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)    
    curr_frame_cell_names+=new_naive_names        
    xs, previous_lineage_image,lin_image_widths=update_xs_after_new_cells(xs,new_naive_names, previous_lineage_image, canvas_lineage_exec, canvas_size_p4, init_delta,lin_image_widths)    
    number_of_added_new_cells+=number_of_now_added_cells        

    lineage_images_cv2[internal_start_frame-1]=previous_lineage_image     
    instruct_var_p4.set("Added cells:\n " + str(new_naive_names))
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage_exec.delete('all')
      
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val <= start_frame}    
    cut_lineage(internal_start_frame)
   
    update_flash([button_execute])
    button_pause.configure(background = button_color)
    button_display.configure(background = button_color)
    R_add_new_cell.configure(background=button_color)
    button_save_added_cell.pack_forget()
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You added new cells in Frame "+str(start_frame)+"  .\nTo resume tracking, push Button 3.")
#####################################
def remove_died_cell():
  R_remove_dead_cell.configure(background="red")
  button_save_removed_cell.pack(side=tk.LEFT,padx=370)
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
    internal_start_frame=start_frame-first_frame_number    
    ###############################
    global previous_lineage_image
    previous_lineage_image=lineage_images_cv2[internal_start_frame-1]
    ###################################
    global xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,\
    dict_of_divisions,naive_names_counter,lin_image_widths,changeable_params_history
    xs,curr_frame_cell_names,flag,edit_id_indicator_pickle,colour_counter,colour_dictionary,dict_of_divisions,number_of_added_new_cells,lin_image_widths,changeable_params_history= extract_changeable_params_history(helper_dir_p4, internal_start_frame)
    edit_id_indicator.set(edit_id_indicator_pickle)     
    ########################################################
    keys=list(lineage_per_frame_p4[internal_start_frame].keys())   
    coords_old=lineage_per_frame_p4[internal_start_frame][keys[0]][14]    
    if "daughter-1" in daughter_indicators or "daughter-2"in daughter_indicators:
        
        dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val < start_frame}
       
    global coords   
    n=len(manual_IDs)
    for i in range(n):# i=0,1,2,3,...,n manual IDs
        int_number=manual_IDs[i]
        ext_name=cell_names_external[i]# luckily, they are in the same order
        curr_frame_cell_names.remove(ext_name)
    coords=np.delete(coords_old, (manual_IDs), axis=0)
              
    cut_lineage(internal_start_frame)
    
    canvas_previous.delete('all')
    canvas_current.delete('all')    
    canvas_lineage.delete('all')
    R_remove_dead_cell.config(bg=button_color)
    update_flash([button_execute])
    button_pause.configure(background = button_color)
    button_display.configure(background = button_color)
    R_remove_dead_cell.configure(background=button_color)
    button_save_removed_cell.pack_forget()
    activate_buttons(all_buttons_page4,[ button_execute])
    instruct_var_p4.set("You deleted cells in Frame  "+str(start_frame)+"  /nTo resume tracking, push Button 3.")
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
#################################################
def create_final_movie_p4():# create final movie + pedigree_per_cell (simplified, i.e. only centroids and areas)
  instruct_label_p4.config(text="Creating lineage and final movie...")
  global outpath,frame_size, helper_dir_p4 
  patch_size=true_patch_size.get()           
  update_lineage(lineage_per_frame_p4,helper_dir_p4, 'wb')
  instruct_label_p4.config(text="Lineage per cell is stored in" +str(helper_dir_p4))
    
  lineage_per_cell=print_excel_files(outpath, frame_size,lineage_per_frame_p4, bordersize,patch_size)
  instruct_label_p4.config(text="Lineage per cell is stored in" +str(helper_dir_p4)+
                          "Creating final movie...")
  create_output_movie(outpath, frame_size)       
  instruct_label_p4.config(text="Lineage per cell is stored in  " +str(os.path.join(helper_dir_p4,"lineage_per_cell.pkl"))+
                          "\nFinal movie is in  " + str(os.path.join(outpath,"lineage_movie.avi")))    
################### Buttons and labels Page 4####################
########################################################
button_execute = Button(frame2_page4, text="2. Execute", font='TkDefaultFont 10 bold', 
               bg=button_color, activebackground="red",command=lambda:[threading.Thread(target=execute).start(), update_flash([]), button_display.configure(bg=button_color)])               
button_execute.pack(side=tk.TOP)

button_display = Button(frame2_page4, text="3. Display result", font='TkDefaultFont 10 bold', 
               bg=button_color,activebackground="red", command=lambda: [display_first_frame(), update_flash([])])
button_display.pack(side=tk.BOTTOM)

button_pause = Button(frame2_page4, text="2a. Pause ",activebackground="red",
               bg=button_color, font='TkDefaultFont 10 bold', command=stop_execution_manually)
button_pause.pack(side=tk.RIGHT, padx=45)   
################################################

instruct_label_p4=tk.Label(frame12_page4,textvariable=instruct_var_p4 ,bg="black", fg="yellow", font=all_font, height=5)
instruct_label_p4.pack(fill=BOTH)
 
button_save_id = Button(frame3c_page4, text="Save ID edits", activebackground="red",font=all_font, 
              bg=button_color, command=lambda:stop_editing_IDs())
#button_save_id.pack(side=tk.LEFT, padx=5)
#button_save_id.pack_forget()

button_save_division = Button(frame3c_page4, text="Save division edits",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:stop_editing_division())
#button_save_division.pack(side=tk.LEFT, padx=5)
#button_save_division.pack_forget()

button_save_added_cell = Button(frame3c_page4, text="Save added cell",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:save_added_cell())
#button_save_added_cell.pack(side=tk.LEFT, padx=5)
#button_save_added_cell.pack_forget()

button_save_removed_cell = Button(frame3c_page4, text="Save removed cell",activebackground="red", font=all_font, 
              bg=button_color, command=lambda:save_removed_cell())
#button_save_removed_cell.pack(side=tk.LEFT, padx=5)
#button_save_removed_cell.pack_forget()
################################################################
global R_edit_ID, R_edit_division, R_add_new_cell,R_remove_dead_cell

edit_label_name=tk.Label(frame3a_page4,text="Edit tools",bg=label_color,  font=("Times", "14")).pack(side=tk.LEFT, padx=200)

R_edit_ID = Radiobutton(frame3b_page4, text="Edit IDs", value="Previous", font=all_font, variable=clicked, command=lambda:start_editing_IDs(), background=button_color, activebackground="red")
R_edit_ID.pack(side=tk.LEFT, padx=15)

R_edit_division = Radiobutton(frame3b_page4, text="Edit division",background=button_color, font=all_font,
                 value="Previous", activebackground="red",variable=clicked,  command=lambda:start_editing_division())
R_edit_division.pack(side=tk.LEFT, padx=15)

R_add_new_cell = Radiobutton(frame3b_page4, text="Add cell", value="Previous", font=all_font, variable=clicked, command=lambda:add_new_cell(), background=button_color, activebackground="red")
R_add_new_cell.pack(side=tk.LEFT, padx=20)

R_remove_dead_cell = Radiobutton(frame3b_page4, text="Remove cell",background=button_color, font=all_font,
                 value="Current", activebackground="red",variable=clicked, command=remove_died_cell)    
R_remove_dead_cell.pack(side=tk.LEFT, padx=20)

button_create_excel = Button(frame4_page4, text="4. Create final movie\n and \nExcel files", command=create_final_movie_p4,bg=button_color, font=all_font,activebackground="red")
button_create_excel.pack(pady=20) 
################################################
global label_curr_frame_name 
label_curr_frame_name = tk.Label(frame9_page4, text="           ", bg="black", fg="cyan", font='TkDefaultFont 10 bold' , width=48, height=2)
label_curr_frame_name.pack()
global view_slider# main screen
view_slider = Scale(frame9_page4, from_=1, to=1, orient=HORIZONTAL,bg=label_color, troughcolor="#513B1C", command=slide_frames, length=370)      
view_slider.pack(pady=3)
l_instr_name_p4=tk.Label(frame9_page4,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="white").pack() 
###############################################

global all_buttons_page4
all_buttons_page4=[button_load,button_execute, button_pause,button_display,\
                   R_edit_ID,R_edit_division, R_add_new_cell,R_remove_dead_cell,\
                   button_save_id,button_save_division,button_save_added_cell,button_save_removed_cell,button_create_excel]
###########################################################################
############################## PAGE-5 (STEP-4): CORRECT SEGMENTATION #######
#############################################################################
page5=pages[4]
page5.title("PAGE 5. CORRECT SEGMENTATION")
page5.config(bg=bg_color)
from helpers_for_PAGE_4 import delete_contour_with_specific_colour,update_frame_dictionary_after_manual_segm_correction,\
 load_models_p5, load_tracked_movie_p5, make_contour_red,update_cheatsheet
from plot import paste_patch, prepare_contours,paste_benchmark_patch,create_name_for_cleaned_patch

from interface_functions import turn_image_into_tkinter,display_both_channels, show_2_canvases
from postprocess import create_output_movie
from print_excel import print_excel_files, extract_const_movie_parameters
from functions import  clean_manual_patch, segment_manual_patch,segment_one_cell_at_a_time,create_intensity_dictionary,remove_cell_from_mask
############ LAYOUT
page5.geometry('1530x2000')
global window_p5_size
window_p5_size =600

frame1_page5 = tk.Frame(master=page5, width=1530, height=5, bg=bg_color)
frame1_page5.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page5 = tk.Frame(master=page5, width=1530, height=50, bg=bg_color)
frame2_page5.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame3_page5 = tk.Frame(master=page5, width=1530, height=30, bg=bg_color)
frame3_page5.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
################################################
frame3a_page5 = tk.Frame(master=page5, width=window_p5_size, height=30, bg=bg_color)
frame3a_page5.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
frame3b_page5 = tk.Frame(master=page5, width=window_p5_size, height=30, bg=bg_color)
frame3b_page5.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)
frame3c_page5 = tk.Frame(master=page5, width=1530-2*window_p5_size, height=20, bg=bg_color)
frame3c_page5.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
############################################################################
frame4a_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size, bg=bg_color)
frame4a_page5.grid(row=4, column=0,rowspan=1,columnspan=1, sticky=W+E+N+S)

frame4b_page5 = tk.Frame(master=page5, width=window_p5_size, height=window_p5_size , bg=bg_color)
frame4b_page5.grid(row=4, column=1,rowspan=1,columnspan=1, sticky=W+E+N+S)

frame4c_page5 = tk.Frame(master=page5,width=1530-2*window_p5_size, bg=bg_color)
frame4c_page5.grid(row=4,column=2,rowspan=1,columnspan=1, sticky=W+N+S)
#################################################################
frame5a_page5 = tk.Frame(master=page5, width=window_p5_size, height=15, bg=bg_color)
frame5a_page5.grid(row=5, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame5b_page5 = tk.Frame(master=page5, width=window_p5_size, height=15, bg=bg_color)
frame5b_page5.grid(row=5, column=1, rowspan=1, columnspan=1,sticky=W+E+N+S)
 
frame5c_page5 = tk.Frame(master=page5, width=window_p5_size, height=15, bg=bg_color)
frame5c_page5.grid(row=5, column=2, rowspan=1, columnspan=1,sticky=W+E+N+S)
#########################################
frame_radio_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame_radio_page5.grid(row=6, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)
########################################################
frame_slider_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame_slider_page5.grid(row=6, column=1, rowspan=1, columnspan=1,sticky=W+E+N+S)
####################################
overlay = tk.Frame(page5,width=50, height=50, bg=bg_color, bd=0)
overlay.grid(row=6, column=1, rowspan=1, columnspan=1,sticky=W+E+N+S)
overlay.lift() 
#####################################
frame_excel_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame_excel_page5.grid(row=6, column=2, rowspan=1, columnspan=1,sticky=W+E+N+S)
##############################
frame6_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame6_page5.grid(row=7, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

frame7_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame7_page5.grid(row=8, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)
###################################################
gap_frame_page5 = tk.Frame(master=page5, width=50, height=5, bg=bg_color)
gap_frame_page5.grid(row=9, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)

####################################
frame8_page5 = tk.Frame(master=page5, width=50, height=50, bg=bg_color)
frame8_page5.grid(row=10, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)
overlay_exit = tk.Frame(master=page5, width=50, height=50, bg=bg_color, bd=0)
#overlay_exit.grid(row=10, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)
#overlay_exit.lift() 
######### POPULATE WITH LABELS
l_title = tk.Label(frame1_page5, text="STEP 4: CORRECT SEGMENTATION",
              bg="yellow", fg="red", font=("Times", "24"))
l_title.pack()

feedback_label_5 = tk.Label(frame2_page5, text="Movie:      \nFluorescent frames:    Bright frames:       Red frames:       \nFrame size:       Cell diameter: ",
                          fg="cyan",bg="black", font='TkDefaultFont 10 bold', width=200,height=3)
feedback_label_5.grid(row=0, column=0, sticky="w")
#####################################
global canvas_bright_p5,canvas_fluor_p5
canvas_bright_p5 = Canvas(frame4a_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_bright_p5.pack()

canvas_fluor_p5 = Canvas(frame4b_page5, bg=bg_color, height=window_p5_size, width=window_p5_size)
canvas_fluor_p5.pack()
################################################
label_bright_name=tk.Label(frame5a_page5, text=" ",bg="black", fg="cyan", font=all_font, height=1)
label_bright_name.pack(fill=BOTH)

label_fluor_name=tk.Label(frame5b_page5, text=" ",bg="black", fg="cyan", font=all_font, height=1)
label_fluor_name.pack(fill=BOTH)
#####################################################
status_name_label=tk.Label(frame4c_page5 , text="STATUS ", height=1, bg="green", fg="black", font='TkDefaultFont 14 bold' )
status_name_label.pack(fill=BOTH)

cell_monitor_label=tk.Label(frame4c_page5 , text="No movie loaded yet ", height=1, bg="black", fg="cyan", font='TkDefaultFont 14 bold' )
cell_monitor_label.pack(fill=BOTH)
mode_monitor_label=tk.Label(frame4c_page5 , text=" ", height=1, bg="black", fg="cyan", font='TkDefaultFont 14 bold' )
mode_monitor_label.pack(fill=BOTH)
zoom_monitor_label=tk.Label(frame4c_page5 , text=" ", height=1, bg="black", fg="cyan", font='TkDefaultFont 14 bold' )
zoom_monitor_label.pack(fill=BOTH)
pan_monitor_label=tk.Label(frame4c_page5 , text=" ", height=1, bg="black", fg="cyan", font='TkDefaultFont 14 bold' )
pan_monitor_label.pack(fill=BOTH)
###########################################
global cheatsheets
cheatsheets=[]
cheat_sheet_label=tk.Label(frame4c_page5 , text=" ", height=1, bg=bg_color, fg="black", font='TkDefaultFont 14 bold' )
cheat_sheet_label.pack(fill=BOTH)
cheatsheets.append(cheat_sheet_label)
############################
for k in range(8):
        if k==5 or k==7:
            label_height=2
        else:
            label_height=1
        item=tk.Label(frame4c_page5 , text=" ", height=label_height, bg=bg_color, fg="black", font='TkDefaultFont 14 bold' )
        item.pack(fill=BOTH)
        cheatsheets.append(item)
#####################################################################
l_instr_name_p5=tk.Label(frame6_page5,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="white").pack()
###################################################
dialog_label_5 = tk.Label(frame7_page5, text="Step-4 allows you to manually correct segmentation in tracked movie."
                          "\nTo load a tracked movie, click Button 1 and navigate to TRACKED_MOVIE_{your movie name}",
                          fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=200,height=3)
dialog_label_5.grid(row=0, column=0, sticky="w")
###################################################
global state_indicator
state_indicator="slide_bar"
############################################
def disable_frame():#overlay slidebar to prevent from touching accidentally   
    overlay.grid(row=6, column=1, rowspan=1, columnspan=1,sticky=W+E+N+S)
    overlay.lift()  # Ensure overlay is on top
###################################################
def enable_frame():
    global state_indicator
    state_indicator="slide_bar"
    overlay.grid_forget()    
#################################################
def disable_exit():#overlay exit button to foce user to save edits   
    overlay_exit.grid(row=10, column=0, rowspan=1, columnspan=3,sticky=W+E+N+S)
    overlay_exit.lift()# Ensure overlay is on top
###################################################
def enable_exit():    
    overlay_exit.grid_forget()    
#################################################
def slide_frames_p5(value):
    cell_monitor_label.config(text="No cell chosen yet")
    global save_frame_edits_alert, previous_frame_number        
    if save_frame_edits_alert ==True:
          save_edits_for_frame()
          previous_frame_number=-2
    image_number = int(value)
    #print("image_number=", image_number)    
    internal_frame_number_for_slider=image_number-first_frame_number_p5
    ###########################################
    activated_channel=active_channel_var.get()
    if activated_channel=="fluor":    
        label_fluor_name.config(text=os.path.basename(path_filled_fluors[internal_frame_number_for_slider]))     
        label_bright_name.config(text=os.path.basename(path_filled_brights[internal_frame_number_for_slider])) 
    else:    
        label_fluor_name.config(text=os.path.basename(path_filled_brights[internal_frame_number_for_slider]))     
        label_bright_name.config(text=os.path.basename(path_filled_fluors[internal_frame_number_for_slider])) 
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,internal_frame_number_for_slider, window_p5_size, activated_channel)
    dialog_label_5.config(text="To check segmentation in each frame, use the slide bar."
                            "\nIf manual correction is needed in a certain frame, stop the slider and right-click the cell that needs correction.")          
############################# load all mecessary images
def choose_and_load_tracked_movie():
    global edits_indicator
    edits_indicator="no"
    global button_load_p5
    update_flash([])
    button_load_p5.configure(background = 'red')
    global output_dir_p5, input_dir_p5,software_folder, helper_dir_p5
    output_dir_p5 = filedialog.askdirectory()# \TRACKED_MOVIE_{movie name}
    print("output_dir_p5 =", output_dir_p5)
    dialog_label_5.config(text="Choose your movie and click on it once (not twice!)")  
    ##################################
    helper_dir_p5=os.path.join(output_dir_p5,"HELPER_FOLDERS_(NOT FOR USER)")               
    head_tail=os.path.split(output_dir_p5)
    head =head_tail[0]    
    input_movie_name="ONE_WELL_MOVIE_"+os.path.basename(head)
    input_dir_p5  =os.path.join(head,input_movie_name)# \ONE_WELL_MOVIE_{movie name}
    print(" input_dir_p5 =",  input_dir_p5 )    
    #######################################################
    global path_filled_brights,path_filled_fluors,path_masks
    global empty_fluors, empty_brights,filled_fluors, filled_brights, masks
    global lineage_per_frame_p5
    dialog_label_5.config(text="loading tracked movie...")
    path_filled_brights,path_filled_fluors,path_masks, empty_fluors, empty_brights, filled_fluors, filled_brights, masks, lineage_per_frame_p5=load_tracked_movie_p5(input_dir_p5,output_dir_p5)
    global frame_p5_size,cell_radius_p5,patch_size_p5,full_core_red_name, first_frame_number_p5,red_dictionary, bordersize, n_digits   
    #############
    frame_p5_size, cell_radius_p5, patch_size_p5,max_number_of_cells,\
           num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number_p5,\
           base_colours,contrast_value,number_cells_in_first_frame,full_core_red_name,red_dictionary, bordersize, delta=extract_const_movie_parameters(helper_dir_p5)
    #################################
    global red_keys
    red_keys =list(red_dictionary.keys())
    print("red_keys",red_keys)
    print("full_core_red_name=",full_core_red_name)
    global resize_coeff, new_shape
    resize_coeff=window_p5_size /frame_p5_size
    global  image_origin_x,image_origin_y, factor_in, factor_out,factor,zoom_coeff,delta_x,delta_y, cell_center_visual_x, cell_center_visual_y# for zooming
    delta_x, delta_y=0,0
    factor_in, factor_out, factor=1,1,1
    image_origin_x,image_origin_y=0,0
    zoom_coeff=1
    new_shape=window_p5_size
    cell_center_visual_x,cell_center_visual_y=300,300
    global last_draw_zoom_coeff
    last_draw_zoom_coeff=1
    ############################
    #global active_channel_var
    #active_channel_var=StringVar()
    #active_channel_var.set("fluor")
    print("frame_p5_size=",frame_p5_size)
    feedback_label_5.configure(text="Movie : "+input_dir_p5+"\nFluorescent frames: "+str(num_frames)+\
                               "   Bright frames: "+str(len(filled_brights))+"   Red frames:"+str(len(red_keys))+\
                                   "\nFrame size = "+ str(frame_p5_size)+" x "+str(frame_p5_size)+"   Cell diameter = "+str(cell_radius_p5*2))   
    global photo_filled_fluors, photo_filled_brights
    dialog_label_5.config(text="Preparing images for display...")
    photo_filled_fluors=[ turn_image_into_tkinter(filled_fluors[i], window_p5_size,[]) for i in range(len(masks))]
    dialog_label_5.config(text="Prepared 50 % of images for display")
    photo_filled_brights=[ turn_image_into_tkinter(filled_brights[i], window_p5_size,[]) for i in range(len(masks))]
    
    global canvas_fluor_p5, canvas_bright_p5
    image_number=1 
    
    show_2_canvases(canvas_bright_p5,canvas_fluor_p5,photo_filled_brights,photo_filled_fluors,image_number, window_p5_size, active_channel_var.get())        
    #view_slider_p5.configure(to=len(masks))
    global save_frame_edits_alert
    save_frame_edits_alert=False   
    view_slider_p5.configure(from_=first_frame_number_p5,to=first_frame_number_p5+len(masks)-1)
    ################################################
    button_load_p5.configure(background = button_color)  
    activate_buttons(all_buttons_page5,[view_slider_p5, button_final_movie])
    ######################### new addtion for click_one_cell
    global mode_variable,zoom_status# used in radio buttons for editing,indicates which canvas is used for IDs extraction, value = "Current" or "Previous"
    mode_variable,zoom_status = StringVar(),StringVar()
    mode_variable.set(" ") 
    zoom_status.set("off")
    #activate_fast_edit_mode()
    global previous_frame_number, previous_cell_number
    previous_frame_number, previous_cell_number=-2, -2
    print("previous_frame_number=",previous_frame_number)
    canvas_fluor_p5.unbind("<Button-3>")   
    canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)
    global oval,oval_x,oval_y
    oval_x,oval_y=1,1
    oval=canvas_fluor_p5.create_oval(oval_x-1, oval_y-1, oval_x+1,
                          oval_y+1, outline="magenta",  width=1)
    global points, contour_parameters, init_contour_parameters
    points,contour_parameters,init_contour_parameters=[],[],[]
    enable_frame()
    global zoom_counter
    zoom_counter=0
    active_channel_var.set("fluor")
    swap_active_channel()
    global current_cell_number
    current_cell_number=None
########################################
def activate_fast_edit_mode():#enter fast segmentation mode
   print("FAST MODE ACTIVATED")
   #button_activate_fast_edit_mode.configure(background = 'red')
   active_fast_label.config(text="Activated", fg="red")
   button_activate_slow_edit_mode.configure(background = button_color)   
   #dialog_label_5.config(text="\nIn the right image, right-click on the cell you want to correct.")   
   mode_variable.set("Fast")   
#########################################################
def activate_hand_drawing_mode_for_one_cell():    
    dialog_label_5.config(text="Draw the contour of the cell with the left mouse.\n If you want to erase the drawn contour, right-click the mouse anywhere in the background.\nOnce you are finished, right-click inside magenta circle to save your edits.")    
    
    global cell_contour_fl, cell_contour_br,points, mask_hand, points_for_original,contour_parameters, init_contour_parameters# for the clicked cel
    cell_contour_fl=[]
    cell_contour_br=[]
    points, points_for_original=[],[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    contour_parameters=[]
    init_contour_parameters=[]
###########################################  
def activate_slow_edit_mode():
    print("SLOW MODE ACTIVATED")
    global state_indicator
    state_indicator="drawing"
    mode_monitor_label.config(text="Slow mode", fg="red") 
    update_cheatsheet(cheatsheets,"Slow",bg_color,label_color)
    mode_variable.set("Slow")
    button_activate_slow_edit_mode.configure(background = 'red')
    #button_activate_fast_edit_mode.configure(background = button_color)
    active_fast_label.config(text="Disabled", fg="cyan")
    #dialog_label_5.config(text="Right-click on the cell you want to correct. Its contours should disappear.")
    activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode,start_zoom_button])
    ########################## delete contour of the clicked ce;;
    global canvas_fluor_p5,canvas_bright_p5
    canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.unbind("<B1-Motion>")
    canvas_fluor_p5.unbind( "<ButtonPress-1>")
    canvas_fluor_p5.unbind("token<ButtonRelease-1>")    
    canvas_fluor_p5.bind("<Button-1>", get_x_and_y)      
    canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse)             
    activate_hand_drawing_mode_for_one_cell()       
    ################################  
    global   filled_fluor, filled_bright, filled_red, empty_fluor, empty_bright, empty_red, cell_color, photo_fluor,photo_bright, filled_fluor_copy, filled_bright_copy
    global final_mask,cell_number_in_frame,intensity_dictionary_for_frame
    
    filled_fluor_copy=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
    filled_bright_copy=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
    
    filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
    filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
    if red_channel_indicator==1:
       filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color)   
    final_mask=remove_cell_from_mask(current_cell_number, final_mask, intensity_dictionary_for_frame)   
    # display frames with erased cell     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y, active_channel_var.get())
    global oval_x,oval_y, factor# create magenta oval on clicked cell
    oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)   
#############################################
def right_click_one_cell(event):# extract info about clicked celland take action
    mode=mode_variable.get()# after right-clicking cell, extract mode, frame_number and cell_number
    print("INSIDE RIGHT CLICK")
    global frame_number, previous_frame_number, previous_cell_number, canvas_fluor_p5, canvas_bright_p5, final_mask, current_cell_number
    global clicked_cell_position_marker, current_cell_number, filled_fluor, filled_bright, filled_red
    global oval, cell_color, cell_ID, zoom_counter, click_indicator,state_indicator
    global oval_x_init,oval_y_init, oval_x,oval_y, contour_parameters  
    ############################################
    global  internal_frame_number_p5,save_frame_edits_alert
    #############################################
    global all_buttons_page5,button_activate_fast_edit_mode,button_activate_slow_edit_mode,start_zoom_button
    activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode,start_zoom_button])
    ##############################################    
    frame_number =view_slider_p5.get()
    print("frame_number=",frame_number)
    print("first_frame_number_p5 =",first_frame_number_p5 )
    print("red_dictioanry", red_dictionary)
    internal_frame_number_p5=frame_number-first_frame_number_p5        
    mask=masks[internal_frame_number_p5]      
    clicked_cell_position_marker=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]# position marker in image of original size!!!  
    print("previous_frame_number=", previous_frame_number)
    ###################################################        
    ####################################################
    zero_or_not=mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]
    print("zero_or_not=",zero_or_not)
    if zero_or_not==0:# you hit background accidentally
        if mode=="Slow":
             erase_line()
             mode_monitor_label.config(text="You deleted contour", fg="cyan")
        else:
            cell_monitor_label.config(text="Error:You clicked on background", fg="red")
    else:# you clicked on a cell body
         print("I clicked on a cell body")
    ##########################################################                                 
         if frame_number!=previous_frame_number:# if you are in a new frame 
             print("I am in a new frame")
             clicked_cell_number_in_mask=zero_or_not                                                      
             get_frame_info(internal_frame_number_p5)
             previous_frame_number=frame_number 
         else:# if you are still the same frame
             print(" I am in the same frame")
             if mode=="Fast":
                 clicked_cell_number_in_mask=final_mask[clicked_cell_position_marker[1],clicked_cell_position_marker[0]]
             else:
                 clicked_cell_number_in_mask=zero_or_not
         ##################################### 
         print(" clicked_cell_number_in_mask=", clicked_cell_number_in_mask)
         clicked_cell_number_in_frame =int(math.log(round(clicked_cell_number_in_mask),2))
         #############################################        
         if current_cell_number==None:      
           print("Clicked on new cell,fast mode")
           activate_fast_edit_mode()
           current_cell_number=clicked_cell_number_in_frame
           global cell_name_to_screen, cell_color_to_screen
           cell_color_to_screen=cells_in_current_frame_sorted[current_cell_number][1][1]
           cell_name_to_screen=cells_in_current_frame_sorted[current_cell_number][0]
           if len(contour_parameters)!=0:
                         erase_line()
           state_indicator="clicking"
           cell_monitor_label.config(text="Edit Cell "+ str(cell_name_to_screen)+" ( "+cell_color_to_screen+" )", fg="cyan")
           mode_monitor_label.config(text="Fast mode", fg="red")
           update_cheatsheet(cheatsheets,"fast",bg_color,label_color)           
           disable_frame()
           canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)
           #canvas_fluor_p5.unbind("<Button-3>")   
           # canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)                                                              
           canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell            
           cell_color=cells_in_current_frame_sorted[clicked_cell_number_in_frame][1][0]
           cell_ID=cells_in_current_frame_sorted[clicked_cell_number_in_frame][0]
           ########################################                   
           oval_x_init,oval_y_init=event.x,event.y# coordinates in window
           oval_x,oval_y=oval_x_init,oval_y_init
                     
           global red_color,filled_fluor_copy,filled_bright_copy,filled_red_copy                  
           red_color= [0,0,255,255]
           filled_fluor_copy,filled_bright_copy=filled_fluor.copy(),filled_bright.copy()                    
           filled_fluor_copy=make_contour_red(filled_fluor_copy, empty_fluor,cell_color)
           filled_bright_copy=make_contour_red(filled_bright_copy, empty_bright,cell_color)
           if red_channel_indicator==1:
                filled_red_copy=filled_red.copy() 
                filled_red_copy=make_contour_red(filled_red_copy, empty_red,cell_color)
                          
           global photo_fluor, photo_bright
           canvas_bright_p5.delete("all")
           canvas_fluor_p5.delete("all")
           #global photo_fluor_copy, photo_bright_copy
           canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y,active_channel_var.get())
           #canvas_fluor_p5.delete(oval)      
           oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
           oval_y+5*factor, outline="magenta", width=1)                               
         else:#if current_cell_number!=None, i.e.you are in the middle of editing  
           if clicked_cell_number_in_frame!=current_cell_number:
               cell_monitor_label.config(text="Error:You clicked on wribg cell", fg="red")
           else:# clicked on the current cell to save it
              print("I hit the cell with the same numvber to save edits")
              if mode=="Fast":                    
                   update_cheatsheet(cheatsheets,"neutral",bg_color,label_color)
                   save_one_edited_cell()
                    
                   save_frame_edits_alert=True 
                   enable_frame()
                    
                   canvas_fluor_p5.unbind("<Button-1>")
                   mode_monitor_label.config(text=" ")
                   state_indicator="slide_bar"
                   #cell_monitor_label.config(text="Saved Cell "+ cell_name+" ( "+cell_color_to_screen+" )", fg="cyan")
                   if zoom_counter!=0:
                        zoom_counter=0
                        zoom_monitor_label.config(text=" ")
                   current_cell_number=None
              if mode=="Slow":
                  print(" SLOW MODE:clicked on  same cell to save it")
                  mode_monitor_label.config(text=" ")
                  update_cheatsheet(cheatsheets,"neutral",bg_color,label_color)
                  save_one_edited_cell()
                  
                  save_frame_edits_alert=True 
                    
                  enable_frame()
                  state_indicator="slide_bar"
                     
                  canvas_fluor_p5.unbind("<Button-1>")
                  canvas_fluor_p5.unbind("<B1-Motion>")
                  canvas_fluor_p5.unbind( "<ButtonPress-1>")
                  canvas_fluor_p5.unbind("token<ButtonRelease-1>")
                  if zoom_counter!=0:
                         zoom_counter=0
                         zoom_monitor_label.config(text=" ")
                  current_cell_number=None
                  #activate_fast_edit_mode()
################################################
def get_x_and_y(event):
    global lasx,lasy
    lasx,lasy=event.x,event.y         
#########################################   
def draw_with_mouse(event):
    #global state_indicator
    #state_indicator="drawing"
    mode_monitor_label.config(text="Hand drawing...", fg="red")
    global coeff
    global lasx,lasy, line_fl, line_br,xx,yy, last_draw_zoom_coeff
    global contour_parameters, cell_contour_fl,cell_contour_br, init_contour_parameters
    xx,yy=event.x,event.y
    line_fl=canvas_fluor_p5.create_line((lasx,lasy,xx,yy), fill="red", width=5)   
    line_br=canvas_bright_p5.create_line((lasx,lasy,xx,yy), fill="red", width=5)
    contour_parameters.append((lasx,lasy,xx,yy))
    init_contour_parameters= contour_parameters
    get_x_and_y(event)
    cell_contour_fl.append(line_fl)
    cell_contour_br.append(line_br)   
    last_draw_zoom_coeff =zoom_coeff
    #print("last_draw_zoom_coeff INSIDE DRAW WITH MOUSE=",last_draw_zoom_coeff )
    points.append([[int(round(lasx/zoom_coeff-image_origin_x)),int(round(lasy/zoom_coeff-image_origin_y))]])
    points_for_original.append([[int(round((lasx-image_origin_x)/resize_coeff)),int(round((lasy-image_origin_y)/resize_coeff))]])  
###################################   
def erase_line():# in case you are not happy with your hand contour and want to delete it
    global cell_contour_fl, cell_contour_br, points,mask_hand, final_mask, points_for_original, contour_parameters, init_contour_parameters    
    for i in range(len(cell_contour_fl)):        
         canvas_fluor_p5.delete(cell_contour_fl[i])
         canvas_bright_p5.delete(cell_contour_br[i])
    contour_parameters=[]
    init_contour_parameters=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    cell_number_in_mask=2**current_cell_number
    final_mask[final_mask==cell_number_in_mask]=0
    points, points_for_original=[],[]
    cell_contour_fl, cell_contour_br=[],[]    
############  ZOOMING FUNCTIONS ##########
###############################################
def start_zoom():
    zoom_status.set("on")
    zoom_monitor_label.config(text="Zoom activated", fg="red")
    
    activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode])   
    global my_image_fl, my_image_br, points, canvas_fluor_p5, canvas_bright_p5,photo_fluor, photo_bright, internal_frame_number,x0,y0, points_for_original
    points,points_for_original=[],[]
    frame_number=view_slider_p5.get()
    internal_frame_number_p5=frame_number-first_frame_number_p5

    canvas_fluor_p5.delete("all")
    canvas_bright_p5.delete("all")
    ####################################
    global oval_x,oval_y,cell_center_visual_x,cell_center_visual_y
    #print("cell_centre_visual_x,cell_center_visual_y START_ZOOM=",cell_center_visual_x,cell_center_visual_y)
    ####### place cell of interest in the center of window when start zooming
    x0, y0=clicked_cell_position_marker[0],clicked_cell_position_marker[1]#x0, y0 - for original photo  
    image_origin_x,image_origin_y= cell_center_visual_x-oval_x, cell_center_visual_y-oval_y
  
    global zoom_counter
    zoom_counter=0
    
    oval_x,oval_y= cell_center_visual_x, cell_center_visual_y
    canvas_bright_p5,canvas_fluor_p5, photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y,active_channel_var.get())
          
    oval=canvas_fluor_p5.create_oval(oval_x-5, oval_y-5, oval_x+5,
                       oval_y+5, outline="magenta", width=1)    
    canvas_fluor_p5.bind('<MouseWheel>', wheel)
    init_zoom_factor =round(frame_p5_size/(4*cell_radius_p5),1) 
    global factor_in, factor_out,  factor_input, factor
    factor_in, factor_out,  factor_input, factor= init_zoom_factor , init_zoom_factor , init_zoom_factor,init_zoom_factor 
    apply_zoom(factor_input)
##############################################
def start_pan():    
    pan_monitor_label.config(text="Pan activated", fg="red")
    canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.unbind("<Button-3>")
    canvas_fluor_p5.unbind("<MouseWheel>")    
    canvas_fluor_p5.bind( "<ButtonPress-1>", drag_start)
    canvas_fluor_p5.bind("token<ButtonRelease-1>", drag_stop)
    canvas_fluor_p5.bind("<B1-Motion>", drag)
    activate_buttons(all_buttons_page5,[stop_pan_button])
    update_cheatsheet(cheatsheets,"pan",bg_color,label_color)                            
    R_bright.config(state=DISABLED)
    R_fluor.config(state=DISABLED)
    zoom_monitor_label.config(text=" ", fg="red")
    mode_monitor_label.config(text=" ", fg="red")
#######################################
def stop_pan():
    pan_monitor_label.config(text=" ")
    canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.unbind("token<ButtonRelease-1>")
    canvas_fluor_p5.unbind("<B1-Motion>")
    mode=mode_variable.get()
    if mode=="Fast":
       canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)        
    else:
       canvas_fluor_p5.bind("<Button-1>", get_x_and_y)        
       canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse)  
    canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)
    canvas_fluor_p5.bind('<MouseWheel>', wheel)
    update_cheatsheet(cheatsheets,mode,bg_color,label_color) 
    activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode])
    R_fluor.config(state=NORMAL)
    R_bright.config(state=NORMAL)
    zoom_monitor_label.config(text="Zoom activated", fg="red")
    mode_monitor_label.config(text=str(mode) +" mode", fg="red")
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
        # record the new position
        x = event.x
        y= event.y
        # recalculater center of image_resized after dragging
        image_origin_x+=delta_x
        image_origin_y+=delta_y
        canvas_fluor_p5.delete("all")
        
        image_object=canvas_fluor_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_fluor)
        canvas_bright_p5.delete("all")
        canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
       
        cell_center_visual_x+=delta_x
        cell_center_visual_y+=delta_y 
       
        oval_x+=delta_x
        oval_y+=delta_y
        oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
        ################### re-draw contour(when in slow mode)       
        global contour_parameters, init_contour_parameters
        if len(contour_parameters)!=0:           
          new_contour_parameters=[]
          for k in range(len(contour_parameters)):
             item=contour_parameters[k]
             #############################
             new_las_x=int(round(delta_x+item[0]))
             new_las_y=int(round(delta_y+item[1]))
             new_xx=int(round(delta_x+item[2]))
             new_yy=int(round(delta_y+item[3]))          
             new_item=[new_las_x,new_las_y,new_xx,new_yy]           
             new_contour_parameters.append(new_item)
          contour_parameters=new_contour_parameters
          #print("new_contour_parameters=", contour_parameters[-1])
          for i in range(len(contour_parameters)):         
            line_fl=canvas_fluor_p5.create_line(contour_parameters[i], fill="red", width=5)
            line_br=canvas_bright_p5.create_line(contour_parameters[i], fill="red", width=5)    
            cell_contour_fl.append(line_fl)
            cell_contour_br.append(line_br)   
          init_contour_parameters= contour_parameters
        ########################
##################################
def apply_zoom(factor_input):
    global  photo_fluor, my_image_fl,photo_bright, my_image_fl_resized, x0, y0,image_object,  zoom_coeff, image_origin_x, image_origin_y, resize_coeff, new_shape,my_image_br_resized 
    global oval_x_init, oval_y_init, oval_x,oval_y, factor, cell_center_visual_x, cell_center_visual_y 
    global points, points_for_original
    my_image_fl_resized=filled_fluor_copy.copy()
    my_image_fl_resized= cv2.resize(my_image_fl_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)      
    my_image_fl_resized = cv2.resize(my_image_fl_resized,(int(my_image_fl_resized.shape[0] * factor_input), int(my_image_fl_resized.shape[1] * factor_input)), cv2.INTER_LINEAR)      
              
    my_image_br_resized=filled_bright_copy.copy()
    my_image_br_resized= cv2.resize(my_image_br_resized,(window_p5_size,window_p5_size), cv2.INTER_LINEAR)
    my_image_br_resized = cv2.resize(my_image_br_resized,(int(my_image_br_resized.shape[0] * factor_input ), int(my_image_br_resized.shape[1] * factor_input)), cv2.INTER_LINEAR)   
    new_shape=my_image_fl_resized.shape[0]
   
    x0_new_factor, y0_new_factor=oval_x_init*factor_input,oval_y_init*factor_input
    activated_channel=active_channel_var.get()
    if activated_channel=="fluor":
        photo_fluor =  turn_image_into_tkinter(my_image_fl_resized,new_shape,[])
        photo_bright =  turn_image_into_tkinter(my_image_br_resized,new_shape,[])
    else:
        photo_bright =  turn_image_into_tkinter(my_image_fl_resized,new_shape,[])
        photo_fluor =  turn_image_into_tkinter(my_image_br_resized,new_shape,[])
                    
    image_origin_x, image_origin_y= cell_center_visual_x-x0_new_factor, cell_center_visual_y-y0_new_factor
    canvas_fluor_p5.delete("all")
    canvas_bright_p5.delete("all")
    ########################################
    image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=photo_fluor)
    canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
    ##################################################
    resize_coeff=new_shape/frame_p5_size
    zoom_coeff=new_shape/window_p5_size
    oval_x, oval_y= cell_center_visual_x, cell_center_visual_y
    oval=canvas_fluor_p5.create_oval(oval_x-5*factor_input, oval_y-5*factor_input, oval_x+5*factor_input,
                       oval_y+5*factor_input, outline="magenta", width=1)
    ############### re-draw contour if any
    global last_draw_zoom_coeff
    fac=factor_input/last_draw_zoom_coeff
    global init_contour_parameters, contour_parameters
    if len(init_contour_parameters)!=0:       
       contour_parameters=[]
       for k in range(len(init_contour_parameters)):
           item=init_contour_parameters[k]
           #############################
           new_las_x=int(round(cell_center_visual_x-fac*(cell_center_visual_x-item[0])))
           new_las_y=int(round(cell_center_visual_y-fac*(cell_center_visual_y-item[1])))
           new_xx=int(round(cell_center_visual_x-fac*(cell_center_visual_x-item[2])))
           new_yy=int(round(cell_center_visual_y-fac*(cell_center_visual_y-item[3])))          
           new_item=[new_las_x,new_las_y,new_xx,new_yy]           
           contour_parameters.append(new_item)
       #print("new_contour_parameters=", contour_parameters[-1])
       for i in range(len(contour_parameters)):         
          line_fl=canvas_fluor_p5.create_line(contour_parameters[i], fill="red", width=5)
          line_br=canvas_bright_p5.create_line(contour_parameters[i], fill="red", width=5)    
          cell_contour_fl.append(line_fl)
          cell_contour_br.append(line_br)           
    factor=factor_input    
################################
def wheel(event):
        ''' Zoom with mouse wheel '''
        global zoom_counter
        zoom_counter+=1
        if zoom_counter==1:
            activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode,start_pan_button])
        activate_buttons(all_buttons_page5,[button_activate_slow_edit_mode,start_pan_button])              
        global factor_in, factor_out, factor_input
        if  event.delta == -120:
          factor_out*=0.8
          factor_in*=0.8 
          factor_input=factor_out
          apply_zoom(factor_input)          
        if   event.delta == 120:
          factor_in*=1.2
          factor_out*=1.2
          factor_input=factor_in
          apply_zoom(factor_input)                
###############################################
def start_drawing():    
    canvas_fluor_p5.unbind("all")   
    canvas_fluor_p5.bind("<Button-1>",  get_x_and_y)
    canvas_fluor_p5.bind("<B1-Motion>", addLine)
    global points, points_for_original
    points=[]
    points_for_original=[]
#####################################################
def stop_zoom():   
    print("inside stop_zoom")
    global  canvas_fluor_p5,canvas_bright_p5,photo_fluor, photo_bright
    canvas_fluor_p5.delete("all")
    canvas_bright_p5.delete("all")    
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,0,0,active_channel_var.get())
    ######################### reset all parameters to initial values    
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
    zoom_monitor_label.config(text=" ")

    global cell_center_visual_x,cell_center_visual_y
    #print("cell_centre_visual_x,cell_center_visual_y BEFORE=",cell_center_visual_x,cell_center_visual_y)
    cell_center_visual_x,cell_center_visual_y=300,300
    #print("cell_centre_visual_x,cell_center_visual_y AFTER=",cell_center_visual_x,cell_center_visual_y)
    canvas_fluor_p5.unbind("<MouseWheel>")
################################################
def save_one_edited_cell():
    activate_buttons(all_buttons_page5,[view_slider_p5, button_final_movie])    
    cell_monitor_label.config(text="Saved Cell  "+ str(cell_name_to_screen)+" ( "+cell_color_to_screen+" )", fg="cyan")
    dialog_label_5.config(text="You saved Cell " + str(cell_name_to_screen)+" ( "+cell_color_to_screen+" )"+
                          ".\nNow, you can either continue editing other cells or finish by pushing Button 6."
                          "\nNote: you cannot exit until you push Button 6.")
    button_activate_slow_edit_mode.configure(background = button_color) 
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, points, filled_fluor, filled_bright, filled_red, final_mask
    print("INSIDE SAVE ONE EDITED CELL")
    #print("len(points)=",len(points))
    #print("len(points_for_original)=",len(points_for_original))
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_BEFORE.tif",final_mask*10)      
    if len(points)!=0:# if it was hand drawing 
       print("it was hand drawing")
       ctr = np.array(points_for_original).reshape((-1,1,2)).astype(np.int32)# turn drawn points into contour (ctr)      
       cell_number_in_mask=2**current_cell_number
                  
       mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)      
       cv2.drawContours(mask_hand,[ctr],0,(255,255,255),-1)       
       mask_hand_uint64= mask_hand.astype(np.uint64)      
       mask_hand_uint64[mask_hand_uint64==255]=cell_number_in_mask     
       final_mask+=mask_hand_uint64
      
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
       modified_cell_IDs[current_cell_number]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], cell_color, cell_ID]  
       #########################################
       global oval
       canvas_fluor_p5.delete(oval)
       cv2.drawContours(filled_fluor,[ctr] , 0, cell_color, 1)
       cv2.drawContours(filled_bright,[ctr] , 0, cell_color, 1)
       if red_channel_indicator==1:
            cv2.drawContours(filled_red,[ctr] , 0, cell_color, 1)
       canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y,active_channel_var.get())
       #oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor,oval_x+5*factor,
                       #oval_y+5*factor, outline="magenta",  width=1)             
       #points=[]          
       #dialog_label_5.config(text="If you want to hand draw  another cell, push Button 4 once again.\n If you are finished with the current frame, press Button 6."
                          #"\nIf you are finished with the whole movie, press Button 7.")
    else:# if it was fast editing
      print("it was fast editing")        
      filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)     
      filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
          
      filled_fluor=paste_patch(filled_fluor,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)      
      filled_bright=paste_patch(filled_bright,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)
      if red_channel_indicator==1:
          filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color)  
          filled_red=paste_patch(filled_red,patch_with_contours,a,b,c,d,cell_color,1.0, frame_p5_size,bordersize)                  
      canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y,active_channel_var.get())
    
    canvas_fluor_p5.delete(oval)      
    oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)
    print("zoom_status=", zoom_status.get())
    if zoom_status.get()=="on":
          stop_zoom()
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_AFTER.tif",final_mask*10)      
                           
#################################################
def edit_by_clicking(event):      
      mode_monitor_label.config(text="Editing by clicking...", fg="red")
      number_of_clicks=[]# this is for flashing only        
      global manually_clicked_centroid, final_mask, a,b,c,d       
      manually_clicked_centroid=[int(round((event.x-image_origin_x)/resize_coeff)),int(round((event.y-image_origin_y)/resize_coeff))]      
      dialog_label_5.config(text=str(manually_clicked_centroid))
      number_of_clicks.append(manually_clicked_centroid)
      
      segmented_frame, segmented_patch,a,b,c,d, final_mask, new_centroid=segment_one_cell_at_a_time(segmentor, refiner,empty_fluor,empty_bright,manually_clicked_centroid, cell_radius_p5, frame_p5_size, patch_size_p5, clicked_cell_position_marker,final_mask,current_cell_number, bordersize)
      ############## modify mask for frame
      new_cX, new_cY=new_centroid[0],new_centroid[1]
      mask_with_current_cell=paste_benchmark_patch(segmented_patch,a,b,c,d,current_cell_number, frame_p5_size, bordersize)      
      cell_number_in_mask=2**current_cell_number     
      final_mask=remove_cell_from_mask(current_cell_number, final_mask, intensity_dictionary_for_frame)     
      final_mask+=mask_with_current_cell# insert current contour of cell
      #cv2.imwrite(r"C:\Users\helina\Desktop\segmented_patch.tif",segmented_patch)      
      ################### modify fluor, bright and red current frame
      global patch_with_contours
      patch_with_contours=prepare_contours(segmented_patch)    
      global filled_fluor_copy, filled_bright_copy, filled_red_copy
      ### here a very important dictionary of modified cells is created multiple times
      modified_cell_IDs[current_cell_number]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], cell_color, cell_ID]      
      dialog_label_5.config(text="If you are unable to achieve good segmentation by just clicking, start hand drawing mode by pushing Button 2.")     
      
      filled_fluor_copy=delete_contour_with_specific_colour(filled_fluor_copy, empty_fluor,red_color)     
      filled_bright_copy=delete_contour_with_specific_colour(filled_bright_copy, empty_bright,red_color)
     
      filled_fluor_copy=paste_patch(filled_fluor_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)      
      filled_bright_copy=paste_patch(filled_bright_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)
      if red_channel_indicator==1:
         filled_red_copy=delete_contour_with_specific_colour(filled_red_copy, empty_red,red_color)      
         filled_red_copy=paste_patch(filled_red_copy,patch_with_contours,a,b,c,d,red_color,1.0, frame_p5_size, bordersize)
            
      #### display  current frame with modified cell    
      global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, oval     
      canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y,active_channel_var.get())
      canvas_fluor_p5.delete(oval)
      if len(number_of_clicks)==1:# it is for disabling right click temorarily        
          #canvas_fluor_p5.unbind("<Button-3>")   
          canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)      
      oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)                
#################################################
def get_frame_info(internal_frame_number_p5):# for manual segmentation correction        
    global frame_dictionary
    frame_dictionary=lineage_per_frame_p5[internal_frame_number_p5]
    keys=list(frame_dictionary.keys())
    global intensity_dictionary_for_frame
    intensity_dictionary_for_frame=create_intensity_dictionary(len(keys))  
    
    global cells_in_current_frame_sorted
    cells_in_current_frame=[(frame_dictionary[key][11],frame_dictionary[key][15],frame_dictionary[key][17]) for key in keys]    
    cells_in_current_frame_sorted=sorted(cells_in_current_frame,key=lambda student: student[2])
    text_for_print=[cells_in_current_frame_sorted[i][0] for i in range(len(cells_in_current_frame_sorted))] 
    dialog_label_5.config(text="Cells detected in the current frame :  " +str(text_for_print)+
                          "\nThere are 2 manul segmentation techniques available: 1. Fast,  where correction is achieved just by clicking on the cell"
                          "   2.  Slow, where correction is done by drawing with the mouse."
                          "\nIt is recommended to start with fast mode: start left-clicking on the cell and the surrounding area.")
    global modified_cell_IDs
    modified_cell_IDs={}
    global mask, empty_fluor, empty_bright, empty_red, red_channel_indicator
    red_channel_indicator=0
    mask=masks[internal_frame_number_p5]
    empty_fluor=empty_fluors[internal_frame_number_p5]
    empty_bright=empty_brights[internal_frame_number_p5]
    ############################################
    
    ###################################    
    global path_filled_bright, path_filled_fluor,path_filled_red,path_mask
    path_filled_bright, path_filled_fluor,path_mask= path_filled_brights[internal_frame_number_p5],path_filled_fluors[internal_frame_number_p5],path_masks[internal_frame_number_p5]
    global final_mask,filled_fluor,filled_bright, filled_red
    filled_fluor=filled_fluors[internal_frame_number_p5]
    filled_bright=filled_brights[internal_frame_number_p5]
    ############################################
    current_frame_number_zfill=str(frame_number).zfill(n_digits)
    print("current_frame_number_zfill=",current_frame_number_zfill)
    #red_keys=list(red_dictionary.keys())
    if current_frame_number_zfill in red_keys:
         red_channel_indicator=1
         empty_red_path =red_dictionary[current_frame_number_zfill]
         print(" empty_red_path =", empty_red_path )
         empty_red=cv2.imread(empty_red_path,0)
         base_name=os.path.basename(empty_red_path)
         path_filled_red =os.path.join(output_dir_p5,"TRACKED_RED_FL_CHANNEL",base_name)
         print("path_filled_red =", path_filled_red )
         filled_red=cv2.imread(path_filled_red,-1)       
    final_mask=copy.deepcopy(mask)
    disable_exit()         
    update_flash([]) 
################################################################
def save_edits_for_frame(): #saves all eduts in current frame and modifies linage for this frame
    global   frame_dictionary
    print("INSIDE SAVE EDITS FOR FRAME")
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_INSIDE_SAVE_FRAME.tif",final_mask*10)          
    frame_dictionary= lineage_per_frame_p5[internal_frame_number_p5]
    debug_item=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]
    if red_channel_indicator==1:
        last_arg=[1,filled_red]
    else:
        last_arg=[0, []]
    modified_frame_dictionary=update_frame_dictionary_after_manual_segm_correction(final_mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,frame_p5_size, patch_size_p5, bordersize, last_arg)    
    lineage_per_frame_p5[internal_frame_number_p5]=modified_frame_dictionary
    debug_item_after=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]      
    modified_cells_keys=list(modified_cell_IDs.keys())
    
    cv2.imwrite(path_filled_bright, filled_bright )# rewrite BRIGHT_MOVIE_RESULTS
    cv2.imwrite(path_filled_fluor, filled_fluor)# rewrite FLEORESCENT_MOVIE_RESULTS
    if red_channel_indicator==1:
        cv2.imwrite(path_filled_red, filled_red )# rewrite RED_MOVIE_RESULTS
    destin_mask_for_plot=np.round(final_mask)
    destin_mask_for_plot = destin_mask_for_plot.astype(np.uint64)
    cv2.imwrite(path_mask, destin_mask_for_plot) # rewrite MASKS)
    ################### rewrite CLEANED_PATCHES
    cell_numbers=list(modified_cell_IDs.keys())
    for cell_number in cell_numbers:
       patch_path=create_name_for_cleaned_patch(path_filled_brights[internal_frame_number_p5], cell_number)
       #print("patch_path=", patch_path)
       patch=modified_cell_IDs[cell_number][2]
       cv2.imwrite(os.path.join(output_dir_p5,"HELPER_FOLDERS_(NOT FOR USER)","CLEANED_PATCHES",patch_path), patch)          
    ############################################
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y,active_channel_var.get())         
    global photo_filled_fluors, photo_filled_brights, filled_fluors, filled_brights# update frames on the screen
    active_channel=active_channel_var.get()
    if active_channel=="fluor":
       photo_filled_fluors[ internal_frame_number_p5]=photo_fluor
       photo_filled_brights[ internal_frame_number_p5]=photo_bright
    else:   
       photo_filled_fluors[ internal_frame_number_p5]=photo_bright
       photo_filled_brights[ internal_frame_number_p5]=photo_fluor
    filled_fluors[ internal_frame_number_p5]=filled_fluor
    filled_brights[ internal_frame_number_p5]=filled_bright
    #filled_reds[ internal_frame_number_p5]=filled_red
    masks[ internal_frame_number_p5]=final_mask
    
    canvas_fluor_p5.delete(oval)   
    #dialog_label_5.config(text="You have 3 oprions now:\n  - Go to the next frame ( by using the slide bar) \n - Finish editing the movie (by pushing Button 7)"
                            #"\n - Leave it for some other time (by clicking  Exit or Next")
    dialog_label_5.config(text=" ")
    global save_frame_edits_alert
    save_frame_edits_alert=False
      
#######################################
def create_final_movie():# create final movie + pedigree_per_cell (simplified, i.e. only centroids and areas) 
  dialog_label_5.config(text="Creating lineage and final movie...")
  cell_monitor_label.config(text="Creating excel files...", fg="red")
  global output_dir_p5,frame_p5_size,save_frame_edits_alert 
 
  if save_frame_edits_alert==True:
    mode=mode_variable.get()
    if mode=="slow":
        save_hand_drawing_for_one_cell()
        activate_fast_edit_mode()
    save_edits_for_frame()         
  update_lineage(lineage_per_frame_p5,helper_dir_p5, 'wb')
  dialog_label_5.config(text="Excel files are being created in    " +str(output_dir_p5)+"RESULTS_PER_CELL")
    
  lineage_per_cell=print_excel_files(output_dir_p5, frame_p5_size,lineage_per_frame_p5, bordersize,patch_size_p5)
  dialog_label_5.config(text="Excel files are stored in    " +str(output_dir_p5)+
                          "RESULTS_PER_CELL")
  create_output_movie(output_dir_p5, frame_p5_size)       
  dialog_label_5.config(text="Excel files are stored in    " +str(os.path.join(output_dir_p5,"RESULTS_PER_CELL"))+
                          "\nFinal movie is in    " + str(os.path.join(output_dir_p5,"lineage_movie.avi")))
  cell_monitor_label.config(text="Excel files created", fg="cyan")
  enable_exit()  
############### POPUPLATE WUTH BUTTONS
global button_load_p5,button_activate_fast_edit_mode, button_activate_slow_edit_mode,\
                   start_zoom_button, start_pan_button,stop_pan_button,\
                   button_final_movie,view_slider_p5
    
button_load_p5 = Button(frame3_page5, text="1. Click to open file menu and choose TRACKED_MOVIE_{your movie name} folder", command=lambda:threading.Thread(target=choose_and_load_tracked_movie).start(), bg=button_color, font=all_font,activebackground="red")
button_load_p5.pack(pady=5)

edit_label_fast = tk.Label(frame3a_page5, text=" FAST edit mode: by clicking",fg="black",bg=label_color, font='TkDefaultFont 10 bold').pack(pady=5)
##################################################   
#button_activate_fast_edit_mode = Button(frame3a_page5, text="2. Activate fast mode", command=activate_fast_edit_mode,bg=button_color, font=all_font,activebackground="red")
#button_activate_fast_edit_mode.pack(pady=5)
#########################################################
active_fast_label = tk.Label(frame3a_page5, text="Disabled",bg="black",fg="cyan", font=all_font)
active_fast_label.pack(pady=5)
##########################################################
edit_label_slow = tk.Label(frame3b_page5, text=" SLOW edit mode: by hand drawing",fg="black",bg=label_color, font='TkDefaultFont 10 bold').pack(pady=5)
button_activate_slow_edit_mode = Button(frame3b_page5, text="2. Activate slow mode",  command=activate_slow_edit_mode,bg=button_color, font=all_font,activebackground="red")
button_activate_slow_edit_mode.pack(side=tk.LEFT, padx=10,pady=5)
###########################################
start_zoom_button = tk.Button(frame3b_page5, text="3. Start zoom", command=start_zoom,bg=button_color, font=all_font,activebackground="red")
start_zoom_button.pack(side=tk.LEFT,padx=10,pady=5)

stop_pan_button = tk.Button(frame3b_page5, text="5. Stop pan", command=stop_pan,bg=button_color, font=all_font,activebackground="red")
stop_pan_button.pack(side=tk.RIGHT,padx=10,pady=5)

start_pan_button = tk.Button(frame3b_page5, text="4. Start pan", command=start_pan,bg=button_color, font=all_font,activebackground="red")
start_pan_button.pack(side=tk.RIGHT,padx=10,pady=5)
#############################################
global button_final_movie
button_final_movie = Button(frame4c_page5, text="6. Create final movie\n and \nExcel files", command=lambda:[threading.Thread(target=create_final_movie).start(),update_cheatsheet(cheatsheets,"neutral",bg_color,label_color)],bg=button_color, font=all_font,activebackground="red")
button_final_movie.pack(side=tk.BOTTOM, padx=100)    
##################################
global active_channel_var
active_channel_var=StringVar()
active_channel_var.set("None")
def swap_active_channel():
    global state_indicator, filled_fluor_copy, filled_bright_copy,photo_fluor, photo_bright,\
        canvas_bright_p5,canvas_fluor_p5, zoom_status, factor_input,contour_parameters, new_contour_parameters
    print("active channel is ", active_channel_var.get())
    if active_channel_var.get()=="fluor":
        R_fluor.config(background="red")
        R_bright.config(background=button_color)
    else:
        R_fluor.config(background=button_color)
        R_bright.config(background="red")
    print("state_indicator=",state_indicator)
    zoom=zoom_status.get()
    print("zoom=", zoom)
    frame_number=view_slider_p5.get()
    
    if state_indicator=="slide_bar":       
       slide_frames_p5(frame_number)
    #print("active channel is ", active_channel_var.get())
             
    if state_indicator=="clicking":
        global oval
        #cv2.imwrite(r"C:\Users\helina\Desktop\filled_fluor_copy.tif",filled_fluor_copy) 
        #print("filled_fluor_copy.shape=",filled_fluor_copy.shape)
        canvas_bright_p5.delete('all')
        canvas_fluor_p5.delete('all')
        #canvas_bright_p5.delete(photo_bright)
        #canvas_fluor_p5.delete(photo_fluor)        
        canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_copy,filled_bright_copy,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y,active_channel_var.get())
        canvas_fluor_p5.delete(oval)      
        oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)                
    if state_indicator=="drawing":
        
      if zoom_status.get()=="on":
          if active_channel_var.get()=="fluor":
             image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=photo_fluor)
             canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_bright)
          else:
             image_object=canvas_fluor_p5.create_image(image_origin_x, image_origin_y, anchor="nw", image=photo_bright)
             canvas_bright_p5.create_image(image_origin_x,image_origin_y, anchor="nw", image=photo_fluor)
           
          oval=canvas_fluor_p5.create_oval(oval_x-5*factor_input, oval_y-5*factor_input, oval_x+5*factor_input,
                       oval_y+5*factor_input, outline="magenta", width=1)
      else:
        canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size,image_origin_x,image_origin_y,active_channel_var.get())
        oval=canvas_fluor_p5.create_oval(oval_x-5*factor, oval_y-5*factor, oval_x+5*factor,
                       oval_y+5*factor, outline="magenta", width=1)                
      #print("len(contour_parameters) inside SWAP=",len(contour_parameters))
      #print("len(cell_contour_fl) inside SWAP=",len(cell_contour_fl))
     
      for i in range(len(contour_parameters)):         
          line_fl=canvas_fluor_p5.create_line(contour_parameters[i], fill="red", width=5)
          line_br=canvas_bright_p5.create_line(contour_parameters[i], fill="red", width=5)    
          cell_contour_fl.append(line_fl)
          cell_contour_br.append(line_br)   
    
        
#########################################################
channel_label = tk.Label(frame_radio_page5, text=" ACTIVE CHANNEL:",fg="black",bg=label_color, font='TkDefaultFont 10 bold').pack(side=tk.LEFT,padx=(100,10))
R_bright = Radiobutton(frame_radio_page5, text="Brightfield", value="bright", font=all_font, variable=active_channel_var, command=lambda:swap_active_channel(), background=button_color, activebackground="red")
R_bright.pack(side=tk.LEFT, padx=10)

R_fluor = Radiobutton(frame_radio_page5, text="Fluorescent", value="fluor", font=all_font, variable=active_channel_var, command=lambda:swap_active_channel(), background=button_color, activebackground="red")
R_fluor.pack(side=tk.LEFT, padx=10)

global view_slider_p5
view_slider_p5 = Scale(frame_slider_page5, from_=1, to=1,orient=HORIZONTAL, troughcolor="green", command=slide_frames_p5, length=window_p5_size)      
view_slider_p5.pack()    
############################################
global all_buttons_page5
all_buttons_page5=[button_load_p5, button_activate_slow_edit_mode,\
                   start_zoom_button, start_pan_button,stop_pan_button,\
                   button_final_movie,view_slider_p5]
################################################################################
#####################################   PAGE 6: VISUALIZE RESULTS  #########################
###########################################
page6=pages[5]
page6.title("5. VISUALISE RESULTS")
page6.config(bg=bg_color)
global  canvas_size_p6
canvas_size_p6=400
######################################
frame1_page6 = tk.Frame(master=page6, width=1530, height=50, bg=bg_color)
frame1_page6.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)

frame2_page6 = tk.Frame(master=page6, width=1530, height=200, bg=bg_color)
frame2_page6.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
########################################################
#frame_monitor_create_progress_p6 = tk.Frame(master=page6, width=1530, height=10, bg=bg_color)
#frame_monitor_create_progress_p6.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W+E+N+S)
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
#container = tk.Frame(frame_monitor_create_progress_p6 , bg=bg_color)
#container.pack(expand=True)
############################################################
frame3a_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=100,  bg=bg_color)
frame3a_page6.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3b_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=100,  bg=bg_color)
frame3b_page6.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3c_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=100,   bg=bg_color)
frame3c_page6.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)
########################################################
frame4_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=canvas_size_p6, bg=bg_color)
frame4_page6.grid(row=3, column=0, rowspan=1, columnspan=1,sticky =  W+E+N+S)

frame5_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=canvas_size_p6,  bg=bg_color)
frame5_page6.grid(row=3, column=1, rowspan=1, columnspan=1,sticky =  W+E+N+S)

frame6_page6 = tk.Frame(master=page6,width=canvas_size_p6, height=canvas_size_p6,  bg=bg_color)
frame6_page6.grid(row=3, column=2, rowspan=1, columnspan=1,sticky =  W+E+N+S)
##############################################################
frame8_page6 = tk.Frame(master=page6, width=canvas_size_p6, height=250, bg=bg_color)
frame8_page6.grid(row=4, column=0, rowspan=1, columnspan=1,sticky =  W+E+N+S)

frame9_page6 = tk.Frame(master=page6, width=canvas_size_p6, height=250, bg=bg_color)
frame9_page6.grid(row=4, column=1, rowspan=1, columnspan=1,sticky =  W+E+N+S)

frame10_page6 = tk.Frame(master=page6, width=canvas_size_p6, height=250, bg=bg_color)
frame10_page6.grid(row=4, column=2, rowspan=1, columnspan=1,sticky =  W+E+N+S)

container_1_fr10_page6 = tk.Frame(master=frame10_page6, width=canvas_size_p6, height=120, bg=bg_color)
#container_1_fr10_page6 .grid(row=0, column=0, rowspan=1, columnspan=1,sticky =  W+E+N+S)
container_1_fr10_page6 .pack(expand=True)


container_2_fr10_page6 = tk.Frame(master=frame10_page6, width=canvas_size_p6, height=120, bg=bg_color)
#container_2_fr10_page6 .grid(row=1, column=0, rowspan=1, columnspan=1,sticky =  W+E+N+S)
container_2_fr10_page6 .pack(expand=True)
frame10_page6.grid_rowconfigure(0, weight=1)
frame10_page6.grid_columnconfigure(0, weight=1)

###################################################################
frame11_page6 = tk.Frame(master=page6, width=1530, height=20, bg=bg_color)
frame11_page6.grid(row=5, column=0, rowspan=1, columnspan=3,sticky =  W+E+N+S)

frame12_page6 = tk.Frame(master=page6, width=1530, height=20)
frame12_page6.grid(row=6, column=0, rowspan=1, columnspan=3,sticky =  W+E+N+S)

gap_frame_page6 = tk.Frame(master=page6, width=1530, height=5, bg=bg_color)
gap_frame_page6.grid(row=7, column=0, rowspan=1, columnspan=3,sticky =  W+E+N+S)

frame13_page6 = tk.Frame(master=page6, width=1530, height=20, bg=bg_color)
frame13_page6.grid(row=8, column=0, rowspan=1, columnspan=3,sticky =  W+E+N+S)
######################################################
canvas_bright = Canvas(frame4_page6, bg=bg_color, height=canvas_size_p6, width=canvas_size_p6)
canvas_bright.pack()
label_file_name=tk.Label(frame4_page6, text=" ", bg="black", fg="cyan",font=all_font,width=50, height=2)
label_file_name.pack()

canvas_lineage = Canvas(frame5_page6, bg=bg_color, height=canvas_size_p6, width=canvas_size_p6)
canvas_lineage.pack()

canvas_patch = Canvas(frame6_page6, bg=bg_color, height=canvas_size_p6, width=canvas_size_p6)
canvas_patch.pack()

canvas_graph = Canvas(frame8_page6, bg=bg_color, height=250, width=canvas_size_p6)
canvas_graph.pack()
###################################################
options_cells = [""]
global cell_ID, cell_property
cell_ID, cell_property = StringVar(page6),StringVar(page6)
cell_ID.set("Choose cell ID")
cell_property.set("Choose cell property")
global ffrom
ffrom=1
global clicks_count
clicks_count=0 
##############################################################
global extract_info_from_file_name

from postprocess import (sorted_aphanumeric, change_dict,extract_info_from_file_name, create_per_cell_info,
              load_and_prepare_result_images)
from print_excel import extract_lineage,extract_const_movie_parameters
from interface_functions import turn_image_into_tkinter
##########################################
def create_display_images_p6():# plot images necessary for display       
        label_instruct_p6.config(text="\nCreating display images ... \n\n\n")   
        still_lineage=cv2.imread(os.path.join( outpath,"still_lineage.tif"), -1)
        create_per_cell_info(pedigree, outpath, still_lineage, progress_bar,first_frame_number_p6, label_create_p6,container_1_fr10_page6 )
        load_display_images_p6()        
#######################################
def retrieve_display_images_p6():# If display iamges were created before, upload them
        #print("INSIDE RETRIEVE")       
        label_instruct_p6.config(text="\n\n\n\n")          
        load_display_images_p6()
 ######################################################
def load_display_images_p6():# load images for display that have already been created before 
      global keys,menu_cell_ID, progress_bar,retrieve_popup_buttons    
      keys=list(pedigree.keys())
      label_instruct_p6.config(text="\nLoading images for display ... \n\n\n")
      ###########################################
      all_buttons_page6.remove(menu_cell_ID_old)      
      menu_cell_ID_old.destroy()     
      menu_cell_ID = OptionMenu(frame3b_page6, cell_ID, *keys,  command= load_cell_info)
      menu_cell_ID.pack()
      menu_cell_ID.config(bg = button_color,font=all_font,activebackground="red")
      menu_cell_ID["menu"].config(bg=label_color,activebackground="red")   
      all_buttons_page6.append(menu_cell_ID )        
      ##################################################
      global red_patches, one_cell_patches, plots, bright_names
      #label_instruct_p6.config(text="\n\n\n\n") 
      red_patches, one_cell_patches, plots, bright_names=load_and_prepare_result_images(outpath, keys, progress_bar,label_create_p6)
      """
      last_frame_number_p6=first_frame_number_p6+num_frames-1
      label_feedback_p6.config(text="Movie:  "+ os.path.join(software_folder, input_movie_folder)+
                    "\nNumber of frames: "+ str(num_frames)+"                   From   "+
                    str(first_frame_number_p6)+"     to    "+str( last_frame_number_p6)+
                    "\nCell names:      "+str(list_of_cell_names))
      """
      ################################################
      
      ##################################################
      label_instruct_p6.config(text="Choose cell ID from the dropdown menu.")
      button_upload_p6.config(bg=button_color)
      global col_dict
      col_dict={"Area":["red", "yellow", "yellow"],"Perimeter":["yellow", "red", "yellow"],"Circularity":["yellow", "yellow", "red"]}
      update_flash([menu_cell_ID])    
      activate_buttons(all_buttons_page6,[menu_cell_ID])
#############################################
def upload_input_movie():# look if display images exist. If so, load them, if not - create them first and then load them.
    update_flash([])   
    global progress_bar
    button_upload_p6.config(bg="red")
    global my_dir,out_folders, outpath, software_folder, options_cells, menu_cell_ID,input_movie_folder
    ###################################    
    outpath = filedialog.askdirectory()# TRACKED_MOVIE_{movie_name} 
    current_movie_folder = os.path.dirname(outpath )
    current_movie_name=os.path.basename( current_movie_folder )          
    input_movie_folder = os.path.join( current_movie_folder, "ONE_WELL_MOVIE_"+ current_movie_name)    
    ########################################################
    label_instruct_p6.config(text="\n\n\n\n")    
    ################### load lineage_per_cell and constant movie params
    global pedigree, frame_size_p6, first_frame_number_p6, num_frames, list_of_cell_names
    helper_dir_p6=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)")
    pedigree_path=os.path.join(helper_dir_p6,"lineage_per_cell.pkl")
    with open(pedigree_path, 'rb') as handle:
         pedigree = pickle.load(handle)
    list_of_cell_names =list(pedigree.keys())
       
    frame_size_p6, true_cell_radius_pickle, patch_size,max_number_of_cells,\
           num_frames, full_core_fluor_name, n_digits, full_core_bright_name,  first_frame_number_p6,\
           base_colours,contrast_value,number_cells_in_first_frame,full_core_red_name, red_dictionary_p5,bordersize_p5,delta_p5=extract_const_movie_parameters(helper_dir_p6)
    #############################################
    last_frame_number_p6=first_frame_number_p6+num_frames-1
    label_feedback_p6.config(text="Movie:  "+ os.path.join(software_folder, input_movie_folder)+
                    "\nNumber of frames: "+ str(num_frames)+"                   From   "+
                    str(first_frame_number_p6)+"     to    "+str( last_frame_number_p6)+
                    "\nCell names:      "+str(list_of_cell_names))
      ################################################
    ##############################################
   
    w,h = 400,150 
    cell_info_folder=os.path.join(outpath,"HELPER_FOLDERS_(NOT FOR USER)","VISUALISATION_HELPERS", "PLOTS")
    if  len(os.listdir(cell_info_folder))==0:# display images are not existent, need to be created
      global  popup_create_display_images
      popup_create_display_images = tk.Toplevel(master=page6, bg=label_color)                        
      popup_create_display_images.geometry('%dx%d+%d+%d' % (w, h, (ws/2) - (w/2), (hs/2) - (h/2)))
      label_create = tk.Label(popup_create_display_images, text="Display images have not been created yet.\nIt might take long to create them. \nPress OK to start.",width=500, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
      label_create.pack()                     
      button_create_p6 = Button(popup_create_display_images, text="OK",     
      bg=button_color,font='TkDefaultFont 14 bold',command=lambda:[ popup_create_display_images.destroy(), Thread(target=create_display_images_p6).start()])
      button_create_p6.pack()      
      ###########################      
    else:
      # diplay images are already there, just upload them
      global  popup_retrieve_display_images      
      label_instruct_p6.config(text="\n\n\n\n")        
      ############################
      popup_retrieve_display_images = tk.Toplevel(master=page6, bg=label_color)                        
      popup_retrieve_display_images.geometry('%dx%d+%d+%d' % (400, 159, (ws/2) - (w/2), (hs/2) - (h/2)))
      label_retrieve = tk.Label(popup_retrieve_display_images, text="Display images are already prepared.\nIt should not take long to load them.\nPress OK to proceed.",width=450, height=5, bg=label_color, fg="black", font='TkDefaultFont 14 bold' )
      label_retrieve.pack()
      global button_retrieve_p6                      
      button_retrieve_p6 = Button(popup_retrieve_display_images, text="OK",
      bg=button_color,font='TkDefaultFont 14 bold', command=lambda:[popup_retrieve_display_images.destroy(),Thread(target=retrieve_display_images_p6).start()])
      button_retrieve_p6.pack()      
############################################
def slide_patch(value):  # value=frame number from patch_slider
    global clicks_count
    #print("clicks_count entering slide_patch =",clicks_count)
    clicks_count+=1
    #print("clicks_count after slide_patch =",clicks_count)
    if clicks_count>=3:
       update_flash([])         
    canvas_bright.delete('all')
    canvas_lineage.delete('all')
    canvas_patch.delete('all')
    canvas_graph.delete('all')        
    internal_frame_number=int(value)-ffrom   
    patch=one_cell_patches[cell_ID.get()][internal_frame_number][0]    
    global im_pil
    im_pil=turn_image_into_tkinter(patch, canvas_size_p6,[])    
    canvas_patch.create_image(0, 0, anchor=NW, image=im_pil)
        
    red_patch=red_patches[cell_ID.get()][internal_frame_number][0]   
    global red_im_pil     
    red_im_pil=turn_image_into_tkinter(red_patch, canvas_size_p6,[])
    canvas_lineage.create_image(0, 0, anchor=NW, image=red_im_pil)
    
    plott_pil=plots[cell_ID.get()][cell_property.get()][ internal_frame_number][0]
    global pl_pil
    pl_pil = Image.fromarray(plott_pil)
    pl_pil.thumbnail((canvas_size_p6,canvas_size_p6), Image.ANTIALIAS)
    pl_pil = ImageTk.PhotoImage(pl_pil)
    canvas_graph.create_image(0, 0, anchor=NW, image=pl_pil)    
    ######################################
    bright_name=bright_names[ int(value)-first_frame_number_p6]
    bright_name_for_show=prepare_file_name_for_show(bright_name)
    label_file_name.configure(text=os.path.basename(bright_name_for_show))
    bright_image=cv2.imread(bright_name, -1)

    global bright_pil  
    bright_pil=turn_image_into_tkinter(bright_image, canvas_size_p6,[])
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
def load_cell_info(value):
  global clicks_count
  clicks_count=0
  update_flash([])
  global all_buttons_page6
  menu_cell_ID.config(fg=result_color,bg="black") 
  cell_property.set("Choose cell property")
  canvas_bright.delete('all')
  canvas_lineage.delete('all')
  canvas_patch.delete('all')
  canvas_graph.delete('all')    
  cell_ID.set(value)
  key=cell_ID.get()  
  menu_cell_ID.config( bg="black",fg = result_color)
  if key!="Choose cell ID":
    global ffrom, tto, patch_slider_old
    ffrom=pedigree[key][0][1]
    tto = pedigree[key][-1][1]   
    if patch_slider_old in all_buttons_page6:
        all_buttons_page6.remove(patch_slider_old)
        patch_slider_old.destroy()
        
        global patch_slider
        patch_slider=Scale(container_2_fr10_page6,from_=ffrom,to=tto,orient=HORIZONTAL,troughcolor="#513B1C",label="Frame "+str(ffrom), command=slide_patch,
                 activebackground="red", bg=label_color,showvalue=0, font=all_font, length=400)    
        patch_slider.pack(side=tk.TOP,pady=40)
        patch_slider_old=patch_slider
        #patch_slider.grid(row=0,column=0,padx=2,pady=5)
        all_buttons_page6.append(patch_slider_old)
  #clicks_count=0
  update_flash([menu_cell_property])
  activate_buttons(all_buttons_page6,[menu_cell_property])
  label_create_p6 .config(text="Cell name  :   "+str(key)+"\nNumber of frames : "+str(tto-ffrom+1)+"\nFrom "+str(ffrom)+"  To  "+str(tto))
  label_instruct_p6.config(text="Choose cell property (Area, Perimeter, or Circularity) \nfrom the dropdown menu.")    
###########################################################
def load_cell_property(value):
    global clicks_count
    clicks_count=0
    #print("clicks_count inside load_cell_property 1=",clicks_count)
    update_flash([])
    global all_buttons_page6
    cell_property.set(str(value))    
    menu_cell_property.config( fg = result_color,bg="black")
    ffrom_1=str(ffrom)      
    slide_patch(ffrom_1)
    patch_slider.set(ffrom_1)
    #clicks_count=0
    #print("clicks_count inside load_cell_property 2=",clicks_count)      
    update_flash([patch_slider])
    activate_buttons(all_buttons_page6,[menu_cell_property, menu_cell_ID,patch_slider])
    label_instruct_p6.config(text="Use slider to move between frames.\nIf you want to switch to a different cell or a different property, use the dropdown menus again.")
######################################################
################### poplulate page-6 with widgets #########
label_title_p6 = tk.Label(frame1_page6, text="STEP 5: VISUALISE RESULTS",
              bg="yellow", fg="red", font=("Times", "24")).pack()
label_instr_name_p6=tk.Label(frame11_page6,text="INSTRUCTIONS FOR USER :" ,bg="black", font=all_font, fg="white").pack()
global button_upload_p6
button_upload_p6 = tk.Button(frame3a_page6, text=" Upload TRACKED movie",
                bg=button_color, font=all_font,command=upload_input_movie)
button_upload_p6.pack()
###########################################
global progress_bar
s = ttk.Style()
s.theme_use('clam')
s.configure("bar.Horizontal.TProgressbar", troughcolor=bg_color, 
                bordercolor="green", background="green", lightcolor="green", 
                darkcolor="black")
progress_bar = ttk.Progressbar(container_1_fr10_page6,style="bar.Horizontal.TProgressbar",orient='horizontal',mode='determinate',length=400)
progress_bar.pack(pady=(20,5))
#############################
global label_create_p6
label_create_p6 = tk.Label(container_1_fr10_page6, text=" ",
              bg=bg_color, fg="cyan", font=all_font,width=50, height=3,  anchor="w",justify="left")
label_create_p6.pack()
##################################################
global patch_slider_old    
patch_slider_old=Scale(container_2_fr10_page6,from_=ffrom,to=ffrom,orient=HORIZONTAL,troughcolor="#513B1C",label="Frame "+str(ffrom), command=slide_patch,
                 activebackground="red", bg=label_color,showvalue=0, font=all_font, length=canvas_size_p6)
patch_slider_old.pack(side=tk.TOP,pady=40)
#############################################
global menu_cell_ID_old,menu_cell_property
menu_cell_ID_old = OptionMenu(frame3b_page6, cell_ID, *options_cells,  command= load_cell_info)
menu_cell_ID_old.pack()
menu_cell_ID_old.config(bg = button_color,font=all_font,activebackground="red")
menu_cell_ID_old["menu"].config(bg=label_color,activebackground="red")
###############################################
options_properties = ["Area", "Perimeter", "Circularity"]
menu_cell_property = OptionMenu(frame3c_page6, cell_property, *options_properties, command=load_cell_property)
menu_cell_property.pack()
menu_cell_property.config(bg = button_color, font=all_font,activebackground="red")
menu_cell_property["menu"].config(bg=label_color,activebackground="red")
###################
text_for_label_feedback_p6="Movie:"+\
                    "\nNumber of frames:"+\
                    "\nCell names:"
label_feedback_p6 = tk.Label(frame2_page6, text=text_for_label_feedback_p6,bg="black", fg="cyan", font=all_font, height=3)
label_feedback_p6.pack(fill=BOTH)
label_instruct_p6 = tk.Label(frame12_page6, text="Push button Upload TRACKED movie.\n\When menu opens,navigate to TRACKED movie folder and click (once, not twice!) on it.\nThen, push Select Folder.",bg="black", fg="yellow", font=all_font,  height=5)
label_instruct_p6.pack(fill=BOTH)
###################################################################
label_centr = tk.Label(frame9_page6, text="Centroid:",bg = "black", fg="yellow" , font=("Times", "16"))
label_centr.pack(side=tk.TOP, pady=(70,2))
label_area = tk.Label(frame9_page6, text="Area:", bg = "black", fg="yellow",font=("Times", "16"))
label_area.pack(side=tk.TOP, pady=2)
label_perim = tk.Label(frame9_page6, text="Perimeter:", bg = "black", fg="yellow",font=("Times", "16"))
label_perim.pack(side=tk.TOP, pady=2)
label_circ = tk.Label(frame9_page6, text="Circularity:", bg = "black", fg="yellow",font=("Times", "16"))
label_circ.pack(side=tk.TOP, pady=2) 

global all_buttons_page6 
all_buttons_page6=[button_upload_p6,patch_slider_old,menu_cell_ID_old,menu_cell_property]

######################### This is the end of Page-6 #############
###########################################################
############## Navigation between pages: buttons Back, Exit, Next plus buttons on title page
#########################################################################
global update_flash
def update_flash(buttons):# buttons are those which will start flashing
    global flashers   
    if flashers!={}:# stop flashing all previous buttons
        keys=list(flashers.keys())
        for key in keys:           
            if isinstance(key, str)==False:
              key.config(bg=button_color)# old buttons become green again
            win.after_cancel(flashers[key])
    flashers={}# delete all previous flashesr
    
    flashers_names =[]
    if len(buttons)!=0:# it can be buttons=[]; in this case, update_flash just stops flashing all previous buttons, without switching new ones
       for i in range(len(buttons)):         
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
##########################################################
def combine_funcs(*funcs):    
    def inner_combined_func(*args, **kwargs): 
        for f in funcs: 
            f(*args, **kwargs)     
    return inner_combined_func 
#################### Make buttons NEXT, EXIT, BACK
######## make initial_buttons on each page flash 
page_titles=["PAGE 1: TITLE PAGE","PAGE 2: EXTRACT MOVIE FROM FOLDER", "PAGE 3: CUT ONE WELL",
             "PAGE 4: EXECUTE AND CORRECT TRACKING", "PAGE 5: CORRECT SEGMENTATION","PAGE 6: VISUALISE RESULTS" ]
initial_buttons=[[button_choose_folder],[button_select],[button_load],[button_load_p5],[button_upload_p6]]
page_numbers=[page1,page2,page3,page4,page5, page6]

locations=[frame3_page1,frame8_page2,frame15_page3,frame11_page4,frame8_page5,frame13_page6]
next_exit_buttons_p3=[]  
for i in range(0,6):        
    location=locations[i]
    if i==0:                   
       Button(location, text="Exit",bg="orange",font=all_font, command=win.destroy).pack(side=tk.LEFT, padx=(700,2))
             
    if i>0:
      f_back=partial(go_to_page,i)
      if i==1:
          flash_buttons=[]
      else:
           flash_buttons=initial_buttons[i-2]
      g_back=partial(update_flash,flash_buttons) 
      butt_back=Button(location, text="Back",bg="orange",font=all_font, command=combine_funcs(f_back,g_back))
      butt_back.pack(side=tk.LEFT, padx=(700,2))      
      butt_exit=Button(location, text="Exit",bg="orange",font=all_font, command=win.destroy)
      butt_exit.pack(side=tk.LEFT, padx=2)
      Button(frame2_page1, text= "GO TO STEP %s" % (i),bg=button_color,font=all_font,command=combine_funcs(f_next,g_next)).grid(row=1+i,column=0,pady=5, padx=200)
      Label(frame2_page1, text= "STEP %s: " % (i)+ page_titles[i][7:],bg="black",fg="yellow",font=all_font).grid(row=1+i,column=1,pady=5, padx=5)
      if i==3:
         next_exit_buttons_p3+=[butt_back,butt_exit] 
    if i<5:
       f_next=partial(go_to_page,i+2)
       g_next=partial(update_flash,initial_buttons[i])       
       butt_next=Button(location, text="Next",bg="orange",font=all_font, command=combine_funcs(f_next,g_next))
       butt_next.pack(side=tk.LEFT, padx=2)
       if i==3:
         next_exit_buttons_p3+=[butt_next] 


win.mainloop()

