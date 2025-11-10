###########################################################################
############################## PAGE-5 (STEP-4): CORRECT SEGMENTATION #######
#############################################################################
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
page5= tk.Tk()

page5.geometry('%dx%d+%d+%d' % (1530, 2000, 0, 0))
ws = page5.winfo_screenwidth() # width of the screen
hs = page5.winfo_screenheight() # height of the screen

bg_color,all_font,button_color,result_color,label_color, slide_trough_color="#A52A2A",'TkDefaultFont 10 bold','#9ACD32',"#00FFFF","#87CEFA","#513B1C"

page5.config(bg=bg_color)

global page_number, software_folder
source_code_folder = os.getcwd()
print("source_code_folder=",source_code_folder)
software_folder=os. path. dirname(source_code_folder)
print("software_folder=",software_folder)



page5.title("CREATE_MANUAK_SEGMENTATION_FOR_TRAINING")
page5.config(bg=bg_color)
from helpers_for_PAGE_4 import delete_contour_with_specific_colour,update_frame_dictionary_after_manual_segm_correction,\
 load_models_p5, make_contour_red,update_cheatsheet, load_tracked_movie_p5
from plot import paste_patch, prepare_contours,paste_benchmark_patch,create_name_for_cleaned_patch,\
    create_first_color_dictionary_for_train, update_color_dictionary,update_naive_names_list

from interface_functions import turn_image_into_tkinter,display_both_channels, show_2_canvases
from postprocess import create_output_movie
from print_excel import print_excel_files, extract_const_movie_parameters, update_lineage, extract_lineage
from functions import  clean_manual_patch, segment_manual_patch,segment_one_cell_at_a_time,create_intensity_dictionary,remove_cell_from_mask
from preprocess import extract_file_name
############ LAYOUT

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
def activate_buttons(all_buttons_list,active_buttons_list):
    for button in all_buttons_list:       
        if button in active_buttons_list:           
            button.config(state=NORMAL)                        
        else:
            button.config(state=DISABLED)   
###################################################
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
#############################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
######################################
def create_and_fill_folders(input_dir_p5,masks_dir, fluor_filled_dir, bright_filled_dir):
    global mock_lineage_per_frame
    mock_lineage_per_frame=[]
    print("INSIDE CREAYTE")
            
    for filename in sorted_aphanumeric(os.listdir(input_dir_p5)):
        #print("filename=", filename)
        if filename.endswith("ch00.tif"):
           im_fluor=cv2.imread(os.path.join(input_dir_p5, filename),-1)
           new_fl_name=os.path.join(fluor_filled_dir, filename)
           #print("new_fl_name=", new_fl_name)
           cv2.imwrite(new_fl_name,im_fluor)
           #####################
           frame_shape=im_fluor.shape
           mask=np.zeros(frame_shape,dtype="uint64")
           mask_name=filename[:-8]+"mask.tif"
           full_mask_name=os.path.join(masks_dir, mask_name)
           cv2.imwrite(full_mask_name,mask)
        if filename.endswith("ch02.tif"):
           mock_lineage_per_frame.append({})
           im_bright=cv2.imread(os.path.join(input_dir_p5, filename),-1)
           new_br_name=os.path.join(bright_filled_dir, filename)
           cv2.imwrite(new_br_name,im_bright)
    
    update_lineage(mock_lineage_per_frame, general_folder_path,'wb')
