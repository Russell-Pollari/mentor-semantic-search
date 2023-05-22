from typing import List
import chromadb  # type: ignore
from chromadb.utils import embedding_functions  # type: ignore
from chromadb.api.models import Collection  # type: ignore

import argparse

from get_data import get_mentor_sentences


PERSIST_DIRECTORY = '.db'
EMBD_FNC = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-mpnet-base-v2")


def get_chroma_client() -> chromadb.Client:
    chroma_client = chromadb.Client(chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=PERSIST_DIRECTORY,
    ))

    return chroma_client


def create_mentor_embeddings(
        mentor_sentences: List[dict],
        collection_name: str = 'mentors') -> Collection:
    chroma_client = get_chroma_client()

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=EMBD_FNC,
        metadata={
            "hnsw:space": "cosine",
        },
    )

    collection.add(
        ids=[mentor['id'] for mentor in mentor_sentences],
        documents=[mentor['sentence'] for mentor in mentor_sentences],
        metadatas=[mentor['metadata'] for mentor in mentor_sentences],
    )

    return collection


def get_mentor_embeddings(collection_name: str = 'mentors') -> Collection:
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(
        name=collection_name,
        embedding_function=EMBD_FNC)
    return collection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create mentor embeddings')
    parser.add_argument('--collection-name',
                        help='Name of the collection',
                        default='mentors')

    args = parser.parse_args()

    mentor_sentences = get_mentor_sentences()

    print('Creating collection {} for {} sentences'.format(
        args.collection_name,
        len(mentor_sentences)))

    collection = create_mentor_embeddings(
        mentor_sentences,
        collection_name=args.collection_name)
