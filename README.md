# WordEmbeddingPlatform
A python library for word embedding query, selection and download.

## Quick start
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

### Getting Started

The broker file,whichlocate at data.world,contains all meta data of available pretrained word embeddings.
For now, there are 8 pretrained embeddings avaiable, we will update it if more pretrained word embeddings are created.

