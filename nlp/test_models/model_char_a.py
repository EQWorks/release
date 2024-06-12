from tensorflow import keras,nn
from tensorflow.keras import layers
import json
import numpy as np
import time
from contextlib import redirect_stdout
import sys

maxlen = 50

chars = set([])

char_size = 100

word_embedding = keras.Input(shape=(maxlen,char_size),name='word_input')

con1 = keras.layers.Conv1D( 100, 6, activation='relu',strides = 3, input_shape=(None,maxlen,char_size))(word_embedding)

pool1 = keras.layers.GlobalMaxPooling1D()(con1)

output = keras.layers.Dense(6, activation='softmax')(pool1)

model = keras.Model(inputs=[word_embedding], outputs=[output])

opt = keras.optimizers.Adam(learning_rate=0.0005)

model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['categorical_accuracy'])
