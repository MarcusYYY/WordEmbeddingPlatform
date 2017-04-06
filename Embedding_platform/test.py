import Northwestern_embedding as Nu

# Nu.check()
# Nu.query_embeddings('arts_40','you')
# Nu.EmbedExtract(file_dir ='/Users/Marcus/Desktop/reuters/reutersR8_all' ,table ='ArtDanceMusic',pad = True)
a = Nu.embedding('agriculture_40',100)
a.download()
# print a.vector
# Nu.HighDensityVocab()
# Nu.RankVocabGenerator()
#Nu.method_a('/Users/Marcus/Desktop/reuters/reutersR8_all',5000,5000,200)
