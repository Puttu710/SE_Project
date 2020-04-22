import os
import numpy as np
import pandas as pd
import tensorflow as tf
import spacy
import matplotlib.pyplot as plt
EN = spacy.load('en_core_web_sm')
from sklearn.preprocessing import MultiLabelBinarizer
import fasttext

data = pd.read_csv('Preprocessed_data.csv')

# Make a dict having tag frequencies
data.tags = data.tags.apply(lambda x: x.split('|'))
tag_freq_dict = {}
for tags in data.tags:
    for tag in tags:
        if tag not in tag_freq_dict:
            tag_freq_dict[tag] = 0
        else:
            tag_freq_dict[tag] += 1


# Get most common tags
tags_to_use = 600
tag_freq_dict_sorted = sorted(tag_freq_dict.items(), key=lambda x: x[1], reverse=True)
final_tags = tag_freq_dict_sorted[:tags_to_use]

for i in range(len(final_tags)):
    final_tags[i] = final_tags[i][0]

# Change tag data to only for final_tags
final_tag_data = []
X = []
for i in range(0, len(data)):
    temp = []
    for tag in data.iloc[i].tags:
        if tag in final_tags:
            temp.append(tag)
    if(temp != []):
        final_tag_data.append(temp)
        X.append(data.iloc[i].processed_title)


tag_encoder = MultiLabelBinarizer()
tags_encoded = tag_encoder.fit_transform(final_tag_data)

# loading tokenizer
import pickle
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
word_index = tokenizer.word_index
vocab_size = len(word_index)

import keras.backend as K

# Custom loss function to handle multilabel classification task
def multitask_loss(y_true, y_pred):
    # Avoid divide by 0
    y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
    # Multi-task loss
    return K.mean(K.sum(- y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred), axis=1))


from keras.models import load_model
import keras.losses
model = load_model('Tag_predictor.h5')

def predict_tags(text):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
    # Predict
    prediction = model.predict([x_test])[0]
    for i,value in enumerate(prediction):
        if value > 0.5:
            prediction[i] = 1
        else:
            prediction[i] = 0
    tags = tag_encoder.inverse_transform(np.array([prediction]))
    return tags




