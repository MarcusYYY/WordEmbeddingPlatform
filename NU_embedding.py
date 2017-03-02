import pandas as pd
import urllib,urllib2,requests,numpy,sys,os,zipfile
from scipy import spatial

def report(count, blockSize, totalSize):
	percent = float(count*blockSize*100/totalSize)
	sys.stdout.write("\r%d%%" % percent + ' complete')
	sys.stdout.flush()

class embedding:

	# load the whole list of current availiable embeddings
	embedding_list = pd.read_csv('https://query.data.world/s/5beqg3omp2z0mtyxnv6tvx5ek')
	embedding_names = embedding_list['embedding_name']
	embedding_sizes = embedding_list['vocabulary size']
	embedding_dimensions = embedding_list['dimension']
	print embedding_list['url'][4]
	if len(embedding_list):
		print 'Embeddings now avaliable.'
		print embedding_list
	else:
		print "No embedding is avaliable now."

	# initiate the embedding class and check if the embedding we want exists
	def __init__(self,name,dimension,path):
		self.name = name
		self.dimension = dimension
		self.flag = True
		if name in embedding.embedding_names.values:
			url = embedding.embedding_list[embedding.embedding_names == name]['url'].values[0]
			print 'The embedding you are looking for exists. The url is',url
			if len(embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')) == 1:
				if embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')[0] != str(dimension):
					print "But the dimension you asked for does not exist."
					self.flag = False
			else:
				dimension_pool = embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')
				if str(dimension) not in dimension_pool:
					print "But the dimension you asked for does not exist."
					self.flag = False
		else:
			print 'The embedding you are looking for does not exist'
			self.flag = False
		self.url = url
		self.size = int(embedding.embedding_list[embedding.embedding_names == name]['vocabulary size'].values[0])
		self.path = path
		self.dl = False
		self.destination = None
		self.vector = None
		self.embed = None
	# download the embeddings in the broker file on data.world and save them 
	# on the local files.

	def download(self):
		if self.flag:
			url = self.url
			form = url.split('.')[-1]
			path = self.path
			if form == 'zip':
				name = url.split('/')[-1]
				self.destination = path + name
				urllib.urlretrieve(url,path + name,reporthook = report)
				print 'The embedding directory is %s .' % self.destination
			else:
				file = pd.read_table(url)
				file.to_csv(path + self.name + '.txt',header = None, index = None ,mode = 'a',)
				self.destination = path + self.name + '.txt'
				print 'The embedding directory is %s .' % self.destination
			self.dl = True
		else:
			print "You can't download the embedding because errors happened."
		
		embed = None

		#extract embedding from zip file or txt file.
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
			for i,row in enumerate(cach):
				if i == 0:
					continue
				values = row.split()
				try:
					word = values[0]
					coefs = numpy.asarray(values[1:],dtype = 'float32')
					word_vector[word] = coefs
				except:
					continue
			self.vector = word_vector
			print 'Word embedding has been successfully downloaded.'
			return word_vector
		else:
			print "The embedding you asked for has not been successfully downloaded. "
	# pick up any number of reference words and find any number of close words in the current embedding
	
	def CloseWord_test(self,num_refer = 10,num_closeWord = 10,iter_times = 10,seed = numpy.random.randint(1000)):
		numpy.random.seed(seed)
		if self.dl:
			refer_idx = numpy.random.randint(self.size,size = num_refer,dtype = numpy.int64)
			vocab = [self.embed.split('\n')[idx].split()[0] for idx in refer_idx]
			refer_matrix = {}
			for word in vocab:
				try:
					refer_matrix[word] = embed[word]
				except:
					continue
			#find the most close num_closeWord words for every reference word
			close_word = {}
			for word in vocab:
				dist = {}
				for key,val in embed.iteritems():
					try:
						dist[key] = 1 - spatial.distance.cosine(val,refer_matrix[word])
					except:
						continue
				dist = sorted(dist,key = dist.__getitem__,reverse = True)
				ans = [key for key in dist]
				close_word[word] = ans[1:num_closeWord]
			return close_word,seed
		else:
			print 'The embedding has not been downloaded yet.'
A = embedding('NYT_Art',100,'2016Spring/')
embed = A.download()
data,seed = A.CloseWord_test(10,10,10)
print data,seed

