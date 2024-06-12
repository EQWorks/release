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
    input_sample = np.zeros((total_size, *(sentence_len,embedd_dim)))
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


def mdoel_valid(embedd_dim,sentence_len,test_date_files,valid_date_files,model_folder,token_len_range,token_len_filter):
    cat_map = {'__label__Added':0,'__label__Changed':1,'__label__Deprecated':2,'__label__Fixed':3,'__label__Removed':4,'__label__Security':5}
    input_sample,out_sample_array= data_gen(test_date_files,cat_map,sentence_len,embedd_dim,token_len_range,token_len_filter)
    max_score = [200000000,0]
    max_model = None
    file_l = os.listdir(model_folder)
    score_l = []
    for f in file_l:
        model = keras.models.load_model('{}/{}'.format(model_folder,f))
        score = model.evaluate(input_sample, out_sample_array)
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
    valid_input,valid_output= data_gen(valid_date_files,cat_map,sentence_len,embedd_dim,token_len_range,token_len_filter)
    model = keras.models.load_model('{}/{}'.format(model_folder,max_model))
    score = model.evaluate(valid_input, valid_output)
    print('valid_score: ',score)
    return max_model,score,max_score,len(valid_input)

if __name__=='__main__':
    #sentence_len = 50
    #embedd_dim = 768
    #test_date_files = '2th_fold.json:1684'
    #valid_date_files = '3th_fold.json:1684'
    #model_folder = 'model_lstm_3_small'
    #token_len_filter = True
    #token_len_range = ['0', '50']
    embedd_dim = int(sys.argv[1])
    sentence_len = int(sys.argv[2])
    test_date_files = sys.argv[3].split(',')
    valid_date_files = sys.argv[4].split(',')
    model_folder = sys.argv[5]
    token_len_filter = sys.argv[6].lower() == 'true'
    token_len_range = sys.argv[7].split(',')
    #python3 embedded_valid.py 768 50 3th_fold.json:1684 4th_fold.json:1691 trans_model1_filtered true 0,50
    mdoel_valid(embedd_dim, sentence_len, test_date_files, valid_date_files, model_folder, token_len_range,
                token_len_filter)