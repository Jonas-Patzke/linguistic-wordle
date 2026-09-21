from flask import Flask, render_template, request
from game_logic import give_hint

app = Flask(__name__)
@app.route("/")
def startseite():
    word = "Haus"
    versuche = 6
    return render_template("wordle.html", word=word, versuche=versuche)

solution = "butterfly"
length_of_word= len(solution)

@app.route("/game")
def game():
    return render_template("game.html", 
    solution= solution, 
    length_of_word= length_of_word
    )

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    word = data["current_word"]

    print("Eingabe:", word)

    if word == solution:
        return "right"

    return "wrong"

if __name__ == "__main__":
    app.run(debug=True)
