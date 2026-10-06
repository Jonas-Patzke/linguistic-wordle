from flask import Flask, render_template, request, jsonify #flask for the connection, render_template to connect the html, request to get data from the html file, jsonify to send data to the html file in the right format
import game_logic
from evaluate import write_data_tabel as wdt, sheet1 #sheet1 is the 
import time
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory

app = Flask(__name__) #connects the game menus site with our python backend over flask
@app.route("/")
def game_menu():
    return render_template("game_menu.html")

solution = game_logic.pick_random_word()# picks a random word out of our data as the solution for the wordle
length_of_word= len(solution) #detects the length, so we adjust the board for the guesses in the game

@app.route("/game")
def game():  #connects the actual wordle game site with our python backend over flask
    return render_template("wordle.html", 
    solution= solution, 
    length_of_word= length_of_word
    )

start_time = time.time() #starting to track the time in seconds for the played game
tries = 1 #set tries to 1 and count it up so the hints can adapt
guessed_words = []
@app.route("/guess", methods=["POST"])
def guess(): #is executed when someone takes a guess
    #define and get global variables
    global start_time #get the time variable 
    global tries #get the tries variable
    global guessed_words #get tne guessed words variable
    #we need the variables to be global, since this method is executed on each guess
    tries_left = True
    request_guess = request.get_json() #store the request to get data fromt the html
    guess = request_guess["current_word"] #get the current guess from the html file by uisng the request variable

    #detect the player name
    try: #since the player.txt is in gitignore, we use try. Its ignored so we dont push eachothers names on github
        with open("../data/player.txt") as player_file: #we have this player.txt to write the name of the person, who plays at the moment, in it
            player = player_file.read().lower() #read the file, content is only one surname
    except:
        player = "unknown"

    #test if the guess is correct and collect the data of the game
    if game_logic.is_correct(solution, guess): #testing if solution equals our guess(word)
        needed_time = round(time.time() - start_time, 2)
        open_tries = 6 - tries #get the tries the player didnt need to win
        guessed_words.append(guess) #append the guess to the list guessed_words
        data_list = [solution, tries, True, needed_time,  player] #create data_list which will fill our google spread sheet
        data_list.extend(guessed_words) #add the guessed words to data_list
        data_list.extend("-" * open_tries) #add the not needed tries to data list by adding "-"
        try: #use try since credentials.json is in gitignore
            with open("../data/credentials.json"): #credentials.json is needed to write in the google spread sheet in python it is in gitignore
                wdt(sheet1, data_list) #writes the data in the spread sheet
        except:
                print("played without uploading data")
        
        return jsonify({
            "won": True, #return True to paint alle guessed letter green
            "colors": game_logic.letter_status(solution, guess)[0], #still return it to thro no error
            "wrong_letters": list(game_logic.letter_status(solution, guess)[1]), #still return it to thro no error
            "valid": True, #still return it to thro no error
            "tries_left" : True, #still return it to thro no error
            "hint": "" #still return it to thro no error, but empty since the player won
        })

    #check if the word is valid to guess
    if game_logic.word_is_valid(guess) == False: #test if the word is valid 
        tries -=1 #remove the try since the word was not guessable
        return jsonify({
            "valid" : False #return False so the text "invalid word" shows on the html site
        })

    #go on with the (wrong) guess 
    guessed_words.append(guess) #if it was valid and not true, add the guess
    if tries == 6: #test, if it was the last try
        tries_left = False #to show the "you lost!" on the html site
        needed_time = round(time.time() - start_time, 2) 
        print("test")
        try: #same as before, we use try since we work with data that is in gitignore
            data_list = [solution, tries, False, needed_time,  player]
            with open("../data/credentials.json"):
                data_list.extend(guessed_words)
                wdt(sheet1, data_list)
        except:
            print("played without uploading data")
    tries +=1
    return jsonify({
        "won": False, #return false, since we use an if state mit in javascript
        "colors": game_logic.letter_status(solution, guess)[0], #color the guessed letters
        "wrong_letters": list(game_logic.letter_status(solution, guess)[1]), #return the letters that were guessed, but arent in teh word to paint the keyboard grey
        "valid": True, #here we also use an if statemaent in javascript
        "tries_left" : tries_left, #
        "hint" : game_logic.give_hint(solution) #give a hint depending on the trie, input is solution since we want to give info about it
    })
    



