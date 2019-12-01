import json
from wordfreq import top_n_list
import string
import re

filenames = ['test/tqa_v2_test.json', 'train/tqa_v1_train.json', 'val/tqa_v1_val.json']
types = ['test', 'train', 'val']
keywords = ['What', 'Where', 'Who', 'How']
for filename, type in zip(filenames, types):
    print(filename)
    with open(f'tqa_train_val_test/{filename}', 'r') as f:
        data = json.load(f)


    with open(f'openNMTdata/src_test_{type}.txt', 'w') as src, open(f'openNMTdata/tgt_test_{type}.txt', 'w') as tgt:
        raw_texts = []
        text_sets = []
        for i in range(len(data)):
            mostCommon = set(top_n_list('en', 100))
            topic = data[i]['adjunctTopics']
            if 'Lesson Summary' in topic and 'Recall' in topic:
                s_text = topic['Lesson Summary']['content']['text']
                q_text = topic['Recall']['content']['text']
                if q_text.find('1. 2.') == -1:
                    # print("TEXT:")
                    # print(s_text)
                    sentences = s_text.split(". ")[:-1]
                    two_sent = []
                    for i in range(len(sentences) - 1):
                        two_sent.append((sentences[i], sentences[i + 1]))
                    texts = [sent.translate(str.maketrans('', '', string.punctuation)).lower() for sent in sentences]
                    texts = [set(sent.split()).difference(mostCommon) for sent in texts]
                    two_texts = []
                    for i in range(len(texts) - 1):
                        two_texts.append(texts[i] | texts[i + 1])
                    # print(sentences)
                    questions = [x for x in re.split('\s*\d.\s*', q_text) if x != '']
                    questions = [x for x in questions if x.split()[0] in keywords]
                    print("QUESTIONS:")
                    for question in questions:
                        words = set(question.split()).difference(mostCommon)
                        set_match = [len(words.intersection(two_text)) / (len(two_text)+.0001) for two_text in two_texts]
                        max_index = max(enumerate(set_match), key = lambda x: x[1])[0]
                        print("Question:", question)
                        print("Matched with:\n", two_sent[max_index])
                        src.write(f"{s_text}.\n")
                        tgt.write(f"{question}\n")


            # for topic, mapping in data[i]['adjunctTopics'].items():
                #print(topic)
                #print(mapping['content']['text'])

                # sentences = sentences[:-1]
                # sentences = [sent for sent in sentences if len(sent) > 2]
                # two_sent = []
                # for i in range(len(sentences) - 1):
                #     two_sent.append((sentences[i], sentences[i + 1]))
                #     # src.write(f"{(sentences[i], sentences[i + 1])}\n")
                # raw_texts.extend(two_sent)
                # texts = [sent.translate(str.maketrans('', '', string.punctuation)).lower() for sent in sentences]
                # texts = [set(sent.split()).difference(mostCommon) for sent in texts]
                # two_texts = []
                # for i in range(len(texts) - 1):
                #     two_texts.append(texts[i] | texts[i + 1])
                # assert len(two_sent) == len(two_texts)
                # text_sets.extend(two_texts)

            # for questionID, mapping in data[i]['questions']['nonDiagramQuestions'].items():
            #     if mapping['questionSubType'] == "True or False": # or mapping['questionSubType'] == "Matching"
            #         question = mapping['beingAsked']['processedText']
            #         question = question.translate(str.maketrans('', '', string.punctuation)).lower()
            #         words = set(question.split()).difference(mostCommon)
            #         #correct = mapping['correctAnswer']['processedText']
            #         for letter in mapping['answerChoices']:
            #             words.update(mapping['answerChoices'][letter]['rawText'].lower().split())
            #         # answer = mapping['correctAnswer']['rawText']
            #         # if answer.find("true") != -1:
            #         #     answer = "true"
            #         # elif answer.find("false") != -1:
            #         #     answer = "false"
            #         # words.update(answer.lower().split())
            #         set_match = [len(words.intersection(text_set)) / (len(text_set)+.0001) for text_set in text_sets]
            #         # print(max(set_match))
            #         max_index = max(enumerate(set_match), key = lambda x: x[1])[0]
            #         print("Question:", question)
            #         # print("Correct answer:", answer)
            #         print("Matched with:\n", raw_texts[max_index])
            #         print()
            #         src.write(f"{raw_texts[max_index]}\n")
            #         tgt.write(f"{question}\n")
