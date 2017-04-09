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
The `check()`  mehtod facilitates showing info of current word embeddings.
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
`query_embedding(table,word)` method provides users to directly query specific word embedding if given table and word.
For example:
```python



