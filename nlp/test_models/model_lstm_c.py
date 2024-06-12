from tensorflow import keras
from tensorflow.keras import layers
import json
import numpy as np
import tensorflow as tf
import time

initial_time = time.time()


embedd_dim = 768

sentence_len = 30

initial_time = time.time()


word_embedding = keras.Input(shape=(None,embedd_dim),name='word_input')

'''
convs = []
for kernel_size in [2]:
    conv_output= layers.TimeDistributed(layers.Conv1D(kernel_size=kernel_size, filters=200, padding='causal',activation='relu', strides=1))(activity_input)
    maxpool_output = layers.TimeDistributed(layers.MaxPooling1D(2))(conv_output)
    convs.append(maxpool_output)

if len(convs) > 1:
    con_convs = layers.Concatenate()(convs)
else:
    con_convs = convs[0]

char_conv = layers.TimeDistributed(layers.Flatten())(con_convs)
'''

#norm_lay = layers.BatchNormalization()(word_embedding)


lstm_forward1 = layers.LSTM(300, activation='relu',return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(word_embedding)
#lstm_forward1 = layers.LSTM(100, activation='relu', dropout=0.2, recurrent_dropout=0.2)(word_embedding)
lstm_forward2 = layers.LSTM(300, activation='relu',dropout=0.2, recurrent_dropout=0.2)(lstm_forward1)
lstm_backward1 = layers.LSTM(300,activation='relu', return_sequences=True, dropout=0.2, recurrent_dropout=0.2,go_backwards = True)(word_embedding)
#lstm_backward1 = layers.LSTM(100,activation='relu', dropout=0.2, recurrent_dropout=0.2,go_backwards = True)(word_embedding)
lstm_backward2 = layers.LSTM(300,activation='relu', dropout=0.2, recurrent_dropout=0.2)(lstm_backward1)
#con_layer1 = layers.Concatenate(axis=1)([lstm_forward1, lstm_backward1])
con_layer2 = layers.Concatenate(axis=1)([lstm_forward2, lstm_backward2])


#con_layer3 = layers.Concatenate(axis=1)([con_layer1, con_layer2])
#bidir_lay = layers.Add()([con_layer1,con_layer2])


#output = layers.TimeDistributed(layers.Dense(48))(bidir_lay)

#droup_out1 = layers.Dropout(.5)(con_layer1)


dense_layer1 = layers.Dense(300,activation='relu')(con_layer2)

droup_out2 = layers.Dropout(.5)(dense_layer1)

dense_layer2 = layers.Dense(300,activation='relu')(droup_out2)


#droup_out3 = layers.Dropout(.2)(dense_layer2)

output = layers.Dense(6, activation='softmax')(dense_layer2)


model = keras.Model(inputs=[word_embedding], outputs=[output])

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['categorical_accuracy'])


date_files = {'1th_fold.json':1684,'2th_fold.json':1684,'3th_fold.json':1684,'4th_fold.json':1691}

total_size = 0
for train_f in date_files:
    total_size+=date_files[train_f]


cat_map = {'__label__Added':0,'__label__Changed':1,'__label__Deprecated':2,'__label__Fixed':3,'__label__Removed':4,'__label__Security':5}

#input_sample = []

content_sample = []


input_sample = np.empty((total_size, *(sentence_len,embedd_dim)))
#out_sample = np.empty((total_size, *(6)))
out_sample = []

out_sample_array = np.empty((total_size, 6))

i = 0
for file_n in date_files:
    data_file = open('{}'.format(file_n), 'r')
    for row in data_file:
        embedded_sentence = []
        row = json.loads(row)
        features = row['features']
        content_sample.append(row['content'])
        out_sample.append(cat_map[row['label']])
        word_i = 0
        for word in features:
            if word_i<sentence_len:
                #embedded_sentence.append([word['layers'][0]['values']])
                input_sample[i,word_i] = np.array(word['layers'][-1]['values'])
                word_i+=1
            else:
                break
        while word_i <sentence_len:
            #embedded_sentence.append([[0]*128])
            input_sample[i, word_i] = np.array([0]*embedd_dim)
            word_i+=1
        i+=1


out_sample=keras.utils.to_categorical(out_sample)

i =0
for sample in out_sample:
    out_sample_array[i,] = np.array(sample)
    i+=1

checkpoint_filepath = 'model_testc_base_2'

checkpoint = keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=True, mode='max')

#callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

#model.fit(input_sample, out_sample_array,epochs=2000,batch_size = 60,validation_split = 0.1,callbacks=[checkpoint,callback])

model.fit(input_sample, out_sample_array,epochs=30,batch_size = 60,validation_split = 0.1,callbacks=[checkpoint])

consumed_time = time.time()-initial_time

model.save('model_testc_base_2_final')

print('consumed_time',consumed_time)