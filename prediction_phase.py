 
# coding: utf-8

# In[18]:


# coding= UTF-8
#
# Author: Fing
# Date  : 2017-12-03

import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import soundfile as sf

def extract_feature(file_name):
    X, sample_rate = sf.read(file_name, dtype='float32')
    print(X,sample_rate)
    if X.ndim > 1:
        X = X[:,0]
    X = X.T

    # short term fourier transform
    stft = np.abs(librosa.stft(X))

    # mfcc
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

    # chroma
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # melspectrogram
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)

    # spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz

def parse_audio_files(parent_dir,sub_dirs,file_ext='*.ogg'):
    features, labels = np.empty((0,193)), np.empty(0)
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            try:
                mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
            except Exception as e:
                print("[Error] extract feature error. %s" % (e))
                continue
            ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
            print(ext_features)
            features = np.vstack([features,ext_features])
            # labels = np.append(labels, fn.split('/')[1])
            #labels = np.append(labels, label)
        #print("extract %s features done" % (sub_dir))
    return np.array(features), np.array(labels, dtype = np.int)

#def one_hot_encode(labels):
#    n_labels = len(labels)
#    n_unique_labels = len(np.unique(labels))
#    one_hot_encode = np.zeros((n_labels,n_unique_labels))
#    one_hot_encode[np.arange(n_labels), labels] = 1
#    return one_hot_encode

# Get features and labels
#r = os.listdir("Test/")
#r.sort()
#features, labels = parse_audio_files('data', r)
#np.save('feat_test.npy', features)
#np.save('label.npy', labels)
#print (extract_feature("1-30226-A.ogg"))
mfccs, chroma, mel, contrast,tonnetz = extract_feature("achala.ogg")
ext_features = np.hstack([mfccs, chroma, mel, contrast,tonnetz])
features=np.empty((0,193))
#print(ext_features)
features = np.vstack([features,ext_features])
#features=np.empty((0,193))
#print(features.shape)
#features = np.vstack([ext_features])
print(features.shape)
#print(np.array(ext_features).shape)


# In[13]:


import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
# Prepare the data
X = np.load('feat.npy')
y = np.load('label.npy').ravel()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=233)
#print(X_test.shape)
# Build the Neural Network
model = Sequential()
model.add(Conv1D(64, 3, activation='relu', input_shape=(193, 1)))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Conv1D(128, 3, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Plot model
# from keras.utils import plot_model
# plot_model(model, to_file='model.png')

# Convert label to onehot
print(y_train)
y_train = keras.utils.to_categorical(y_train, num_classes=3)
y_test = keras.utils.to_categorical(y_test, num_classes=3)
#print(y_train)
X_train = np.expand_dims(X_train, axis=2)
#print(X_train.shape)
X_test = np.expand_dims(X_test, axis=2)
#print(X_train.shape)
model.fit(X_train, y_train, batch_size=64, epochs=50)


# In[19]:


features=np.expand_dims(features, axis=2)
#print(features.shape)
print(y_train.shape)
print(features.shape)
score, acc = model.evaluate(X_test, y_test, batch_size=16)
print('Test score:', score)
print('Test accuracy:', acc)


# In[20]:


import os
#X_test = np.expand_dims(X_test[0], axis=2)
#print( "%.16f" % float("1.70000043572e-05")
final=model.predict(features)
#print(final)
#print(list(final[0]))
index=list(final[0]).index(max(list(final[0])))
for i in final[0]:
    print( "%.16f" % float(i))
print("Max Index %d"%index)
print("Name ::: %s"%os.listdir("data/")[index])

