import numpy as np
import os
from random import shuffle
import pickle
import json
import cv2
from keras.models import load_model
from keras.models import model_from_json
from keras.optimizers import Adam
from keras.utils import multi_gpu_model
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, concatenate,UpSampling2D
from keras.layers import  Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
###########################################################
Size=96.0
Batch=16
N_channels=3
N_CHANNELS=3
###############################################
def IOU(y_true, y_pred):
  numerator = tf.reduce_sum(tf.round(y_true) * tf.round(y_pred))
  denominator = tf.reduce_sum(tf.round(y_true)) + tf.reduce_sum(tf.round(y_pred))-numerator
  return numerator / (denominator + tf.keras.backend.epsilon())
########################################################################  
def my_loss(weights):
    def loss(y_true,y_pred):
      y_pred = tf.clip_by_value(y_pred, 10e-8, 1. - 10e-8)
      return tf.reduce_mean((y_true * (-tf.log(y_pred)) +(1. - y_true) * (-tf.log(1. - y_pred)))*weights)
    return loss
#####################################################
def characters(x):# this is for sorting by cell number   "0001"
    return(x[-8:-4])
########################################################################
def load_and_organize_images(folder_dir):
    DATA=[]
    names_fluor=[]
    names_bright=[]
    names_labels=[]
    names_from_segmentor=[]
    names_weights=[]
    for filename in os.listdir(folder_dir):
        if filename[-18:-14]=="fluo":
             full_name=os.path.join(folder_dir, filename)        
             names_fluor.append(full_name)       
        if filename[-18:-14]=="brig":
             full_name=os.path.join(folder_dir, filename)        
             names_bright.append(full_name)         
        if filename[-18:-14]=="labl":
             full_name=os.path.join(folder_dir, filename)       
             names_labels.append(full_name) 
        if filename[-18:-14]=="segm":
             full_name=os.path.join(folder_dir, filename)       
             names_from_segmentor.append(full_name) 
        if filename[-18:-14]=="neww":
             full_name=os.path.join(folder_dir, filename)       
             names_weights.append(full_name)
    names_bright_sorted=sorted(names_bright,key=characters)
    names_fluor_sorted=sorted(names_fluor,key=characters)
    names_labels_sorted=sorted(names_labels,key=characters)
    names_from_segmentor_sorted=sorted(names_from_segmentor,key=characters)
    names_weights_sorted=sorted(names_weights,key=characters)    
    n=len(names_bright_sorted)    
    for i in range(n):
        fluor=cv2.imread(names_fluor_sorted[i],0)
        bright=cv2.imread(names_bright_sorted[i],0)
        label=cv2.imread(names_labels_sorted[i],0)
        from_segmentor=cv2.imread(names_from_segmentor_sorted[i],0)
        if len(names_weights_sorted)==0:
            weight_map=np.ones((96,96),dtype='float32')
        else:
            weight_map=cv2.imread(names_weights_sorted[i],0)
        DATA.append((fluor,bright,label,weight_map,from_segmentor))
    return DATA    
##############################################################################   
def augment_train(TRAIN): 
 for i in range(len(TRAIN)):          
     new_sample=[]
     for k in range(5):        
         im1=TRAIN[i][k].copy()   
         im11 = cv2.flip( im1, 1)
         new_sample.append(im11)
     TRAIN.append(new_sample)     
     new_sample=[]     
     for k in range(5):        
         im1=TRAIN[i][k].copy()   
         im11 = cv2.flip( im1, 0)
         new_sample.append(im11)
     TRAIN.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=TRAIN[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_90_COUNTERCLOCKWISE )
         new_sample.append(im11)
     TRAIN.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=TRAIN[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_180 )
         new_sample.append(im11)
     TRAIN.append(new_sample)     
     new_sample=[]
     for k in range(5):        
         im1=TRAIN[i][k].copy()   
         im11 = cv2.rotate( im1,cv2.ROTATE_90_CLOCKWISE )
         new_sample.append(im11)
     TRAIN.append(new_sample)        
 return TRAIN
