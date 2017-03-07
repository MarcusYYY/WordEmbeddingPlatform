# -*- coding: utf-8 -*-
import os,re
import numpy
import pandas as pd 
import urllib,urllib2,requests,sys,csv 
from gensim.models import Word2Vec



def make_signature(EMBED_DIR,seed):
	numpy.random.seed(seed)
	# fpath = 'glove.6B/25MB/Weather_Environment_Energy.txt'
	for embed in sorted(os.listdir(EMBED_DIR)):
		fpath = os.path.join(EMBED_DIR,embed)
		print embed
		if fpath.split('/')[-1] == '.DS_Store':
			continue
		model = Word2Vec.load_word2vec_format(fpath, binary=False)
		emb_vocab = list(model.vocab.keys())
		signature_idx = numpy.random.randint(0,len(emb_vocab),1000,dtype = numpy.int64)
		signature = [emb_vocab[idx] for idx in signature_idx]
		with open('signature_'+ embed,'w') as f:
			f.write(str(seed) + '\n')
			for row in signature:
				f.write(' ')
				f.write(row.encode("utf-8"))

EMBED_DIR = 'glove.6B/25MB/'
make_signature(EMBED_DIR,1337)
		
	



