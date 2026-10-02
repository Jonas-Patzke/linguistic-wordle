from flask import Flask, render_template, request, jsonify
import game_logic
from evaluate import write_data_tabel as wdt, sheet2
import time
import webbrowser
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory


#NOTE: we used the same code as in app.py, but changed every hint to an empty string and selected a different port to open the game

app = Flask(__name__)
@app.route("/")
def game_menu():
    return render_template("game_menu.html")

solution = game_logic.pick_random_word()# picks a random word out of our data
length_of_word= len(solution)

@app.route("/game")
def game():
    return render_template("wordle.html", 
    solution= solution, 
    length_of_word= length_of_word
    )

start_time = time.time()
tries = 0
guessed_words = []
@app.route("/guess", methods=["POST"])
def guess():
    global start_time
    data = request.get_json()
    word = data["current_word"]
    global tries
    tries +=1
    tries_left = True
    global guessed_words
    try:
        with open("../data/player.txt") as player_file:
            player = player_file.read().lower()
    except:
        player = "unknown"
    print("Eingabe:", word)
    if game_logic.is_correct(solution, word):
        needed_time = round(time.time() - start_time, 2)
        open_tries = 6 - tries
        guessed_words.append(word)
        data_list = [solution, tries, True, needed_time,  player]
        data_list.extend(guessed_words)
        data_list.extend("-" * open_tries) 
        try:
            with open("../data/credentials.json"):
                wdt(sheet2, data_list)
        except:
                print("played without uploading data")
        
        return jsonify({
            "won": True,
            "colors": game_logic.letter_status(solution, word)[0],
            "wrong_letters": list(game_logic.letter_status(solution, word)[1]),
            "valid": True,
            "tries_left" : True,
            "hint": ""
        })
    elif game_logic.word_is_valid(word) == False:
        tries -=1
        return jsonify({
            "valid" : False
        })
    guessed_words.append(word)
    if tries == 6:
        tries_left = False
        needed_time = round(time.time() - start_time, 2) 
        try:
            data_list = [solution, tries, False, needed_time,  player]
            with open("../data/credentials.json"):
                data_list.extend(guessed_words)
                wdt(sheet2, data_list)
        except:
            print("played without uploading data")
    return jsonify({
        "won": False,
        "colors": game_logic.letter_status(solution, word)[0],
        "wrong_letters": list(game_logic.letter_status(solution, word)[1]),
        "valid": True,
        "tries_left" : tries_left,
        "hint" : ""

    })

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5001")
    app.run(debug=True, use_reloader=False, port=5001)
    
    