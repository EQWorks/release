from tensorflow import keras,nn
from tensorflow.keras import layers
import json
import numpy as np
import time
from contextlib import redirect_stdout
import sys

#https://keras.io/examples/nlp/text_classification_with_transformer/

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




def mdoel_build(embedd_dim,sentence_len,neuron_size,train_files,test_files,outpath, model_name,seq_range,token_len_filter,lr):
    cat_map = {'__label__Added':0,'__label__Changed':1,'__label__Deprecated':2,'__label__Fixed':3,'__label__Removed':4,'__label__Security':5}
    word_embedding = keras.Input(shape=(None,embedd_dim),name='word_input')
    num_heads = 3
    ff_dim = neuron_size
    attn_output1 = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embedd_dim)(word_embedding, word_embedding)
    attn_output1_2 = layers.Dropout(0.1)(attn_output1)
    out1 = layers.LayerNormalization(epsilon=1e-6)(word_embedding + attn_output1_2)
    ffn_output1 = keras.Sequential([layers.Dense(ff_dim, activation="relu"), layers.Dense(embedd_dim), ])(out1)
    ffn_output1_2 = layers.Dropout(0.1)(ffn_output1)
    att1 = layers.LayerNormalization(epsilon=1e-6)(out1 + ffn_output1_2)
    pool1 = layers.GlobalMaxPooling1D()(att1)
    dense_layer2 = layers.Dense(neuron_size,activation='relu')(pool1)
    dense_layer3 = layers.Dense(neuron_size, activation='relu')(dense_layer2)
    dense_layer4 = layers.Dense(neuron_size, activation='relu')(dense_layer3)
    droup_out3 = layers.Dropout(.5)(dense_layer4)
    output = layers.Dense(6, activation='softmax')(droup_out3)
    model = keras.Model(inputs=[word_embedding], outputs=[output])
    opt = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['categorical_accuracy'])
    with open('{}_summary.txt'.format(model_name), 'w') as f:
        with redirect_stdout(f):
            model.summary()
    #date_files = {'0th_fold.json':1684,'2th_fold.json':1684,'3th_fold.json':1684,'4th_fold.json':1691}
    input_sample,out_sample_array = data_gen(train_files,cat_map,sentence_len,embedd_dim,seq_range,token_len_filter)
    print('input_sample len: ',len(input_sample))
    test_sample, test_label = data_gen(test_files, cat_map,sentence_len,embedd_dim,seq_range,token_len_filter)
    print('test_sample len: ', len(test_sample))
    checkpoint_filepath = outpath+'/{epoch:02d}-{categorical_accuracy:.4f}-{loss:.4f}.hdf5'
    checkpoint1 = keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=False, mode='max')
    #callback = keras.callbacks.EarlyStopping(monitor='val_categorical_accuracy', patience=50)
    initial_time = time.time()
    #model.fit(input_sample, out_sample_array,epochs=50,batch_size = 200,validation_data = (test_sample, test_label))
    model.fit(input_sample, out_sample_array,epochs=50,batch_size = 200,validation_data = (test_sample, test_label),callbacks=[checkpoint1])
    consumed_time = time.time()-initial_time
    print('consumed_time',consumed_time)
    return consumed_time,len(input_sample)


if __name__=='__main__':
    #embedd_dim,sentence_len,neuron_size,train_files,outpath, model_name
    embedd_dim = int(sys.argv[1])
    sentence_len = int(sys.argv[2])
    neuron_size = int(sys.argv[3])
    train_files = sys.argv[4].split(',')
    test_files = sys.argv[5].split(',')
    outpath = sys.argv[6]
    model_name = sys.argv[7]
    seq_range = sys.argv[8].split(',')
    token_len_filter = sys.argv[9].lower() == 'true'
    lr = float(sys.argv[10])
    mdoel_build(embedd_dim, sentence_len, neuron_size, train_files, test_files, outpath, model_name,seq_range,token_len_filter,lr)