###############################
def load_images_for_segm(input_dir_p5,masks_dir, fluor_filled_dir, bright_filled_dir):    
    path_filled_brights, path_filled_fluors,path_masks=[],[],[]
    empty_fluors, empty_brights,filled_fluors, filled_brights, masks=[],[],[],[],[]
    
    for filename in sorted_aphanumeric(os.listdir(input_dir_p5)):
        if filename.endswith("ch02.tif"):
           im_bright=cv2.imread(os.path.join(input_dir_p5, filename),-1)
           #image_bright=cv2.cvtColor(im_bright,cv2.COLOR_GRAY2BGRA)
           empty_brights.append(im_bright)
        if filename.endswith("ch00.tif"):
           im_fluor=cv2.imread(os.path.join(input_dir_p5, filename),-1)
           #image_fluor=cv2.cvtColor(im_fluor,cv2.COLOR_GRAY2BGRA)
           empty_fluors.append(im_fluor)
    for filename in sorted_aphanumeric(os.listdir(fluor_filled_dir)):
           path_im_fluor=os.path.join(fluor_filled_dir, filename)
           im_fluor_filled=cv2.imread(path_im_fluor ,1)
           path_filled_fluors.append(path_im_fluor)
           filled_fluors.append(im_fluor_filled)  
    for filename in sorted_aphanumeric(os.listdir(bright_filled_dir)):
           path_im_bright=os.path.join(bright_filled_dir, filename)
           im_bright_filled=cv2.imread(path_im_bright ,1)
           path_filled_brights.append(path_im_bright)
           filled_brights.append(im_bright_filled)   
     
    for filename in sorted_aphanumeric(os.listdir(masks_dir)):
           path_im_mask=os.path.join(masks_dir, filename)
           im_mask=cv2.imread(path_im_mask ,-1)
           path_masks.append(path_im_mask)
           masks.append(im_mask)                                 
    print("len(masks)=",len(masks))
    
    mock_lineage_per_frame=extract_lineage(general_folder_path)               
    return path_filled_brights,path_filled_fluors,path_masks, empty_fluors, empty_brights, filled_fluors, filled_brights, masks, mock_lineage_per_frame
############################# load all mecessary images
def load_raw_movie():
    global edits_indicator
    edits_indicator="no"
    global button_load_p5
    #update_flash([])
    button_load_p5.configure(background = 'red')
    global output_dir_p5, input_dir_p5,software_folder, helper_dir_p5, general_folder_path
    input_dir_p5 = filedialog.askdirectory()# \TRACKED_MOVIE_{movie name}
    print("input_dir_p5 =", input_dir_p5)
    dialog_label_5.config(text="Choose your movie and click on it once (not twice!)")  
    ##################################
    general_folder_path=os.path.dirname(input_dir_p5)
    print("general_folder_path=",general_folder_path)
    general_folder_name=os.path.basename(  general_folder_path)
    print("general_folder_name=",  general_folder_name)
    masks_dir=os.path.join(general_folder_path,"MASKS")
    fluor_filled_dir=os.path.join(general_folder_path,"TRACKED_GREEN_FL_CHANNEL")
    bright_filled_dir=os.path.join(general_folder_path,"TRACKED_BRIGHTFIELD_CHANNEL")
    segmented_dir=os.path.join(general_folder_path,"SEGMENTED")
    if not os.path.exists(masks_dir):
           print("I am here")
           os.mkdir(masks_dir)   
           os.mkdir(fluor_filled_dir)   
           os.mkdir(bright_filled_dir)
           os.mkdir(segmented_dir)
           create_and_fill_folders(input_dir_p5,masks_dir, fluor_filled_dir, bright_filled_dir)        
    ########################################
    global path_filled_brights,path_filled_fluors,path_masks,mock_lineage_per_frame
    global empty_fluors, empty_brights,filled_fluors, filled_brights, masks
    
    dialog_label_5.config(text="loading tracked movie...")
    path_filled_brights,path_filled_fluors,path_masks, empty_fluors, empty_brights, filled_fluors, filled_brights, masks, mock_lineage_per_frame=load_images_for_segm(input_dir_p5,masks_dir, fluor_filled_dir, bright_filled_dir)
    print("len(filled_fluors)=", len(filled_fluors))
    test_image=filled_fluors[0]
    #print("test_image.shape=",test_image.shape)
    #print("test_image.dtype=",test_image.dtype)
    global frame_p5_size,cell_radius_p5,patch_size_p5, first_frame_number_p5, bordersize, n_digits   
    #############
    frame_p5_size=empty_fluors[0].shape[0]
    cell_radius_p5,patch_size_p5=20,96
    global full_core_fluor_name, n_digits, first_frame_number_p5, num_frames
    #print("path_filled_fluors[0]=", path_filled_fluors[0])
    debug_name=os.path.basename(path_filled_fluors[0])
    #print("debug_name=", debug_name)
    full_core_fluor_name, n_digits, first_frame_number_p5= extract_file_name(os.path.basename(path_filled_fluors[0]))
    #first_frame_number_p5=1
    #print('full_core_fluor_name, n_digits, first_frame_number_p5 = ', full_core_fluor_name, n_digits, first_frame_number_p5)
    bordersize, n_digits=100,4
    num_frames=len(empty_fluors)
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
    global last_draw_zoom_coeff
    last_draw_zoom_coeff=1
    ############################
   
    print("frame_p5_size=",frame_p5_size)
    feedback_label_5.configure(text="Movie : "+input_dir_p5+"\nFluorescent frames: "+str(num_frames)+\
                               "   Bright frames: "+str(len(filled_brights))+"   Red frames: 0"+\
                                   "\nFrame size = "+ str(frame_p5_size)+" x "+str(frame_p5_size)+"   Cell diameter = "+str(cell_radius_p5*2))   
    global photo_filled_fluors, photo_filled_brights
    dialog_label_5.config(text="Preparing images for display...")
    photo_filled_fluors=[ turn_image_into_tkinter(filled_fluors[i], window_p5_size,[]) for i in range(len(filled_fluors))]
    dialog_label_5.config(text="Prepared 50 % of images for display")
    photo_filled_brights=[ turn_image_into_tkinter(filled_brights[i], window_p5_size,[]) for i in range(len(filled_brights))]
    
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
        
