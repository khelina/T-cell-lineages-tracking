import numpy as np
import os
import PIL
from PIL import Image
from random import shuffle
from math import sqrt
###########################################################
N_frames=4
N_cells=1
coeff=382.0/100.0
################################################
def characters(x):
    return(x[-13:-9])
##################################################################################
def load_images(folder_dir): 
 raw_files_ch00=[]
 for filename in sorted(os.listdir(folder_dir),key=characters):
      if filename.endswith("ch00.tif"):
        full_name=os.path.join(folder_dir, filename)
        #print(full_name)
        raw=Image.open(full_name)
        raw2=raw.copy()
        raw_files_ch00.append(raw2) # list of raw big  100 images 
        raw.close()
 return raw_files_ch00
#######################

##################################
    
def order_clip(y): # y - list of numpy arrays
    z=np.concatenate(y, axis=1)
    d=z[np.lexsort(np.fliplr(z).T)]
    labels=[]
    for i in range(len(y)):
      a=d[:,(2*i):(2*i+2)]
      labels.append(a/100)
    return labels
##########################################
#########################
def create_valid(directory):

 subdirs = [x[1] for x in os.walk(directory)]
 folders=subdirs[0]
 VALID=[]
 for i in range(len(folders)):
     dirr=os.path.join(directory,folders[i])
     print(dirr)
     raw_files_ch00=load_images(dirr)
     n=len(raw_files_ch00)
     print("number of images in this folder=",n)
     for filename in os.listdir(dirr):
        if filename.endswith(".npz"):
            data=np.load(os.path.join(dirr,filename))          
            new_centr=data["new_centr"] 
            print("loaded centroids from",os.path.join(dirr,filename))
            print("len(new_centr)=",len(new_centr))
           
     film_0=[]
     for k in range(len(new_centr)):
            frame=raw_files_ch00[k].copy()            
            raw1 = frame.resize((100, 100), PIL.Image.LANCZOS)
            film_0.append((raw1,new_centr[k]/coeff))
     N_valid_1=len(film_0)-N_frames+1 # number of videos with a film
     for iii in range(N_valid_1):# iii = number of the 1st frame in video
       VIDEO=np.zeros((100,100,N_frames))
       LABEL0=[]
       for iiii in range(N_frames):
         frame=np.array(film_0[iii+iiii][0])
         VIDEO[:,:,iiii]=(frame-np.mean(frame))/np.std(frame)
         LABEL0.append(film_0[iii+iiii][1])    
       LABEL=order_clip(LABEL0)   
       VALID.append((VIDEO,LABEL))
     print("len(VALID)=",len(VALID))
 shuffle(VALID)
 VALID=VALID[:2048]
 N_valid=len(VALID)
 valid_samples=np.zeros((N_valid,100,100, N_frames))
 labels_1=np.zeros((N_valid,N_cells*2))
 labels_2=np.zeros((N_valid,N_cells*2))
 labels_3=np.zeros((N_valid,N_cells*2))
 labels_4=np.zeros((N_valid,N_cells*2))
 for pp in range(N_valid):
    valid_samples[pp,:,:,:]=VALID[pp][0]   
    labels_1[pp,:]=VALID[pp][1][0].reshape((N_cells*2,))
    labels_2[pp,:]=VALID[pp][1][1].reshape((N_cells*2,))
    labels_3[pp,:]=VALID[pp][1][2].reshape((N_cells*2,))
    labels_4[pp,:]=VALID[pp][1][3].reshape((N_cells*2,))
 valid_labels_mult=[labels_1,labels_2,labels_3,labels_4]
 valid_samples=valid_samples.reshape((N_valid,100,100,N_frames,1))   
 return (valid_samples,valid_labels_mult)   

