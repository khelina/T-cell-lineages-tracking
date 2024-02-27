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
from functools import partial
import copy
###################### Choose Windows or Mac (this is about button colors)
import platform
x=platform.system()
if x == "Darwin":
    from tkmacosx import Button
elif x == "win32":
    from tk import Button
##################### Design the interface
page4 = tk.Tk()
page4.geometry('1530x2000')
page4.title("DeepKymoTracker: TRACK AND SEGMENT")
bg_color,all_font,button_color ,result_color,label_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA"

page4.config(bg=bg_color)
frame1 = tk.Frame(master=page4, width=1528, height=50, bg=bg_color)
frame1.grid(row=0, column=0, rowspan=1, columnspan=6, sticky=W+E+N+S)

frame2 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame3.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame4 = tk.Frame(master=page4, width=382, height=30, bg=bg_color)
frame4.grid(row=1, column=2, rowspan=2, columnspan=1, sticky=W+E+N+S)

frame5 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame5.grid(row=2, column=0, rowspan=1, columnspan=1)

frame6 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame6.grid(row=2, column=1, rowspan=1, columnspan=1)

frame7 = tk.Frame(master=page4, width=382, height=382, bg=bg_color)
frame7.grid(row=2, column=2, rowspan=1, columnspan=1)

frame8 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame8.grid(row=3, column=0, rowspan=1, columnspan=1,sticky=W+E+N+S)

frame9 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame9.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame10 = tk.Frame(master=page4, width=382, height=1538, bg=bg_color)
frame10.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)

canvas_previous = Canvas(frame5, bg=bg_color, height=382, width=382)
canvas_previous.pack(anchor='nw', fill='both', expand=True)
canvas_current = Canvas(frame6, bg=bg_color, height=382, width=382)
canvas_current.pack(anchor='nw', fill='both', expand=True)

