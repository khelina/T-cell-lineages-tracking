import numpy as np
import os
from random import shuffle
import json
import tensorflow as tf
from keras.models import Model,load_model
from keras.layers import Input, concatenate,UpSampling2D
from keras.layers import  Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.callbacks import LearningRateScheduler
from keras.utils import multi_gpu_model

from keras.models import model_from_json
import cv2
###########################################################
Size=96.0
Batch=16
N_channels=3
################################################

def characters(x):# this is for sorting by cell number   "0001"
    return(x[-9:-4])
##########################################################################    
def load_and_organize_images(folder_dir,DATA):
    names_fluor=[]
    names_bright=[]
    names_segmented=[]
    names_zero=[]
    names_weights=[]
    for filename in os.listdir(folder_dir):
        if filename[-18:-14]=="ch00":
             full_name=os.path.join(folder_dir, filename)        
             names_fluor.append(full_name)       
        if filename[-18:-14]=="ch02":
             full_name=os.path.join(folder_dir, filename)        
             names_bright.append(full_name)         
        if filename[-18:-14]=="segm":
             full_name=os.path.join(folder_dir, filename)       
             names_segmented.append(full_name) 
        if filename[-18:-14]=="zero":
             full_name=os.path.join(folder_dir, filename)       
             names_zero.append(full_name) 
        if filename[-18:-14]=='_map':
             full_name=os.path.join(folder_dir, filename)       
             names_weights.append(full_name)
    names_bright_sorted=sorted(names_bright,key=characters)
    names_fluor_sorted=sorted(names_fluor,key=characters)
    names_segmented_sorted=sorted(names_segmented,key=characters)
    names_zero_sorted=sorted(names_zero,key=characters)
    names_weights_sorted=sorted(names_weights,key=characters)
    
    print("len(bright)", len(names_bright_sorted))
    print("len(fluor)", len(names_fluor_sorted))
    print("len(segmented)", len(names_segmented_sorted))
    print("len(zero)", len(names_zero_sorted))
    print("len(weig)", len(names_weights_sorted))
    
    
    
    n=len(names_bright_sorted)
    for i in range(n):
        fluor=cv2.imread(names_fluor_sorted[i],0)
        bright=cv2.imread(names_bright_sorted[i],0)
        zero_frame=cv2.imread(names_zero_sorted[i],0)      
        label=cv2.imread(names_segmented_sorted[i],0)
      
        if len(names_weights_sorted)==0:
            weight_map=np.ones((96,96),dtype='float32')
        else:
            weight_map=cv2.imread(names_weights_sorted[i],0)
        DATA.append((fluor,bright,zero_frame,weight_map,label))
    return DATA
         

################################################################################## 

def augment_train(data): 
 for i in range(len(data)):          
     new_sample=[]
     for k in range(5):        
         im1=data[i][k].copy()   
         im11 = cv2.flip( im1, 1)
         new_sample.append(im11)
     data.append(new_sample)     
     new_sample=[]     
     for k in range(5):        
         im1=data[i][k].copy()   
         im11 = cv2.flip( im1, 0)
         new_sample.append(im11)
     data.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=data[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_90_COUNTERCLOCKWISE )
         new_sample.append(im11)
     data.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=data[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_180 )
         new_sample.append(im11)
     data.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=data[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_90_CLOCKWISE )
         new_sample.append(im11)
     data.append(new_sample)        
 return data
