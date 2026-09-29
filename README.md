# Linguistic-wordle

Linguistic-wordle is a wordle inspired game, which uses words extracted from the novel *Moby Dick* and enriches them with linguistic features. The project builds a custom word database by using Natural Language Processing tools like spacy and NLTK. 
Our goal is an interactive word-guessing game based on real linguistic data.

# Features
- Extracts words from *Moby Dick*
- Tokenization and lemmatization with spacy
- Removes proper nouns
- Filters words by length (5-10 characters)
- Computes linguistic features like word length, part-of-speech, syllable count...
- builds a custom database
- provides game logic in wordle-style
- runs as a small Flask web application

# Installation & Setup
You can just clone the project and install the required packages, which you need to start the game. Then you can just run the main.py data and the game opens automaticly.

# Usage
1. Open the link http://127.0.0.1:5000 to open the game.
2. Click "Start Game" to begin to play.
3. Enter your guesses in the input field.
4. The different colors have different meanings for the letters.
   - **grey**: letter is not contained in the word.
   - **yellow**: correct letter, but in the wrong position.
   - **green**: correct letter in the correct position.
5. Continue to guess until you find the right word or run out of attempts.

# Contributions
Jonas Patzke and Veronika Rapp are maintainers for this repository.

# License
For our data we used the licens-free novel "Moby Dick".
