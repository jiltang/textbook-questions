import csv
import sacrebleu
from rouge import Rouge
import sys

refs = []
actuals = []
preds = []
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f, delimiter = '\t', quoting=csv.QUOTE_NONE)
    for text, actual, pred in reader:
        actuals.append(actual)
        preds.append(pred)
refs.append(actuals)

print(sacrebleu.corpus_bleu(preds, refs))

r = Rouge()
scores = r.get_scores(preds, actuals, avg=True)
for k, v in scores.items():
    print(k, v)
