from tensorflow import keras,nn
from tensorflow.keras import layers
import json
import numpy as np
import tensorflow as tf
import os
import sys

#sudo python3 -m pip install h5py==2.10.0


def data_gen(train_files,cat_map,sentence_len,embedd_dim,seq_range,token_len_filter):
    date_files = {}
    for file_d in train_files:
        file_name,file_len = file_d.split(':')
        date_files[file_name] = int(file_len)
    total_size = 0
    for train_f in date_files:
        total_size+=date_files[train_f]
    input_sample = np.empty((total_size, *(sentence_len,embedd_dim)))
    out_sample = []
    i = 0
    for file_n in date_files:
        data_file = open('{}'.format(file_n), 'r')
        for row in data_file:
            row = json.loads(row)
            features = row['features']
            if token_len_filter:
                if len(features) > int(seq_range[0]) and len(features) <= int(seq_range[1]):
                    out_sample.append(cat_map[row['label']])
                    word_i = 0
                    for word in features:
                        if word_i<sentence_len:
                            input_sample[i,word_i] = np.array([sum(x)/len(x) for x in zip(word['layers'][-1]['values'],word['layers'][-2]['values'])])
                            word_i+=1
                        else:
                            break
                    i+=1
            else:
                out_sample.append(cat_map[row['label']])
                word_i = 0
                for word in features:
                    if word_i < sentence_len:
                        input_sample[i, word_i] = np.array(
                            [sum(x) / len(x) for x in zip(word['layers'][-1]['values'], word['layers'][-2]['values'])])
                        word_i += 1
                    else:
                        break
                i += 1
    input_sample = input_sample[0:i]
    out_sample = out_sample[0:i]
    out_sample=keras.utils.to_categorical(out_sample)
    out_sample_array = np.empty((len(out_sample), 6))
    i =0
    for sample in out_sample:
        out_sample_array[i,] = np.array(sample)
        i+=1
    return (input_sample,out_sample_array)


sentence_len = 50

embedd_dim = 768

token_len_range=['0','50']

token_len_filter = True

model_folder = 'transB_1_filtered'

test_date_files =['3th_fold.json:1684']

cat_map = {'__label__Added':0,'__label__Changed':1,'__label__Deprecated':2,'__label__Fixed':3,'__label__Removed':4,'__label__Security':5}

input_sample,out_sample_array= data_gen(test_date_files,cat_map,sentence_len,embedd_dim,token_len_range,token_len_filter)

positions = tf.range(start=0, limit=sentence_len, delta=1)
position_embb = layers.Embedding(input_dim=sentence_len, output_dim=embedd_dim)(positions)
word_pos = input_sample + position_embb
max_score = [200000000,0]
max_model = None
file_l = os.listdir(model_folder)
score_l = []


for f in file_l:
    model = keras.models.load_model('{}/{}'.format(model_folder,f))
    score = model.evaluate(word_pos, out_sample_array)
    #print(f,score)
    score_l.append((f,score))
    if score[1] > max_score[1]:
        max_score = score
        max_model = f
    elif score[1] == max_score[1] and max_model is not None:
        epoch_n,train_acc,train_loss = f.replace('.hdf5','').split('-')
        epoch_n_m, train_acc_m, train_loss_m = max_model.replace('.hdf5', '').split('-')
        if score[0]<max_score[0]:
            max_score = score
            max_model = f
        elif score[0]==max_score[0]:
            if epoch_n>epoch_n_m:
                max_score = score
                max_model = f

print('max_score: ',max_score)
print ('max_model: ',max_model)