##################################################
def create_samples_for_refiner(input_data, data_type):# data_type is either TRAIN or VALID 
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
     frame[:,:,2]=input_data[pp][4].astype(np.float32)    
    
     means = frame.mean(axis=(0,1), dtype='float64')
     stds = frame.std(axis=(0,1), dtype='float64')    
     frame = (frame - means) / stds    
     data_inputs[pp,:,:,:]=frame
     label0=input_data[pp][2].astype(np.float32)
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
######################################################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha
###############################################################
def scheduler(epoch, lr):
   return lr * tf.math.exp(-0.1) 
   
############################ Create training and validation data ########
train_directory="C://Users//kfedorchuk//SEGMENTATION FOR THESIS//REFINER_TRAIN_SET//inputs for REFINER FOUR_CELLS_Pos0302f"
TRAIN=load_and_organize_images(train_directory) 
print("len(TRAIN)=", len(TRAIN))                       
train_inputs, train_weights, train_labels=create_samples_for_refiner(TRAIN, "TRAIN")
print("number of training samples after augmentation=", train_labels.shape[0])
##########################################################################################################
valid_directory="C:\\Users\\kfedorchuk\\SEGMENTATION FOR THESIS\\REFINER_VALID_SET\\inputs for REFINER FIVE_Pos0201c"
VALID=load_and_organize_images(valid_directory)
print("len(VALID)=", len(VALID))          
valid_inputs, valid_weights, valid_labels=create_samples_for_refiner(VALID, "VALID")      
validation_data=([valid_inputs,valid_weights],valid_labels)
    
######################### Create model ############

input_image = Input(shape=(int(Size),int(Size),N_channels))
weights_tensor = Input(shape=(int(Size),int(Size),1))
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(input_image)
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
drop2 = Dropout(0.3)(conv2)# added myself
pool2 = MaxPooling2D(pool_size=(2, 2))(drop2)

conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
drop3 = Dropout(0.5)(conv3)# added myself
pool3 = MaxPooling2D(pool_size=(2, 2))(drop3)

conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
drop4 = Dropout(0.5)(conv4)
pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
drop5 = Dropout(0.5)(conv5)

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
############################# Train model ##############

NUM_EPOCHS=3
INIT_LR=0.00005
callbacks = [LearningRateScheduler(poly_decay)]
List_of_train_errors=[]
History_of_training=[]
learn_rate=INIT_LR

parallel_model = multi_gpu_model(model, gpus=2)
parallel_model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [IOU])
history=parallel_model.fit([train_inputs,train_weights], train_labels, validation_data=validation_data, batch_size=Batch, epochs=1,callbacks=callbacks, shuffle=True, verbose=2)
History_of_training.append(history.history)
   
################################ Save weights, model and history #########
name_history="REFINER_HISTORY.json"
with open(name_history,"w") as f:
    json.dump(History_of_training,f)
print("saved history in file ",name_history)

name_weights="REFINER.weights.h5"  
model.save_weights(name_weights)
print("saved weights in file", name_weights)

model.compile(optimizer = 'adam', loss=my_loss(weights_tensor),metrics=[IOU])
model_json=model.to_json()
with open("REFINER.json","w") as json_file:
   json_file.write(model_json)
print("saved the model")

################################### PLOT LEARNING CURVES #######################################################
import matplotlib.pyplot as plt

x=History_of_training
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
###################################################################
















###############################################################
#from keras.utils import plot_model
#plot_model(model, to_file='unet_model.png')
#####################################################################################################
def poly_decay(epoch):
 maxEpochs = NUM_EPOCHS
 baseLR = INIT_LR
 power = 2.0
 alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power
 return alpha

mc = ModelCheckpoint('best_model.h5', monitor='val_bce', mode='min', save_best_only=True,save_weights_only=True,verbose=1)
#es = EarlyStopping(monitor='val_bce', mode='min', verbose=1)
IoU=[]
val_IOU=[]
NUM_EPOCHS=10
INIT_LR=0.00009
batch=32
print("initial learing rate=",INIT_LR)
callbacks = [LearningRateScheduler(poly_decay), mc]
    ####################################################################################################
