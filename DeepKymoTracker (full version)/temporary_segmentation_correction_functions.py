##########################################
def click_one_cell_fast_mode(event):
    global frame_number, frame_indicator, cell_indicator,internal_frame_number
    frame_number=view_slider_p5.get()
       
    if frame_number!=frame_indicator:# if you are in a new frame
       if frame_indicator!=-2:
           print("entered new frame")
           #cell_indicator=-2
           save_edits_for_frame()          
       else:
          print("have not started editing yet")
       
       cell_indicator=-2# if you are in a new frame and did not start clicking yet
       frame_indicator=frame_number
       internal_frame_number=frame_number-first_frame_number_p5
       get_frame_info_fast_mode(internal_frame_number)
    else:# if it is still the same frame
         print("in the same frame")
    ##################################################
    global clicked_cell_positon_marker, cell_number
    clicked_cell_positon_marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
    
    #print("internal_frame_number=", internal_frame_number)
    mask=masks[internal_frame_number]
    cell_number=mask[clicked_cell_positon_marker[1],clicked_cell_positon_marker[0]]-1
    
    #print("cell_number=", cell_number)
    #print("cell_indicator=", cell_indicator)
    if cell_number>=0:# in case you accidentally hit background (instead of cell)
                 if cell_number!=cell_indicator:# you clicked on a new cell
                     print("clicked on new cell")
                     global oval, cell_color, cell_ID
                     canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
                     cell_color=cells_in_current_frame_sorted[cell_number][1]
                     cell_ID=cells_in_current_frame_sorted[cell_number][0]
                     ########################################
                     global init_x,init_y# create magenta oval on clicked cell
                     init_x,init_y=event.x,event.y
                     oval=canvas_fluor_p5.create_oval(init_x-5, init_y-5, init_x+5,
                          init_y+5, outline="magenta", width=1)
                 else:# you clicked on the same cell
                     print("clicked on  same cell")
                 cell_indicator=cell_number
    else:
         print("clicked on  background")
################################################################
def save_hand_drawing_for_one_cell():
    button_activate_hand_drawing_mode_for_one_cell.configure(background = button_color)
    update_flash([view_slider_p5])
    button_activate_slow_edit_mode.configure(background = button_color) 
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, points    
    ctr = np.array(points).reshape((-1,1,2)).astype(np.int32)# turn drawn points into contour (ctr)
    final_mask[final_mask==hand_cell_number+1]=0
    cv2.drawContours(mask_hand,[ctr],0,(255,255,255),-1)
    final_mask[mask_hand==255]=hand_cell_number+1
    ######### need to get segmented_frame and segmented_patch here to pass to modified_cell_IDs                     
    segmented_frame= np.zeros((frame_p5_size+2*Bordersize,frame_p5_size+2*Bordersize),dtype="uint8")
    cv2.drawContours(segmented_frame,[ctr] , 0, 255, -1)
    im2, contours, hierarchy = cv2.findContours(segmented_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cell_contour=contours[0]                                
    M = cv2.moments(cell_contour) 
    if M["m00"]==0.:
          M["m00"]=0.001
    new_cX = np.round(M["m10"] / M["m00"],2)
    new_cY = np.round(M["m01"] / M["m00"],2)
    new_base=cv2.copyMakeBorder(segmented_frame , top=Bordersize, bottom=Bordersize, left=Bordersize, right=Bordersize, borderType= cv2.BORDER_CONSTANT, value=0. )
    a_new,b_new,c_new,d_new=int(round(new_cX))+Bordersize-patch_size_p5,int(round(new_cX))+Bordersize+ patch_size_p5,int(round(new_cY))+Bordersize-patch_size_p5,int(round(new_cY))+Bordersize+patch_size_p5           
    segmented_patch = new_base[c_new:d_new, a_new:b_new]
    #modified_cell_IDs[hand_cell_number]=[segmented_frame, final_mask, segmented_patch]
    modified_cell_IDs[hand_cell_number]=[segmented_frame, final_mask, segmented_patch,[new_cX, new_cY], colour_four_channel, cell_ID]      
    #########################################
    global oval
    canvas_fluor_p5.delete(oval)
    cv2.drawContours(filled_fluor,[ctr] , 0, colour_four_channel, 1)
    cv2.drawContours(filled_bright,[ctr] , 0, colour_four_channel, 1)
    cv2.drawContours(filled_red,[ctr] , 0, colour_four_channel, 1)
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)
    oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)      
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask_after_3.tif", final_mask*10)  
    cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\mask_hand.tif", mask_hand)
   
    points=[]
      
    
    dialog_label_5.config(text="If you want to hand draw  another cell, push Button 4 once again.\n If you are finished with the current frame, press Button 6."
                          "\nIf you are finished with the whole movie, press Button 7.")