#####################################
def click_cell_to_add(event):
    global cell_number
    cell_number+=1
    print("cell_number=", cell_number)
    global helper_mask_one_cell
    helper_mask_one_cell=np.zeros((frame_p5_size,frame_p5_size),dtype="uint8")
        
    rad =10
    center=(event.x,event.y)
    #################################
    number_of_now_added_cells=1
    global colour_dictionary, new_naive_names, colour_counter, base_colours, basic_naive_names, naive_names_counter,curr_frame_cell_names          
    new_naive_names,naive_names_counter=update_naive_names_list(basic_naive_names, number_of_now_added_cells,naive_names_counter)    
    colour_dictionary, colour_counter=update_color_dictionary(colour_dictionary,new_naive_names,base_colours, colour_counter)    
    curr_frame_cell_names+=new_naive_names 
    cell_name=new_naive_names[0]
    #number_of_added_new_cells+=number_of_now_added_cells 
    #colour_dictionary, new_naive_names, base_colours, colour_counter, basic_naive_names,  naive_names_counter= create_first_color_dictionary_for_train(0)
    print("colour_dictionary=", colour_dictionary)
    print("new_naive_names=", new_naive_names)
    print("base_colours=", base_colours)
    print("colour_counter=", colour_counter)
    print("basic_naive_names=", basic_naive_names)
    print("naive_names_counter=", naive_names_counter)
    print("curr_frame_cell_names=",  curr_frame_cell_names)
    print("cell_name=",  cell_name)
    ###############################################
    cell_colour=base_colours[colour_counter-1]
    print("cell_colour=",  cell_colour)
    cell_colour_for_plot =cell_colour[0]
    print("cell_colour_for_plot=",  cell_colour_for_plot)
    thickness=2
    true_center=(int(center[0]/resize_coeff) ,int(center[1]/resize_coeff ))    
    circle_fl=canvas_fluor_p5.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline =cell_colour[1],width = 2)    
    circle_br=canvas_bright_p5.create_oval(event.x-rad,event.y-rad,event.x+rad,event.y+rad,outline = cell_colour[1],width = 2)      
    cv2.circle(current_fluor_image, true_center, rad,cell_colour_for_plot , thickness)
    cv2.circle(current_bright_image, true_center, rad, cell_colour_for_plot, thickness)
    ######################################################
    cv2.circle(helper_mask_one_cell, true_center, rad, 255, -1)   
    current_mask[helper_mask_one_cell==255]=2**cell_number
    #################################################
    cv2.imwrite(current_fluor_path,current_fluor_image)
    cv2.imwrite(current_bright_path,current_bright_image)
    cv2.imwrite(current_mask_path,current_mask)
    ###################################################
    
    frame_cells["cell_%s" % cell_number]=[cell_name, cell_colour, cell_number]
    print(" frame_cells=",  frame_cells)                                                   
   