#######################  training without parallel plotting  ###############
from keras.utils import multi_gpu_model

parallel_model = multi_gpu_model(model, gpus=4)
#parallel_model.compile(optimizer='adam', loss='mse',metrics=['mae'])
parallel_model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [bce,IOU])
history=parallel_model.fit([train_samples,train_weights], train_labels, validation_data=validation_data, batch_size=batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)
IoU+=history.history["IOU"]
val_IOU+=history.history["val_IOU"]


print("Updating training set...")
for i in range(train_samples.shape[0]):
       frame=(train_samples[i,:,:,:]).reshape((1,int(Size),int(Size),3))
       weight=(train_weights[i,:,:]).reshape((1,int(Size),int(Size),1))
       segmentation1=(model.predict([frame,weight], batch_size=1,verbose=0))*255
       segmentation2=segmentation1.reshape((1,int(Size),int(Size)))
       segmentation=segmentation2.reshape((int(Size),int(Size)))
       means = segmentation.mean(axis=(0,1), dtype='float64')
       stds = segmentation.std(axis=(0,1), dtype='float64')    
       segmentation_normalized = (segmentation - means) / stds 
       train_samples[i,:,:,2]=segmentation_normalized
       train_weights[i,:,:,0]=update_weights_map(train_weights[i,:,:,0],segmentation,(train_labels[i,:,:,0]*255))
print("updated training set")


###########################################################################

##################### plotting the result on the whole validation set #######
json_file_segm=open("segment_unet.json","r")
model_segm=json_file_segm.read()
json_file_segm.close()
model_segm = model_from_json(model_segm)
model_segm.load_weights('segment_unet.weights.h5' )
model_segm.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
############################################################################
json_file_step2=open("segment_step_2_advanced.json","r")
model_step2=json_file_step2.read()
json_file_step2.close()
model_step2 = model_from_json(model_step2)
model_step2.load_weights('segment_step_2_advanced.weights.h5' )
model_step2.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
###########################################################
def final_predict(output_1,fluor,bright,model):
    frame=np.zeros((int(Size),int(Size),N_CHANNELS))
    frame[:,:,0]=np.array(fluor.reshape((96,96)),dtype="float32")               
    frame[:,:,1]=np.array(bright.reshape((96,96)),dtype="float32")
    frame[:,:,2]=np.array(output_1.reshape((96,96)),dtype="float32")  
    means = frame.mean(axis=(0,1), dtype='float64')
    stds = frame.std(axis=(0,1), dtype='float64')    
    frame = (frame - means) / stds     
    frame=frame.reshape((1,96,96,3))
    segmentation=model.predict(frame, batch_size=1,verbose=0)
    pred1=np.round(segmentation)
    output0=np.int_(pred1)
    output0=output0*255
    output=output0.reshape((int(Size),int(Size)))
    return output
##########################################################################


for i in range(valid_samples.shape[0]):
       frame=(valid_samples[i,:,:,:]).reshape((1,int(Size),int(Size),3))
      
       #weight=(valid_weights[i,:,:]).reshape((1,int(Size),int(Size),1))
       frame_plot=frame[0,:,:,0]
       frame_plot=frame_plot.astype(np.uint8)
       cv2.imwrite("C:\\Users\\kfedorchuk\\Documents\\PIXELWISE\\input_%s.tif" % (i),frame_plot*200)
       
       labell=valid_labels[i,:,:,:]
       labell=labell.astype(np.uint8)
       cv2.imwrite("C:\\Users\\kfedorchuk\\Documents\\PIXELWISE\\label_%s.tif" % (i),labell*255)    
       
       segmentation=model_segm.predict(frame, batch_size=1,verbose=0)
       pred1=np.round(segmentation)
       output0=np.int_(pred1)
       output0=output0*255
       output=output0.reshape((int(Size),int(Size)))
       output=output.astype(np.uint8)
       cv2.imwrite("C:\\Users\\kfedorchuk\\Documents\\PIXELWISE\\result_%s.tif" % (i),output)
       print("plotted output number %s" % (i))
       
       fluor=frame[:,:,0]
       bright=frame[:,:,1]
       final_result=final_predict(output,fluor,bright,model_step2)
       
       
       
       
       