################################################################
def get_one_cell_ID(event): # for hand drawing   
  global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5, cell_ID, oval  
  global hand_cell_number,hand_cell_color, filled_fluor, filled_bright, colour_four_channel, filled_red         
  hand_cell_number=final_mask[int(event.y/window_p5_size*frame_p5_size),int(event.x/window_p5_size*frame_p5_size)]-1
  print(" hand_cell_number=", hand_cell_number)
  if hand_cell_number>=0:# hand_cell_number=0 if you accidentally hit background instead of cell body
   #if hand_cell_number not in modified_cell_IDs:
        #modified_cell_IDs.append(hand_cell_number)
   final_mask[final_mask==hand_cell_number+1]=0# erase clicked cell from mask
    
   cell_ID=cells_in_current_frame_sorted[hand_cell_number][0]
   colour_four_channel=cells_in_current_frame_sorted[hand_cell_number][1]    
   colour_three_channel=colour_four_channel[:-1]
   colour_three_channel.reverse()    
  
   hand_cell_color="#%02x%02x%02x" % tuple(colour_three_channel)
   
   
   filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,colour_four_channel)
   filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,colour_four_channel)
   filled_red=delete_contour_with_specific_colour(filled_red, empty_red,colour_four_channel) 
   # display frames with erased cell    
   canvas_bright,canvas_fluor,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)
   canvas_fluor_p5.delete(oval)      
   global init_x,init_y# create magenta oval on clicked cell
   init_x,init_y=event.x,event.y
   oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)
   cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\filled_fluor_after_click.tif", filled_fluor)
   dialog_label_5.config(text="To be able to start hand drawing, push Button 4a.")
##########################################
def activate_slow_edit_mode_final():   
    button_activate_slow_edit_mode.configure(background = 'red')
    button_activate_fast_edit_mode.configure(background = button_color)
    dialog_label_5.config(text="Right-click on the cell you want to correct. Its contours should disappear.")
    update_flash([button_activate_hand_drawing_mode_for_one_cell])
    ########################## delete contour of the clicked ce;;
   
                     ###############################
    #if cell_indicator!=-2:                     
                           #save_hand_drawing_for_one_cell_slow()
    #########################################
    global oval, cell_color, cell_ID
    canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
    cell_color=cells_in_current_frame_sorted[cell_number][1]
    cell_ID=cells_in_current_frame_sorted[cell_number][0]
    ########################################
    final_mask[final_mask==cell_number+1]=0# erase clicked cell from mask
    global photo_fluor, photo_bright, canvas_bright_p5  
    global  filled_fluor, filled_bright, colour_four_channel, filled_red         
    filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
    filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
    filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color) 
    # display frames with erased cell    
    canvas_bright,canvas_fluor,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)
          
    global init_x,init_y# create magenta oval on clicked cell
    #init_x,init_y=event.x,event.y
    oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)    
    dialog_label_5.config(text="To be able to start hand drawing, push Button 4a.")   
    ###########################################

    activate_hand_drawing_mode_for_one_cell()
    #canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")
    
    #canvas_fluor_p5.bind("<Button-1>",  activate_hand_drawing_mode_for_one_cell) 
    
    canvas_fluor_p5.bind("<Button-3>", erase_line_slow) 
##################################################
def activate_slow_edit_mode():   
    button_activate_slow_edit_mode.configure(background = 'red')
    button_activate_fast_edit_mode.configure(background = button_color)
    dialog_label_5.config(text="Right-click on the cell you want to correct. Its contours should disappear.")
    update_flash([button_activate_hand_drawing_mode_for_one_cell])
    
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")
    
    canvas_fluor_p5.bind("<Button-3>", click_one_cell_slow_mode) 