def start_adding_cells():
    global canvas_fluor_p5,canvas_bright_p5
    canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.unbind("<B1-Motion>")
    canvas_fluor_p5.unbind( "<ButtonPress-1>")
    canvas_fluor_p5.unbind("token<ButtonRelease-1>")  
    canvas_fluor_p5.bind("<Button-1>", click_cell_to_add)
    canvas_fluor_p5.unbind("<Button-3>")
    global frame_number_from_slider ,internal_frame_number_p5
    frame_number_from_slider =view_slider_p5.get()
    print("frame_number_from_slider=",frame_number_from_slider)
    print("first_frame_number_p5 =",first_frame_number_p5 )   
    internal_frame_number_p5=frame_number_from_slider-first_frame_number_p5
    ###################################################
    global current_fluor_path,current_bright_path,current_mask_path 
    current_fluor_path=path_filled_fluors[internal_frame_number_p5]
    current_bright_path=path_filled_brights[internal_frame_number_p5] 
    current_mask_path=path_masks[internal_frame_number_p5]
    ###################################################
    global current_fluor_image,current_bright_image, current_mask
    current_fluor_image=filled_fluors[internal_frame_number_p5]
    current_fluor_image = cv2.cvtColor(current_fluor_image,cv2.COLOR_BGR2BGRA) 
    current_bright_image=filled_brights[internal_frame_number_p5]
    current_bright_image = cv2.cvtColor(current_bright_image,cv2.COLOR_BGR2BGRA)
    current_mask=masks[internal_frame_number_p5]
    #########################################################
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(current_fluor_image,current_bright_image,canvas_fluor_p5,canvas_bright_p5,new_shape,image_origin_x,image_origin_y, active_channel_var.get())
    global circles_fl
    circles_fl=[]
    
    global cell_number
    cell_number=-1
    global frame_cells
    frame_cells={}
    
    global colour_dictionary, new_naive_names, colour_counter, base_colours, basic_naive_names, naive_names_counter, curr_frame_cell_names          
    colour_dictionary, new_naive_names, base_colours, colour_counter, basic_naive_names,  naive_names_counter= create_first_color_dictionary_for_train(0)
    curr_frame_cell_names=[]
    print("colour_dictionary=", colour_dictionary)
    print("new_naive_names=", new_naive_names)
    print("base_colours=", base_colours)
    print("colour_counter=", colour_counter)
    print("basic_naive_names=", basic_naive_names)
    print("naive_names_counter=", naive_names_counter)
    print(" curr_frame_cell_names=",  curr_frame_cell_names)
