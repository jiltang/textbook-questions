import random

words = ['this', 'that', 'who', 'cat', 'training', 'test', 'validation', 'words', 'use', 'python', 'cat']


for split in ("train", "test", "dev"):
    with open(f"../copy_data/{split}_dat.txt", 'w') as f:
        for i in range(1000):
            text = " ".join(random.choices(words, k=15))
            f.write(text + "\t" + text + "\n")
