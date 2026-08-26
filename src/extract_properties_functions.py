import nltk
from nltk.corpus import cmudict
nltk.download('cmudict')
cmu = cmudict.dict()

def number_of_letters(lemma): #extract the number of letters
  return len(lemma)

def pos_tagger(spacy_token):#map part-of-speech to each token
  pos_tags = {}
  for token in spacy_token:
    pos_tags.update({token.text: token.pos_})
  return pos_tags

def count_syllables_cmu(word): #counts syllables
  word = word.lower()
  if word not in cmu:
    return None
  pronunciations = cmu[word][0] #extract only the first pronunciation
  syllables = sum(1 for letter in pronunciations if letter[-1].isdigit()) #vocals have a number
  return syllables

def extract_syllables(tokens): #application for all tokens
  result = []
  for token in tokens:
    s = count_syllables_cmu(token.text)
    if s is not None:
      result.append((token.text, s))
  return result

def extract_constituents(tokens): #extract constituents
  result = []
  for token in tokens:
    result.append((token.text, token.dep_))
  return result

def extract_properties_over_token(spacy_token):
  print(pos_tagger(spacy_token)) #print function is just for visualization
