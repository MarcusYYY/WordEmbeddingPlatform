import pandas as pd
import urllib,urllib2,requests

class embedding:
	embedding_list = pd.read_csv('https://query.data.world/s/5beqg3omp2z0mtyxnv6tvx5ek')
	embedding_names = embedding_list['embedding_name']
	embedding_sizes = embedding_list['vocabulary size']
	embedding_dimensions = embedding_list['dimension']
	print 'All embeddings currently avaliable.'
	print embedding_names.values

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

	def download(self):
		url = self.url
		form = url.split('.')[-1]
		if form == 'zip':
			response = urllib2.urlopen(url)
			zipcontent = response.read()
			name = url.split('/')[-1]
			print name
			with open(name,'w') as f:
				f.write(zipcontent)
		else:
			r = requests.get(url)
			with open(self.name + '.txt','w') as f:
				f.write(r.content)


A = embedding('NYT_Art',100)
