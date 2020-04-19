import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import re
import inflect
from nltk.corpus import stopwords
import spacy
EN = spacy.load('en_core_web_sm')
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

data = pd.read_csv('models/Preprocessed_data.csv')
all_title_embeddings = pd.read_csv('models/title_embeddings.csv').values
#print(all_title_embeddings)
# Import saved Wordvec Embeddings
w2v_model = gensim.models.word2vec.Word2Vec.load('models/SO_word2vec_embeddings.bin')

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

