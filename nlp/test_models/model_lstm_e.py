from tensorflow import keras
from tensorflow.keras import layers
import json
import numpy as np
import tensorflow as tf
import time
from contextlib import redirect_stdout



initial_time = time.time()

num_heads = 3

ff_dim = 1000



embedd_dim = 768

sentence_len = 30
'''
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential([layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)
    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
'''

word_embedding = keras.Input(shape=(None,embedd_dim),name='word_input')
attn_output1 = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embedd_dim)(word_embedding,word_embedding)
attn_output1_2=layers.Dropout(0.1)(attn_output1)
out1 = layers.LayerNormalization(epsilon=1e-6)(word_embedding+attn_output1_2)
ffn_output1=keras.Sequential([layers.Dense(ff_dim, activation="relu"), layers.Dense(embedd_dim),])(out1)
ffn_output1_2 = layers.Dropout(0.1)(ffn_output1)
att1 = layers.LayerNormalization(epsilon=1e-6)(out1+ffn_output1_2)

pool1 = layers.GlobalAveragePooling1D()(att1)

attn_output2 = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embedd_dim)(word_embedding,word_embedding)
attn_output2_2=layers.Dropout(0.1)(attn_output2)
out2 = layers.LayerNormalization(epsilon=1e-6)(word_embedding+attn_output2_2)
ffn_output2=keras.Sequential([layers.Dense(ff_dim, activation="relu"), layers.Dense(embedd_dim),])(out2)
ffn_output2_2 = layers.Dropout(0.1)(ffn_output2)
att2 = layers.LayerNormalization(epsilon=1e-6)(out2+ffn_output2_2)

pool2 = layers.GlobalMaxPooling1D()(att2)

con_layer1 = layers.Concatenate(axis=1)([pool1,pool2])

dense_layer2 = layers.Dense(700,activation='relu')(con_layer1)

dropout2 = layers.Dropout(0.2)(dense_layer2)

output = layers.Dense(6, activation='softmax')(dropout2)

model = keras.Model(inputs=[word_embedding], outputs=[output])

opt = keras.optimizers.Adam(learning_rate=0.0005)

model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['categorical_accuracy'])

with open('modelsummary.txt', 'w') as f:
    with redirect_stdout(f):
        model.summary()


#date_files = {'1th_fold.json':1684,'2th_fold.json':1684,'3th_fold.json':1684,'4th_fold.json':1691}

date_files = {'0th_fold.json':1684,'2th_fold.json':1684,'3th_fold.json':1684,'4th_fold.json':1691}


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
                #input_sample[i, word_i] = np.array(word['layers'][-1]['values'])
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

checkpoint_filepath = 'model_ds/model_d-{epoch:02d}-{val_categorical_accuracy:.3f}-{val_loss:.3f}.hdf5'

checkpoint1 = keras.callbacks.ModelCheckpoint(checkpoint_filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=True, mode='max')



model.fit(input_sample, out_sample_array,epochs=10,batch_size = 1200,validation_split = 0.25)

model.fit(input_sample, out_sample_array,epochs=50,batch_size = 1200,validation_split = 0.25,callbacks=[checkpoint1])

consumed_time = time.time()-initial_time


print('consumed_time',consumed_time)

