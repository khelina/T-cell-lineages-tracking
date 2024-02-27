
import numpy as np
import os
import PIL
from PIL import Image
from random import shuffle
import re
import pickle
###########################################################
SIZE=100.0
N_frames=4
N_cells=4
Coeff=382.0/SIZE
batch=32
print("batch size=", batch)
################################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##################################################################################
def load_images(folder_dir,p, indic): 
 file_names=[] 
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith(".tif"):
        full_name=os.path.join(folder_dir, filename)
        file_names.append(full_name)
      if filename.endswith(".npz"):         
        data=np.load(os.path.join(dirr,filename))          
        new_centr=data["new_centr"]                 
        print("loaded centroids from",os.path.join(dirr,filename))
        print("len(new_centr)=",len(new_centr))
 raw_files_ch00=[]
 if indic=="train" and (p==0 or p==1):
            number=5000
 else:
     number= len(file_names)         
 for ii in range(number):
        raw=Image.open(file_names[ii])
        raw2=raw.copy()
        raw_files_ch00.append(raw2) # list of raw big  100 images 
        raw.close()
 new_centr=new_centr[:number]      
 return raw_files_ch00, new_centr
##################################
def calculate_iou_min(y_true, y_pred):
    y_true = y_true.astype(np.float32)
    y_pred = y_pred.astype(np.float32)
    y_true=y_true*382.0# because they were normalized
    y_pred=y_pred*382.0       
    results = []    
    for i in range(0,y_true.shape[0]):
      frame_results=[]
      for k in range(N_cells):        
        a1 = y_true[i,2*k]-20.0
        a2 = y_pred[i,2*k]-20.0        
        b1=a1+40.0
        b2=a2+40.0
        if (b2<=a1 or a2>=b1):
          iw=0.0
        else:
          iw=min(b2-a1,b1-a2)       
        c1 = y_true[i,2*k+1]-20.0
        c2 = y_pred[i,2*k+1]-20.0    
        d1=c1+40.0
        d2=c2+40.0
        if (d2<=c1 or c2>=d1):
          ih=0.0
        else:
          ih=min(d1-c2,d2-c1)
        intersection=iw*ih
        union=3200.0-intersection
        iou=intersection/union 
        #iou = iou.astype(np.float32)
        frame_results.append(iou)
      results.append(min(frame_results))
    output= np.mean(results)
    output=output.astype(np.float32)                             
    return output
##################################################
def IoU_min(y_true, y_pred):    
    iou = tf.py_func(calculate_iou_min, [y_true, y_pred], tf.float32)
    return iou
############################################
def calculate_iou_av(y_true, y_pred):
    y_true = y_true.astype(np.float32)
    y_pred = y_pred.astype(np.float32)
    y_true=y_true*382.0
    y_pred=y_pred*382.0       
    results = []    
    for i in range(0,y_true.shape[0]):
      frame_results=[]
      for k in range(N_cells):        
        a1 = y_true[i,2*k]-20.0
        a2 = y_pred[i,2*k]-20.0        
        b1=a1+40.0
        b2=a2+40.0
        if (b2<=a1 or a2>=b1):
          iw=0.0
        else:
          iw=min(b2-a1,b1-a2)       
        c1 = y_true[i,2*k+1]-20.0
        c2 = y_pred[i,2*k+1]-20.0    
        d1=c1+40.0
        d2=c2+40.0
        if (d2<=c1 or c2>=d1):
          ih=0.0
        else:
          ih=min(d1-c2,d2-c1)
        intersection=iw*ih
        union=3200.0-intersection
        iou=intersection/union 
        #iou = iou.astype(np.float32)
        frame_results.append(iou)
      results.append(sum(frame_results)/len(frame_results))
    output= np.mean(results)
    output=output.astype(np.float32)                             
    return output
#################################################
def IoU_av(y_true, y_pred):    
    iou = tf.py_func(calculate_iou_av, [y_true, y_pred], tf.float32)
    return iou
