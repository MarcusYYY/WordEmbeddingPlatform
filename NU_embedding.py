import pandas as pd
import urllib,urllib2,requests,numpy

class embedding:
	embedding_list = pd.read_csv('https://query.data.world/s/5beqg3omp2z0mtyxnv6tvx5ek')
	embedding_names = embedding_list['embedding_name']
	embedding_sizes = embedding_list['vocabulary size']
	embedding_dimensions = embedding_list['dimension']
	if len(embedding_list):
		print 'These are all embeddings currently avaliable.'
		print embedding_names.values
	else:
		print "No embeddings are avaliable now."

	def __init__(self,name,dimension):
		self.name = name
		self.dimension = dimension
		if name in embedding.embedding_names.values:
			url = embedding.embedding_list[embedding.embedding_names == name]['url'].values[0]
			print 'The embedding you are looking for exists. The url is',url
			if len(embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')) == 1:
				if embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')[0] != str(dimension):
					print "But the dimension you asked for does not exist."
			else:
				dimension_pool = embedding.embedding_list[embedding.embedding_names == name]['dimension'].values[0].split('_')
				if str(dimension) not in dimension_pool:
					print "But the dimension you asked for does not exist."
		else:
			print 'The embedding you are looking for does not exist'
		self.url = url
		self.size = embedding.embedding_list[embedding.embedding_names == name]['vocabulary size'].values[0]

	def download(self):
		url = self.url
		form = url.split('.')[-1]
		if form == 'zip':
			response = urllib2.urlopen(url)
			zipcontent = response.read()
			name = url.split('/')[-1]
			with open(name,'w') as f:
				f.write(zipcontent)
		else:
			r = requests.get(url)
			with open(self.name + '.txt','w') as f:
				f.write(r.content)

A = embedding('NYT_Art',100)
A.download()