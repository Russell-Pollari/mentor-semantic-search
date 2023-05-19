## Installation

Clone this repo and install dependencies
```
$ pip install requirements.txt
```

## Usage

### Create embeddings
```
$ python create_embeddings.py <path_to_json>
```
where <path_to_json> is a json file with mentor data

embedding collection is saved in .db folder


### Query embeddings
```
$ python query_embeddings.py <query>
```
where `query` is a string

-----

See also: eda.pynb for API usage
