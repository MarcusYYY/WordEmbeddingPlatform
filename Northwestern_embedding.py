import pandas as pd
import urllib,urllib2,requests,numpy,sys,os,zipfile,gensim,string,collections,re,nltk,requests
from scipy import spatial
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize,word_tokenize
from datadotworld import DataDotWorld

def report(count, blockSize, totalSize):
	percent = float(count*blockSize*100/totalSize)
	sys.stdout.write("\r%d%%" % percent + ' complete')
	sys.stdout.flush()

# SQL query for specific word embedding in given table
def query_embeddings(table,word):
	dataset_ = "marcusyyy/test-for-python-lib"
	client = DataDotWorld(token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50Om1hcmN1c3l5eSIsImlzcyI6ImFnZW50Om1hcmN1c3l5eTo6MDhmZDM1MzYtOWY3NC00MzhiLTliZDQtMDJlYzg2NjIzOTYyIiwiaWF0IjoxNDg0MzQ3MzEzLCJyb2xlIjpbInVzZXJfYXBpX3dyaXRlIiwidXNlcl9hcGlfcmVhZCJdLCJnZW5lcmFsLXB1cnBvc2UiOnRydWV9.Wu4joO62ZbheE7GwUcY5sK0HvLn9v6xl3srKRiu85thGjsrDS5pYwo0glop06j2KvodI7h3sQShneSV7TjnSFg")
	query_ = 'SELECT * FROM ' + table + " where `Column A` = '" + word + "'"
	try:
		results = client.query(dataset=dataset_, query=query_)
		vector = results.as_string().split('\n')[1]
		print vector
		result = {}
		key = str(vector.split(',')[0])
		array = numpy.asarray(vector.split(',')[1:],dtype = 'float32')
		result[key] = array
		return result
	except RuntimeError,e:
		print e

# Get the subset of the pretrained embeddings according to the raw text input.
def EmbedExtract(file_dir,table,batch = 240):
	with open(file_dir) as f:
		input_txt = []
		sentences = sent_tokenize(f.read())
		for s in sentences:
			tokens = word_tokenize(s)
			input_txt = input_txt + tokens
		inp_vocab = set(input_txt)
		inp_vsize = (len(inp_vocab))
	f.close()
	dataset_ = "marcusyyy/test-for-python-lib"
	client = DataDotWorld(token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50Om1hcmN1c3l5eSIsImlzcyI6ImFnZW50Om1hcmN1c3l5eTo6MDhmZDM1MzYtOWY3NC00MzhiLTliZDQtMDJlYzg2NjIzOTYyIiwiaWF0IjoxNDg0MzQ3MzEzLCJyb2xlIjpbInVzZXJfYXBpX3dyaXRlIiwidXNlcl9hcGlfcmVhZCJdLCJnZW5lcmFsLXB1cnBvc2UiOnRydWV9.Wu4joO62ZbheE7GwUcY5sK0HvLn9v6xl3srKRiu85thGjsrDS5pYwo0glop06j2KvodI7h3sQShneSV7TjnSFg")
	query_ = ''
	final_result = []
	back_query = ''
	print 'Embedding extraction begins.'
	words = list(inp_vocab)
	i = 0
	back_up_i = 0
	while i < len(words):
		if i == 0:
			query_ = 'SELECT * FROM ' + table + " where `Column A` = '" + words[i] + "'"
		elif i % batch == 0:
			process = str((i)*100/len(words))
			try:
				results = client.query(dataset=dataset_, query=query_)
				print process + "%" + ' has been completed.'
				back_query = query_
				back_up_i = i
			except RuntimeError,e:
				i = back_up_i
				print 'Batch size ' + str(batch)
				batch = int(batch * 0.9)
				if batch == 0:
					print "404 Error"
					break
				print 'Batch size too large. Reducing to ' + str(batch)
				continue
			vector = results.as_string().split('\n')[1:]
			final_result.extend(vector)
			query_ = 'SELECT * FROM ' + table + " where `Column A` = '" + words[i] + "'"
		else:
			query_ = query_ + " OR `Column A` = '" + words[i] + "'"
		i = i + 1
	print 'Embedding successfully extracted.'
	final_result = str('\r'.join(final_result))
	ans = final_result.split('\r')
	overlap_words = []
	for word in ans:
		overlap_words.append(word.split(',')[0])
	int_count = int(len(set.intersection(set(overlap_words),set(words))))
	missing_words = str(len(words) - int_count)
	percent = str(int_count * 100 / len(words))
	print 'There are ' + missing_words + " tokens that can't be found in this pretrained word embedding."
	print percent + "%" + " words can be found in this pretrained word embedding."
	return final_result

class embedding:
	# Initiate the embedding class and check if the embedding we want exists
	def __init__(self,name=None,dimension=None,path=None):
		# Load the whole list of current availiable embeddings
		embedding_list = pd.read_csv('https://query.data.world/s/7786jpst5l8zq6gpow2aqe1mw')
		embedding_names = embedding_list['embedding_name']
		embedding_sizes = embedding_list['vocabulary size']
		embedding_dimensions = embedding_list['dimension']
		embedding_score = 0
		if name == None:
			if len(embedding_list):
				print 'Embeddings now avaliable.'
				print embedding_list
			else:
				print "No embedding is avaliable now."

		self.name = name
		self.dimension = dimension
		self.flag = True
		if name in embedding_names.values:
			url = embedding_list[embedding_names == name]['url'].values[0]
			print 'The embedding you are looking for exists. The url is',url
			self.url = url
			if len(embedding_list[embedding_names == name]['dimension'].values[0].split('_')) == 1:
				if embedding_list[embedding_names == name]['dimension'].values[0].split('_')[0] != str(dimension):
					print "But the dimension you asked for does not exist."
					self.flag = False
			else:
				dimension_pool = embedding_list[embedding_names == name]['dimension'].values[0].split('_')
				if str(dimension) not in dimension_pool:
					print "But the dimension you asked for does not exist."
					self.flag = False
		else:
			print 'The embedding you are looking for does not exist.'
			self.flag = False
		if self.flag:
			try:
				self.size = int(embedding_list[embedding_names == name]['vocabulary size'].values[0])
			except:
				if embedding_list[embedding_names == name]['vocabulary size'].values[0][-1] == 'K':
					num = embedding_list[embedding_names == name]['vocabulary size'].values[0][:-1]
					num = int(num) * 1000
					embedding_list[embedding_names == name]['vocabulary size'].values[0] = num
				else:
					num = embedding_list[embedding_names == name]['vocabulary size'].values[0][:-1]
					num = int(num) * 1000000
					embedding_list[embedding_names == name]['vocabulary size'].values[0] = num
			self.path = path
			self.dl = False
			self.destination = None
			self.vector = None
			self.embed = None
			self.table = embedding_list['table'][embedding_names == name]

	# Download the embeddings in the broker file on data.world and save them 
	# on the local files.
	def download(self,file_format):
		if self.flag:
			url = self.url
			path = self.path
			if file_format == 'zip':
				name = url.split('/')[-1]
				if not os.path.exists(path):
					os.makedirs(path)
				urllib.urlretrieve(url,path + name,reporthook = report)
				self.destination = path + name
				print self.destination
				print 'The embedding path is %s .' % self.destination
			else:
				if file_format == 'txt':
					if not os.path.exists(path):
						os.makedirs(path)
					r = requests.get(url,stream = True)
					self.destination = path + self.name + '.txt'
					with open(self.destination,'wb') as f:
						for chunk in r.iter_content(chunk_size = 1024):
							if chunk:
								f.write(chunk)
					print 'The embedding path is %s .' % self.destination
				elif file_format == 'csv':
					if not os.path.exists(path):
						os.makedirs(path)
					self.destination = path + self.name + '.csv'
					df = pd.read_csv(self.url)
					df.to_csv(self.destination,index = False)
					print 'The embedding path is %s .' % self.destination
			self.dl = True
		else:
			print "You can't download the embedding because errors happened."
		
		embed = None
		#Extract embedding from zip file or txt file.
		if self.dl:
			if zipfile.is_zipfile(self.destination):
				zf = zipfile.ZipFile(self.destination,'r')
				names = zf.namelist()
				if len(names) != 1:
					dimension = self.dimension
					for filename in names:
						try:
							data = zf.read(filename)
							dimension_of_embed = data.split('\n')[1].split(' ')
							if len(dimension_of_embed) == dimension + 1:
								embed = data
						except KeyError:
							print 'ERROR: Did not find %s in zip file' % filename
				else:
					embed = zf.read(names[0])
			else:
				file = open(self.destination)
				embed = file.read()
			self.embed = embed
			#store the word vector into dictionary
			word_vector = {}
			cach = embed.split('\n')
			for num,row in enumerate(cach):
				if file_format == 'csv':
					values = row.split(',')
				else:
					values = row.split()
				if len(values) < 3:
					continue
				try:
					word = values[0]
					coefs = numpy.asarray(values[1:],dtype = 'float32')
					word_vector[word] = coefs
				except:
					continue
			self.vector = word_vector
			print 'Word embedding has been successfully downloaded.'
			print 'And you can use YourEmbeddingName.vector to check it.'
			return word_vector
		else:
			print "The embedding you asked for has not been successfully downloaded. "
	
	# embedding selection by numbers of signature words overlap		
	def EmbedSelect(self,file_dir):
		with open(file_dir) as f:
			input_txt = []
			sentences = sent_tokenize(f.read())
			for s in sentences:
				tokens = word_tokenize(s)
				input_txt = input_txt + tokens
			inp_vocab = set(input_txt)
	        inp_vsize = (len(inp_vocab))
		f.close()
		signature_dir = embedding.embedding_list['signature']
		emb_sign_url = ''
		for item in signature_dir:
			if pd.notnull(item):
				embed = pd.read_csv(item,header = None)
				embed = embed.values[1].tolist()
				embed = set(embed[0].split(' ')[1:])
				int_count = float(len(set.intersection(embed,inp_vocab)))
				if int_count > embedding.embedding_score:
					embedding.embedding_score = int_count
					emb_sign_url = item
		return str(embedding.embedding_list['embedding_name'][signature_dir == emb_sign_url].values[0])