###########################################################################################
def create_samples_for_segmentor(input_data, data_type):# data_type is either TRAIN or VALID 
    if data_type=="TRAIN":     
        input_data=augment_train(input_data)
        shuffle(input_data)
    a=(len(input_data)//Batch)*Batch
    input_data=input_data[:a]
    N_data=len(input_data)
    data_inputs=np.zeros((N_data,int(Size),int(Size),N_channels))
    data_labels=np.zeros((N_data,int(Size),int(Size)))
    data_weights=np.zeros((N_data,int(Size),int(Size)))
    
    for pp in range(N_data):
     frame=np.zeros((int(Size),int(Size),N_channels)) 
     frame[:,:,0]=input_data[pp][0].astype(np.float32)
     frame[:,:,1]=input_data[pp][1].astype(np.float32)
     frame[:,:,2]=input_data[pp][2].astype(np.float32)    
    
     means = frame.mean(axis=(0,1), dtype='float64')
     stds = frame.std(axis=(0,1), dtype='float64')    
     frame = (frame - means) / stds    
     data_inputs[pp,:,:,:]=frame
     label0=input_data[pp][4].astype(np.float32)
     labell=label0/255.0
     data_labels[pp,:,:]=labell
     if data_type=="TRAIN":
       weight=input_data[pp][3].astype(np.float32)
     else:
       weight=np.ones((96,96),dtype='float32')
     data_weights[pp,:,:]=weight      

    data_labels=data_labels.reshape((N_data,int(Size),int(Size),1))
    data_weights=data_weights.reshape((N_data,int(Size),int(Size),1)) 
    return data_inputs, data_weights, data_labels 
##############################################################################################

##############################################################################################
#train_directory="C:\\Users\\kfedorchuk\\SEGMENTATION FOR THESIS\\SEGMENTOR_TRAIN_SET"
train_directory="SEGMENTOR_VALID_SET"

TRAIN=[]

 
TRAIN=load_and_organize_images(train_directory,TRAIN)
print("TRAIN=", len(TRAIN)) 
train_inputs, train_weights, train_labels =create_samples_for_segmentor(TRAIN, "TRAIN")         
print("TRAIN after augmentation=", len(TRAIN))

#################### CHECK TRAIN SET   ##########
"""
path="C:\\Users\\kfedorchuk\\SEGMENTATION FOR THESIS\\PLAYGROUND"
nn=455
sample=TRAIN[nn]
cv2.imwrite(os.path.join(path,"fluor.tif"),sample[0])
cv2.imwrite(os.path.join(path,"bright.tif"),sample[1])
cv2.imwrite(os.path.join(path,"zero.tif"),sample[2])
cv2.imwrite(os.path.join(path,"weight.tif"),sample[3]*10)
cv2.imwrite(os.path.join(path,"target.tif"),sample[4])
"""

##################################################################################################
#valid_directory="C:\\Users\\kfedorchuk\\SEGMENTATION FOR THESIS\\SEGMENTOR_VALID_SET"
valid_directory="SEGMENTOR_TRAIN_SET"

VALID=[]
VALID=load_and_organize_images(valid_directory,VALID)
print("VALID=", len(VALID)) 
valid_inputs, valid_weights, valid_labels =create_samples_for_segmentor(VALID, "VALID")         


validation_data=([valid_inputs,valid_weights],valid_labels) 


################################################################################

###################################################################


#smooth = 1e-7

def IOU(y_true, y_pred):
  numerator = tf.reduce_sum(tf.round(y_true) * tf.round(y_pred))
  # some implementations don't square y_pred
  denominator = tf.reduce_sum(tf.round(y_true)) + tf.reduce_sum(tf.round(y_pred))-numerator

  return numerator / (denominator + tf.keras.backend.epsilon())



  
def my_loss(weights):
    def loss(y_true,y_pred):
      y_pred = tf.clip_by_value(y_pred, 10e-8, 1. - 10e-8)
      return tf.reduce_mean((y_true * (-tf.log(y_pred)) +(1. - y_true) * (-tf.log(1. - y_pred)))*weights)
    return loss

################################################################


##############################################


input_image = Input(shape=(int(Size),int(Size),N_channels))
weights_tensor = Input(shape=(int(Size),int(Size),1))
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(input_image)
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
#drop2 = Dropout(0.4)(conv2)# added myself
pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
#drop3 = Dropout(0.4)(conv3)# added myself
pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
drop4 = Dropout(0.3)(conv4)
pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
drop5 = Dropout(0.3)(conv5)

up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(drop5))
merge6 = concatenate([drop4,up6], axis = 3)
conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge6)
conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)

