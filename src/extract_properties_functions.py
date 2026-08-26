import nltk
from nltk.corpus import cmudict
import re
nltk.download('cmudict')
cmu = cmudict.dict()

def number_of_letters(lemma): #extract the number of letters
  return len(lemma)

def pos_tagger(spacy_token):#map part-of-speech to each token
  pos_tags = {}
  for token in spacy_token:
    pos_tags.update({token.text: token.pos_})
  return pos_tags

def extract_frequenzy(text_file, word_set):
  count_dict = {}
  with open(text_file, "r", encoding="utf-8") as file:
    text = file.read
  for word in word_set:
    regex = "\b" + word + "\b"
    count_dict.update({word: len(re.findall(regex, text))})


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


def extract_properties_over_token(spacy_token):
  print(pos_tagger(spacy_token)) #print function is just for visualisation