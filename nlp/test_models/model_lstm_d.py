from tensorflow import keras
from tensorflow.keras import layers
import json
import numpy as np
import tensorflow as tf
import time

initial_time = time.time()


embedd_dim = 768

sentence_len = 30



word_embedding = keras.Input(shape=(None,embedd_dim),name='word_input')

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

droup_out2 = layers.Dropout(.2)(dense_layer1)

dense_layer2 = layers.Dense(300,activation='relu')(droup_out2)

droup_out3 = layers.Dropout(.2)(dense_layer2)

dense_layer3 = layers.Dense(300,activation='relu')(droup_out3)

droup_out4 = layers.Dropout(.2)(dense_layer3)

dense_layer4 = layers.Dense(300,activation='relu')(droup_out4)

droup_out5 = layers.Dropout(.2)(dense_layer4)

con_layer3 = layers.Concatenate(axis=1)([droup_out2,droup_out3,droup_out4,droup_out5])

dense_layer5 = layers.Dense(300,activation='relu')(con_layer3)

#droup_out3 = layers.Dropout(.2)(dense_layer2)

output = layers.Dense(6, activation='softmax')(dense_layer5)


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
                input_sample[i,word_i] = np.array([sum(x)/len(x) for x in zip(word['layers'][-1]['values'],word['layers'][-2]['values'])])
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

checkpoint_filepath = 'model_ds/model_d-{epoch:02d}-{val_categorical_accuracy:.2f}-{val_loss:.2f}.hdf5'

checkpoint1 = keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=False, mode='max')

#callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

#model.fit(input_sample, out_sample_array,epochs=2000,batch_size = 60,validation_split = 0.1,callbacks=[checkpoint,callback])

model.fit(input_sample, out_sample_array,epochs=50,batch_size = 600,validation_split = 0.25,callbacks=[checkpoint1])

consumed_time = time.time()-initial_time

model.save('model_testc_base_2_final')

print('consumed_time',consumed_time)

