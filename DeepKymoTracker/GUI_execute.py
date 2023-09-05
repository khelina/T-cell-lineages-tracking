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

#########################################
window = tk.Tk()
window.geometry('1530x2000')
window.title("TRACKING BEGIN WITH N CELLS")
frame1 = tk.Frame(master=window, width=1528, height=50, bg="grey")
frame1.grid(row=0, column=0, rowspan=1, columnspan=4, sticky=W+E+N+S)

frame2 = tk.Frame(master=window, width=382, height=30, bg="red")
frame2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame3 = tk.Frame(master=window, width=382, height=30, bg="yellow")
frame3.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame4 = tk.Frame(master=window, width=382, height=30, bg="green")
frame4.grid(row=1, column=2, rowspan=2, columnspan=1, sticky=W+E+N+S)

frame13 = tk.Frame(master=window, width=382, height=30, bg="orange")
frame13.grid(row=1, column=3, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame5 = tk.Frame(master=window, width=382, height=382, bg="white")
frame5.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame6 = tk.Frame(master=window, width=382, height=382, bg="blue")
frame6.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame7 = tk.Frame(master=window, width=382, height=382, bg="brown")
frame7.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+N+S)

#frame7a = tk.Frame(master=window, width=382, height=382, bg="brown")
#frame7a.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+N+S)

