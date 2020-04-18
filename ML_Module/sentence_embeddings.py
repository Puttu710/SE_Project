import os
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from sklearn import preprocessing
import spacy
EN = spacy.load('en_core_web_sm')

import logging
logging.getLogger('tensorflow').disabled = True

data = pd.read_csv('Preprocessed_data.csv')

import fasttext
fasttext_model = fasttext.load_model('embeddings.bin')

#Calculate Sentence Embeddings
def question_to_vec(question, embeddings, dim=100):
    question_embedding = np.zeros(dim)
    valid_words = 0
    for word in question.split(' '):
        if word in embeddings.words:
            valid_words += 1
            question_embedding += embeddings[word]
    if valid_words > 0:
        return question_embedding/valid_words
    else:
        return question_embedding


all_title_embeddings = []
for title in data.processed_title:
    all_title_embeddings.append(question_to_vec(title, fasttext_model))
all_title_embeddings = np.array(all_title_embeddings)

embeddings = pd.DataFrame(data = all_title_embeddings)
embeddings.to_csv('title_embeddings.csv', index=False)

