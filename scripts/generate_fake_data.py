import random

words = ['this', 'that', 'who', 'cat', 'training', 'test', 'validation', 'words', 'use', 'python', 'cat']


for split in ("train", "test", "dev"):
    with open(f"../fake_data/{split}.tsv", 'w') as f:
        for i in range(1000):
            text = " ".join(random.choices(words, k=15))
            question = " ".join(random.choices(words, k=10))
            f.write(text + "\t" + question + "\n")
