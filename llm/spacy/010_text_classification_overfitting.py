import spacy
from spacy.training import Example
from spacy.lang.en import English

# TextCategorizer does not use features from other pipeline components so we start with a blank model
# nlp = spacy.blank('en')
nlp = English()

nlp.add_pipe('textcat_multilabel')


TRAIN_DATA_MULTI_LABEL = [
    ("I'm angry and confused", {"cats": {"ANGRY": 1.0, "CONFUSED": 1.0, "HAPPY": 0.0}}),
    ("I'm confused but happy", {"cats": {"ANGRY": 0.0, "CONFUSED": 1.0, "HAPPY": 1.0}}),
]

train_examples = [
    Example.from_dict(nlp.make_doc(text), annotations)
    for text, annotations
    in TRAIN_DATA_MULTI_LABEL
]

optimizer = nlp.initialize(get_examples=lambda: train_examples)

test_text = "I'm confused but happy"

# test the trained model
doc = nlp(test_text)
print(f'Before over-fitting {doc.cats}')

for i in range(100):
    losses = {}
    nlp.update(train_examples, sgd=optimizer, losses=losses)
    print(f'Losses {losses}')

doc = nlp(test_text)
print(f'After over-fitting HAPPY and CONFUSED categories predictions are very close to 1 {doc.cats}')


