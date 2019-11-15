import csv
import sacrebleu

refs = []
actuals = []
preds = []
with open('fake_data/perfect-output.tsv', 'r') as f:
    reader = csv.reader(f, delimiter = '\t')
    for text, actual, pred in reader:
        actuals.append(actual)
        preds.append(pred)
refs.append(actuals)

print(sacrebleu.corpus_bleu(preds, refs))
