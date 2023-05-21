## Installation

Clone this repo and install dependencies
```
$ pip install -r requirements.txt
```

Create .env file 
```
MONGO_URI=<mongodb_connection_string>
```

## Usage

### Create embeddings
```
usage: create_embeddings.py [-h] [--path-to-data PATH_TO_DATA] [--collection-name COLLECTION_NAME]

Create mentor embeddings

optional arguments:
  -h, --help            show this help message and exit
  --collection-name COLLECTION_NAME
                        Name of the collection
```


### Query embeddings
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
