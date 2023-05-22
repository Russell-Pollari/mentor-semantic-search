# Installation

Clone this repo and install dependencies
```
$ pip install -r requirements.txt
```

Create .env file 
```
MONGO_URI=<mongodb_connection_string>
CHROMA_API_IMPL=rest
CHROMA_SERVER_HOST=<host IP address>
CHROMA_SERVER_HTTP_PORT=8000

```

# Usage

## Start Chroma server

**Local sever with docker**   
`docker-compose up -d --build`

Then set `CHROMA_SERVER_HOST=localhost`

**Quick and dirty AWS deployment**

See https://docs.trychroma.com/deployment

`aws cloudformation create-stack --stack-name my-chroma-stack --template-url https://s3.amazonaws.com/public.trychroma.com/cloudformation/latest/chroma.cf.json`


Get the host ip address
`aws cloudformation describe-stacks --stack-name my-chroma-stack --query 'Stacks[0].Outputs'`

And set `CHROMA_SERVER_HOST=<IP address>`

## Create embeddings
```
usage: create_embeddings.py [-h] [--path-to-data PATH_TO_DATA] [--collection-name COLLECTION_NAME]

Create mentor embeddings

optional arguments:
  -h, --help            show this help message and exit
  --collection-name COLLECTION_NAME
                        Name of the collection
```


## Query embeddings
```
usage: query_embeddings.py [-h] [--collection-name COLLECTION_NAME] [--query QUERY]
                           [--n-results N_RESULTS]

Query mentor embeddings

optional arguments:
  -h, --help            show this help message and exit
  --collection-name COLLECTION_NAME
                        Name of collection to query
  --query QUERY         Query to run
  --n-results N_RESULTS
                        Number of results to return

```
