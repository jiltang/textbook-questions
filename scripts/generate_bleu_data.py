import random

words = ['this', 'that', 'who', 'cat', 'training', 'test', 'validation', 'words', 'use', 'python', 'cat']


with open(f"../fake_data/perfect-output.tsv", 'w') as f:
    for i in range(1000):
        text = " ".join(random.choices(words, k=15))
        question = " ".join(random.choices(words, k=10))
        f.write(text + "\t" + question + "\t" + question + "\n")
