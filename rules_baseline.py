from textblob import TextBlob

def generate_question(s):
  blobbed = TextBlob(s)
  print(blobbed.tags)
  reverse = {}
  for i, (_, tag) in blobbed.tags:
    if tag not in reverse:
      reverse[tag] = i

  # 
  if all(key in reverse for key in ['NNP', 'VBG', 'VBZ', 'IN']):
    print('What' + ' ' + blobbed.words[reverse['VBZ']] +' '+ blobbed.words[reverse['NNP']]+ ' '+ blobbed.words[reverse['VBG']] + '?')

generate_question("this is a test")