##########################################
def create_train(film_0,TRAIN): 
 methods=[Image.FLIP_LEFT_RIGHT,Image.FLIP_TOP_BOTTOM,Image.ROTATE_90,Image.ROTATE_180,Image.ROTATE_270]
 film_1=[]
 film_2=[]
 film_3=[]
 film_4=[]
 film_5=[]
 for i in range(len(film_0)):
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im1=im.transpose(methods[0])
    cen1=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen1[ii][0]=SIZE-cen[ii][0]
     cen1[ii][1]=cen[ii][1]
    film_1.append((im1,cen1))
        
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im2=im.transpose(methods[1])
    cen2=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen2[ii][0]=cen[ii][0]
     cen2[ii][1]=SIZE-cen[ii][1]
    film_2.append((im2,cen2))
      
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im3=im.transpose(methods[2])
    cen3=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen3[ii][0]=cen[ii][1]
     cen3[ii][1]=SIZE-cen[ii][0]
    film_3.append((im3,cen3))
      
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im4=im.transpose(methods[3])
    cen4=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen4[ii][0]=SIZE-cen[ii][0]
     cen4[ii][1]=SIZE-cen[ii][1]
    film_4.append((im4,cen4))
       
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im5=im.transpose(methods[4])
    cen5=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen5[ii][0]=SIZE-cen[ii][1]
     cen5[ii][1]=cen[ii][0]
    film_5.append((im5,cen5))           
 FILMS=[film_0,film_1,film_2,film_3,film_4,film_5]
 N_train_1=len(film_0)-N_frames # number of videos within a film
 for p in range(6):
  for iii in range(N_train_1):# iii = number of the 1st frame in video
    VIDEO=np.zeros((int(SIZE),int(SIZE),N_frames+1))
    LABEL0=[]
    for iiii in range(N_frames+1):
        frame=np.array(FILMS[p][iii+iiii][0])            
        VIDEO[:,:,iiii]=(frame-np.mean(frame))/np.std(frame)
        LABEL0.append(FILMS[p][iii+iiii][1]/SIZE)         
    TRAIN.append((VIDEO,LABEL0))
 return TRAIN
###########################################
def create_valid(film_0,VALID):          
  N_valid=len(film_0)-N_frames # number of videos with a film
  for iii in range(N_valid):# iii = number of the 1st frame in video
    VIDEO=np.zeros((int(SIZE),int(SIZE),N_frames+1))
    LABEL0=[]
    for iiii in range(N_frames+1):
        frame=np.array(film_0[iii+iiii][0])   
        VIDEO[:,:,iiii]=(frame-np.mean(frame))/np.std(frame)
        LABEL0.append(film_0[iii+iiii][1]/SIZE)    
    #LABEL=order_clip(LABEL0)   
    VALID.append((VIDEO,LABEL0))
  return VALID
##########################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha
########################### loading data and creating training set ################
############################################################
TRAIN=[]
folders=["FOUR_TRAIN_STEP_40/FOUR_TRAIN_STEP_40_1",
         "FOUR_TRAIN_STEP_40/FOUR_TRAIN_STEP_HIST_CLOSE",
         "FOUR_TRAIN_STEP_40/FOUR_TRAIN_REAL_0602",
         "FOUR_TRAIN_STEP_40/FOUR_CELLS_Pos0702f",
         "FOUR_TRAIN_STEP_40/FOUR_CELLS_Pos0202f"]
for i in range(len(folders)):     
     dirr=folders[i]
     print(dirr)
     raw_files_ch00,new_centr=load_images(dirr,i,"train")
     n=len(raw_files_ch00)
     print("images=",len(raw_files_ch00))
     print("centroids=", len(new_centr))       
     for k in range(0,n,5):
            film_0=[]
            for ii in range(5):
                frame=raw_files_ch00[k+ii].copy()
                raw1 = frame.resize((int(SIZE), int(SIZE)), PIL.Image.LANCZOS)
                
                film_0.append((raw1,new_centr[k+ii]/Coeff))           
            TRAIN=create_train(film_0,TRAIN)
     print("len(TRAIN) after this folder", len(TRAIN))
