from flask import Flask, render_template, request, jsonify
import game_logic

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

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    word = data["current_word"]
    print("Eingabe:", word)
    if game_logic.is_correct(solution, word):
        return jsonify({
            "won": True,
            "colors": game_logic.letter_status(solution, word)[0],
            "wrong_letters": list(game_logic.letter_status(solution, word)[1])
        })
    return jsonify({
        "won": False,
        "colors": game_logic.letter_status(solution, word)[0],
        "wrong_letters": list(game_logic.letter_status(solution, word)[1])

    })

if __name__ == "__main__":
    app.run(debug=True)
