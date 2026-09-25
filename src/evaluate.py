import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 
import build_database as bd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory to find our txt

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "../data/credentials.json",
    scopes=scopes
)

client = gspread.authorize(creds)
sheet = client.open_by_url(
"https://docs.google.com/spreadsheets/d/1A2AqtIRgllnj0LVhDF0N7CrbK-haPZxRQNYx09a9gTQ/edit?gid=0#gid=0"
).sheet1

sheet.append_row(["test", 1, True, 60, "first test"])

def word_distribution(file): #input should be one of our pickle files, either the propertie_dict or the words from the CMUdict and ther pos-tags
    words= bd.read_pickle(file) #
    distribution = {}
    for word in words:
        try: #for propertie_dict
            pos_tag= words.get(word).get("pos") 
        except: #for the words of the CMUdict
            pos_tag= words.get(word)
        try: #check if we already have an entry 
            count= distribution.get(pos_tag) + 1 #gives an error, if there is no entry
            distribution.update({pos_tag: count})
        except: 
            distribution.update({pos_tag: 1}) #creates the first entry for the pos-tag keys and their values
    return distribution #returns a dict with pos-tags as keys and the count of word with this tag as value
        
