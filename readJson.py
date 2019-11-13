import json

with open('tqa_train_val_test/val/tqa_v1_val.json', 'r') as f:
    data = json.load(f)

for topic, mapping in data[0]['topics'].items():
    print(topic)
    print(mapping['content']['text'])

for questionID, mapping in data[0]['questions']['nonDiagramQuestions'].items():
    print(questionID)
    print(mapping['beingAsked']['rawText'])
    for answerChoice, answerMapping in mapping['answerChoices'].items():
        print(answerChoice, answerMapping['processedText'])
    print("Correct answer:", mapping['correctAnswer']['processedText'])

# for topic, mapping in data[0]['questions'].items():
#     print(topic)
#     print(mapping['content']['text'])
