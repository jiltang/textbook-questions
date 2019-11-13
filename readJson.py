import json
from wordfreq import top_n_list
import string

with open('tqa_train_val_test/test/tqa_v2_test.json', 'r') as f:
    data = json.load(f)

with open('test_dat.txt', 'w') as f:
    for i in range(len(data)):
        raw_texts = []
        text_sets = []
        mostCommon = set(top_n_list('en', 500))

        for topic, mapping in data[i]['topics'].items():
            print(topic)
            print(mapping['content']['text'])
            raw_texts.append(mapping['content']['text'])
            text = mapping['content']['text'].translate(str.maketrans('', '', string.punctuation)).lower()
            text = set(text.split()).difference(mostCommon)
            text_sets.append(text)

        for questionID, mapping in data[i]['questions']['nonDiagramQuestions'].items():
            if mapping['questionSubType'] == "True or False" or mapping['questionSubType'] == "Matching":
                question = mapping['beingAsked']['processedText']
                question = question.translate(str.maketrans('', '', string.punctuation)).lower()
                words = set(question.split()).difference(mostCommon)
                #correct = mapping['correctAnswer']['processedText']
                answer = mapping['correctAnswer']['rawText']
                if answer.find("true") != -1:
                    answer = "true"
                elif answer.find("false") != -1:
                    answer = "false"
                words.update(answer.lower().split())
                set_match = [len(words.intersection(text_set)) / (len(text_set)+.0001) for text_set in text_sets]
                max_index = max(enumerate(set_match), key = lambda x: x[1])[0]
                print("Question:", question)
                print("Correct answer:", answer)
                print("Matched with:\n", raw_texts[max_index])
                print()
                f.write(f"{raw_texts[max_index]}\t{question}\t{answer}\n")
