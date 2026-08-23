import spacy
import re
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory to find our txt
# 1. Extract first three chapters

def load_text(path):     #load text from a file
  with open(path, "r", encoding="utf-8") as f:
    return f.read()

def extract_chapters(text, n=3):     #extract the first n chapters
  parts = text.split("CHAPTER ")[1:]
  selected = parts[:n]
  return "\n".join("CHAPTER" + p for p in selected)

def save_text(path, content):      #save text in a file
  with open(path, "w", encoding="utf-8") as f:
    f.write(content)

def run_extraction():   #the whole extraction Prozess
  raw = load_text("../data/MOBY-DICK; or, THE WHALE.txt")
  chapters = extract_chapters(raw, 3)
  save_text("../data/first_three_chapters.txt", chapters)
  
#if __name__ == "__main__":  #starts automaticly running
# run_extraction()


#------------------------------------------------------------------------------------------------------------------
#1.5 prepare the file for a smooth tokenization

def clean_lowercase(text_file): #convert file in lowercase
  with open(text_file, "r", encoding="utf-8") as f:
    content = f.read()
  content = content.lower()
  return content
  


#------------------------------------------------------------------------------------------------------------------
#2. tokenize + lemmmatize
#since we return a list of strings in lemmatize, we have to
#use our text cleaning functions before we use lemmatize()
#we will use spacy to filter for stop words and punctuation, but its only possible with token objects
#token.is_alpha = true, if our token is made out of letters
#token.is_stop = true, if our tiken is a stop word
# NOTE: we have edge cases in our chapter tokens(e.g. chapteri), since the book uses roman numbers

def tokenize(text_file):  #tokenize our chapters and return token objects
  with open(text_file, "r", encoding="utf-8") as f:
    content = f.read()
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(content)
  return doc


def lemmatize(text_file): # lemmatize and return a list of lemma
  lemma = [token.lemma_ for token in tokenize(text_file)]
  print([token.lemma_ for token in tokenize(text_file)]) # print() zur Visualisierung, muss später noch entfernt werden
  return lemma


lemmatize("../data/first_three_chapters.txt")


def filter_tokens(text_file): #filters the tokens, so we haven't unnecessary words and punctuation
  doc = tokenize(text_file)
  filtered = [token for token in doc if token.is_alpha and not token.is_stop]
  print(filtered[:50]) #nur Kontrolle muss später löschen
  return filtered 

def chapter_edge_case(words_lemma: list):
  pos = 0
  for word in words_lemma:
    if re.match("chapter(i)*", word) != None:
      words_lemma.pop(pos)
      pos += 1
  words_lemma.append("chapter")
  return words_lemma

ffh = ["chapterii", "utw", "chapteriiii"]
print(chapter_edge_case(ffh))