#########################################
def stop_adding_cells():    
    filled_fluors[internal_frame_number_p5]=current_fluor_image
    filled_brights[internal_frame_number_p5]=current_bright_image
    masks[internal_frame_number_p5]=current_mask
    print("frame_cells=",frame_cells)
    mock_lineage_per_frame[ internal_frame_number_p5]=frame_cells
    update_lineage(mock_lineage_per_frame, general_folder_path,'wb')
    print("mock_lineage_per_frame=",mock_lineage_per_frame)
    canvas_fluor_p5.unbind("<Button-1>")
    canvas_fluor_p5.unbind("<Button-3>")   
    canvas_fluor_p5.bind("<Button-3>", right_click_one_cell)
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
           print("cells_in_current_frame_sorted=",cells_in_current_frame_sorted)
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
      patch_with_contours=prepare_contours(segmented_patch,1)    
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
    print("INSIDE get_frame_info")
    print("mock_lineage_per_frame=",mock_lineage_per_frame)
    frame_dictionary=mock_lineage_per_frame[internal_frame_number_p5]
    keys=list(frame_dictionary.keys())
    global intensity_dictionary_for_frame
    intensity_dictionary_for_frame=create_intensity_dictionary(len(keys))  
    
    global cells_in_current_frame_sorted
    cells_in_current_frame=[(frame_dictionary[key][0],frame_dictionary[key][1],frame_dictionary[key][2]) for key in keys]    
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
    
    global path_filled_bright, path_filled_fluor,path_filled_red,path_mask
    path_filled_bright, path_filled_fluor,path_mask= path_filled_brights[internal_frame_number_p5],path_filled_fluors[internal_frame_number_p5],path_masks[internal_frame_number_p5]
    global final_mask,filled_fluor,filled_bright, filled_red
    filled_fluor=filled_fluors[internal_frame_number_p5]
    filled_fluor = cv2.cvtColor(filled_fluor,cv2.COLOR_BGR2BGRA)
    filled_bright=filled_brights[internal_frame_number_p5]
    filled_bright = cv2.cvtColor(filled_bright,cv2.COLOR_BGR2BGRA)
    ############################################
    current_frame_number_zfill=str(frame_number).zfill(n_digits)
    print("current_frame_number_zfill=",current_frame_number_zfill)
    
    final_mask=copy.deepcopy(mask)
    disable_exit()         
    #update_flash([]) 
################################################################
def save_edits_for_frame(): #saves all eduts in current frame and modifies linage for this frame
    global   frame_dictionary
    print("INSIDE SAVE EDITS FOR FRAME")
    #cv2.imwrite(r"C:\Users\helina\Desktop\final_mask_INSIDE_SAVE_FRAME.tif",final_mask*10)          
    frame_dictionary= mock_lineage_per_frame[internal_frame_number_p5]
    #debug_item=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]
    if red_channel_indicator==1:
        last_arg=[1,filled_red]
    else:
        last_arg=[0, []]
    modified_frame_dictionary=frame_dictionary
    #modified_frame_dictionary=update_frame_dictionary_after_manual_segm_correction(final_mask, filled_fluor,filled_bright,modified_cell_IDs,frame_dictionary,frame_p5_size, patch_size_p5, bordersize, last_arg)    
    mock_lineage_per_frame[internal_frame_number_p5]=modified_frame_dictionary
    #debug_item_after=lineage_per_frame_p5[internal_frame_number_p5]["cell_0"][3]      
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
       #cv2.imwrite(os.path.join(output_dir_p5,"HELPER_FOLDERS_(NOT FOR USER)","CLEANED_PATCHES",patch_path), patch)          
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
    
button_load_p5 = Button(frame3_page5, text="1. Click to open file menu and choose TRACKED_MOVIE_{your movie name} folder", command=lambda:threading.Thread(target=load_raw_movie).start(), bg=button_color, font=all_font,activebackground="red")
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
button_start_cell = Button(frame4c_page5, text="Start cell", command=start_adding_cells)
button_start_cell.pack(side=tk.BOTTOM, padx=100)
button_stop_cell = Button(frame4c_page5, text="Stop cell", command=stop_adding_cells)
button_stop_cell.pack(side=tk.BOTTOM, padx=100)      
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
button_exit=Button(frame8_page5, text="Exit",bg="orange",font=all_font, command=page5.destroy).pack(side=tk.LEFT, padx=(700,2))
###################################
global all_buttons_page5
all_buttons_page5=[button_load_p5, button_activate_slow_edit_mode,\
                   start_zoom_button, start_pan_button,stop_pan_button,\
                   button_final_movie,view_slider_p5]
################################################################################
global models, models_directory,segmentor,refiner
from helpers_for_PAGE_4 import load_models_p5
from preprocess import create_models
software_folder=r"C:\Users\helina\Desktop\DeepKymoTracker"
models_directory = os.path.join(software_folder, "TRAINED MODELS")

models,models_directory=create_models(software_folder)
segmentor, refiner= load_models_p5(software_folder)
#############################
page5.mainloop()
