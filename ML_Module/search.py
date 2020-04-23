import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import re
import inflect
from nltk.corpus import stopwords
import spacy
EN = spacy.load('en_core_web_sm')
from sklearn.preprocessing import MultiLabelBinarizer
import nltk

def tokenize_text(text):
    "Apply tokenization using spacy to docstrings."
    tokens = EN.tokenizer(text)
    return [token.text.lower() for token in tokens if not token.is_space]

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = nltk.stem.lancaster.LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def normalize(words):
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    return words

def tokenize_code(text):
    "A very basic procedure for tokenizing code strings."
    return RegexpTokenizer(r'\w+').tokenize(text)

def preprocess_text(text):
    return ' '.join(normalize(tokenize_text(text)))

data = pd.read_csv('Preprocessed_data.csv')
all_title_embeddings = pd.read_csv('title_embeddings.csv').values

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

#print(all_title_embeddings)
# Import saved Wordvec Embeddings
w2v_model = gensim.models.word2vec.Word2Vec.load('SO_word2vec_embeddings.bin')

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

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
keras.losses.multitask_loss = multitask_loss
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


def question_to_vec(question, embeddings, dim=300):
    question_embedding = np.zeros(dim)
    valid_words = 0
    for word in question.split(' '):
        if word in embeddings:
            valid_words += 1
            question_embedding += embeddings[word]
    if valid_words > 0:
        return question_embedding/valid_words
    else:
        return question_embedding

def searchresults(search_string, num_results):
    search_string = preprocess_text(search_string)
    search_vect = np.array([question_to_vec(search_string, w2v_model)])
    
    search_results = []
    cosine_similarities = pd.Series(cosine_similarity(search_vect, all_title_embeddings)[0]) 
    #cosine_similarities = cosine_similarities*(0.4*data.overall_scores + 0.1*(data.sentiment_polarity))

    for i,j in cosine_similarities.nlargest(int(num_results)).iteritems():
        output = ''
        for t in data.question_content[i][:200].split():
            if t.lower() in search_string:
                output += " <b style='color: #464646'>"+str(t)+"</b>"
            else:
                output += " "+str(t)
        temp = {
            'title': str(data.original_title[i]),
            'url': str(data.question_url[i]),
            'tags': str(data.tags[i]),
            'similarity_score': str(j)[:5],
            'votes': str(data.overall_scores[i]),
            'body':str(output)
        }
        search_results.append(temp)
    return search_results