canvas_lineage = Canvas(frame7, bg=bg_color, height=382, width=382)
canvas_lineage.grid(row=0,column=0)
########################### These labels do not change
label_previous = tk.Label(frame8, text="Previous Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_previous.grid(row=0, column=5, padx=100)

label_current = tk.Label(frame9, text="Current Frame", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_current.grid(row=0, column=0,padx=100)

label_lineage = tk.Label(frame10, text="Lineage", bg="#87CEFA", fg="black", font='TkDefaultFont 10 bold' )
label_lineage.grid(row=0, column=0, padx=100)
################################
global  flashers
flashers ={}
global start_flash, stop_flash, turn_image_into_tkinter,show_3_canvases
from interface_functions import start_flash, stop_flash,turn_image_into_tkinter,show_3_canvases
#####################################
global  lineage_per_frame,start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions, cells
lineage_per_frame,start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions, cells = None,1, {},{},{},{}
global out_folders, count, pedigree
out_folders, pedigree, = [], None 
count = np.zeros((100), dtype="uint8")


global my_dir, edit_id_indicator
my_dir, edit_id_indicator = '', "no"
global per_cell_dict
per_cell_dict = {}
global clicked
clicked = StringVar()
clicked.set("Begin with 1 cell")

title_label = tk.Label(frame1, text="DeepKymoTracker: Track and Segment T cells",
              bg="yellow", fg="red", font=("Times", "24"))
title_label.grid(row=0, column=1, padx=2, sticky="n")
#################
def load_models(software_folder):    
    os.chdir(software_folder)
    global predict_first_frame, create_output_folders,\
        detect_division, update_dictionary_after_division, check_division_frame_number, predict_tracking, predict_tracking_general, backup_track, predict_first_frame, segment_and_clean,\
        create_previous_frame, plot_frame, create_color_dictionary,\
        create_pedigree, create_output_movie, create_models, extract_lineage,create_dictionary_of_xs,\
        create_lineage_image_one_frame, extract_file_name, load_clip, update_lineage

    from preprocess import create_output_folders, create_models, extract_file_name,load_clip

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_division_frame_number)

    from functions import (predict_tracking_general,  backup_track, predict_first_frame, segment_and_clean,
                           hungarian, create_previous_frame, predict_tracking, extract_lineage, update_lineage)
    
    from plot import plot_frame, create_color_dictionary
    from postprocess import create_pedigree,  create_output_movie, create_dictionary_of_xs, create_lineage_image_one_frame
    from keras.models import model_from_json

    from keras.optimizers import Adam
    global models
    
    directory = os.path.join(software_folder, "TRAINED MODELS")
    model_names = ["Tracker-1", "Tracker-2", "Tracker-3","Tracker-4","Tracker-5","Tracker-6",
                   "Segmentor", "Refiner"]
    models = []
    for name in model_names:        
        full_name = os.path.join(directory, name)
        json_file = open(full_name + "-model.json", "r")
        model_read = json_file.read()
        json_file.close()        
        models.append((model_read, full_name))   
    feedback_label.configure(text="Loading input movie ...")    
###########
input_info_label = tk.Label(frame1, text=my_dir, bg="brown")
input_info_label.grid(row=2, column=1, padx=2)

progressbar = ttk.Progressbar(
    frame9, orient='horizontal', mode='determinate', length=100)
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
        shutil.rmtree(outpath)
        os.mkdir(outpath)
    out_folders = create_output_folders(outpath)    
    ######## calcilate number of frames, core name in file names
    ######## and n_digits in numbering files in input movie 
    names=[]
    for filename in os.listdir(my_dir):   
        if filename.endswith("ch00.tif"):
            feedback_label.configure(text="Loading input movie ...")                      
            full_name = os.path.join(my_dir, filename)
            names.append(full_name)
    global num_frames, full_core_name, n_digits, first_frame_number
    num_frames=len(names)
    full_core_name, n_digits, first_frame_number= extract_file_name(names[0])    
    input_info_label.config(text= "Input movie:"+ "\n"+str(my_dir)+"\nNumber of frames: "+str(num_frames), fg="#00FFFF", bg="black")
    del names
   
    ########### load the first clip         
    global fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names                 
    fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(0,full_core_name,n_digits, num_frames, first_frame_number)
    global  frame_size, previous_lineage_image     
    frame_size=fluor_images[0].shape[0] 
    if num_frames<=382:
        size=num_frames
    else:
        size=num_frames
    previous_lineage_image =np.zeros((size, size,3), dtype="uint8") 
    feedback_label.config(text="Movie loaded, {} frames.\nNow, you need to specify how many cells are there in Frame 1.".format(num_frames))   
    button_load.configure(background = '#9ACD32')   
    start_flash([R1, R2],"radio", page4, flashers)
######################################################
button_load = Button(frame1, text="1. Click to open file menu and then select input movie folder",
               bg=button_color,font='TkDefaultFont 10 bold', command=lambda:[threading.Thread(target=choose_folder).start(), stop_flash("load", page4, flashers)])
button_load.grid(row=2, column=0, padx=10, pady=20)
start_flash([button_load],"load", page4, flashers)
label_min_cells = tk.Label(
    frame1, text="2. How many cells are there in Frame-1 ?",font='TkDefaultFont 10 bold', bg=label_color)
label_min_cells.grid(row=3, column=0, padx=2)
########################################
global cell_radius, window_size, max_number_of_cells
cell_radius=20 
window_size=382
max_number_of_cells=5  

global manual_popup_centroids, coords_very_first # coords_very_first is necessary for plotting lineage later
manual_popup_centroids, coords_very_first= [],[]
################################
def begin_with_one_cell():
    stop_flash("radio", page4, flashers)
    feedback_label.configure(text="Calculating position of cell in Frame 1 ...")
    R1.configure(bg="red")
    R2.configure(bg=button_color)
    global coords, coords_very_first
    
    full_name=models[0][1]
    model = model_from_json(models[0][0])
    model.load_weights(full_name + "-weights.h5")   
    model.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
       
    coords = predict_first_frame(fluor_images_compressed, model)  
    coords_very_first= coords.tolist()
        
    global colours, template_names, prev_frame
    colours, template_names = create_color_dictionary(
        max_number_of_cells, coords.shape[0])# 10 =maximum number of cells
    global xs
    xs=create_dictionary_of_xs( template_names, coords_very_first, num_frames)
  
    global text
    text = template_names[:coords.shape[0]]  
    prev_frame = np.zeros((382, 382), dtype="float64")
    for i in range(coords.shape[0]):
        one_circle = np.zeros((382, 382), dtype="uint8")
        one_circle = cv2.circle(
            one_circle, (int(coords[i][0]), int(coords[i][1])), 10, i+1, -1)
        one_circle = one_circle.astype('float64')
        prev_frame += one_circle
        page4.update()
      
    R2.configure(bg=button_color, fg="black")
    R1.configure(bg="black", fg="#00FFFF")
    
    start_flash([button_execute], "exec", page4, flashers)
    feedback_label.config(text="The centroids of the cell in Frame 1 has been calculated.\n\nTo start execution, press Button 3.")    
####################################   
R1 = Radiobutton(frame1, text="1 cell", value="1 cell", font=all_font, variable=clicked, command=begin_with_one_cell, background=button_color, activebackground="red")
R1.grid(row=3, column=1, pady=10)
############################
def create_popup_canvas():
    stop_flash("radio", page4, flashers)
    feedback_label.configure(text="Waiting for manual assignment of cell positions in Frame 1 ...")
    R1.configure(bg=button_color, fg="black")
    global popup
    popup = tk.Toplevel(master=page4, width=frame_size, height=frame_size)
    sub1 = tk.Frame(master=popup, width=frame_size, height=50, bg="#A52A2A")
    sub1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    global label_click_popup
    label_click_popup = tk.Label(
        sub1, text="Click on each cell with the left button of the mouse,\nthen save", bg="black",fg="yellow", font='TkDefaultFont 10 bold')
    label_click_popup.pack()
     
    sub2 = tk.Frame(master=popup, width=frame_size, height=frame_size, bg="#A52A2A")
    sub2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

    global canvas_popup
    canvas_popup = Canvas(sub2, bg='black', height=frame_size, width=frame_size)
    canvas_popup.pack(anchor='nw', fill='both', expand=True)
    canvas_popup.bind("<Button-1>", draw_circle)
      
    sub3 = tk.Frame(master=popup, width=frame_size, height=50, bg="#A52A2A")
    sub3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    global button_save_popup
    button_save_popup = Button(sub3, text="Save", bg=button_color,activebackground="red", command=close_popup_canvas)
    button_save_popup.pack()
    start_flash([button_save_popup], "save", popup,flashers)
    
    full_name = fluor_names[0]
    global photo  
    photo = Image.open(full_name)
    photo = photo.resize((382, 382), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(photo)
    canvas_popup.create_image(0, 0, anchor=NW, image=photo)
    stop_flash("label", popup,flashers)
    stop_flash("radio", page4, flashers)
    label_min_cells.configure(background = label_color)   
#############################    
def close_popup_canvas():      
      R2.configure(background="black", fg="#00FFFF")
      stop_flash("save", popup,flashers)    
      global coords, manual_popup_centroids, coords_very_first    
      stop_flash("click", popup, flashers)
      start_flash([button_save_popup], "save", popup, flashers)
      coords_very_first=manual_popup_centroids
      global colours, template_names, prev_frame
      colours, template_names = create_color_dictionary(
        max_number_of_cells, len(manual_popup_centroids))# 10 =maximum number of cells
      global xs
      xs=create_dictionary_of_xs( template_names, coords_very_first, num_frames)   
      N_cells=len(manual_popup_centroids)      
      global text
      text = template_names[:N_cells]   
      prev_frame = np.zeros((frame_size, frame_size), dtype="float64")
      coords = np.zeros((N_cells, 2))
      for i in range(N_cells):
        coords[i] = manual_popup_centroids[i]
        one_circle = np.zeros((frame_size, frame_size), dtype="uint8")
        one_circle = cv2.circle(
            one_circle, (int(manual_popup_centroids[i][0]), int(manual_popup_centroids[i][1])), 10, i+1, -1)
        one_circle = one_circle.astype('float64')
        prev_frame += one_circle      
      feedback_label.config(text="The positions of cells in Frame 1 has been saved.\n\nTo start execution, press Button 3.")
      stop_flash("save", popup, flashers)
      start_flash([button_execute], "exec", page4, flashers)   
      popup.destroy()
#######################################
R2 = Radiobutton(frame1, text="More than 1 cell",background=button_color, font='TkDefaultFont 10 bold',
                 value="More than 1 cell", activebackground="red",variable=clicked, command=create_popup_canvas)
R2.grid(row=3, column=2)
################ draw red spots in popup canvas in response to mouse click
def draw_circle(event):
    canvas_popup.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    manual_popup_centroids.append([event.x, event.y])
####################################################  
global text, variable_stop, manual_division_indicator, mother_number
text, variable_stop, manual_division_indicator, mother_number=StringVar(), "Do not stop", StringVar(), IntVar()
manual_division_indicator.set("no")
#############################################################
global trackers, segmentor, refiner
trackers, segmentor, refiner= None, None, None

zero_image = Image.new('RGB', (window_size, window_size))
zero_image = ImageTk.PhotoImage(zero_image)
global lineage_images, output_images
lineage_images, output_images, lineage_images_cv2=[], [zero_image],[] 
############################################################
def clear_memory_of_models(trackers, segmentor, refiner):     
     keras.backend.clear_session()    
     if segmentor:       
        del segmentor     
     if refiner:
         del refiner        
     if trackers:      
          del trackers    
     tf.reset_default_graph() 
###########################################
def cut_lineage(start_frame): # after manual editing
    lineage_per_frame=extract_lineage(outpath)
    del lineage_per_frame[(start_frame-1):]# was -1       
    update_lineage(lineage_per_frame,outpath,'wb')
    global output_images,lineage_images,lineage_images_cv2    
    del output_images[(start_frame):]   
    global previous_lineage_image    
    previous_lineage_image=lineage_images_cv2[start_frame-1]   
    del lineage_images_cv2[(start_frame-1):] 
    del lineage_images[(start_frame-1):]         
    global dict_of_divisions 
    print("dict_of_divisions_before=",dict_of_divisions)     
    dict_of_divisions = {key:val for key, val in dict_of_divisions.items() if val < start_frame}
    print("dict_of_divisions_after=",dict_of_divisions) 
###########################################################
def execute():
 try:
    canvas_previous.delete("all")
    canvas_current.delete("all")
    canvas_lineage.delete("all")
    button_execute.configure(background = 'red')
    stop_flash("exec", page4, flashers)
    label_edit_results.configure(text=" ")
    label_edit_instructions.configure(text=" ")
    feedback_label.config(text="Wait, loading models ...")
    global lineage_images, output_images, lineage_per_frame, pedigree, previous_lineage_image     
    if lineage_per_frame:
        del lineage_per_frame
    if pedigree:
        del pedigree
    
    global variable_stop, start_frame, trackers, segmentor, refiner# this variable allows to stop the loop (controlled by Stop button)     
    global coords, prev_frame,  count, text, cells, old_number_of_cells, edit_id_indicator    
    N_cells = coords.shape[0]
    division_indicator=0
    centroids_for_benchmarking=[coords]
    n =num_frames  
    k = start_frame-1  # the first frame of clip     
    kk = 0  # the number of frame within clip   
    clear_memory_of_models(trackers, segmentor, refiner)
    trackers, segmentor, refiner=create_models(N_cells, models)   
    feedback_label.config(text="Execution is about to begin ...")
    start_flash([button_pause],"pause", page4, flashers)
    progressbar.grid(row=1, column=0, padx=20)
    progressbar["value"]=((start_frame)/num_frames)*100
    while k < n:
        global fluor_images, fluor_images_compressed,bright_images, fluor_names, bright_names
        if k>0:
         del fluor_images, fluor_images_compressed,bright_images, fluor_names, bright_names 
         fluor_images,fluor_images_compressed,bright_images,fluor_names,bright_names =load_clip(k,full_core_name,n_digits, num_frames, first_frame_number)
       
        clip_centr = predict_tracking_general(
                coords, fluor_images, fluor_images_compressed, fluor_names, k, out_folders[0], trackers,n, cell_radius, frame_size)
        print("TRACKING PREDICTED FOR CLIP BEGINNING WITH FRAME  ", k+1)     
        for kk in range(len(clip_centr)):# it is actually 4 (number of frames in clip)
            print("FRAME NUMBER = ", k+kk+1)# segmenting all the 4 frames in the clip
            progressbar["value"]=((k+kk+1)/num_frames)*100
            time.sleep(0.02)
            frame9.update_idletasks()                    
            clip_centr =  backup_track(
                clip_centr, coords, kk, cell_radius)  # correct too big jumps            
            tracked_centroids=clip_centr[kk]
            print("tracked centroids=", tracked_centroids)           
            empty_fluor = fluor_images[kk]         
            empty_bright = bright_images[kk]            
            count, cells, coords,  text, number_of_splits = segment_and_clean(
                dict_of_divisions, cells, count, coords, prev_frame,text, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, k+kk, edit_id_indicator, mother_number, out_folders, cell_radius, frame_size, colours)
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
               count, cut_patches, mother_8_name = detect_division(
                   cells, count, k, kk)             
               if (np.any(count == 2) or np.any(count == 1)):                  
                   if mother_8_name != []:
                       count = check_division_frame_number(
                           count, cells, dict_of_divisions, mother_8_name, k+kk)                      
               if np.any(count == 2):
                   cells, text, count, division_indicator, coords = update_dictionary_after_division(
                       cut_patches, cells, text, count, division_indicator, coords, frame_size, colours)
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
            coords, destin_fluor = plot_frame(cells, clip_centr, k, kk,
                                fluor_images, fluor_names, out_folders, coords, coords, bright_images, bright_names, frame_size )          
            current_lineage_image=create_lineage_image_one_frame(out_folders,cells, previous_lineage_image, xs, k+kk)
            
            previous_lineage_image=current_lineage_image# need it for the next lineage image                      
            image_seg=destin_fluor
            photo_image_seg=turn_image_into_tkinter(image_seg)
            canvas_current.create_image(0,0,anchor=NW,image=photo_image_seg)
            output_images.append(photo_image_seg)
                     
            image_lin=current_lineage_image
            image_lin_copy=copy.deepcopy(image_lin)         
            lineage_images_cv2.append(image_lin_copy)                    
            photo_image_lin=turn_image_into_tkinter(image_lin)
            canvas_lineage.create_image(0,0,anchor=NW,image=photo_image_lin)          
            lineage_images.append(photo_image_lin)
           
            centroids_for_benchmarking.append(coords)            
            prev_frame = create_previous_frame(cells, frame_size)
                              
            if (division_indicator == 1):
                print("division occured in frame ", k+kk+1)              
                dict_of_divisions[text[-1][:-1]] = k+kk
                break        
        if (division_indicator == 1):
            k = k+kk+1
            N_cells = coords.shape[0]
            clear_memory_of_models(trackers, segmentor, refiner)
            trackers, segmentor, refiner=create_models(N_cells, models)              
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
 button_execute.configure(background = '#9ACD32')
 start_flash([button_display],"display", page4, flashers)
 stop_flash("pause", page4, flashers)
 button_pause.configure(background = '#9ACD32')
 print("dict_of_divisions after execution =", dict_of_divisions) 
###############################################
button_execute = Button(frame2, text="3. Execute", font='TkDefaultFont 10 bold', 
               bg='#9ACD32', activebackground="red",command=lambda:[threading.Thread(target=execute).start(), stop_flash("exec", page4, flashers)])               
button_execute.grid(row=0, column=0, pady=20)

feedback_label = tk.Label(frame1, text=" Welcome to DeepKymoTracker! \n\nTo choose input movie you want to track, press Button 1. ",fg="yellow",bg="black", font='TkDefaultFont 10 bold', width=120, height=4)
feedback_label.grid(row=1, column=0,columnspan=4, sticky=W)
#############################################################
def stop_execution_manually():
    button_execute.configure(background = button_color)
    global variable_stop
    variable_stop = "Stop"
    button_pause.configure(background = '#9ACD32')
#################################################################    
button_pause = Button(frame2, text="3a. Pause ",activebackground="red",
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
       
    global pedigree, lineage_per_frame
    lineage_per_frame=extract_lineage(outpath)
    # creates and saves per cell pedigree  
    pedigree = create_pedigree(lineage_per_frame, outpath) 
        
    feedback_label.config(text="Check results by sliding the bar under Current Frame."
                    "\n - If you need to edit cell IDs, press Button 5."
                    "\n - If you need to edit missed division, press Button 6."
                    "\n - If you are happy with the result press Button 7 to create lineage movie.")   
    global view_slider
    view_slider = Scale(frame9, from_=1, to=len(
        output_images)-1, orient=HORIZONTAL, troughcolor="green", command=slide_frames, length=370)      
    view_slider.grid(row=0, column=0, pady=5)
    button_display.configure(background = '#9ACD32')  
    threading.Thread(target=start_flash([button_start_id, button_start_division, button_final_movie], "edit", page4, flashers)).start()  
################################################
button_display = Button(frame2, text="4. Display result", font='TkDefaultFont 10 bold', 
               bg='#9ACD32',activebackground="red", command=lambda: [display_first_frame(), stop_flash("display", page4, flashers)])
button_display.grid(row=2, column=0, padx=20)
##################################
global manual_IDs,manual_centroids,mother_name 
manual_IDs,  manual_centroids, mother_name=[], [], None
###########3#######################
def get_cell_IDs_manually(event):# gets cell ID from previous frame during editing
    global manual_IDs  
    keys=list(lineage_per_frame[int(view_slider.get())-1].keys())#was -2  
    previous_image=lineage_per_frame[int(view_slider.get())-1][keys[0]][13]   
    previous_resized =cv2.resize(previous_image, (window_size,window_size), interpolation = cv2.INTER_AREA)  
    cell_number=int(previous_resized[event.y,event.x])-1   
    manual_IDs.append(cell_number)     
    cell_name_internal="cell_"+ str(cell_number) 
    cell_name_external=lineage_per_frame[int(view_slider.get())-2][cell_name_internal][11]# was -1  
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
    button_final_movie.configure(background = '#9ACD32')
    canvas_current.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    manual_centroids.append([event.x, event.y])   
    label_edit_results.configure(text="Cells chosen in Previous Frame:\n " + str(cell_names_external) +"\n""Centroids assigned in Current Frame:\n " + str(manual_centroids), bg="black")
######################################
def start_editing_IDs():
    label_edit_instructions.configure(text="Click on the cell in Previous Frame.\nMake sure you click on the cell body!\nThen click on the same cell in Current Frame \nMake sure you click on the centroid!")
    button_final_movie.configure(background = '#9ACD32')
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
####################################################
def stop_editing_IDs():
    button_start_id.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>") 
    global start_frame, lineage_per_frame, edit_id_indicator
    edit_id_indicator="yes"
    
    start_frame=int(view_slider.get())
    print("start_frame=", start_frame)
    keys=list(lineage_per_frame[start_frame-2].keys())   
    coords_old=lineage_per_frame[start_frame-2][keys[0]][14] 
    for i in range(len(manual_centroids)):
        coords_old[manual_IDs[i]]=manual_centroids[i] 
    global coords, text
    coords=coords_old  
    global prev_frame    
    prev_frame=lineage_per_frame[start_frame-1][keys[0]][13]    
    feedback_label.config(text="")
    print("text_before=",text) 
  
    cut_lineage(start_frame)
    text1=[lineage_per_frame[start_frame-2][key][11] for key in keys]
    text=sorted(text1)
    
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
###################################################
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
    button_final_movie.configure(background = button_color)
    start_flash([button_save_division],"save_division", page4, flashers)  
    threading.Thread(target=stop_flash("edit", page4, flashers)).start()
    button_start_division.configure(background = 'red')
    button_start_id.configure(background = '#9ACD32')
    button_final_movie.configure(background = '#9ACD32')
########################################
def stop_editing_division():
    button_start_division.configure(background = button_color)
    canvas_previous.unbind("<Button 1>")
    canvas_current.unbind("<Button 1>")
    global text, prev_frame
    text=[]  
    global start_frame, lineage_per_frame
    start_frame=int(view_slider.get())    
    keys=list(lineage_per_frame[start_frame-1].keys())# from previous frame was -2   
    prev_frame=lineage_per_frame[start_frame-1][keys[0]][13]# prev_frame-1 is not a mistake!!! was -1
   
    coords_old=lineage_per_frame[start_frame-1][keys[0]][14] 
    global manual_IDs, mother_number, mother_name    
    manual_division_indicator.set("yes")
    mother_number=manual_IDs[0] 
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage_per_frame[start_frame-2][mother_name_internal][11]
    mother_color=lineage_per_frame[start_frame-2][mother_name_internal][-2]
                                        
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
    for num in all_cell_numbers_sorted:
            true_cell_name=lineage_per_frame[start_frame-2]["cell_" + str(num)][11] 
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
    dict_of_divisions[mother_name] = start_frame-1   
    cut_lineage(start_frame) 
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
button_start_id = Button(frame3, text="5. Start editing IDs", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:start_editing_IDs())
button_start_id.grid(row=0, column=0)

label_edit_instructions = tk.Label(frame3, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="yellow", width=50, height=4)
label_edit_instructions.grid(row=2, column=0, columnspan=2)

button_save_id = Button(frame3, text="5a. Save ID edits", activebackground="red",font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:stop_editing_IDs())
button_save_id.grid(row=3, column=0)
###############################################################
button_start_division = Button(frame4, text="6. Start editing division", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:[threading.Thread(start_editing_division()).start(), stop_flash("edit", page4, flashers)])
button_start_division.grid(row=6, column=0)

label_edit_results = tk.Label(frame4, text=" ", font='TkDefaultFont 10 bold',  bg="black", fg="#00FFFF", width=45, height=4)
label_edit_results.grid(row=7, column=0)

button_save_division = Button(frame4, text="6a. Save division edits",activebackground="red", font='TkDefaultFont 10 bold', 
              bg='#9ACD32', command=lambda:stop_editing_division())
button_save_division.grid(row=8, column=0, columnspan=1)
####################################
def create_final_movie():    
    button_start_division.configure(background = '#9ACD32')
    button_start_id.configure(background = '#9ACD32')    
    create_output_movie(outpath,out_folders, frame_size)       
    button_final_movie.configure(background = '#9ACD32')
    feedback_label.config(text="Finished creating final movie!\nIt has been saved in  "+os.path.join(outpath,"lineage_movie.avi")+" \n\nTHE END")
##############################
global button_final_movie
button_final_movie = Button(frame10, text="7. Create final movie", font='TkDefaultFont 10 bold', 
               bg='#9ACD32', command=lambda: [threading.Thread(target=create_final_movie).start(),stop_flash("edit", page4, flashers), feedback_label.config(text="Creating final movie..." ), button_final_movie.configure(background = 'red')])
button_final_movie.grid(row=6, column=0, padx=100, pady=20)
#################################################################
page4.mainloop()

