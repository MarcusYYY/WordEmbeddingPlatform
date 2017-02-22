import numpy as np
import os

BASE_DIR = ''
GLOVE_DIR = BASE_DIR + 'glove.6B/'
TEXT_DATA_DIR = BASE_DIR + '20_newsgroup'

embeddings_index_100 = {}

f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'))
count = 0
for line in f:
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float')
        embeddings_index_100[word] = coefs
    except:
        continue
f.close()

embeddings_index_300 = {}
f = open(os.path.join(GLOVE_DIR, 'glove.6B.300d.txt'))
count = 0
for line in f:
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float')
        embeddings_index_300[word] = coefs
    except:
        continue
f.close()

embeddings_index_400 = {}
for key,val in embeddings_index_100.iteritems():
	embeddings_index_400[key] = list(np.concatenate((embeddings_index_100[key],embeddings_index_300[key]),axis = 0))
file = open('glove.6B.400d.txt','w')
count = 0
for key,val in embeddings_index_400.iteritems():
	if count > 100:
		break
	file.write('%s '% key)
	idx = 0
	for num in embeddings_index_400[key]:
		file.write('{0} '.format(num))
		idx = idx + 1
		if idx == 400:
			file.write('\n')
	count = count + 1

