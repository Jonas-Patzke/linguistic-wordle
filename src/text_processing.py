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
  return "../data/first_three_chapters.txt"

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

def tokenize(text):  #tokenize our chapters and return token objects, input text is coming from clean_lowercase function
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(text)
  return doc


def lemmatize(tokenized_chapters): # lemmatize and return a list of lemma
  lemma = [token.lemma_ for token in tokenized_chapters]
  return lemma



def filter_tokens(spacy_tokens): #filters the tokens, so we haven't unnecessary words and punctuation
  filtered = [token for token in spacy_tokens if token.is_alpha and not token.is_stop]
  return filtered 

def remove_duplicates(words_lemma:list): #removes token duplicate - input is a list of lemma, outpus is a set of lemma
  lemma = set(words_lemma)
  return lemma

def remove_proper_names(pos_dict: dict): #input is the returned dict from pos_tagger function
  pos_without_proper_names = []
  for word in pos_dict:
    if pos_dict.get(word) != "PROPN": 
      pos_without_proper_names.append(word)
  return pos_without_proper_names #returns a list of words without proper names


#------------------------------------------------------------------------------------------------------------------------------------------------
#edge cases
#we have edge cases in our chapter tokens(e.g. chapteri), since the book uses roman numbers
#NOTE: edge cases have to solved, before removing token duplicates, since our input in edge case functions is a list

def chapter_edge_case(words_lemma: list): #removes all chapter edge cases and adds 1 "chapter" to the list
  pos = 0
  for word in words_lemma:
    if re.match("chapter(i)*", word) != None:
      words_lemma.pop(pos)
      pos += 1
  words_lemma.append("chapter")
  return words_lemma

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#Wrap it all up in a function

def create_token():
    extracted_chapters = run_extraction() #extract chapters
    token = tokenize(clean_lowercase(extracted_chapters)) #1. put everything in lower case, 2. tokenize
    filtered_token = filter_tokens(token) #filter to remove stopwords and every token, that doesnt 
    return filtered_token

def create_lemma(token):
    lemma = lemmatize(token) #lemmatize
    lemma_edge_case = chapter_edge_case(lemma) #deleting "chapter" + n * "i" and add one "chapter"
    lemma_without_duplicates = remove_duplicates(lemma_edge_case) #remove duplicate words
    return lemma_without_duplicates




  