######################################
def extract_cell_ID_and_marker_by_right_click(event):# for fast mode
    # extract info about clicked cell (from mask)
    global clicked_cell_positon_marker, cell_number,cell_color, mask, cell_ID, cell_name, oval
    clicked_cell_positon_marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
    cell_number=mask[clicked_cell_positon_marker[1],clicked_cell_positon_marker[0]]-1
    print("cell_number=", cell_number)
   
    if cell_number>=0:# in case you accidentally hit background (instead of cell)
      canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
      cell_color=cells_in_current_frame_sorted[cell_number][1]
      cell_ID=cells_in_current_frame_sorted[cell_number][0]
      ########################################
   
      global init_x,init_y# create magenta oval on clicked cell
      init_x,init_y=event.x,event.y
      oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)
      ########################################
      dialog_label_5.config(text="Chosen cell ID="+str(cell_ID)+"\nmarker=" +str(clicked_cell_positon_marker))
      
      print("clicked_cell_positon_marker=", clicked_cell_positon_marker)
      dialog_label_5.config(text="Start left-clicking on the cell itself and on the surrouning background to see how segmentation changes."
                          "\nOnce you are happy wiht the result, repeat the process all over again with another cell, or if you are finished, click Button 6."
                          "\nYou can  undo by clicking Button 2 and then starting editing the frame all over again. Warning: you cannot undo edits after pushing Button 6 !")
###################
######################################
def extract_cell_ID_and_marker_by_right_click(event):# for fast mode
    # extract info about clicked cell (from mask)
    global clicked_cell_positon_marker, cell_number,cell_color, mask, cell_ID, cell_name, oval
    clicked_cell_positon_marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
    cell_number=mask[clicked_cell_positon_marker[1],clicked_cell_positon_marker[0]]-1
    print("cell_number=", cell_number)
   
    if cell_number>=0:# in case you accidentally hit background (instead of cell)
      canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
      cell_color=cells_in_current_frame_sorted[cell_number][1]
      cell_ID=cells_in_current_frame_sorted[cell_number][0]
      ########################################
   
      global init_x,init_y# create magenta oval on clicked cell
      init_x,init_y=event.x,event.y
      oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)
      ########################################
      dialog_label_5.config(text="Chosen cell ID="+str(cell_ID)+"\nmarker=" +str(clicked_cell_positon_marker))
      
      print("clicked_cell_positon_marker=", clicked_cell_positon_marker)
      dialog_label_5.config(text="Start left-clicking on the cell itself and on the surrouning background to see how segmentation changes."
                          "\nOnce you are happy wiht the result, repeat the process all over again with another cell, or if you are finished, click Button 6."
                          "\nYou can  undo by clicking Button 2 and then starting editing the frame all over again. Warning: you cannot undo edits after pushing Button 6 !")
###################
##########################################      
def erase_line(event):# in case you are not happy with your hand contour and want to delete it
    global cell_contour_fl, cell_contour_br, points,mask_hand, final_mask
    for i in range(len(cell_contour_fl)):        
         canvas_fluor_p5.delete(cell_contour_fl[i])
         canvas_bright_p5.delete(cell_contour_br[i])
    points=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
    final_mask[final_mask==cell_number+1]=0
    ######################
    #if hand_cell_number  in modified_cell_IDs:
       #del  modified_cell_IDs [hand_cell_number ]
       #modified_cell_IDs.remove(hand_cell_number)
    ##################################
    cell_contour_fl=[]
    cell_contour_br=[]
##########################################################
############ This is the 3rd type of segmentation correction:
############ manual drawing with mouse.Needs saving after each cell
   
