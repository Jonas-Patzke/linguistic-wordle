import webbrowser
from app import app
#main.py starts our wordle game

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000") #opens the wrle game authomaticly in the browser
    app.run(debug=True, use_reloader=False) #changed the parameter, so the game doesnt open multiple times on one execute

