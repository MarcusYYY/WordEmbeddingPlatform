from __future__ import print_function
import os
import numpy as np
import keras
np.random.seed(1360)
from keras.preprocessing.text import Tokenizer
import sys
from scipy import spatial


BASE_DIR = ''
GLOVE_DIR = BASE_DIR + 'glove.6B/'
TEXT_DATA_DIR = BASE_DIR + '20_newsgroup'
MAX_NB_WORDS = 2000

#compute the overlap close words of same word in different embeddings 
def Score_similarity(ref_1,ref_2):
    score = 0
    for word in ref_1.keys():
        for close_word in ref_1[word]:
            if close_word in ref_2[word]:
                score = score + 1
    return score

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'full_v3.txt'))
count = 0
for line in f:
    if count == 0:
        count = count + 1
        continue
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    except:
        continue
f.close()

texts = []  # list of text samples
labels_index = {}  # dictionary mapping label name to numeric id
labels = []  # list of label ids
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    if os.path.isdir(path):
        label_id = len(labels_index)
        labels_index[name] = label_id
        for fname in sorted(os.listdir(path)):
            if fname.isdigit():
                fpath = os.path.join(path, fname)
                if sys.version_info < (3,):
                    f = open(fpath)
                else:
                    f = open(fpath, encoding='latin-1')
                texts.append(f.read())
                f.close()
                labels.append(label_id)

# finally, vectorize the text samples into a 2D integer tensor
tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
word_index = tokenizer.word_index

word_rank = sorted(word_index,key = word_index.__getitem__)
indices = np.arange(len(word_index)/100)
np.random.shuffle(indices)
idx = indices[:10]
reference = [word_rank[i] for i in idx]

#fetch the word vector of reference words
count = 0
reference_matrix = {}
for word in reference:
    try:
        reference_matrix[word] = embeddings_index[word]
    except:
        continue

#find the most close 10 word for every reference word
close_word = {}

for word in reference:
    dist = {}
    for key, val in embeddings_index.iteritems():
        try:
            dist[key] = 1 - spatial.distance.cosine(val,reference_matrix[word])
        except:
            continue
    dist = sorted(dist,key = dist.__getitem__,reverse = True)
    ans = [key for key in dist]
    close_word[word] = ans[1:200]

final_ans = []
for path in os.listdir(GLOVE_DIR + '25MB'):
    embeddings_index_ = {}
    f = open(os.path.join(GLOVE_DIR + '25MB/', path))
    count = 0
    for line in f:
        if count == 0:
            count = count + 1
            continue
        values = line.split()
        word = values[0]
        try:
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index_[word] = coefs
        except:
            continue
    f.close()
    close_word_ = {}
    for word in reference:
        dist = {}
        for key, val in embeddings_index_.iteritems():
            try:
                dist[key] = 1 - spatial.distance.cosine(val,embeddings_index_[word])
            except:
                continue
        dist = sorted(dist,key = dist.__getitem__,reverse = True)
        ans = [key for key in dist]
        close_word_[word] = ans[1:200]
    final_ans.append(path)
    final_ans.append(Score_similarity(close_word,close_word_))
print(final_ans)

