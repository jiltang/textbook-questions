import csv
import sacrebleu

import sys

refs = []
actuals = []
preds = []
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter = '\t', quoting=csv.QUOTE_NONE)
    for items in reader:
        actuals.append(actual)
        preds.append(pred)
refs.append(actuals)

print(sacrebleu.corpus_bleu(preds, refs))