###########################################################
def click_one_cell_slow_mode(event):
    global frame_number, frame_indicator, cell_indicator,internal_frame_number
    frame_number=view_slider_p5.get()
       
    if frame_number!=frame_indicator:# if you are in a new frame
       if frame_indicator!=-2:
           print("entered new frame")
           #cell_indicator=-2
           save_edits_for_frame()          
       else:
          print("have not started editing yet")
       cell_indicator=-2
       frame_indicator=frame_number
       internal_frame_number=frame_number-first_frame_number_p5
       get_frame_info_slow_mode(internal_frame_number)
    else:# if it is still the same frame
         print("in the same frame")
    ##################################################
    global clicked_cell_positon_marker, cell_number
    clicked_cell_positon_marker=[int(round(event.x/window_p5_size*frame_p5_size)),int(round(event.y/window_p5_size*frame_p5_size))]
    
    #print("internal_frame_number=", internal_frame_number)
    mask=masks[internal_frame_number]
    cell_number=mask[clicked_cell_positon_marker[1],clicked_cell_positon_marker[0]]-1
    if cell_number==-1:
        erase_line_slow()
    #print("cell_number=", cell_number)
    #print("cell_indicator=", cell_indicator)
    if cell_number>=0:# in case you accidentally hit background (instead of cell)
                 if cell_number!=cell_indicator:# you clicked on a new cell
                     print("clicked on new cell")
                     ###############################
                     if cell_indicator!=-2:                     
                           save_hand_drawing_for_one_cell_slow()
                     #########################################
                     global oval, cell_color, cell_ID
                     canvas_fluor_p5.delete(oval)# delete magenta oval on previous cell
                     cell_color=cells_in_current_frame_sorted[cell_number][1]
                     cell_ID=cells_in_current_frame_sorted[cell_number][0]
                     ########################################
                     final_mask[final_mask==cell_number+1]=0# erase clicked cell from mask
                     global photo_fluor, photo_bright, canvas_bright_p5  
                     global  filled_fluor, filled_bright, colour_four_channel, filled_red         
                     filled_fluor=delete_contour_with_specific_colour(filled_fluor, empty_fluor,cell_color)
                     filled_bright=delete_contour_with_specific_colour(filled_bright, empty_bright,cell_color)
                     filled_red=delete_contour_with_specific_colour(filled_red, empty_red,cell_color) 
                     # display frames with erased cell    
                     canvas_bright,canvas_fluor,photo_fluor, photo_bright=display_both_channels(filled_fluor,filled_bright,canvas_fluor_p5,canvas_bright_p5,window_p5_size)
                     canvas_fluor_p5.delete(oval)      
                     global init_x,init_y# create magenta oval on clicked cell
                     init_x,init_y=event.x,event.y
                     oval=canvas_fluor_p5.create_oval(init_x-3, init_y-3, init_x+3,
                       init_y+3, outline="magenta", fill="magenta", width=2)
                     cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\filled_fluor_after_click.tif", filled_fluor)
                     dialog_label_5.config(text="To be able to start hand drawing, push Button 4a.")   
                     ###########################################
                     activate_hand_drawing_mode_for_one_cell()
                     ##############################################
                    
                 else:# you clicked on the same cell
                     print("clicked on  same cell")
                 cell_indicator=cell_number
    else:
         print("I hit background")

############# This is the 2nd type of segmentation correction:
def get_frame_info():# for manual segmentation correction
    button_frame_info.configure(background = 'red')
    
    global segmentor, refiner
    if segmentor==None and refiner==None:      
        software_folder = os.getcwd() 
        segmentor, refiner= load_models_p5(software_folder)
        dialog_label_5.config(text="Loaded models")
    global frame_number, internal_frame_number
    frame_number=view_slider_p5.get()
    print("frame_number=", frame_number)
    internal_frame_number=frame_number-first_frame_number_p5
    print("internal_frame_number=", internal_frame_number)
    global frame_dictionary
    frame_dictionary=lineage_per_frame_p5[internal_frame_number]
    keys=list(frame_dictionary.keys())
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
    mask=masks[internal_frame_number]
    empty_fluor=empty_fluors[internal_frame_number]
    empty_bright=empty_brights[internal_frame_number]
    empty_red=empty_reds[internal_frame_number]
    global filled_fluor_init, filled_bright_init,filled_red_init 
    filled_fluor_init=filled_fluors[internal_frame_number]
    filled_bright_init=filled_brights[internal_frame_number]
    filled_red_init=filled_reds[internal_frame_number]     
    #######################################
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_init,filled_bright_init,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
    #########################################    
    global path_filled_bright, path_filled_fluor,path_filled_red,path_mask
    path_filled_bright, path_filled_fluor,path_filled_red,path_mask= path_filled_brights[internal_frame_number],path_filled_fluors[internal_frame_number],path_filled_reds[internal_frame_number],path_masks[internal_frame_number]
    global final_mask, filled_fluor,filled_bright, filled_red
    final_mask, filled_fluor, filled_bright, filled_red = copy.deepcopy(mask),copy.deepcopy(filled_fluor_init), copy.deepcopy(filled_bright_init),copy.deepcopy(filled_red_init)    
    update_flash([])  
    button_frame_info.configure(background = "red")
    global oval# create invisible magenta oval
    oval= canvas_fluor_p5.create_oval(5-3, 5-3, 5+3,
                       5+3, outline="magenta", fill="magenta", width=2)
    canvas_fluor_p5.itemconfig(1, state='hidden')
