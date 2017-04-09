# WordEmbeddingPlatform
A python library for word embedding query, selection and download.

### Prerequsite
Before downloading this library, you might want to install datadotworld library first since this platform works
with data.world.
You can install it using `pip`  directly from this github repo:
```
pip install git+git://github.com/datadotworld/data.world-py.git
```
### Configure
You may want to set datadotworld up with your access token.
To do that, run the following command:
```
dw configure
```
Your API token can be obtained on data.world under [Settings > Advanced]
(https://data.world/settings/advanced )

### Check embeddings

The broker file,which is at data.world,contains all meta data of available pretrained word embeddings.
For now, there are 8 pretrained embeddings avaiable, we will update it if more pretrained word embeddings are created.
The `check()`  method facilitates showing info of current word embeddings.
For example:
```python
>>>import Embedding_platform as ep
>>>ep.check()
embedding_name                                        agriculture_40
dimension                                                        100
vocabulary size                                                19007
url                https://query.data.world/s/ewf2464mqcr7tyiatbh...
table                                                 agriculture_40
file_format                                                      csv
```
We only use one embedding to illustrate the broker file structure.

### Query embeddings
The `query_embeddings(table,world)` method provides users a convenient way to query the word embedding for specified table and word.
For example
```python
>>>print ep.query_embeddings('agriculture_40','the')
['the', -1.004704, 0.037287, -0.016309, -0.088428, -1.1478, 0.331032, -0.77213, -0.07757, -0.874058, 
-1.170626, -0.253766, 1.137803, 1.045363, 2.386086, 0.229137, 0.272712, -0.334886, -1.015797, 0.662011, 
-0.472902, -0.333736, 1.604692, 0.924259, 0.707687, -0.153192, 1.007494, 1.09558, -1.159106, 0.88615, 
1.214197, -1.345269, -2.309988, 0.581767, -2.040186, 0.019013, -0.090971, -0.690396, 1.578381, -0.441838, 
0.968358, 0.865741, -1.263163, -0.829032, -0.313665, 0.138191]
```
### Embedding extraction
The `EmbedExtract(file_dir,table,pad,check,download)` method aims to extract overlap word vectors in the pretrained embeddings given raw text input.Argument `file_dir` is the absoulte path of text input, `table` is the name of embeddings stored on data.world. If `pad = True` ,the method will add those words which do not appear in the embedding but exist in raw input. If `check = True`, it means the results of the extracted embedding will be shown on the screen and the lib will download the extracted embedding if `download = True`.
For example
```python
>>>ep.EmbedExtract(file_dir ='/Users/Desktop/input_corpora' ,table ='agriculture_40',pad = True,check = True,download = True)
```
### Embedding initiation and download
For example
```python
>>>A = ep.embedding('agriculture_40',100)
The embedding you are looking for exists. The url is https://query.data.world/s/enfkzx0yrnxevzcy9m7fm81hi
>>>print A.name
agriculture_40
>>>print A.dimension
100
>>>A.download(path = 'Embedding/')
The embedding path is /Users/Embedding_platform/Embedding/agriculture_40.csv .
Word embedding has been successfully downloaded.
Check the vector attribute by using embedding_name.vector
```
### Embedding selection
The `method_a(inp_dir,num_sig,num_sig_embedding,num_stopwords)` is an embedding selection method based on[.......].
`inp_dir` is the path of input corpora.`num_sig` means the number of words chosen as signature of the input corpora. `num_sig_embedding` indicates the number of words picked as signature of the pretrained embedding. And`num_stopwords` is the number of stopwords we ignore in this method.
For example
```python
>>>INPUT_DIR = '/Users/Marcus/Desktop/Archive/Maas_IMDB'
>>>ep.method_a(inp_dir = INPUT_DIR,num_sig = 5000,num_sig_embedding = 5000,num_stopwords = 100)
100 most frequent words will be removed as stop words.
Pick up 5000 top frequent words as signature of all avaliable embeddings.
Fetching agriculture_40 embeddings and creating its signature.
Fetching art_40 embeddings and creating its signature.
Fetching books_40 embeddings and creating its signature.
Fetching econ_40 embeddings and creating its signature.
Fetching govt_40 embeddings and creating its signature.
Fetching movies_40 embeddings and creating its signature.
Fetching weather_40 embeddings and creating its signature.
Processing High Density Vocabulary list.
Assembled High Density Vocabulary found in at least  85.0  percent of embeddings.
Pick top 5000 most frequently occurring words in the corpus as signature. 
[('movies_40', 2892.3935935935065),
 ('books_40', 2915.7785785784804),
 ('art_40', 3016.7237237236086),
 ('agriculture_40', 3236.933733733591),
 ('govt_40', 3243.128928928771),
 ('weather_40', 3267.9365365363774),
 ('econ_40', 3275.4096096094536)]
 The best pretrained embedding is econ_40.
 ```
 