up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv6))
merge7 = concatenate([conv3,up7], axis = 3)
conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge7)
conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)

up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv7))
merge8 = concatenate([conv2,up8], axis = 3)
conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge8)
conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)

up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv8))
merge9 = concatenate([conv1,up9], axis = 3)
conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge9)
conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
conv9 = Conv2D(2, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
conv10 = Conv2D(1, 1, activation = 'sigmoid')(conv9)

model = Model(inputs = [input_image,weights_tensor], outputs = conv10)


    
   

#########################################################
#from keras.utils import plot_model
#plot_model(model, to_file='unet_model.png')
#####################################################################################################



###############################################################################################
###############  This is a better training yielding in perfect learning curves. The ideais to evaluate training set after each epoch wothout weights ()
######################################################################################
List_of_train_errors=[]

def evaluate_train_and_save(model,train_inputs, train_labels):
   test_weights=np.ones((train_weights.shape))
   score = model.evaluate([train_inputs,test_weights], train_labels, verbose = 0)
   print("corrected train score=", score)
   List_of_train_errors.append(score)   
   name_real_train_errors="SEGMENTOR_REAL_TRAIN_ERRORS.json"
   with open(name_real_train_errors,"w") as f:
    json.dump(List_of_train_errors,f)
   print("saved real train errors in file ",name_real_train_errors)



List_of_valid_errors=[]

def evaluate_valid_and_save(model,valid_inputs,valid_weights,valid_labels):
   score = model.evaluate([valid_inputs,valid_weights], valid_labels, verbose = 0)
  
   print("valid score=", score)
   List_of_valid_errors.append(score)   
   name_real_valid_errors="SEGMENTOR_REAL_VALID_ERRORS.json"
   with open(name_real_valid_errors,"w") as f:
    json.dump(List_of_valid_errors,f)
   
   print("saved real valid errors in file ",name_real_valid_errors)
   return score[1]
   
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha


def scheduler(epoch, lr):
   return lr * tf.math.exp(-0.1)

callbacks = [LearningRateScheduler(scheduler)]
model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [IOU])
#model.save("SEGMENTOR.h5")



NUM_EPOCHS=50
INIT_LR=0.00001
callbacks = [LearningRateScheduler(poly_decay)]
List_of_train_errors=[]
History_of_training=[]
learn_rate=INIT_LR



for Epoch in range(NUM_EPOCHS):  
  print("REAL EPOCH NUMBER=", Epoch+1, end =" ")
  print("out of",NUM_EPOCHS)

  #print("learning rate=",learn_rate)
  parallel_model = multi_gpu_model(model, gpus=2)
  parallel_model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [IOU])
  history=parallel_model.fit([train_inputs,train_weights], train_labels, validation_data=validation_data, batch_size=Batch, epochs=1,callbacks=callbacks, shuffle=True, verbose=2)
  History_of_training.append(history.history)
  evaluate_train_and_save(model,train_inputs, train_labels) 
  SIGN=evaluate_valid_and_save(model,valid_inputs,valid_weights,valid_labels)
  if Epoch==0:
       PREV_SIGN=SIGN
  print("PREV_SIGN=", PREV_SIGN)
  if (Epoch==0 or SIGN > PREV_SIGN):       
       name_weights="SEGMENTOR.weights.h5"  
       model.save_weights(name_weights)
       print("saved weights in file", name_weights)
       PREV_SIGN=SIGN

  
####################################################################################
#destination="C:\\Users\\kfedorchuk\SEGMENTATION FOR THESIS"



name_history="SEGMENTOR_HISTORY.json"
with open(name_history,"w") as f:
    json.dump(History_of_training,f)
print("saved history in file ",name_history)




"""
name_weights="SEGMENTOR.weights.h5"  
model.save_weights(name_weights)
print("saved weights in file", name_weights)
"""

