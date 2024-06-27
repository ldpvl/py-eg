import spacy
import pandas as pd
import os

from spacy.tokens import DocBin


pd.options.display.max_columns = None
pd.options.display.width = None # when set to None or 0, will auto-resize display width based on terminal window size
# pd.options.display.max_rows = None


# TextCategorizer does not use features from other pipeline components, so we start with a blank model
nlp = spacy.blank('en')

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# change the working directory to the output directory because we are going to be writing some output files later on
try:
    os.mkdir(OUTPUT_DIR)
except:
    pass

os.chdir(OUTPUT_DIR)

WIKI_QA_CORPUS_DIR = os.path.join(SCRIPT_DIR, 'resources', 'WikiQACorpus')

tsv_to_df = lambda filename: pd.read_csv(os.path.join(WIKI_QA_CORPUS_DIR, filename), sep='\t')

# print(tsv_to_df('WikiQA-train.tsv'))


def generate_docs(tsv_filename, output_filename, doc_limit=100):
    docs = DocBin()
    doc_count = 0
    # iterating over dataframe rows is generally slow, this example is just for convenience
    for index, row in tsv_to_df(tsv_filename).iterrows():
        doc_count += 1

        doc = nlp.make_doc(row['Sentence'])
        doc.cats[row['DocumentTitle']] = 1 # do we need to assign all DocumentTitles?
        docs.add(doc)

        if doc_limit and doc_limit == doc_count:
            break

    docs.to_disk(output_filename)
    return docs


def generate_train_and_dev_spacy_datasets():
    # write train and dev spacy data to disk which then will be used for training
    generate_docs('WikiQA-train.tsv', 'train.spacy')
    generate_docs('WikiQA-dev.tsv', 'dev.spacy')


# below command can be run to generate the training config from the base_config.cfg downloaded from spacy.io
# the training config just need to be generated once and can be reused
# NOTE: run the command inside the "resources" directory
# spacy init fill-config base_config.cfg 020_training_config.cfg

# to train the textcat model, the below command can be run
# NOTE: run the command inside the script's directory
# spacy train resources/020_training_config.cfg --output output --paths.train train.spacy --paths.dev dev.spacy

def train():
    # instead of using command line to train, we can also train programmatically using python
    from spacy.cli.train import train as spacy_train
    spacy_train(
        config_path=os.path.join(SCRIPT_DIR, 'resources', '020_training_config.cfg'),
        output_path=os.path.join(OUTPUT_DIR),
        overrides={
            "paths.train": os.path.join(OUTPUT_DIR, 'train.spacy'),
            "paths.dev": os.path.join(OUTPUT_DIR, 'dev.spacy'),
        },
    )

def test_the_trained_nlp():
    trained_nlp = spacy.load(os.path.join(OUTPUT_DIR, 'model-best'))

    # perform the trained pipeline on this text
    text = "it is very cold in a glacier cave"
    doc = trained_nlp(text)

    print(f'Predicted categories: {doc.cats}')


generate_train_and_dev_spacy_datasets()
train()
test_the_trained_nlp()