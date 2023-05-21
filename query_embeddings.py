import pandas as pd
from chromadb.api.types import QueryResult  # type: ignore

import argparse

from create_embeddings import get_mentor_embeddings


def query_mentor_embeddings(
    query: str,
    collection=None,
    n_results: int = 10,
) -> QueryResult:
    cleaned_query = query.replace('data', '')

    results = collection.query(
        query_texts=cleaned_query,
        n_results=n_results,
    )

    return results


def format_results(result: QueryResult) -> pd.DataFrame:
    df = pd.DataFrame({
        'distance': result['distances'][0],
        'document': result['documents'][0],
        'doc_id': result['ids'][0],
        'userId': [metadata['_id'] for metadata in result['metadatas'][0]],
        'field': [metadata['field'] for metadata in result['metadatas'][0]],
    })

    df['profile'] = df.apply(
        lambda row: 'https://app.sharpestminds.com/u/' + str(row['userId']),
        axis=1)
    grouped_df = df.groupby('userId').agg({
        'document': lambda x: ', '.join(x),
        'profile': 'first'
    })
    grouped_df['num_sentences'] = df.groupby('userId').size()

    grouped_df = grouped_df.sort_values(by=['num_sentences'], ascending=False)

    return grouped_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query mentor embeddings')
    parser.add_argument('--query',
                        default="healthcare analytics",
                        help='Query to run')
    parser.add_argument('--collection-name',
                        default="mentors_l1_distance",
                        help='Name of collection to query')
    parser.add_argument('--n-results',
                        default=10,
                        help='Number of results to return')
    args = parser.parse_args()

    collection = get_mentor_embeddings(collection_name=args.collection_name)
    results = query_mentor_embeddings(args.query, collection)
    df = format_results(results)
    print(df)