model.compile(optimizer = 'adam', loss=my_loss(weights_tensor),metrics=[IOU])
model_json=model.to_json()
with open("SEGMENTOR.json","w") as json_file:
   json_file.write(model_json)
print("saved the model")


model.save('SEGMENTOR.h5') 
 

"""
######
#########################################################
################################### PLOT LEARNING CURVES #######################################################

############################################
with open("SEGMENTOR_REAL_TRAIN_ERRORS.json", 'r') as filehandle:
     List_of_train_errors= json.load(filehandle)
############################################
with open("SEGMENTOR_REAL_VALID_ERRORS.json", 'r') as filehandle:
     List_of_valid_errors= json.load(filehandle)

########################################


import matplotlib.pyplot as plt



train_loss=[List_of_train_errors[i][0] for i in range(NUM_EPOCHS) ]
valid_loss=[List_of_valid_errors[i][0] for i in range(NUM_EPOCHS) ]
plt.plot(valid_loss,"magenta")
plt.plot(train_loss,"green")
plt.title('')
plt.ylabel('mse loss')
plt.xlabel('epoch')
plt.legend(['validation loss ='+str(round(valid_loss[-1],5)), 'training loss = '+str(round(train_loss[-1],5))], loc='upper right')
plt.show()


train_IOU=[List_of_train_errors[i][1] for i in range(NUM_EPOCHS) ]
valid_IOU=[List_of_valid_errors[i][1] for i in range(NUM_EPOCHS) ]
plt.plot(valid_IOU,"red")
plt.plot(train_IOU,"blue")
plt.title('IOU')
plt.ylabel('IOU')
plt.xlabel('epoch')
plt.legend(['validation IOU ='+str(round(valid_IOU[-1],5)), 'training IOU = '+str(round(train_IOU[-1],5))], loc='lower right')
plt.show()




######################## plotting bad training curves ##############
x=History_of_training

val_loss=x


val_loss=[x[i]["val_loss"][0] for i in range(len(x))]
train_loss=[x[i]["loss"][0] for i in range(len(x))]

plt.plot(val_loss,"magenta")
plt.plot(train_loss,"green")
plt.title('')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['validation loss ='+str(round(val_loss[-1],5)), 'training loss = '+str(round(train_loss[-1],5))], loc='upper right')
plt.show()

val_IOU=[x[i]["val_IOU"][0] for i in range(len(x))]
train_IOU=[x[i]["IOU"][0] for i in range(len(x))]


plt.plot(val_IOU,"red")
plt.plot(train_IOU,"blue")
plt.title('IOU')
plt.ylabel('IOU')
plt.xlabel('epoch')
plt.legend(['validation IOU ='+str(round(val_IOU[-1],5)), 'training IOU = '+str(round(train_IOU[-1],5))], loc='lower right')
plt.show()

################################################################################################

################# TESTING ON OTHER MOVIES ###############
json_file_segmentor=open("SEGMENTOR.json","r")
model=json_file_segmentor.read()
json_file_segmentor.close()
model= model_from_json(model)
model.load_weights("SEGMENTOR.weights.h5")







test_directory="C:\\Users\\kfedorchuk\\SEGMENTATION FOR THESIS\\PATCHES FOR TESTING SEGMENTOR\\PATCHES from FIVE_Pos0701a"

fluorescent,brightfield,segmented,zero_frames,weights_maps=load_images(test_directory)              
print("images loaded")
print("number of test samples=", len(segmented))
if len(weights_maps)==0:
 print("no weights maps found")      
test_inputs, test_weights, test_labels=create_samples(fluorescent,brightfield,segmented,zero_frames,weights_maps, "VALID")
test_data=([test_inputs,test_weights],test_labels)

#model = load_model('SEGMENTOR.h5', custom_objects={ 'loss': my_loss(test_weights) })
#model = load_model('SEGMENTOR.h5')
model.compile(optimizer = 'adam', loss="binary_crossentropy",metrics=[IOU])

score = model.evaluate(test_inputs, test_labels, verbose = 0)
print("score=", score)
"""