##########################################################
############################################
def get_frame_info_slow_mode(internal_frame_number):# for manual segmentation correction
    button_frame_info.configure(background = 'red')
    
    global segmentor, refiner
    if segmentor==None and refiner==None:      
        software_folder = os.getcwd() 
        segmentor, refiner= load_models_p5(software_folder)
        dialog_label_5.config(text="Loaded models")
    #global internal_frame_number
    #frame_number=view_slider_p5.get()
    print("frame_number inside get_frame_info=", frame_number)
    #internal_frame_number=frame_number-first_frame_number_p5
    print("internal_frame_number=", internal_frame_number)
    global frame_dictionary
    frame_dictionary=lineage_per_frame_p5[internal_frame_number]
    keys=list(frame_dictionary.keys())
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
    mask=masks[internal_frame_number]
    empty_fluor=empty_fluors[internal_frame_number]
    empty_bright=empty_brights[internal_frame_number]
    empty_red=empty_reds[internal_frame_number]
    global filled_fluor_init, filled_bright_init,filled_red_init 
    filled_fluor_init=filled_fluors[internal_frame_number]
    filled_bright_init=filled_brights[internal_frame_number]
    filled_red_init=filled_reds[internal_frame_number]     
    #######################################
    global photo_fluor, photo_bright, canvas_bright_p5,canvas_fluor_p5
    canvas_fluor_p5.unbind_all("<Button-1>")
    canvas_fluor_p5.unbind_all("<Button-3>")     
    canvas_bright_p5,canvas_fluor_p5,photo_fluor, photo_bright=display_both_channels(filled_fluor_init,filled_bright_init,canvas_fluor_p5,canvas_bright_p5,window_p5_size)      
    #########################################    
    global path_filled_bright, path_filled_fluor,path_filled_red,path_mask
    path_filled_bright, path_filled_fluor,path_filled_red,path_mask= path_filled_brights[internal_frame_number],path_filled_fluors[internal_frame_number],path_filled_reds[internal_frame_number],path_masks[internal_frame_number]
    global final_mask, filled_fluor,filled_bright, filled_red
    final_mask, filled_fluor, filled_bright, filled_red = copy.deepcopy(mask),copy.deepcopy(filled_fluor_init), copy.deepcopy(filled_bright_init),copy.deepcopy(filled_red_init)    
    update_flash([])  
    button_frame_info.configure(background = "red")
    global oval# create invisible magenta oval
    oval= canvas_fluor_p5.create_oval(5-3, 5-3, 5+3,
                       5+3, outline="magenta", fill="magenta", width=2)
    #canvas_fluor_p5.itemconfig(1, state='hidden')
##################################################
    
###############################################
def activate_fast_edit_mode():#enter fast segmentation mode
   button_activate_fast_edit_mode.configure(background = 'red')
   button_activate_slow_edit_mode.configure(background = button_color)   
   dialog_label_5.config(text="\nIn the right image, right-click on the cell you want to correct.")
   
   canvas_fluor_p5.unbind_all("<Button-1>")
   canvas_fluor_p5.unbind_all("<Button-1>")   
   canvas_fluor_p5.bind("<Button-1>", edit_by_clicking)
   
   canvas_fluor_p5.unbind_all("<Button-3>")
   ######## for click_one_cell()
   #canvas_fluor_p5.bind("<Button-3>", extract_cell_ID_and_marker_by_right_click)  
   canvas_fluor_p5.bind("<Button-3>", click_one_cell_fast_mode)
  
  


########################
def activate_hand_drawing_mode_for_one_cell():
    button_activate_hand_drawing_mode_for_one_cell.configure(background = 'red')
    update_flash([button_save_hand_drawing_for_one_cell])
    dialog_label_5.config(text="Draw the contour of the cell with the left mouse. Warning:  Be careful not to draw on neughbouring close cells!\n If you want to undo right-click the mouse anywhere in the image.\nOnce you are finished, push Button 4b.")
    
    canvas_fluor_p5.unbind_all("<Button-1>")
    #canvas_fluor_p5.unbind_all("<Button-3>")
    
    canvas_fluor_p5.bind("<Button-1>", get_x_and_y)    
    canvas_fluor_p5.bind("<B1-Motion>",draw_with_mouse, add="+")
    
    #canvas_fluor_p5.bind("<Button-3>",erase_line)
    #canvas_fluor_p5.bind("<Button-3>",erase_line, add="+")
    global cell_contour_fl, cell_contour_br,points, mask_hand# for the clicked cell
    cell_contour_fl=[]
    cell_contour_br=[]
    points=[]
    mask_hand=np.zeros((frame_p5_size,frame_p5_size),np.uint8)
   

####################################################
##################################
#########################################################
############# Splitting mergeed cells . Need to save the edits after you finish.
"""        
#############################################
def get_cell_IDs(event):# gets cell ID from  frame during Type 2 editing         
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
"""         