##########################################################################################
######################################################### training + creating fun video for presentation  ########
IoU=[]
val_IOU=[]

#############################################################


NUM_EPOCHS=1
INIT_LR=0.00009
callbacks = [LearningRateScheduler(poly_decay)]
model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [bce,IOU])

for cycle in range(10,20):  
  model_json_step_2=model.to_json()
  with open("segment_step_2_advanced.json","w") as json_file:
   json_file.write(model_json_step_2)
  model.save_weights("segment_step_2_advanced.weights.h5")  
  json_file_step_2=open("segment_step_2_advanced.json","r")
  model_step_2=json_file_step_2.read()
  json_file_step_2.close()
  model_step_2 = model_from_json(model_step_2)
  model_step_2.load_weights("segment_step_2_advanced.weights.h5")
  model_step_2.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
  predict_and_plot(input_sample,model_step_2,cycle)
  print("plotted outcome number", cycle)
  history=model.fit([train_samples,train_weights], train_labels, validation_data=validation_data, batch_size=batch, epochs=NUM_EPOCHS,callbacks=callbacks, shuffle=True, verbose=2)

IoU+=history.history["IOU"]
val_IOU+=history.history["val_IOU"]     

print("Updating training set...")
for i in range(train_samples.shape[0]):
       frame=(train_samples[i,:,:,:]).reshape((1,int(Size),int(Size),3))
       weight=(train_weights[i,:,:]).reshape((1,int(Size),int(Size),1))
       segmentation1=(model.predict([frame,weight], batch_size=1,verbose=0))*255
       segmentation2=segmentation1.reshape((1,int(Size),int(Size)))
       segmentation=segmentation2.reshape((int(Size),int(Size)))
       means = segmentation.mean(axis=(0,1), dtype='float64')
       stds = segmentation.std(axis=(0,1), dtype='float64')    
       segmentation_normalized = (segmentation - means) / stds 
       train_samples[i,:,:,2]=segmentation_normalized
       train_weights[i,:,:,0]=update_weights_map(train_weights[i,:,:,0],segmentation,(train_labels[i,:,:,0]*255))
print("updated training set")
    
###################################################################################    
    

history_file='segment_step_2.pickle'

with open(history_file, 'wb') as file_pi:
        pickle.dump(history.history, file_pi)
print("saved history in file",history_file)
    
    
    
name='segment_step_2_advanced.weights.h5'  
model.save_weights(name)
print("saved weights in file",name)


from keras.optimizers import Adam
model.compile(Adam(lr=0.003), loss='mse',metrics=['mae'])
model_json=model.to_json()
with open("segment_step_2_adavanced.json","w") as json_file:
   json_file.write(model_json)
############################################################# execute segment_step_2   #######
pp=29
frame=valid_samples[pp,:,:,:]
weights=valid_weights[pp,:,:,:]
weights=weights.reshape((1,64,64,1))
frame=frame.reshape((1,64,64,3))
segmentation=model.predict(frame, batch_size=1,verbose=1)
pred1=np.round(segmentation)
output0=np.int_(pred1)
output0=output0*255
output=output0.reshape((int(Size),int(Size)))
         
fluor=(frame[0,:,:,0]).reshape((64,64))
bright=(frame[0,:,:,1]).reshape((64,64))
oldsegm=(frame[0,:,:,2]).reshape((64,64))
lab=valid_labels[pp,:,:,:]
weig=valid_weights[pp,:,:,:]


cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\fluor.tif",fluor*100)
cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\bright.tif",bright*100)
cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\oldsegm.tif",oldsegm*255)

cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\label.tif",lab*255)
cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\weights.tif",weig*10)       
cv2.imwrite("C:\\Users\\kfedorchuk\\Desktop\\output.tif",output)



model.compile(optimizer = 'adam', loss = my_loss(weights_tensor), metrics = [bce,IOU])
model.evaluate([frame,weights],lab.reshape((1,64,64,1)),verbose=1)
###########################################################################

###############################################################