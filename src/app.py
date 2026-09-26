from flask import Flask, render_template, request, jsonify
import game_logic
from evaluate import write_data_tabel as wdt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory

app = Flask(__name__)
@app.route("/")
def game_menu():
    word = "Haus"
    versuche = 6
    return render_template("game_menu.html", word=word, versuche=versuche)

solution = game_logic.pick_random_word()# picks a random word out of our data
length_of_word= len(solution)

@app.route("/game")
def game():
    return render_template("wordle.html", 
    solution= solution, 
    length_of_word= length_of_word
    )

tries = 0
guessed_words = []
@app.route("/guess", methods=["POST"])
def guess():
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
        open_tries = 6 - tries
        guessed_words.append(word)
        data_list = [word, tries, True, "time",  player]
        data_list.extend(guessed_words)
        data_list.extend("-" * open_tries) 
        try:
            with open("../data/credentials.json"):
                wdt(data_list)
        except:
                print("played without uploading data")
        
        return jsonify({
            "won": True,
            "colors": game_logic.letter_status(solution, word)[0],
            "wrong_letters": list(game_logic.letter_status(solution, word)[1]),
            "valid": True,
            "tries_left" : True
        })
    elif game_logic.word_is_valid(word) == False:
        tries -=1
        return jsonify({
            "valid" : False
        })
    guessed_words.append(word)
    if tries == 6:
        tries_left = False
        try:
            data_list = [word, tries, False, "time",  player]
            with open("../data/credentials.json"):
                data_list.extend(guessed_words)
                wdt(data_list)
        except:
            print("played without uploading data")
    return jsonify({
        "won": False,
        "colors": game_logic.letter_status(solution, word)[0],
        "wrong_letters": list(game_logic.letter_status(solution, word)[1]),
        "valid": True,
        "tries_left" : tries_left

    })

if __name__ == "__main__":
    app.run(debug=True)
