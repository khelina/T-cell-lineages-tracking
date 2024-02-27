import numpy as np
import os
import PIL 
from PIL import Image
from random import shuffle
import re
import json
#import matplotlib.pyplot as plt


###########################################################
N_frames=4
N_cells=1
coeff=382.0/100.0
Batch=128
################################################
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

###############################################################
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
    
def order_clip(y): # y - list of numpy arrays
    z=np.concatenate(y, axis=1)
    d=z[np.lexsort(np.fliplr(z).T)]
    labels=[]
    for i in range(len(y)):
      a=d[:,(2*i):(2*i+2)]
      labels.append(a/100)
    return labels
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
def create_valid(film_0,VALID):          
  N_train_1=len(film_0)-N_frames+1 # number of videos with a film
  for iii in range(N_train_1):# iii = number of the 1st frame in video
    VIDEO=np.zeros((100,100,N_frames))
    LABEL0=[]
    for iiii in range(N_frames):
        frame=np.array(film_0[iii+iiii][0])
        VIDEO[:,:,iiii]=(frame-np.mean(frame))/np.std(frame)
        LABEL0.append(film_0[iii+iiii][1])    
    LABEL=order_clip(LABEL0)   
    VALID.append((VIDEO,LABEL))
  return VALID
###################
 ##################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha
##################################################################
def calculate_iou(y_true, y_pred):
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

def IoU(y_true, y_pred):    
    iou = tf.py_func(calculate_iou, [y_true, y_pred], tf.float32)
    return iou
########################################
#######################################
"""
def calculate_iou(y_true, y_pred):
    results = []    
    for i in range(0,y_true.shape[0]):        
        y_true = y_true.astype(np.float32)
        y_pred = y_pred.astype(np.float32)
        x_boxTrue_tleft = y_true[i,0]-20 # numpy index selection
        y_boxTrue_tleft = y_true[i,1]-20
        boxTrue_width = 40
        boxTrue_height = 40
        area_boxTrue = (boxTrue_width * boxTrue_height)       
        x_boxPred_tleft = y_pred[i,0]-20
        y_boxPred_tleft = y_pred[i,1]-20
        boxPred_width = 40
        boxPred_height = 40
        area_boxPred = (boxPred_width * boxPred_height)      
        x_boxTrue_br = x_boxTrue_tleft + boxTrue_width
        y_boxTrue_br = y_boxTrue_tleft + boxTrue_height      
        x_boxPred_br = x_boxPred_tleft + boxPred_width
        y_boxPred_br = y_boxPred_tleft + boxPred_height        
        x_boxInt_tleft = np.max([x_boxTrue_tleft,x_boxPred_tleft])
        y_boxInt_tleft = np.max([y_boxTrue_tleft,y_boxPred_tleft])        
        x_boxInt_br = np.min([x_boxTrue_br,x_boxPred_br])
        y_boxInt_br = np.min([y_boxTrue_br,y_boxPred_br]) 
        area_of_intersection = \
        np.max([0,(x_boxInt_br - x_boxInt_tleft)]) * np.max([0,(y_boxInt_br - y_boxInt_tleft)])
        iou = area_of_intersection / ((area_boxTrue + area_boxPred) - area_of_intersection)      
        iou = iou.astype(np.float32)
        results.append(iou)   
    return np.mean(results)# for the batch

def IoU(y_true, y_pred):    
    iou = tf.py_func(calculate_iou, [y_true, y_pred], tf.float32)
    return iou
"""
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
     #n=(n//4)*4
     #print("n=",n)
     for k in range(0,n-4+1,1):
            film_0=[]
            for ii in range(4):
                frame=raw_files_ch00[k+ii].copy()            
                raw1 = frame.resize((100, 100), PIL.Image.LANCZOS)
                film_0.append((raw1,new_centr[k+ii]/coeff))
            TRAIN=create_train(film_0,TRAIN)
     print("len(TRAIN)=",len(TRAIN))

