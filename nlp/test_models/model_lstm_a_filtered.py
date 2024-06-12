from tensorflow import keras
from tensorflow.keras import layers
import json
import numpy as np
import tensorflow as tf
import time

if_filter = False

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




lstm_forward1 = layers.LSTM(200, activation='relu',dropout=0.2, recurrent_dropout=0.2)(word_embedding)
#lstm_backward1 = layers.LSTM(200,activation='relu', dropout=0.2, recurrent_dropout=0.2)(word_embedding)
#con_layer1 = layers.Concatenate(axis=1)([lstm_forward1, lstm_backward1])
#con_layer2 = layers.Concatenate(axis=1)([lstm_forward1, lstm_backward1])


#con_layer3 = layers.Concatenate(axis=1)([con_layer1, con_layer2])
#bidir_lay = layers.Add()([con_layer1,con_layer2])


#output = layers.TimeDistributed(layers.Dense(48))(bidir_lay)

#droup_out1 = layers.Dropout(.5)(con_layer1)


#dense_layer1 = layers.Dense(500,activation='relu')(con_layer2)

droup_out1 = layers.Dropout(.2)(lstm_forward1)

dense_layer2 = layers.Dense(200,activation='relu')(droup_out1)

droup_out2 = layers.Dropout(.2)(dense_layer2)

dense_layer3 = layers.Dense(200,activation='relu')(droup_out2)

droup_out3 = layers.Dropout(.2)(dense_layer3)

dense_layer4 = layers.Dense(200,activation='relu')(droup_out3)

droup_out4 = layers.Dropout(.2)(dense_layer4)

con_layer1 = layers.Concatenate(axis=1)([droup_out2, droup_out3,droup_out4])

#droup_out3 = layers.Dropout(.2)(dense_layer2)

output = layers.Dense(6, activation='softmax')(con_layer1)

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




total_sampe_c = 0

i = 0
for file_n in date_files:
    data_file = open('{}'.format(file_n), 'r')
    for row in data_file:
        embedded_sentence = []
        row = json.loads(row)
        features = row['features']
        content_sample.append(row['content'])
        sample_tokens = []
        for token_d in features:
            if if_filter:
                if token_d['token'] in ['.', ',', ';', '?']:
                    sample_tokens.append(token_d['layers'][-1]['values'])
                elif len(token_d['token']) > 1 and '##' not in token_d['token'] and token_d['token'].isalpha() :
                    sample_tokens.append(token_d['layers'][-1]['values'])
                elif '##' in token_d['token'] and len(token_d['token']) >= 4 and not token_d['token'].replace('##','').isnumeric():
                    sample_tokens.append(token_d['layers'][-1]['values'])
            else:
                sample_tokens.append(token_d['layers'][-1]['values'])
        if sample_tokens:
            out_sample.append(cat_map[row['label']])
            total_sampe_c+=1
            word_i = 0
            for word in sample_tokens:
                if word_i<sentence_len:
                    #embedded_sentence.append([word['layers'][0]['values']])
                    input_sample[i,word_i] = np.array(word)
                    word_i+=1
                else:
                    break
            while word_i <sentence_len:
                #embedded_sentence.append([[0]*128])
                input_sample[i, word_i] = np.array([0]*embedd_dim)
                word_i+=1
            i+=1


input_sample = input_sample[0:total_sampe_c]
out_sample = out_sample[0:total_sampe_c]


out_sample=keras.utils.to_categorical(out_sample)

out_sample_array = np.empty((total_sampe_c, 6))

i =0
for sample in out_sample:
    out_sample_array[i,] = np.array(sample)
    i+=1

checkpoint_filepath = 'model_ds/model_d-{epoch:02d}-{val_categorical_accuracy:.2f}-{val_loss:.2f}.hdf5'

checkpoint = keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=True, mode='max')

#callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

#model.fit(input_sample, out_sample_array,epochs=2000,batch_size = 60,validation_split = 0.1,callbacks=[checkpoint,callback])

model.fit(input_sample, out_sample_array,epochs=50,batch_size = 200,validation_split = 0.2,callbacks=[checkpoint])

consumed_time = time.time()-initial_time

print('consumed_time',consumed_time)