###########################################
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
     cen1[ii][0]=100.0-cen[ii][0]
     cen1[ii][1]=cen[ii][1]
    film_1.append((im1,cen1))
        
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im2=im.transpose(methods[1])
    cen2=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen2[ii][0]=cen[ii][0]
     cen2[ii][1]=100.0-cen[ii][1]
    film_2.append((im2,cen2))
      
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im3=im.transpose(methods[2])
    cen3=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen3[ii][0]=cen[ii][1]
     cen3[ii][1]=100.0-cen[ii][0]
    film_3.append((im3,cen3))
      
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im4=im.transpose(methods[3])
    cen4=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen4[ii][0]=100.0-cen[ii][0]
     cen4[ii][1]=100.0-cen[ii][1]
    film_4.append((im4,cen4))
       
    im=film_0[i][0].copy()
    cen=film_0[i][1].copy()
    im5=im.transpose(methods[4])
    cen5=np.zeros((N_cells,2))
    for ii in range(N_cells):
     cen5[ii][0]=100.0-cen[ii][1]
     cen5[ii][1]=cen[ii][0]
    film_5.append((im5,cen5))   
        
 FILMS=[film_0,film_1,film_2,film_3,film_4,film_5]


 N_train_1=len(film_0)-N_frames+1 # number of videos with a film

 for p in range(6):
  for iii in range(N_train_1):# iii = number of the 1st frame in video
    VIDEO=np.zeros((100,100,N_frames))
    LABEL0=[]
    for iiii in range(N_frames):
        frame=np.array(FILMS[p][iii+iiii][0])
        VIDEO[:,:,iiii]=(frame-np.mean(frame))/np.std(frame)
        LABEL0.append(FILMS[p][iii+iiii][1])    
    LABEL=order_clip(LABEL0)   
    TRAIN.append((VIDEO,LABEL))
 return TRAIN
##########################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha
########################### loading data and creating training set ################

directory="ONE_CELL_TRAIN_SET"
subdirs = [x[1] for x in os.walk(directory)]
folders=subdirs[0]
TRAIN=[]

for i in range(len(folders)):
     dirr=os.path.join(directory,folders[i])
     print(dirr)
     raw_files_ch00=load_images(dirr)
     n=len(raw_files_ch00)
     print("number of images in this folder=",n)
     for filename in os.listdir(dirr):
        if filename.endswith(".npz"):
            data=np.load(os.path.join(dirr,filename))          
            new_centr=data["new_centr"]
          
            print("loaded centroids from",os.path.join(dirr,filename))
            print("len(new_centr)=",len(new_centr))
     film_0=[]
     for k in range(len(new_centr)):
            frame=raw_files_ch00[k].copy()            
            raw1 = frame.resize((100, 100), PIL.Image.LANCZOS)
            film_0.append((raw1,new_centr[k]/coeff))
     TRAIN=create_train(film_0,TRAIN)
     #film_1=film_0[::-1]
     print("len(TRAIN)=",len(TRAIN))
     #TRAIN=create_train(film_1,TRAIN)
     #print("created reversed clips")
     #print("len(TRAIN)=",len(TRAIN))
############################################################
shuffle(TRAIN)
TRAIN=TRAIN[:47872]
N_train=len(TRAIN)
train_samples=np.zeros((N_train,100,100, N_frames))
labels_1=np.zeros((N_train,N_cells*2))
labels_2=np.zeros((N_train,N_cells*2))
labels_3=np.zeros((N_train,N_cells*2))
labels_4=np.zeros((N_train,N_cells*2))
for pp in range(N_train):
    train_samples[pp,:,:,:]=TRAIN[pp][0]   
    labels_1[pp,:]=TRAIN[pp][1][0].reshape((N_cells*2,))
    labels_2[pp,:]=TRAIN[pp][1][1].reshape((N_cells*2,))
    labels_3[pp,:]=TRAIN[pp][1][2].reshape((N_cells*2,))
    labels_4[pp,:]=TRAIN[pp][1][3].reshape((N_cells*2,))
train_labels_mult=[labels_1,labels_2,labels_3,labels_4]
train_samples=train_samples.reshape((N_train,100,100,N_frames,1)) 


#############################################  checking equality       ##########

#########################################################
#validation_data=create_valid("ONE_CELL_VALID_SET")

directory="ONE_CELL_VALID_SET"
subdirs = [x[1] for x in os.walk(directory)]
folders=subdirs[0]
VALID=[]