############################################################
shuffle(TRAIN)
a=(len(TRAIN)//Batch)*Batch
TRAIN=TRAIN[:a]
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
     #n=(n//4)*4
     #print("n=", n)
     for k in range(0,n-4+1,1):
            film_0=[]
            for ii in range(4):
                frame=raw_files_ch00[k+ii].copy()            
                raw1 = frame.resize((100, 100), PIL.Image.LANCZOS)
                film_0.append((raw1,new_centr[k+ii]/coeff))
            VALID=create_valid(film_0,VALID)
     print("len(VALID)=",len(VALID))
    
############################################################
shuffle(VALID)
a=(len(VALID)//Batch)*Batch
VALID=VALID[:a]
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

import keras
from keras.models import Model
from keras.layers import Input, Lambda
from keras.layers import Dense, Dropout
from keras.layers import Flatten,BatchNormalization, Activation
from keras.layers.convolutional import Conv3D
from keras.layers.pooling import MaxPooling3D
from keras.callbacks import LearningRateScheduler
import tensorflow as tf
from keras.utils import multi_gpu_model
###################################

#########################           CREATING MODEL     ###############################################
input_clip = Input(shape=(100,100,N_frames,1))

x = Conv3D(32, kernel_size=(3,3,3), padding='same', kernel_initializer='glorot_normal', bias_initializer='ones')(input_clip)
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

model = Model(inputs=input_clip, outputs=outputs)

"""
#####################################################################################################
###############################################################
NUM_EPOCHS=30
INIT_LR=0.009
callbacks = [LearningRateScheduler(poly_decay)]
    ####################################################################################################



parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(optimizer='adam', loss='mse',metrics = ["mae",IoU])

history=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=Batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)
 

with open("track_one_history.json","w") as f:
    json.dump(history.history,f)
print("saved history")
  
model.save_weights('track_one.weights.h5')
print("saved weights")


#model.compile(Adam(lr=0.003), loss='mse',metrics=['mae',JoU])
model_json=model.to_json()
with open("track_one_model.json","w") as json_file:
   json_file.write(model_json)
"""
###############################################################################################
###############  This is a better training yielding in perfect learning curves. The ideais to evaluate training set after each epoch wothout weights ()
######################################################################################
List_of_train_errors=[]

def evaluate_train_and_save(model,train_samples, train_labels_mult):
   
   score = model.evaluate(train_samples, train_labels_mult, verbose = 0)
   print("corrected train score=", score)
   List_of_train_errors.append(score)   
   name_real_train_errors="TRACKER_1_TRAIN_ERRORS.json"
   with open(name_real_train_errors,"w") as f:
    json.dump(List_of_train_errors,f)
   print("saved real train errors in file ",name_real_train_errors)



List_of_valid_errors=[]

def evaluate_valid_and_save(model,valid_samples,valid_labels_mult):
   score = model.evaluate(valid_samples, valid_labels_mult, verbose = 0)
  
   print("valid score=", score)
   List_of_valid_errors.append(score)   
   name_real_valid_errors="TRACKER_1_VALID_ERRORS.json"
   with open(name_real_valid_errors,"w") as f:
    json.dump(List_of_valid_errors,f)
   
   print("saved real valid errors in file ",name_real_valid_errors)
   return min(score[6],score[8],score[10],score[12])
   


def scheduler(epoch, lr):
   return lr * tf.math.exp(-0.1)

callbacks = [LearningRateScheduler(scheduler)]
#model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [IOU])
model.compile(optimizer='adam', loss='mse',metrics = ["mae",IoU])
#model.save("SEGMENTOR.h5")



NUM_EPOCHS=150
INIT_LR=0.009
print("learning rate=", INIT_LR)
callbacks = [LearningRateScheduler(poly_decay)]
List_of_train_errors=[]
History_of_training=[]
learn_rate=INIT_LR
parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(optimizer='adam', loss='mse',metrics = [IoU])
history=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=Batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2) 

"""
for Epoch in range(NUM_EPOCHS):  
  print("REAL EPOCH NUMBER=", Epoch+1, end =" ")
  print("out of",NUM_EPOCHS)

  #print("learning rate=",learn_rate)
 
  #history=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=batch, epochs=1,callbacks=callbacks, shuffle=True, verbose=2)
 
  history=parallel_model.fit(train_samples, train_labels_mult, validation_data=validation_data, batch_size=Batch, epochs=1,callbacks=callbacks, shuffle=True, verbose=2)
  #del parallel_model
  History_of_training.append(history.history)
  evaluate_train_and_save(model,train_samples, train_labels_mult) 
  SIGN=evaluate_valid_and_save(model,valid_samples,valid_labels_mult)
  if Epoch==0:
       PREV_SIGN=SIGN
  print("PREV_SIGN=", PREV_SIGN)
  if (Epoch==0 or SIGN > PREV_SIGN):       
       name_weights="TRACKER_1.weights.h5"  
       model.save_weights(name_weights)
       print("saved weights in file", name_weights)
       PREV_SIGN=SIGN
      
"""
  
####################################################################################
#destination="C:\\Users\\kfedorchuk\SEGMENTATION FOR THESIS"


name_history="TRACKER_1_HISTORY.json"
with open(name_history,"w") as f:
    json.dump(history.history,f)
print("saved history in file ",name_history)





name_weights="TRACKER_1.weights.h5"  
model.save_weights(name_weights)
print("saved weights in file", name_weights)


model.compile(optimizer='adam', loss='mse',metrics = [IoU])
model_json=model.to_json()
with open("TRACKER_1_model.json","w") as json_file:
   json_file.write(model_json)
print("saved the model")


#model.save('TRACKER_1.h5') 
 





"""

history=json.load(open("/Users/kfedorchuk/Desktop/track_one_history.json","r"))   

print(history.keys())

# summarize history for accuracy
plt.plot(history['accuracy'])
plt.plot(history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


def IoU(boxA, boxB):
    xA=max(boxA[0],boxB[0])
    yA=max(boxA[1],boxB[1])
    xB=min(boxA[2],boxB[2])
    yB=min(boxA[3],boxB[3])
    interArea=max(0,xB-xA+1)*max(0,yB-yA+1)
    boxAArea=(boxA[2]-boxA[0]+1)*(boxA[3]-boxA[1]+1)
    boxBArea=(boxB[2]-boxB[0]+1)*(boxB[3]-boxB[1]+1)
    iou=interArea/float(boxAArea+boxBArea-interArea)
    return iou


smooth = 1e-7
def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def IOU(y_true, y_pred):
  numerator = tf.reduce_sum(tf.round(y_true) * tf.round(y_pred))
  # some implementations don't square y_pred
  denominator = tf.reduce_sum(tf.round(y_true)) + tf.reduce_sum(tf.round(y_pred))-numerator

  return numerator / (denominator + tf.keras.backend.epsilon())


smooth = smooth=1e-7
  
def my_loss(weights):
    def loss(y_true,y_pred):
      y_pred = tf.clip_by_value(y_pred, 10e-8, 1. - 10e-8)
      return tf.reduce_mean((y_true * (-tf.log(y_pred)) +(1. - y_true) * (-tf.log(1. - y_pred)))*weights)+dice_coef_loss(y_true,y_pred)
    return loss
"""