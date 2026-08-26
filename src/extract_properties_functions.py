import spacy

def number_of_letters(lemma): #extract the number of letters
  return len(lemma)

def pos_tagger(spacy_token):#map part-of-speech to each token
  pos_tags = {}
  for token in spacy_token:
    pos_tags.update({token.text: token.pos_})
  return pos_tags


#-------------------------------------------------------------------------------------------------------------

def extract_properties_over_token(spacy_token):
  print(pos_tagger(spacy_token))