for i in range(len(folders)):
     dirr=os.path.join(directory,folders[i])
     print(dirr)
     raw_files_ch00=load_images(dirr)
     n=len(raw_files_ch00)
     print("number of images in this folder=",n)
     for filename in os.listdir(dirr):
        if filename.endswith(".npz"):
            data=np.load(os.path.join(dirr,filename))          
            new_centr=data["new_centr"]
          
            print("loaded centroids from",os.path.join(dirr,filename))
            print("len(new_centr)=",len(new_centr))
     film_0=[]
     for k in range(len(new_centr)):
            frame=raw_files_ch00[k].copy()            
            raw1 = frame.resize((100, 100), PIL.Image.LANCZOS)
            film_0.append((raw1,new_centr[k]/coeff))
     VALID=create_train(film_0,VALID)
     #film_1=film_0[::-1]
     print("len(VALID)=",len(VALID))
     #TRAIN=create_train(film_1,TRAIN)
     #print("created reversed clips")
     #print("len(TRAIN)=",len(TRAIN))
############################################################
shuffle(VALID)
VALID=VALID[:47872]
N_valid=len(VALID)
valid_samples=np.zeros((N_valid,100,100, N_frames))
labels_1=np.zeros((N_valid,N_cells*2))
labels_2=np.zeros((N_valid,N_cells*2))
labels_3=np.zeros((N_valid,N_cells*2))
labels_4=np.zeros((N_valid,N_cells*2))
for pp in range(N_valid):
    valid_samples[pp,:,:,:]=VALID[pp][0]   
    labels_1[pp,:]=VALID[pp][1][0].reshape((N_cells*2,))
    labels_2[pp,:]=VALID[pp][1][1].reshape((N_cells*2,))
    labels_3[pp,:]=VALID[pp][1][2].reshape((N_cells*2,))
    labels_4[pp,:]=VALID[pp][1][3].reshape((N_cells*2,))
valid_labels_mult=[labels_1,labels_2,labels_3,labels_4]
valid_samples=valid_samples.reshape((N_valid,100,100,N_frames,1)) 

validation_data=(valid_samples,valid_labels_mult)

#########################################################################
#######################################################################

import numpy as np

from PIL import Image, ImageDraw
import keras
from keras.models import Model
from keras.layers import Input, Lambda
from keras.layers import Dense, Dropout
from keras.layers import Flatten,BatchNormalization, Activation
from keras.layers.convolutional import Conv3D
from keras.layers.pooling import MaxPooling3D
from keras.callbacks import LearningRateScheduler
from keras.optimizers import SGD, Adam
import tensorflow as tf

###################################

#########################           CREATING MODEL     ###############################################
nine_frames = Input(shape=(100,100,N_frames,1))

x = Conv3D(32, kernel_size=(3,3,3), padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(nine_frames)
x=BatchNormalization()(x)
x=Activation('relu')(x)
#x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(64, kernel_size=(3,3,3),padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)
x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(128, kernel_size=(3,3,3),padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)
x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)


x= Conv3D(256, kernel_size=(3,3,3),padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)
x = MaxPooling3D(pool_size=(2, 2, 1),strides=None, padding='valid', data_format=None)(x)

x= Conv3D(512, kernel_size=(3,3,3),padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(x)
x=BatchNormalization()(x)
x=Activation('relu')(x)
##################################

######################################
def crop(x,frame):
    return x[:,:,:,frame:(frame+1),:]
##################################
outputs=[]
for k in range(N_frames):
    b = Lambda(crop, arguments={'frame':k})(x)  
    name=Flatten()(b)
    
    name = Dense(256)(name)
    name=BatchNormalization()(name)
    name=Activation('relu')(name)
    #name=Dropout((0.3))(name)
    """
    name = Dense(4)(name)
    name=BatchNormalization()(name)
    name=Activation('relu')(name)
    #name=Dropout((0.01))(name)
    """
    name=Dense(N_cells*2,activation='linear')(name)
    outputs.append(name)

model = Model(inputs=nine_frames, outputs=outputs)


#####################################################################################################
###############################################################
NUM_EPOCHS=30
INIT_LR=0.009
callbacks = [LearningRateScheduler(poly_decay)]
    ####################################################################################################

from keras.utils import multi_gpu_model

parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(optimizer='adam', loss='mse',metrics=['mae'])

# This `fit` call will be distributed on 8 GPUs.
# Since the batch size is 256, each GPU will process 32 samples.
fashion_train=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=64, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)
   
model.save_weights('one_cell.weights.h5')
print("saved weights")
"""
model.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
model_json=model.to_json()
with open("one_cell.json","w") as json_file:
   json_file.write(model_json)
   
"""

