import nltk
from nltk.corpus import cmudict
import re
nltk.download('cmudict')
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory to find our txt
cmu = cmudict.dict() #cmudict to python dict

def number_of_letters(lemma: list): #extract the number of letters
  len_dict = {}
  for lemmas in lemma:
    len_dict.update({lemmas: len(lemmas)})
  return len_dict

def pos_tagger(spacy_token):#map part-of-speech to each token
  pos_tags = {}
  for token in spacy_token:
    pos_tags.update({token.text: token.pos_})
  return pos_tags

def extract_frequenzy(text_file, word_set):
  count_dict = {}
  with open(text_file, "r", encoding="utf-8") as file:
    text = file.read()
  for word in word_set:
    regex = r"\b" + word + r"\b"
    count_dict.update({word: len(re.findall(regex, text))})
  return count_dict


def count_syllables_cmu(word): #counts syllables
  pronunciations = cmu[word][0] #extract only the first pronunciation
  syllables = sum(1 for letter in pronunciations if letter[-1].isdigit()) #vocals have a number
  return syllables

def extract_syllables(words): #application for all tokens
  syllables_dict = {}
  for word in words:
    s = count_syllables_cmu(word)
    syllables_dict.update({word: s})
  return syllables_dict

def extract_constituents(tokens): #extract constituents
  constituents_dict = {}
  for token in tokens:
    constituents_dict.update({token.text: token.dep_})
  return constituents_dict