frame11 = tk.Frame(master=window, width=382, height=50, bg="blue")
frame11.grid(row=2, column=3, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame8 = tk.Frame(master=window, width=382, height=50, bg="grey")
frame8.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame9 = tk.Frame(master=window, width=382, height=50, bg="orange")
frame9.grid(row=3, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame10 = tk.Frame(master=window, width=382, height=50, bg="yellow")
frame10.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=W+E+N+S)


frame12 = tk.Frame(master=window, width=382, height=50, bg="green")
frame12.grid(row=3, column=3, rowspan=1, columnspan=1, sticky=W+E+N+S)

######################################################
canvas_5 = Canvas(frame5, bg='black', height=382, width=382)
canvas_5.pack(anchor='nw', fill='both', expand=True)
canvas_6 = Canvas(frame6, bg='black', height=382, width=382)
canvas_6.pack(anchor='nw', fill='both', expand=True)

canvas_7 = Canvas(frame7, bg='black', height=382, width=382)
canvas_7.grid(row=0,column=0)

#canvas_7a = Canvas(frame7, bg='black', height=382, width=382)
#canvas_7a.grid(row=0,column=0)
canvas_11 = Canvas(frame11, bg='black', height=382, width=382)
canvas_11.pack(anchor='nw', fill=None, expand=True)
canvas_12 = Canvas(frame12, bg='black', height=382, width=382)
canvas_12.pack(anchor='nw', fill=None, expand=True)
################################
global lineage, start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions
lineage, start_frame,dict_of_divisions, dict_of_missed_divisions, dict_of_true_divisions = [], 1, {},{},{}
global out_folders
out_folders = []
dict_of_divisions={}
lineage=[]
   
global coords_1, coords_very_first
coords_1, coords_very_first = [], []

global my_dir
my_dir = ''
global per_cell_dict
per_cell_dict = {}
global clicked
clicked = StringVar()
clicked.set("Begin with 1 cell")
# Frame 1

l0 = tk.Label(frame1, text="TRACK AND SEGMENT",
              bg="yellow", fg="red", font=("Times", "24"))
l0.grid(row=0, column=1, padx=2)


def load_models():

    software_folder = filedialog.askdirectory()

    os.chdir(software_folder)

    global predict_first_frame, create_output_folders, load_one_well_images,\
        detect_division, update_dictionary_after_division, check_frame, predict_tracking, predict_tracking_general, check_tracker_1, predict_first_frame, segment_and_clean,\
        hungarian, create_previous_frame, create_current_frame, plot_frame, create_color_dictionary,\
        create_lineage, create_per_cell_info, create_lineage_movie_1

    from preprocess import create_output_folders, load_one_well_images

    from division_detector import (detect_division,
                                   update_dictionary_after_division, check_frame)

    from functions import (predict_tracking, check_tracker_1, predict_first_frame, segment_and_clean,
                           hungarian, create_previous_frame, create_current_frame)

    from plot import plot_frame, create_color_dictionary
    from postprocess import create_lineage, create_per_cell_info, create_lineage_movie_1
    from keras.models import model_from_json

    from keras.optimizers import Adam
    global models
    directory = os.path.join(software_folder, "TRAINED MODELS")
    model_names = ["Tracker-1", "Tracker-2", "Tracker-3","Tracker-4","Tracker-5",
                   "Segmentor", "Refiner"]
    models = []
    for name in model_names:
        progressbar_2["value"] += 20
        time.sleep(0.02)
        frame2.update_idletasks()
        full_name = os.path.join(directory, name)
        json_file = open(full_name + "-model.json", "r")
        model_read = json_file.read()
        json_file.close()
        model = model_from_json(model_read)
        model.load_weights(full_name + "-weights.h5")
        model.compile(Adam(lr=0.003), loss='mse', metrics=['mae'])
        models.append(model)
    print("models loaded")
    print("len(models)=", len(models))
    l3.config(text="Models loaded", fg="blue")


b0 = tk.Button(frame1, text="1. Load models",
               bg='#ffb3fe', command=lambda:load_models())
b0.grid(row=1, column=0)


progressbar_2 = ttk.Progressbar(
    frame1, orient='horizontal', mode='determinate', length=50)
progressbar_2.grid(row=1, column=1, padx=20)

l3 = Label(frame1, text=" ", padx=20)
l3.grid(row=1, column=2)


def choose_folder():
    l0.config(text=" ")
    l1.config(text=" ")
    global my_dir
    my_dir = filedialog.askdirectory()
    l1.config(text="Chosen folder: " + my_dir, fg="blue")

    global out_folders, outpath
    software_folder = os.path.dirname(my_dir)
    input_movie_folder = os.path.basename(my_dir)
    outpath = os.path.join(software_folder, "OUTPUT_"+input_movie_folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    else:
        shutil.rmtree(outpath)
        os.mkdir(outpath)
    out_folders = create_output_folders(outpath)

    global fluor_compressed, fluor_images, bright_images, names, bright_names

    # def load_images(folder_dir):
    print("loading images...")
    # writes fluor_images and bright_images in folder my
    
    fluor_images, bright_images, fluor_compressed, names, bright_names = [], [], [], [], []
    for filename in sorted_aphanumeric(os.listdir(my_dir)):
        if filename.endswith("ch00.tif"):
        
            progressbar_1["value"] += 50
            #progressbar_1["value"]=((i+1)/len(names))*100
            time.sleep(0.02)
            frame1.update_idletasks()

            full_name = os.path.join(my_dir, filename)
            names.append(full_name)
            raw = cv2.imread(full_name, 0)
            raw2 = raw.copy()
            raw1_compressed = cv2.resize(
                raw2, (100, 100), interpolation=cv2.INTER_LANCZOS4)
            fluor_compressed.append(raw1_compressed)
            raw3 = raw.copy()
            fluor_images.append(raw3)
        if filename.endswith("ch02.tif"):
            full_name = os.path.join(my_dir, filename)
            bright_names.append(full_name)
            bright0 = cv2.imread(full_name, 0)
            bright = bright0.copy()
            bright_images.append(bright)
    global num_frames
    num_frames = len(names)
    print("loading finished")

    # fluor_images_compressed,fluor_images,bright_images,names,bright_names=load_images(os.path.join(software_folder,input_movie_folder))

    l0.config(text="Movie loaded, {} frames".format(len(names)), fg="blue")
    print(len(names))


b1 = tk.Button(frame1, text="2. Click to open file menu and then select input movie folder",
               bg='#ffb3fe', command=lambda:choose_folder())
b1.grid(row=2, column=0, padx=10, pady=20)

l1 = tk.Label(frame1, text=my_dir)
l1.grid(row=2, column=1, padx=2)


progressbar_1 = ttk.Progressbar(
    frame1, orient='horizontal', mode='indeterminate', length=50)
progressbar_1.grid(row=2, column=2, padx=10)


l0 = tk.Label(frame1, text=my_dir)
l0.grid(row=2, column=3, padx=2)

l2 = tk.Label(
    frame1, text="3. How many cells are there in the 1st frame of your movie?")
l2.grid(row=3, column=0, padx=2)
def begin_with_one_cell():
    R1.config(fg="blue")
    R2.config(fg="black")
    global coords_1, coords_very_first
    coords_1, coords_very_first=[],[]
    first_clip_compressed = [fluor_compressed[i] for i in range(0, 4, 1)]
    coords_first = predict_first_frame(first_clip_compressed, models[0])
    coords_1= coords_first.tolist()
    coords_very_first=coords_1
    print("coords_1=", coords_1)
    global colours, template_names, prev_frame
    colours, template_names = create_color_dictionary(
        10, len(coords_1))# 10 =maximum number of cells
    global text
    text = template_names[:len(coords_1)]
    print("text=", text)
    prev_frame = np.zeros((382, 382), dtype="float64")
    for i in range(len(coords_very_first)):
        one_circle = np.zeros((382, 382), dtype="uint8")
        one_circle = cv2.circle(
            one_circle, (int(coords_first[i][0]), int(coords_first[i][1])), 10, i+1, -1)
        one_circle = one_circle.astype('float64')
        prev_frame += one_circle
   
R1 = Radiobutton(frame1, text="1 cell", value="1 cell", variable=clicked, command=begin_with_one_cell)
R1.grid(row=3, column=1)
#######################################

############################


def create_popup():
    R1.config(fg="black")
    R2.config(fg="blue")
    global popup
    popup = tk.Toplevel(master=window, width=382, height=382)
    sub1 = tk.Frame(master=popup, width=382, height=50, bg="black")
    sub1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

    l1 = tk.Label(
        sub1, text="Click on each cell with the left button of the mouse,\nthen close the window", bg="#feffb3")
    l1.pack()
    #l1.grid(row=1, column=1,padx=2)
    sub2 = tk.Frame(master=popup, width=382, height=382, bg="black")
    sub2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

    global canvas
    canvas = Canvas(sub2, bg='black', height=382, width=382)
    canvas.pack(anchor='nw', fill='both', expand=True)
    canvas.bind("<Button-1>", draw_circle)
    sub3 = tk.Frame(master=popup, width=382, height=30, bg="black")
    sub3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)
    b3 = tk.Button(sub3, text="Save", bg='#ffb3fe', command=close_popup)
    b3.pack()
    
    full_name = names[0]
    global photo
    photo = Image.open(full_name)
    photo = photo.resize((382, 382), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(photo)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    
def close_popup():
      #print("coords_1=", coords_1)
      global coords_very_first
      coords_very_first=coords_1
      global colours, template_names, prev_frame
      colours, template_names = create_color_dictionary(
        10, len(coords_1))# 10 =maximum number of cells
      #print("template_names=", template_names)
      N_cells=len(coords_1)
      
      global text
      text = template_names[:len(coords_1)]
      #print("text=", text)
      prev_frame = np.zeros((382, 382), dtype="float64")
      for i in range(len(coords_very_first)):
        one_circle = np.zeros((382, 382), dtype="uint8")
        one_circle = cv2.circle(
            one_circle, (int(coords_very_first[i][0]), int(coords_very_first[i][1])), 10, i+1, -1)
        one_circle = one_circle.astype('float64')
        prev_frame += one_circle
      popup.destroy()
      

R2 = Radiobutton(frame1, text="More than 1 cell",fg="black",
                 value="More than 1 cell", variable=clicked, command=create_popup)
R2.grid(row=3, column=2)


def sorted_aphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def draw_circle(event):
    canvas.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    coords_1.append([event.x, event.y])
    
global text, variable_stop, manual_division_indicator, mother_number
text, variable_stop, manual_division_indicator, mother_number=StringVar(), StringVar(), StringVar(), IntVar()
text,variable_stop, manual_division_indicator, mother_number="", "","", None
######################   Frame 2  ##################
def my_exec_1():

 try:
    segmentor = models[5]
    refiner = models[6]

    start = start_frame  # the 1st frame of the movie. 1 is default
    
   
    global coords_first,prev_frame
    
    N_cells = int(len(coords_1))
    coords_first = np.zeros((N_cells, 2))
    for i in range(N_cells):
            coords_first[i] = coords_1[i]
    
    coords = coords_first
    global text   
         
    cells = {}
    n = len(names)
    #n=650    
    k = start-1  # the first frame of clip
    # counts can be 1 or 2 (the first division is ignored)
    count = np.zeros((100), dtype="uint8")# 10=maximem number of cells
    kk = 0  # the number of frame with clip
    
    l_finish.config(text="")
    while k < n:
        #print("k=",k)
        #print("N_cells=", N_cells)
        #if N_cells <= 3:
        clip_centr = predict_tracking(
                coords, fluor_images, fluor_compressed, names, k, out_folders[0], models,n)
       # else:
            #clip_centr = predict_tracking_general(
                #coords, fluor_images, fluor_compressed, names, k, out_folders[0], models,n)
        print("TRACKING PREDICTED FOR CLIP BEGINNING WITH FRAME  ", k)

        #print("clip_centr=", clip_centr)
        for kk in range(len(clip_centr)):
            print("k+kk=", k+kk)# segmenting all the 4 frames in the clip
            
            clip_centr = check_tracker_1(
                clip_centr, coords, kk)  # correct too big jumps
            tracked_centroids, rule = hungarian(
                coords, clip_centr[kk])  # correct id swappings
            empty_fluor = fluor_images[k+kk]
            #print("tracked_centroids=", tracked_centroids)
            empty_bright = bright_images[k+kk]

            #print("coords_before segm=", coords)
            count, cells, coords,  text = segment_and_clean(
                dict_of_divisions, cells, count, coords, prev_frame, text, segmentor, refiner, empty_fluor, empty_bright, tracked_centroids, k+kk, manual_division_indicator, mother_number, out_folders)
            
            #print("coords_after segm=", coords)
            # pages.append([cells["cell_0"][-2],cells["cell_0"][-1],k+kk])
            print("cells after segmentation=", list(cells.keys()))
            lineage.append(cells)
            ################## Division Detector,look for figure 8 
            division_indicator = 0  
            count, cut_patches, mother_8_name = detect_division(
                cells, count, k, kk)
            #print("count=", count)
            if (np.any(count == 2) or np.any(count == 1)):
                #print("cell_name=", cell_name)
                if mother_8_name != []:
                    count = check_frame(
                        count, cells, dict_of_divisions, mother_8_name, k+kk)
                    #print("count after check frame=", count)
            if np.any(count == 2):
                cells, text, count, division_indicator, coords = update_dictionary_after_division(
                    cut_patches, cells, text, count, division_indicator, coords)
            if division_indicator == 1 and mother_8_name != []:
                dict_of_divisions[mother_8_name] = k+kk
                print("8-figure division in frame ", k+kk)
                dict_of_true_divisions[mother_8_name] = k+kk
            ####################################################    
            N_cells = len(cells)
            print("cells after division detector=", list(cells.keys()))
            # after.append([cells["cell_0"][-2],cells["cell_0"][-1],k+kk])
            # cells=recalculate_centres(cells)

            coords = plot_frame(text, cells, clip_centr, k, kk,
                                fluor_images, names, out_folders, coords, coords, colours)
          
            #print("coords_after plot=", coords)
            
           
            current_frame = create_previous_frame(cells)

            current_frame_for_plot = create_current_frame(current_frame)

            current_frame_for_plot = current_frame_for_plot.astype('float64')

            summ = prev_frame*50+current_frame_for_plot
            cv2.imwrite(
                "C:\\Users\\kfedorchuk\\Desktop\\pre_curr\\pre_curr_%s.tif" % (k+kk+1), summ)
          
            prev_frame = current_frame

            if (division_indicator == 1):
                print("division occured in frame ", k+kk)
                # list_of_mothers.append(mitotic_cell)
                dict_of_divisions[text[-1][:-1]] = k+kk
                break
        if (division_indicator == 1):
            k = k+kk+1
        else:
            k += 4
        if variable_stop=="Stop":
               l_finish.config(text="Stopped manually", fg="blue")
               break
 except:
       #messagebox.showerror("Title", "Message")
       tk.messagebox.showerror('Error',traceback.format_exc()) 
       #tk.messagebox.showerror('Python Error', 'Error occured during execution. Go to the next step.')
 l_finish.config(text="Finished", fg="blue")
 #print("dict_of_divisions=", dict_of_divisions)
 
 a=[(lineage[i].keys(),i) for i in range(len(lineage))]
 #print(a)
 
#####################################################
#b3 = Button(frame2, text="4. Run algorithm", bg='#ffb3fe', command=lambda:threading.Thread(target=my_exec_1, args=()).start())

b3 = tk.Button(frame2, text="4. Run algorithm",
               bg='#ffb3fe', command=lambda: my_exec_1())

b3.grid(row=1, column=0, padx=10, pady=20)


l_finish = tk.Label(frame2, text="")
l_finish.grid(row=1, column=1, padx=2)


def stop_exec():
    global variable_stop
    variable_stop = "Stop"


stop_button = tk.Button(frame2, text="4a. Stop ",
               bg='#ffb3fe', command=lambda: stop_exec())
stop_button.grid(row=1, column=2, padx=10, pady=20)



####################################


def slide_result(value):
    
    #canvas_7a.tag_lower()
    #canvas7.tag_raise()   
    #frame7a.grid_remove()
    #frame7.tkraise()
    #frame7.grid()
    #canvas_7 = Canvas(frame7, bg='black', height=382, width=382)

        
    canvas_6.delete('all')
    canvas_5.delete('all')    
    canvas_7.delete('all')
    
    image_number = int(value)
    canvas_6.create_image(0, 0, anchor=NW, image=output_images[image_number])
    canvas_5.create_image(0, 0, anchor=NW, image=output_images[image_number-1])
    canvas_7.create_image(
        0, 0, anchor=NW, image=lineage_images[image_number-1])


# in most cases it is [-13:-9] (for names like t0001_ch02.tif)
def characters(x):
    # if it is t00001_ch02.tif it should be changed to [-14:-9]
    return(x[-14:-9])
    # if t001_ch02.tif it is [-12:-9]


def display_frames():
    global pedigree
    # creates and saves per cell pedigree
    print("len(lineage)=", len(lineage))
    pedigree = create_lineage(lineage, outpath, colours)
    print("pedigree.keys()=", pedigree.keys())
    print("len(pedigree)=", len(pedigree))
    global still_lineage
    lineage_images_cv, still_lineage = create_lineage_movie_1(
        pedigree, colours, template_names, outpath, coords_very_first, num_frames)
    print("len(lineage_images_cv)=", len(lineage_images_cv))
    global lineage_images
    lineage_images = []
    for ii in range(len(lineage_images_cv)):

        image_lin = lineage_images_cv[ii]
        image_lin_copy = np.uint8(image_lin)
        im_lin_rgb = cv2.cvtColor(image_lin_copy, cv2.COLOR_BGR2RGB)
        photo_image_lin = Image.fromarray(im_lin_rgb)
        photo_image_lin = ImageTk.PhotoImage(photo_image_lin)
        lineage_images.append(photo_image_lin)

    
    output_names = []

    source = out_folders[3]
    for filename in os.listdir(source):
        if filename.endswith("ch00.tif"):
            full_name = os.path.join(source, filename)
            output_names.append(full_name)
    output_names_sorted = sorted(output_names, key=characters)
    global output_images
    output_images = []
    for i in range(len(output_names_sorted)):
        file_name = output_names_sorted[i]
        image = cv2.imread(file_name, -1)
        image_copy = np.uint8(image)
        image_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
        photo_image = Image.fromarray(image_rgb)
        photo_image = ImageTk.PhotoImage(photo_image)
        output_images.append(photo_image)

    print("len(output_images)=", len(output_images))
    global zero_image
    zero_image = Image.new('RGB', (382, 382))
    zero_image = ImageTk.PhotoImage(zero_image)
    output_images.insert(0, zero_image)

    print("len(output_images)=", len(output_images))
    #canvas_7a.tag_lower()
    #canvas7.tag_raise()   
    #frame7a.grid_remove()        
   
    #frame7a.grid_remove()
    #frame7.tkraise()
    #frame7.grid()
    #canvas_7 = Canvas(frame7, bg='black', height=382, width=382)
    #canvas_7.grid(row=0,column=0)
        
    canvas_6.create_image(0, 0, anchor=NW, image=output_images[1])
    canvas_5.create_image(0, 0, anchor=NW, image=output_images[0])
    canvas_7.create_image(0, 0, anchor=NW, image=lineage_images[0])

    global view_slider
    view_slider = Scale(frame9, from_=1, to=len(
        output_images)-1, orient=HORIZONTAL, troughcolor="blue", command=slide_result, length=380)
    view_slider.grid(row=1, column=0, sticky="e")

#l110.configure(text="Finished!", fg="blue")


b4 = tk.Button(frame2, text="5. Display result",
               bg='#ffb3fe', command=lambda: display_frames())
b4.grid(row=2, column=0, padx=10, pady=20)

# Franmes 8-10
l8 = tk.Label(frame8, text=" Previous frame")
l8.grid(row=0, column=0, padx=10, pady=20)

l8 = tk.Label(frame9, text=" Current frame")
l8.grid(row=0, column=0)


l8 = tk.Label(frame10, text="Lineage")
l8.grid(row=0, column=0, padx=20)

l_centr = tk.Label(frame10, text="Centroid:")
l_centr.grid(row=2, column=0, pady=40)

l_area = tk.Label(frame10, text="Area:")
l_area.grid(row=3, column=0, padx=2)

l_perim = tk.Label(frame10, text="Peimeter:")
l_perim.grid(row=4, column=0, padx=2)

l_circ = tk.Label(frame10, text="Circularity:")
l_circ.grid(row=5, column=0, padx=2)

# Frame 13
global chosen_1, chosen_2, chosen_property
chosen_1, chosen_2, chosen_property = StringVar(), StringVar(), StringVar()
global ffrom, tto
ffrom, tto = tk.IntVar(), tk.IntVar()


def create_per_cell_dictionary():

    global per_cell_dict
    per_cell_dict = create_per_cell_info(
        pedigree, out_folders[4], still_lineage, colours)
    print("len(per_cell_dictionary=", len(per_cell_dict))
    print("per_cell_dictionary.keys()=", per_cell_dict.keys())
    options_1 = list(per_cell_dict.keys())
    drop_1 = OptionMenu(frame13, chosen_1, *options_1,
                        command=display_first_patch)
    drop_1.grid(row=1, column=0, padx=2)
    drop_1.config(fg = "blue") 
    #drop_1["menu"].config(fg="blue")
    chosen_2.set("area")
    #global canvas_7a
    #canvas_7a = Canvas(frame7, bg='black', height=382, width=382)
    #canvas_7a.grid(row=0,column=0)
    
    #global canvas_7a
    #canvas_7a = Canvas(frame7, bg='black', height=382, width=382)
    #canvas_7a.grid(row=0,column=0)
    #canvas_7a.pack(anchor='nw', fill=None, expand=True)

def slide_patch(value):  # value=frame number from patch_slider
    # chosen_1 is a cell name
    
    
    
    #frame7.grid_remove()
    #frame7a.tkraise()
    #frame7a.grid()
    #canvas_7a = Canvas(frame7a, bg='black', height=382, width=382)
    #canvas_7a.grid(row=0,column=0)
    #canvas_7.tag_lower()
    #canvas7a.tag_raise()   
        
    canvas_11.delete('all')
    canvas_5.delete('all')
    canvas_6.delete('all')    
    canvas_7a.delete('all')
    canvas_12.delete('all')
    
    # image_number=0
    print("chosen_1.get()=", chosen_1.get())
    print("value=", value)
    image_number=0
    for i in range(len(pedigree[chosen_1.get()])):
        if pedigree[chosen_1.get()][i][1] == int(value)-1:
            image_number = i+1
    print("image_number=", image_number)
    patch = per_cell_dict[chosen_1.get()][0][image_number-1]
    global im_pil
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(patch_rgb)
    im_pil = im_pil.resize((382, 382), Image.ANTIALIAS)
    im_pil = ImageTk.PhotoImage(im_pil)

    red_patch = per_cell_dict[chosen_1.get()][-1][image_number-1]
    global red_im_pil
    red_patch_rgb = cv2.cvtColor(red_patch, cv2.COLOR_BGR2RGB)
    red_im_pil = Image.fromarray(red_patch_rgb)
    red_im_pil = red_im_pil.resize((382, 382), Image.ANTIALIAS)
    red_im_pil = ImageTk.PhotoImage(red_im_pil)
    
    dictt={"area":4,"perimeter":5,"circularity":6}   
    global plott_pil   
    plott_pil=per_cell_dict[chosen_1.get()][dictt[chosen_2.get()]][image_number-1]
    """
    print("chosen_property=", prop)
    if prop=="area":
        plott_pil =per_cell_dict[chosen_1.get()][4][0]
    elif prop=="perimeter":
        plott_pil =per_cell_dict[chosen_1.get()][5][0]
    else:
        plott_pil =per_cell_dict[chosen_1.get()][6][0]
    """
    plott_pil.thumbnail((382,382), Image.ANTIALIAS)
    #plott_pil = plott_pil.resize((382, 382), Image.ANTIALIAS)
    plott_pil = ImageTk.PhotoImage(plott_pil)

    canvas_5.create_image(0, 0, anchor=NW, image=output_images[image_number-1])
    
    canvas_6.create_image(0, 0, anchor=NW, image=output_images[image_number])
    canvas_7a.create_image(0, 0, anchor=NW, image=red_im_pil)
    canvas_11.create_image(0, 0, anchor=NW, image=im_pil)
    canvas_12.create_image(0, 0, anchor=NW, image=plott_pil)
    view_slider.set(value)

    l_centr.config(text="Centroid: " +
              str(per_cell_dict[chosen_1.get()][-2][image_number-1]))
    combination=col_dict[chosen_2.get()]
    
    l_area.config(text="Area: " +
               str(per_cell_dict[chosen_1.get()][1][image_number-1]), fg=combination[0])
    l_perim.config(text="Perimeter: " +
               str(per_cell_dict[chosen_1.get()][2][image_number-1]), fg=combination[1])
    l_circ.config(text="Circularity: " +
               str(per_cell_dict[chosen_1.get()][3][image_number-1]), fg=combination[2])


def display_first_patch(value):  # value=cell name from dropdown menu
    
    #frame7.grid_remove()
    #frame7a.tkraise()
    #frame7a.grid()
        
    #frame7a = tk.Frame(master=window, width=382, height=382, bg="brown")
    #frame7a.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=W+N+S)
    
    
    #canvas_7.tag_lower()
    #canvas7a.tag_raise()   
    global canvas_7a
    canvas_7a = Canvas(frame7, bg='black', height=382, width=382)
    canvas_7a.grid(row=0,column=0)
        
    canvas_5.delete('all')
    canvas_6.delete('all')
    canvas_7a.delete('all')
    
    # chosen_1 is the same
    key = chosen_1.get()
    print("key=", key)
    # patch=pedigree[key][0][2]
    patch = per_cell_dict[chosen_1.get()][0][0]
    patch_rgb = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
    global im_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(patch_rgb)
    im_pil = im_pil.resize((382, 382), Image.ANTIALIAS)
    im_pil = ImageTk.PhotoImage(im_pil)

    red_patch = per_cell_dict[chosen_1.get()][-1][0]
    red_patch_rgb = cv2.cvtColor(red_patch, cv2.COLOR_BGR2RGB)
    global red_im_pil
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    red_im_pil = Image.fromarray(red_patch_rgb)
    red_im_pil = red_im_pil.resize((382, 382), Image.ANTIALIAS)
    red_im_pil = ImageTk.PhotoImage(red_im_pil)
    
    dictt={"area":4,"perimeter":5,"circularity":6}   
    global plott_pil   
    plott_pil=per_cell_dict[chosen_1.get()][dictt[chosen_2.get()]][0]
    """
    print("chosen_property=", prop)
    if prop=="area":
        plott_pil =per_cell_dict[chosen_1.get()][4][0]
    elif prop=="perimeter":
        plott_pil =per_cell_dict[chosen_1.get()][5][0]
    else:
        plott_pil =per_cell_dict[chosen_1.get()][6][0]
    """
    plott_pil.thumbnail((382,382), Image.ANTIALIAS)
    #plott_pil = plott_pil.resize((382, 382), Image.ANTIALIAS)
    plott_pil = ImageTk.PhotoImage(plott_pil)
    

    global ffrom, tto
    ffrom, tto = pedigree[key][0][1]+1, pedigree[key][-1][1]+1
    print("ffrom=", ffrom)
    print("tto=", tto)
    global patch_slider
    patch_slider = Scale(frame13, from_=ffrom, to=tto, orient=HORIZONTAL,
                         troughcolor="blue", command=slide_patch, length=380)
    patch_slider.grid(row=2, column=0, sticky="e")
    patch_slider.set(pedigree[key][0][1]+1)

    canvas_5.create_image(0, 0, anchor=NW, image=output_images[ffrom-1])
   
    canvas_6.create_image(0, 0, anchor=NW, image=output_images[ffrom])
    canvas_7a.create_image(0, 0, anchor=NW, image=red_im_pil)
    canvas_11.create_image(0, 0, anchor=NW, image=im_pil)
    canvas_12.create_image(0, 0, anchor=NW, image=plott_pil)

    view_slider.set(ffrom)
    global col_dict
    col_dict={"area":["red", "black", "black"],"perimeter":["black", "red", "black"],"circularity":["black", "black", "red"]}
    l_centr.config(text="Centroid: " + str(per_cell_dict[chosen_1.get()][-2][0]))
    combination=col_dict[chosen_2.get()]
    l_area.config(text="Area: " + str(per_cell_dict[chosen_1.get()][1][0]), fg=combination[0])
    l_perim.config(text="Perimeter: " + str(per_cell_dict[chosen_1.get()][2][0]), fg=combination[1])
    l_circ.config(text="Circularity: " + str(per_cell_dict[chosen_1.get()][3][0]), fg=combination[2])


b5 = tk.Button(frame13, text="6. Create per cell info",
               bg='#ffb3fe', command=lambda: create_per_cell_dictionary())
b5.grid(row=0, column=0, padx=10, pady=20)
options_2 = ["area", "perimeter", "circularity"]
drop_2 = OptionMenu(frame13, chosen_2, *options_2)

drop_2.grid(row=1, column=1, padx=2)
chosen_2.set("cell property")

global cell_numbers_chosen_5
cell_numbers_chosen_5=[]
###########3#######################   Frame 8
def get_cell_number_5(event):# gets cell ID form previous frame during editing
    global cell_numbers_chosen_5
  
    keys=list(lineage[int(view_slider.get())-2].keys())
    print("keys=", keys)
    previous_image=lineage[int(view_slider.get())-1][keys[0]][13]
    #previous_image=prev_frame    
    cell_number=int(previous_image[event.y,event.x])-1   
    cell_numbers_chosen_5.append(cell_number)
  
    global colour
    #print("colours=", colours)
    cell_name_internal="cell_"+ str(cell_number)
    print("cell_name_internal=",cell_name_internal)
    cell_name_external=lineage[int(view_slider.get())-2][cell_name_internal][11]
    print("cell_name_external=",cell_name_external)
    cell_names_external.append(cell_name_external)
    l12.config(text=str(cell_names_external))
    print("cell_names_external=", cell_names_external)
    #l12.config(text=str(cell_numbers_chosen_5))
    colour_four=colours[cell_name_external]    
    colour_three=colour_four[:-1]
    colour_three.reverse()    
    global colour
    colour="#%02x%02x%02x" % tuple(colour_three)

    canvas_5.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    print("cell_numbers_chosen_5=", cell_numbers_chosen_5)
#########################
def get_new_coords_6(event):
    
    canvas_6.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline=colour, fill=colour, width=2)
    coords_chosen_6.append([event.x, event.y])
    l11.config(text=str(coords_chosen_6))
    print("coords_chosen_6=", coords_chosen_6)
########################################
def prepare_for_editing_IDs():
    global coords_chosen_6, cell_numbers_chosen_5, cell_names_external
    coords_chosen_6, cell_numbers_chosen_5, cell_names_external=[],[], []
    l11.config(text="current centroids"+str(coords_chosen_6))
    l12.config(text="IDs"+str(cell_numbers_chosen_5))
    canvas_5.bind("<Button-1>", get_cell_number_5) 
    canvas_6.bind("<Button-1>", get_new_coords_6)
    l_finish.config(text="")
    
def stop_editing_IDs():
    canvas_5.unbind("<Button 1>")
    canvas_6.unbind("<Button 1>") 
    global start_frame, lineage
    
    start_frame=int(view_slider.get())
    print("start_frame=", start_frame)
    keys=list(lineage[start_frame-2].keys())
    print("keys=", keys)
  
   
    coords_old=lineage[start_frame-2][keys[0]][14]   
    for i in range(len(coords_chosen_6)):
        coords_old[cell_numbers_chosen_5[i]]=coords_chosen_6[i]
    global coords_1
    coords_1 =[list(coords_old[k]) for k in range(len(coords_old))]
    global prev_frame
    
    prev_frame=lineage[start_frame-1][keys[0]][13]
    """
    global text
    text=[]
    pr_frame=lineage[start_frame-2][keys[0]][13]
    
    all_cell_numbers=[]
    m=int(np.max(pr_frame))
    for i in range(1,m+1):
      if np.any(pr_frame==i):
          all_cell_numbers.append(i-1)    
    print(" all_cell_numbers",  all_cell_numbers)
    all_cell_numbers_sorted =sorted(all_cell_numbers)
    print(" all_cell_numbers_sorted",  all_cell_numbers_sorted)
    for num in all_cell_numbers_sorted:
            true_cell_name=lineage[start_frame-2]["cell_" + str(num)][11]
            text.append(true_cell_name)
    """
    l_finish.config(text="")
    print("coords_1=",  coords_1)         
    print("text=", text)
    lineage=lineage[:start_frame-1]
 
###################################################
def prepare_for_editing_division():
    global mother_number,manual_division_indicator
    mother_number=None
    manual_division_indicator="no"
    
    global coords_chosen_6, cell_numbers_chosen_5,cell_names_external
    coords_chosen_6, cell_numbers_chosen_5, cell_names_external=[],[],[]
    l11.config(text=str(coords_chosen_6))
    l12.config(text=str(cell_names_external))
    canvas_5.bind("<Button-1>", get_cell_number_5) 
    canvas_6.bind("<Button-1>", get_new_coords_6)
    l_finish.config(text="")
########################################
def stop_editing_division():
    canvas_5.unbind("<Button 1>")
    canvas_6.unbind("<Button 1>")
    global text, prev_frame
    text=[]
   
    global start_frame, lineage
    start_frame=int(view_slider.get())
    print("start_frame=", start_frame)
    
    keys=list(lineage[start_frame-2].keys())# from previous frame
    print("keys=", keys)
    prev_frame=lineage[start_frame-1][keys[0]][13]# prev_frame-1 is not a mistake!!!
    
   
    coords_old=lineage[start_frame-1][keys[0]][14]
    print("coords_old=", coords_old)
    print("coords_chosen_6=", coords_chosen_6)
    
    
    global cell_numbers_chosen_5, mother_number, manual_division_indicator
    
    manual_division_indicator="yes"
    mother_number=cell_numbers_chosen_5[0]   
    mother_name_internal="cell_"+ str(mother_number)   
    mother_name=lineage[start_frame-2][mother_name_internal][11]
    print("mother_name=", mother_name)                                  
    
    daughter_1_number=mother_number
    daughter_2_number=len(coords_old)
    
    daughter_1_name=mother_name+"0"
    daughter_2_name=mother_name+"1"
    print("daughter_1_name=", daughter_1_name)
    print("daughter_2_name=", daughter_2_name)
    
    
    
    all_cell_numbers=[]# from prev_frame, for creating daughter names
    m=int(np.max(prev_frame))
    for i in range(1,m+1):
      if np.any(prev_frame==i):
          all_cell_numbers.append(i-1)    
    print(" all_cell_numbers",  all_cell_numbers)
    all_cell_numbers_sorted =sorted(all_cell_numbers)
    print(" all_cell_numbers_sorted",  all_cell_numbers_sorted)
    for num in all_cell_numbers_sorted:
            true_cell_name=lineage[start_frame-2]["cell_" + str(num)][11]
            text.append(true_cell_name)
    text[mother_number]=daughter_1_name
    text.append(daughter_2_name)
    print("text=", text)
    
    
    #cell_numbers=[all_cell_numbers]+[daughter_2_number]
    coords_daughter_1=coords_chosen_6[0]
    coords_daughter_2=coords_chosen_6[1]

    coords_old[mother_number]=coords_daughter_1
    coords_old=np.concatenate((coords_old,np.array(coords_daughter_2).reshape((1,2)))) 
    global coords_1
    coords_1 =[list(coords_old[k]) for k in range(len(coords_old))]
    global dict_of_division
    dict_of_divisions[mother_name] = start_frame-1
    
    print("dict_of_divisions=",  dict_of_divisions)   
    print("coords_1=",  coords_1)
    lineage=lineage[:(start_frame-1)]
#######################################

#b5 = tk.Button(frame13, text="6. Create per cell info",
               #bg='#ffb3fe', command=lambda: create_per_cell_dictionary())
#b5.grid(row=0, column=0, padx=10, pady=20)
###############################################
b11 = tk.Button(frame8, text="Edit IDs",
              bg='#ffb3fe', command=lambda:prepare_for_editing_IDs())
b11.grid(row=1, column=1)


l12 = tk.Label(frame8, text="cell_IDs_chosen")
l12.grid(row=2, column=0)


l11 = tk.Label(frame8, text="coordinates chosen")
l11.grid(row=2, column=1)

b12 = tk.Button(frame8, text="Stop editing IDs",
              bg='#ffb3fe', command=lambda:stop_editing_IDs())
b12.grid(row=3, column=1, pady=20)
###############################################################

b_start_division = tk.Button(frame8, text="Edit division",
              bg='#ffb3fe', command=lambda:prepare_for_editing_division())
b_start_division.grid(row=6, column=1)

l_mother_cell = tk.Label(frame8, text="Mother")
l_mother_cell.grid(row=7, column=0)

l_daughters = tk.Label(frame8, text="Daughters")
l_daughters.grid(row=7, column=1)

b_stop_division = tk.Button(frame8, text="Stop editing division",
              bg='#ffb3fe', command=lambda:stop_editing_division())
b_stop_division.grid(row=8, column=1)

window.mainloop()
#########################################################
"""
def correct_tracking():
    k=chosen_1.get()
    global coords_1
    x5,y5=event.x,event.y
    intensity=
    color5=
    canvas_5.create_oval(x5-2, y5-2, x5+2,
                       y5+2, outline="red", fill="red", width=2)

############
def get_new_coords_6(event):
    global coords_1
    canvas_6.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    coords_1.append([event.x, event.y])
    print("new_coords=", coords_1)
###############################################
def get_cell_number_5(event):
    global cell_number
    canvas_5.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    coords_1.append([event.x, event.y])
    print("new_coords=", coords_1)
###################

def draw_circle(event):
    global coords_1
    canvas.create_oval(event.x-2, event.y-2, event.x+2,
                       event.y+2, outline="red", fill="red", width=2)
    coords_1.append([event.x, event.y])
    print("coords=", coords_1)

###################


   
##################################################
####################################################


l3=Label(frame3,text=" ")
l3.grid(row=1,column=0,padx=2)


l2=Label(frame3,text=" ")
l2.grid(row=0,column=1,padx=2)


b3a=tk.Button(frame3,text="3. Check result", bg='#ffb3fe',command=lambda: display_result())
b3a.grid(row=1, column=0,padx=10,pady=20)  

b4=tk.Button(frame3,text="4. Create Output Movie", bg='#ffb3fe',command=lambda: create_movie())
b4.grid(row=2, column=0,padx=10,pady=20)
l5=tk.Label(frame3,text=" ")
l5.grid(row=3, column=0,padx=2) 

def slide(value):
    global canvas_1 
    canvas_1.delete("all")
    image_number=int(value)
    print("image_number=", image_number)      
   # global full_name
    full_name=out_names[image_number-1]
    print("full_name=", full_name)
    #l2.config(text=full_name)
    global photo_1        
    photo_1 = Image.open(full_name)  
    photo_1 = photo_1.resize((382,382), Image.ANTIALIAS)
    photo_1 = ImageTk.PhotoImage(photo_1)
    canvas_1.create_image(0,0, anchor=NW, image=photo_1)
 
#######################################################


def display_result():
   global out_names
   out_names=[]
   source=out_folders[3]
   print("source=", source)
   for filename in sorted_aphanumeric(os.listdir(source)):
        out_name=os.path.join(source, filename)
        out_names.append(out_name)
   
   #global full_name
   full_name=out_names[0]
   
   global photo_2        
   photo_2 = Image.open(full_name)
    
   photo_2 = photo_2.resize((382,382), Image.ANTIALIAS)
   photo_2 = ImageTk.PhotoImage(photo_2)
   canvas_1.create_image(0,0, anchor=NW, image=photo_2)
   global slider
   slider=Scale(frame3,from_=1,to=len(out_names),orient=HORIZONTAL,troughcolor="blue", command=slide)
   slider.grid(row=1, column=1,sticky="e")


def create_movie():
 software_folder =os.path.dirname(my_dir) 
 os.chdir(software_folder) 
 from postprocess import create_lineage,create_per_cell_info,create_lineage_movie   
 pedigree=create_lineage(lineage,outpath)# creates and saves per cell pedigree
 create_per_cell_info(pedigree, out_folders[4])# creates folder CELL_INFO
 create_lineage_movie(pedigree,colours,template_names,outpath)
 l5.config(text="Finished!!! Find lineage_.avi video in the output folder")



#############################################
#canvas.bind("<Button-1>", get_x_and_y)
#canvas.bind("<Button-1>", draw_circle)
    
window.mainloop()
"""
