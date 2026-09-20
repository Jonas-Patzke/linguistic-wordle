from nltk.corpus import cmudict
import random
cmu = cmudict.dict() #cmudict to python dict

def pick_random_word(dict_with_words):
    random_number = random.randint(0, len(dict_with_words) -1)
    return list(dict_with_words.keys())[random_number]

def word_is_valid(guess):
    if guess.lower() in cmu:
        return True
    return False

def is_correct(word, guess):
    if guess == word:
        return True
    return False

def letter_status(word,guess): #input are the worde we have to gues and our guess
    letter_pos = 0
    color_list = [] #list where we want to append colors
    letters = set(word) #set to test, if we want to append yellow
    for letter in guess:
        if letter == word[letter_pos]: #correct letter in correct position = append greeb
            color_list.append("green")
        elif letter in letters: #letter in wrong position = append yellow
            color_list.append("yellow")
        else:   #nothing of the above = append grey
            color_list.append("grey")
        letter_pos += 1
    return color_list

try_number = 0

def give_hint(word, properties):
    global try_number
    try_number += 1
    info = properties[word]
    if try_number == 1:
        return f"The word has {info['syllables']} syllables."
    elif try_number == 2:
        return f"The word is a {info['pos']}."
    elif try_number == 3:
        return f"The word starts with '{word[0]}'."
    elif try_number == 4:
        return f"The word has {info['length']} letters."
    elif try_number == 5:
        return f"The word ends with '{word[-1]}'."
    elif try_number == 6:
        return f"The word appears {info['frequency']} times in the text."
    else:
        return "No more hints available."

print(pick_random_word({1:1,2:2,3:3}))
