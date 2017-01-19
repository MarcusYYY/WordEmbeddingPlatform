import re
from scipy import spatial

#set up dictionaries of different word embeddings
words_glove_25 = {}
words_text_25 = {}
words_glove_50 = {}
words_text50 = {}
words_text8_50 = {}
glove_6b_50d = {}

path_all = ['glove.twitter.27B-glove.twitter.27B.25d.txt','text_emb_25.txt','glove.twitter.27B-glove.twitter.27B.50d.txt','text_emb_50.txt','text8_emb.txt','glove.6B-glove.6B.50d.txt']

for path in path_all:
	words = {}
	file = open(path)
	
	for row in file:
		items = row.split(' ')
		word = items[0]
		num = []
		for idx in range(1,len(items)):
			num.append(float(items[idx]))
		if not words.has_key(word):
			words[word] = num

	if path == 'glove.twitter.27B-glove.twitter.27B.25d.txt':
		words_glove_25 = words
	elif path == 'text_emb_25.txt':
		words_text_25 = words
	elif path == 'glove.twitter.27B-glove.twitter.27B.50d.txt':
		words_glove_50 = words
	elif path == 'text_emb_50.txt':
		words_text50 = words
	elif path == 'text8_emb.txt':
		words_text8_50 = words
	else:
		glove_6b_50d = words



#cosine similarity between twitter_glove25d and text25d
distance = 0
for keys in words_text_25:
	if words_glove_25.has_key(keys):
		dist = spatial.distance.cosine(words_text_25[keys],words_glove_25[keys])
		distance = distance + dist
print 'cosine similarity between glove.twitter.27B-glove.twitter.27B.25d.txt and text_emb_25 '
print distance

#cosine similarity between twitter_glove50d and text50d
distance = 0
for keys in words_text50:
	if words_glove_50.has_key(keys):
		dist = spatial.distance.cosine(words_text50[keys],words_glove_50[keys])
		distance = distance + dist
print 'cosine similarity between glove.twitter.27B-glove.twitter.27B.50d.txt and text_emb_50 '
print distance

#cosine similarity between glove.6b_50d and text8_50d
distance = 0
for keys in words_text50:
	if glove_6b_50d.has_key(keys):
		dist = spatial.distance.cosine(glove_6b_50d[keys],words_text50[keys])
		distance = distance + dist
print 'cosine similarity between glove.6B-glove.6B.50d and text_emb_50 '
print distance

#cosine similarity between twitter_glove50d and text8_50d
distance = 0
for keys in words_text8_50:
	if words_glove_50.has_key(keys):
		dist = spatial.distance.cosine(words_text8_50[keys],words_glove_50[keys])
		distance = distance + dist
print 'cosine similarity between glove.twitter.27B-glove.twitter.27B.50d.txt and text8_emb '
print distance

#cosine similarity between glove.6b_50d and text8_50d
distance = 0
for keys in words_text8_50:
	if glove_6b_50d.has_key(keys):
		dist = spatial.distance.cosine(glove_6b_50d[keys],words_text8_50[keys])
		distance = distance + dist
print 'cosine similarity between glove.6B-glove.6B.50d and text8_emb '
print distance
