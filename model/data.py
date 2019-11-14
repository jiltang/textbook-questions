import numpy as np
import torchtext
import spacy
spacy_en = spacy.load('en')

def tokenizer(text): # create a tokenizer function
    return [tok.text for tok in spacy_en.tokenizer(text)]

def loadData(path, dim=50):
    TEXT = torchtext.data.Field(sequential=True, tokenize=tokenizer, lower=True, init_token="[SOS]", eos_token="[EOS]", include_lengths=True, batch_first=True)
    # QUESTION = torchtext.data.Field(sequential=True, tokenize=tokenizer, lower=True, init_token="[SOS]", eos_token="[EOS]", include_lengths=True, batch_first=True)

    train, val, test = torchtext.data.TabularDataset.splits(
            path=f"../{path}/", train='train_dat.txt',
            validation='val_dat.txt', test='test_dat.txt', format='tsv',
            fields=[('Text', TEXT), ('Question', TEXT)])

    TEXT.build_vocab(train, val, vectors=f"glove.6B.{dim}d")
    # QUESTION.build_vocab(train, val, vectors=f"glove.6B.{dim}d")


    trainLoader, valLoader, testLoader = torchtext.data.Iterator.splits(
            (train, val, test), sort_key=lambda x: len(x.Text),
            batch_sizes=(32, 1, 32), device=-1)

    vocab = TEXT.vocab
    return trainLoader, valLoader, testLoader, vocab
