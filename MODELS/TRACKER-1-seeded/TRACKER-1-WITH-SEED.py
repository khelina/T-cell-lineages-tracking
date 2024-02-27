import numpy as np
import os
import PIL
from PIL import Image
from random import shuffle
from math import sqrt
import re
import pickle
import numpy as np

from PIL import Image, ImageDraw
import keras
from keras.models import Model
from keras.layers import Input, Lambda, Concatenate
from keras.layers import Dense, Dropout
from keras.layers import Flatten,BatchNormalization, Activation
from keras.layers.convolutional import Conv3D
from keras.layers.pooling import MaxPooling3D
from keras.callbacks import LearningRateScheduler
from keras.optimizers import SGD, Adam
import tensorflow as tf

###########################################################
SIZE=100.0
N_frames=4
N_cells=1
coeff=382.0/SIZE
batch=16
print("batch size=", batch)
################################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
##################################################################################
def load_images(folder_dir): 
 raw_files_ch00=[]
 for filename in sorted_aphanumeric(os.listdir(folder_dir)):
      if filename.endswith(".tif"):
        full_name=os.path.join(folder_dir, filename)
        #print(full_name)
        raw=Image.open(full_name)
        raw2=raw.copy()
        raw_files_ch00.append(raw2) # list of raw big  100 images 
        raw.close()
 return raw_files_ch00
##################################
def IoU(y_true, y_pred):
    #y_true = y_true.astype(np.float32)
    #y_pred = y_pred.astype(np.float32)
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
          iw=tf.minimum(b2-a1,b1-a2)       
        c1 = y_true[i,2*k+1]-20.0
        c2 = y_pred[i,2*k+1]-20.0    
        d1=c1+40.0
        d2=c2+40.0
        if (d2<=c1 or c2>=d1):
          ih=0.0
        else:
          ih=tf.minimum(d1-c2,d2-c1)
        intersection=iw*ih
        union=3200.0-intersection
        iou=intersection/union 
        #iou = iou.astype(np.float32)
        frame_results.append(iou)
      results.append(sum(frame_results)/len(frame_results))
    output= tf.reduce_mean(results)
    #output=output.astype(np.float32)                             
    return output
#################################################
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
def create_valid(clip,VALID):          
    VIDEO=np.zeros((100,100,N_frames+1))
    LABEL0=[]
    for iii in range(5):
        frame=np.array(clip[iii][0])
        VIDEO[:,:,iii]=(frame-np.mean(frame))/np.std(frame)
        LABEL0.append(clip[iii][1]/SIZE)    
    #LABEL=order_clip(LABEL0)   
    VALID.append((VIDEO,LABEL0))
    return VALID
##################################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha
########################### loading data and creating training set ################
############################################################
directory="ONE_CELL_SEEDS_TRAIN"
subdirs = [x[1] for x in os.walk(directory)]
print("found  train folders", subdirs)
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
     for k in range(0,n,5):
            film_0=[]
            for ii in range(5):
                frame=raw_files_ch00[k+ii].copy()            
                raw1 = frame.resize((int(SIZE), int(SIZE)), PIL.Image.LANCZOS)
                film_0.append((raw1,new_centr[k+ii]/coeff))
            TRAIN=create_train(film_0,TRAIN)
print("len(TRAIN)=",len(TRAIN))
############################################################
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

#############################################  creating validation data      ##########
directory="ONE_CELL_SEEDS_VALID"
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
     for k in range(0,n,5):
            film_0=[]
            for ii in range(5):
                frame=raw_files_ch00[k+ii].copy()            
                raw1 = frame.resize((int(SIZE), int(SIZE)), PIL.Image.LANCZOS)
                film_0.append((raw1,new_centr[k+ii]/coeff))
            VALID=create_valid(film_0,TRAIN)
print("len(VALID)=",len(VALID))############################################################
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
print("validation_data.shape",validation_data[0].shape)
#########################           CREATING MODEL     ###############################################
def get_compiled_model():
  input_clip = Input(shape=(int(SIZE),int(SIZE),N_frames+1,1))

  x = Conv3D(32, kernel_size=(3,3,3), padding='same', kernel_initializer='he_normal', bias_initializer='ones')(input_clip)
  x=BatchNormalization()(x)
  x=Activation('relu')(x)
  
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
  def crop(x,frame):
    return x[:,:,:,frame:(frame+1),:]
  outputs=[]
  for k in range(1,N_frames+1):
    b = Lambda(crop, arguments={'frame':k})(x)  
    name=Flatten()(b)    
    name = Dense(256)(name)
    name=BatchNormalization()(name)
    name=Activation('relu')(name)    
    name=Dense(N_cells*2,activation='linear')(name)
    outputs.append(name)
  model = Model(inputs=input_clip, outputs=outputs)
  model.compile(optimizer='adam', loss='mse',metrics=['mae',IoU])
  return model
#####################################################################################################
NUM_EPOCHS=150
INIT_LR=0.009
callbacks = [LearningRateScheduler(poly_decay)]
strategy = tf.distribute.MirroredStrategy()
print("Number of devices: {}".format(strategy.num_replicas_in_sync))
with strategy.scope():    
    model = get_compiled_model()
history=model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)

name='Tracker-1-seeded.weights.h5'  
model.save_weights(name)
print("saved weights in file",name)

history_file='history_Tracker-1-seeded.pickle'

with open(history_file, 'wb') as file_pi:
        pickle.dump(history.history, file_pi)
print("saved history in file",history_file)
#####################################################################