print(" final len(TRAIN)=",len(TRAIN))
#######################################
directory="FOUR_TRAIN_STEP_40"
##################################################################
shuffle(TRAIN)
a=(len(TRAIN)//batch)*batch
TRAIN=TRAIN[:a]
N_train=len(TRAIN)
train_samples=np.zeros((N_train,int(SIZE),int(SIZE), N_frames+1))
#labels_1=np.zeros((N_train,N_cells*2))
labels_2=np.zeros((N_train,N_cells*2))
labels_3=np.zeros((N_train,N_cells*2))
labels_4=np.zeros((N_train,N_cells*2))
labels_5=np.zeros((N_train,N_cells*2))
for pp in range(N_train):
    train_samples[pp,:,:,:]=TRAIN[pp][0]   
    #labels_1[pp,:]=TRAIN[pp][1][0].reshape((N_cells*2,))
    labels_2[pp,:]=TRAIN[pp][1][1].reshape((N_cells*2,))
    labels_3[pp,:]=TRAIN[pp][1][2].reshape((N_cells*2,))
    labels_4[pp,:]=TRAIN[pp][1][3].reshape((N_cells*2,))
    labels_5[pp,:]=TRAIN[pp][1][4].reshape((N_cells*2,))
train_labels_mult=[labels_2,labels_3,labels_4,labels_5]
train_samples=train_samples.reshape((N_train,int(SIZE),int(SIZE),N_frames+1,1)) 
#############################################  creating validatio data      ##########
directory="FOUR_VALID"
subdirs = [x[1] for x in os.walk(directory)]
folders=subdirs[0]
VALID=[]
for i in range(len(folders)):     
     dirr=os.path.join (directory,folders[i])
     print(dirr)
     raw_files_ch00,new_centr=load_images(dirr,i,"valid")
     n=len(raw_files_ch00)
     print("images=",len(raw_files_ch00))
     print("centroids=", len(new_centr))       
     for k in range(0,n,5):
            film_0=[]
            for ii in range(5):
                frame=raw_files_ch00[k+ii].copy()
                raw1 = frame.resize((int(SIZE), int(SIZE)), PIL.Image.LANCZOS)
                
                film_0.append((raw1,new_centr[k+ii]/Coeff))           
            VALID=create_valid(film_0,VALID)
print("final len(VALID)=",len(VALID))
############################################################
#############################################  creating validatio data      ##########

############################################################
shuffle(VALID)
a=(len(VALID)//batch)*batch
VALID=VALID[:a]
N_valid=len(VALID)
valid_samples=np.zeros((N_valid,int(SIZE),int(SIZE), N_frames+1))
#labels_1=np.zeros((N_valid,N_cells*2))
labels_2=np.zeros((N_valid,N_cells*2))
labels_3=np.zeros((N_valid,N_cells*2))
labels_4=np.zeros((N_valid,N_cells*2))
labels_5=np.zeros((N_valid,N_cells*2))
for pp in range(N_valid):
    valid_samples[pp,:,:,:]=VALID[pp][0]   
    #labels_1[pp,:]=VALID[pp][1][0].reshape((N_cells*2,))
    labels_2[pp,:]=VALID[pp][1][1].reshape((N_cells*2,))
    labels_3[pp,:]=VALID[pp][1][2].reshape((N_cells*2,))
    labels_4[pp,:]=VALID[pp][1][3].reshape((N_cells*2,))
    labels_5[pp,:]=VALID[pp][1][4].reshape((N_cells*2,))
valid_labels_mult=[labels_2,labels_3,labels_4,labels_5]
valid_samples=valid_samples.reshape((N_valid,int(SIZE),int(SIZE),N_frames+1,1)) 
validation_data=(valid_samples,valid_labels_mult)
#########################################################

print("validation_data.shape",validation_data[0].shape)

#######################################################################

import numpy as np


#import keras
from keras.models import Model
from keras.layers import Input, Lambda
from keras.layers import Dense, Dropout
from keras.layers import Flatten,BatchNormalization, Activation
from keras.layers.convolutional import Conv3D
from keras.layers.pooling import MaxPooling3D
from keras.callbacks import LearningRateScheduler
from keras.optimizers import  Adam
import tensorflow as tf
from keras.layers import LeakyReLU


#########################           CREATING MODEL     ###############################################
input_clip = Input(shape=(int(SIZE),int(SIZE),N_frames+1,1))

x = Conv3D(32, kernel_size=(3,3,3), padding='same', kernel_initializer='he_normal', bias_initializer='ones')(input_clip)
x=BatchNormalization()(x)
x=Activation('relu')(x)
#x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(64, kernel_size=(3,3,3),padding='same', kernel_initializer='he_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)
x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(128, kernel_size=(3,3,3),padding='same', kernel_initializer='he_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)


x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(256, kernel_size=(3,3,3),padding='same', kernel_initializer='he_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)


x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)

x= Conv3D(512, kernel_size=(3,3,3),padding='same', kernel_initializer='he_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)



######################################
def crop(x,frame):
    return x[:,:,:,frame:(frame+1),:]
##################################
outputs=[]

for k in range(1,N_frames+1):
    b = Lambda(crop, arguments={'frame':k})(x)  
    name=Flatten()(b)
    
    name = Dense(1024,kernel_initializer='he_normal', bias_initializer='ones')(name)
    name=BatchNormalization()(name)
    #name = LeakyReLU(alpha=0.2)(name)
    name=Activation('relu')(name)
    name=Dropout((0.03))(name)
    
    name = Dense(512)(name)
    name=BatchNormalization()(name)
    #name = LeakyReLU(alpha=0.2)(name)
    name=Activation('relu')(name)
    #name=Dropout((0.01))(name)
    
    name=Dense(N_cells*2,activation='linear')(name)
    outputs.append(name)
    
model = Model(inputs=input_clip, outputs=outputs)

model.summary()
#########################################################################
#from keras.utils import plot_model
#plot_model(model, to_file='model.png')
#####################################################################################################

NUM_EPOCHS=150
INIT_LR=0.01
callbacks = [LearningRateScheduler(poly_decay)]
    ####################################################################################################

from keras.utils import multi_gpu_model

parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(optimizer='adam', loss='mse',metrics=[IoU_av, IoU_min])

# This `fit` call will be distributed on 8 GPUs.
# Since the batch size is 256, each GPU will process 32 samples.
history=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)

history_file='TRACKER-4-history.pickle'

with open(history_file, 'wb') as file_pi:
        pickle.dump(history.history, file_pi)
print("saved history in file",history_file)

