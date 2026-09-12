from nltk.corpus import cmudict
cmu = cmudict.dict() #cmudict to python dict
def word_is_valid(guess):
    if guess.lower() in cmu:
        return True
    return False

def is_correct(word, guess):
    if guess == word:
        return True
    return False


        