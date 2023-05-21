from nltk.tokenize import sent_tokenize
import chromadb
from chromadb.utils import embedding_functions

import re
import json
import sys
import argparse


EMBD_FNC = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
PERSIST_DIRECTORY = '.db'


def clean_readme(readme):
    header_pattern = r'^\s*#{1,6}\s+(.*)$'
    return re.sub(header_pattern, '', readme, flags=re.MULTILINE)


def split_into_sentences(text):
    cleaned_text = clean_readme(text)
    lines = cleaned_text.split('\n')
    sentences = []
    [sentences.extend(sent_tokenize(line)) for line in lines]
    return sentences


def camelcase_to_natural_language(camelcase_string):
    spaced_string = re.sub(r'(?<!^)(?=[A-Z])', ' ', camelcase_string)
    natural_language = spaced_string.capitalize()
    
    return natural_language


def tags_to_sentences(tags, prefix = "I have experience with "):
    return [prefix + camelcase_to_natural_language(tag) for tag in tags]


def load_json(path_to_file):
    with open(path_to_file) as f:
        return json.load(f)


def get_mentor_sentences(path_to_file):
    mentors = load_json(path_to_file)
    mentor_sentences = []

    for mentor in mentors:
        sentences = split_into_sentences(mentor.get('readme', ''))
        mentor_sentences.extend([{
            'sentence': sentence,
            'id': mentor['_id'] + '_' + str(index),
            'metadata': {
                '_id': mentor['_id'],
                'field': 'readme',
            }
        }
            for index, sentence in enumerate(sentences)
        ])

        if mentor.get('currentRole') is not None:
            mentor_sentences.append({
                'sentence': mentor['currentRole'],
                'id': mentor['_id'] + '_currentRole',
                'metadata': {
                    '_id': mentor['_id'],
                    'field': 'currentRole',
                }
            })   

    return mentor_sentences


def get_chroma_client():
    chroma_client = chromadb.Client(chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=PERSIST_DIRECTORY,
    ))

    return chroma_client


def create_mentor_embeddings(mentor_sentences, collection_name="mentors"):
    chroma_client = get_chroma_client()

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=EMBD_FNC,
        # metadata={
        #     "hnsw:space": "cosine",
        #     "hnsw:construction_ef": "20",
        #     "hnsw:M": "20",
        # } 
    )

    collection.add(
        ids=[mentor['id'] for mentor in mentor_sentences],
        documents=[mentor['sentence'] for mentor in mentor_sentences],
        metadatas=[mentor['metadata'] for mentor in mentor_sentences],
    )

    return collection


def get_mentor_embeddings(collection_name="mentors"):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(name=collection_name, embedding_function=EMBD_FNC)
    return collection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create mentor embeddings')
    parser.add_argument('--path-to-data', help='Path to the data directory', default='data/mentors.json')
    parser.add_argument('--collection-name', help='Name of the collection', default='mentors')

    args = parser.parse_args()
    
    mentor_sentences = get_mentor_sentences(args.path_to_data)

    print ('Creating collection {} for {} sentences'.format(args.collection_name, len(mentor_sentences)))

    collection = create_mentor_embeddings(mentor_sentences, collection_name=args.collection_name)