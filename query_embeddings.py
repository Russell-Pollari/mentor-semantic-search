import pandas as pd
import sys

from create_embeddings import get_mentor_embeddings 


def query_mentor_embeddings(
    query,
    collection = None,
    n_results = 10,
):
    cleaned_query = query.replace('data', '')
    results = collection.query(
        query_texts=cleaned_query,
        n_results=n_results,
    )

    return results


def format_results(result):
    df = pd.DataFrame({
        'distance': result['distances'][0],
        'document': result['documents'][0],
        'doc_id': result['ids'][0],
        'userId': [metadata['_id'] for metadata in result['metadatas'][0]],
        'field': [metadata['field'] for metadata in result['metadatas'][0]],
    })

    df['profile'] = df.apply(lambda row: 'https://app.sharpestminds.com/u/' + str(row['userId']), axis=1)
    grouped_df = df.groupby('userId').agg({'document': lambda x: ', '.join(x), 'profile': 'first' })
    grouped_df['num_sentences'] = df.groupby('userId').size()

    grouped_df = grouped_df.sort_values(by=['num_sentences'], ascending=False).head(10)
    return grouped_df


if __name__ == '__main__':
    try:
        query = sys.argv[1]
    except:
        query = "healthcare analytics"

    collection = get_mentor_embeddings(collection_name="mentors_l1_distance")
    results = query_mentor_embeddings(query, collection, n_results=10)
    print(results)

    df = format_results(results)
    print (df)

