from build_database import read_pickle as rp
import random

def pick_random_word(): #pick a random word the player has to guess
    dict_with_words = rp("../data/propertie_dict.pkl")
    random_number = random.randint(0, len(dict_with_words) -1)
    return list(dict_with_words.keys())[random_number]

def word_is_valid(guess): #a word should only be able to guess if its an actuall word in the cmudict
    cmu = rp("../data/CMUdict_5_to_7.pkl")
    return guess.lower() in cmu

def is_correct(word, guess): #test if the guess is correct
    if guess == word:
        return True
    return False

def letter_status(solution,guess): #input are the worde we have to gues and our guess
    letter_pos = 0
    wrong_letters = set() #a set of letters we guessed, but are not in the word so we can visualize is on our letter board in html
    color_list = [] #list where we want to append colors
    letters = set(solution) #set to test, if we want to append yellow
    for letter in guess:
        if letter == solution[letter_pos]: #correct letter in correct position = append greeb
            color_list.append("green")
        elif letter in letters: #letter in wrong position = append yellow
            color_list.append("yellow")
        else:   #nothing of the above = append grey
            color_list.append("grey")
            wrong_letters.add(letter.upper()) #upper() since our boxes in html inherit the upper version of a letter 
        letter_pos += 1
    return [color_list, wrong_letters] #return the colors in the order we have to paint our guessed letters and all the letters we guessed and arent in the word

try_number = 0

def give_hint(word, properties): #input is a word and a list of its properties, more exactly give_hint(word, dictionary.get(word))
    global try_number
    try_number += 1
    info = properties[word]
    vowels = "aeiou"
    vowels_count = sum(1 for letter in word.lower() if letter in vowels)
    if try_number == 1:
        return f"The word has {info['syllables']} syllables."
    elif try_number == 2:
        return f"The word is a {info['pos']}."
    elif try_number == 3:
        return f"The word starts with '{word[0]}'."
    elif try_number == 4:
        return f"The word contains {vowels_count} vowel(s)."
    elif try_number == 5:
        return f"The word ends with '{word[-1]}'."
    elif try_number == 6:
        return f"The word appears {info['frequency']} times in the text."
    else:
        return "No more hints available."


