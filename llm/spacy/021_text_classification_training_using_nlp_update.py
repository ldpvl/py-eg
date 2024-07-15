import spacy
import os
import pandas as pd

from spacy.training import Example
from spacy.lang.en import English


# https://spacy.io/api/language#update
# Changed in v3.0
# The Language.update method now takes a batch of Example objects instead of the raw texts and annotations or Doc
# and GoldParse objects. An Example streamlines how data is passed around. It stores two Doc objects: one for holding
# the gold-standard reference data, and one for holding the predictions of the pipeline.
#
# For most use cases, you shouldn't have to write your own training scripts anymore.
# Instead, you can use spacy train with a config file and custom registered functions if needed.
# See the training documentation for details.


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
WIKI_QA_CORPUS_DIR = os.path.join(SCRIPT_DIR, 'resources', 'WikiQACorpus')

tsv_to_df = lambda filename: pd.read_csv(os.path.join(WIKI_QA_CORPUS_DIR, filename), sep='\t')


# TextCategorizer does not use features from other pipeline components, so we start with a blank model
# nlp = spacy.blank('en')
nlp = English()

nlp.add_pipe('textcat') # single label


def generate_train_examples(doc_limit=100):
    doc_count = 0

    for index, row in tsv_to_df('WikiQA-train.tsv').iterrows():
        doc_count += 1
        doc = nlp.make_doc(row['Sentence'])
        annotations = {'cats': {row['DocumentTitle']: 1.0}}

        yield Example.from_dict(doc, annotations)

        if doc_limit and doc_limit == doc_count:
            break


def train():
    train_examples = list(generate_train_examples())
    optimizer = nlp.initialize(get_examples=lambda: train_examples)

    for i in range(20):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)
        print(f'Losses {losses}')


train()
test_text = "It's very cold in a glacier cave"
doc = nlp(test_text)
print(f'After training {doc.cats}')


