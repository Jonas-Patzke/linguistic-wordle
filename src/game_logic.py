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

print(letter_status("haus","eeee"))