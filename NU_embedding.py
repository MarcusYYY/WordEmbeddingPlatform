import pandas as pd
import urllib,urllib2,requests,numpy,sys,os,zipfile

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
		self.size = embedding.embedding_list[embedding.embedding_names == name]['vocabulary size'].values[0]
		self.path = path
		self.dl = False
		self.destination = None

	# download the embeddings in the broker file on data.world

	def download(self):
		if self.flag:
			url = self.url
			form = url.split('.')[-1]
			path = self.path
			if form == 'zip':
				name = url.split('/')[-1]
				self.destination = path + name
				print self.destination
				urllib.urlretrieve(url,path + name,reporthook = report)
			else:
				file = pd.read_table(url)
				file.to_csv(path + self.name + '.txt',header = None, index = None ,mode = 'a',)
				self.destination = path + name + '.txt'
			self.dl = True
		else:
			print "You can't download the embedding because errors happened."

	# pick any number of reference words and find any number of close words in the current embedding
	def Reference_word(self,num_refer,num_closeWord,num_sample = 10):
		embed = None
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
		return embed
	
A = embedding('glove.6B',100,'2016Spring/')
A.download()
data = A.Reference_word(100,100,10)
