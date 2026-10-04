# Linguistic-wordle

Linguistic-wordle is a wordle inspired game, which uses words extracted from the novel *Moby Dick* and enriches them with linguistic features. The project builds a custom word database by using Natural Language Processing tools like spacy and NLTK. 
Our goal is an interactive word-guessing game based on real linguistic data.

# Features
- Extracts words from *Moby Dick*
- Tokenization and lemmatization with spacy
- Removes proper nouns
- Filters words by length (5-7 characters)
- Computes linguistic features like word length, part-of-speech, syllable count...
- builds a custom database
- provides game logic in wordle-style
- runs as a small Flask web application

# Installation & Setup
You can just clone the project and install the required packages, which you need to start the game. Then you can just run the main.py data and the game opens automaticly.

# Usage
1.Open main.py and wait a few seconds, the game shoul open automaticly in your browser (if not open http://127.0.0.1:5000)
2. Click "Start Game" to begin to play.
3. Enter your guesses in the input field.
4. The different colors have different meanings for the letters.
   - **grey**: letter is not contained in the word.
   - **yellow**: correct letter, but in the wrong position.
   - **green**: correct letter in the correct position.
5. Continue to guess until you find the right word or run out of attempts.

If you want to play again, you have to press run code 2 times:
  
   -  1st click ends hosting the last game
   
   - 2nd click starts the new game

<img width="1734" height="934" alt="image" src="https://github.com/user-attachments/assets/8ecdefbf-f344-43d3-9b7f-fcf323ae7525" />


To recreate or view the used data the files evaluate.py and process_and_extract.py have to be used in orderto get the results.
All you have to do is to run the code. To find the data we collected from our wordle game, follow this link:

https://docs.google.com/spreadsheets/d/1A2AqtIRgllnj0LVhDF0N7CrbK-haPZxRQNYx09a9gTQ/edit?gid=0#gid=0

For the data of the worlde game without linguistic hints, follow this link:

https://docs.google.com/spreadsheets/d/1h02HEgTMySWGgAWkalbT35zez5A9_lhq0dfTx997jG4/edit?gid=0#gid=0

In the cells B52 to D52 in both spread sheets is the result, in the order average tries, winrate and average time to solve in seconds.


# Contributions
Jonas Patzke and Veronika Rapp are maintainers for this repository.

# License
For our data we used the licens-free novel "Moby Dick".
