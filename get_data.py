import pymongo
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

import os
import re


load_dotenv()


def connect_to_db():
    load_dotenv()
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client.get_default_database()
    return db


def clean_readme(readme):
    header_pattern = r'^\s*#{1,6}\s+(.*)$'
    return re.sub(header_pattern, '', readme, flags=re.MULTILINE)


def split_readme_into_sentences(readme):
    cleaned_text = clean_readme(readme)
    lines = cleaned_text.split('\n')
    sentences = []
    [sentences.extend(sent_tokenize(line)) for line in lines]
    return sentences


def get_mentors():
    db = connect_to_db()
    mentors = db.users.find({
        "roles": "mentor",
        "readme": {"$exists": True},
    }, {
        "_id": 1,
        "readme": 1,
        "currentRole": 1,
    })
    return mentors


def get_mentor_sentences():
    mentors = get_mentors()
    mentor_sentences = []

    for mentor in mentors:
        sentences = split_readme_into_sentences(mentor.get('readme', ''))
        mentor_sentences.extend([{
            'sentence': sentence,
            'id': mentor['_id'] + '_' + str(index),
            'metadata': {
                '_id': mentor['_id'],
                'field': 'readme',
            }}
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


if __name__ == '__main__':
    sentences = get_mentor_sentences()
    print('Found', len(sentences), 'sentences')
