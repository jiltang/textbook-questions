import data
import os
import time
import random

def lastSentence(text):
  sentences = [s.strip() for s in text.split('.') if s.strip() != ""]
  # determine last sentence
  i = -1
  last_sentence = ""
  while abs(i) <= len(sentences) and sentences[i].isdigit():
    last_sentence = "." + sentences[i] + last_sentence
    i -= 1
  if abs(i) <= len(sentences):
    last_sentence = sentences[i] + last_sentence
  return last_sentence

# Construct the predicted question by appending 
# do to the last sentence of the text
def doLastSentence(text):
  last_sentence = lastSentence(text)
  
  # generate prediction
  if last_sentence[0:2].lower() != "do":
    predicted = "Do " + last_sentence[0].lower()
  else:
    predicted = last_sentence[0].upper()
  predicted += last_sentence[1:]
  if last_sentence[-1] != "?":
    predicted += "?"
  return predicted

# DirectIn baseline
# Prediction question is the longest sub-sentence of the 
# sentence split on the splitters ["?","!",",",".",";"]
def directIn(text):
  subsentences = [text]
  for deli in ["?","!",",",".",";"]:
    temp = []
    for subsentence in subsentences:
      temp.extend([s.strip() for s in subsentence.split(deli) if s.strip() != ""])
    subsentences = temp.copy()

  max_len = max(len(s) for s in subsentences)
  max_subsentences = [s for s in subsentences if len(s) == max_len]
  return random.choice(max_subsentences)

if __name__ == "__main__":
  data = ["squad", "val"]
  method = "doLast"

  output_path = os.path.join("../outputs", "baseline" )
  print(f"Constructing new output directory at {output_path}")

  input_file = "../" + data[0] + "/" + data[1] + "_dat.txt"
  with open(input_file, "r") as input:
    for line in input:
      if data[0] == "textbook":
        text, question, answer = line.split("\t")
      elif data[0] == "squad":
        text, question = line.split("\t")
      else:
        raise "invalid dataset"
      text = text.strip()
      question = question.strip()

      predicted = ""
      if method == "last":
        predicted += lastSentence(text)
      elif method == "doLast":
        predicted += doLastSentence(text)
      elif method == "directIn":
        predicted += directIn(text)
      else:
        raise "invalid method"
      with open(os.path.join(output_path, f"{data[0]}_{data[1]}_{method}_baseline_predicted.txt"), 'a+') as f:
        f.write(text + '\t' + question + '\t' + predicted + '\n')