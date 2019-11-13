import json
from wordfreq import zipf_frequency

with open('tqa_train_val_test/val/tqa_v1_val.json', 'r') as f:
    data = json.load(f)

print(len(data))

for topic, mapping in data[1]['topics'].items():
    print(topic)
    print(mapping['content']['text'])

for questionID, mapping in data[1]['questions']['nonDiagramQuestions'].items():
    if mapping['questionSubType'] == "True or False":
        # print(questionID)
        # print(mapping['globalID'])
        # print(mapping['questionSubType'])
        question = mapping['beingAsked']['processedText']
        print(question)
        freqs = [zipf_frequency(word, 'en') for word in question.split()]
        min_index = min(enumerate(freqs), key=lambda x: x[1])[0]
        for freq, word in zip(freqs, question.split()):
            print(word, "\t\t", freq)
        print("least common word:", question.split()[min_index].lower())
        correct = mapping['correctAnswer']['processedText']
        print("Correct answer:", mapping['answerChoices'][correct]['processedText'])
    # for answerChoice, answerMapping in mapping['answerChoices'].items():
    #      print(answerChoice, answerMapping['processedText'])
    #      answer = answerMapping['processedText']
         #if answer == "True" or answer == "False":

    # correct = mapping['correctAnswer']['rawText']
    # print("Correct answer:", mapping['answerChoices'][correct])

# for topic, mapping in data[0]['questions'].items():
#     print(topic)
#     print(mapping['content']['text'])
