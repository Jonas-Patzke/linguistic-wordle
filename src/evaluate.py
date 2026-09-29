import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 
from pathlib import Path
import build_database as bd
import os
import matplotlib.pyplot as plt
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

#sheet.append_row(["test", 1, True, 60, "first test"])

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
        

def create_diagram(distribution_dict): 
    df = pd.DataFrame(word_distribution(distribution_dict).items(), columns=["pos-tag", "count"]) #create a datafram
    diagram = df.plot(x="pos-tag", y="count", kind="bar", stacked=True, figsize=(10, 8)) #create the diagram
    plt.show() #show the diagram

#create_diagram("../data/propertie_dict.pkl") #create a diagram for the pos-tag distribution over the propertie dict
#create_diagram("../data/CMUdict_5_to_7_without_propn.pkl") ##create a diagram for the pos-tag distribution over the cmu dict

def write_data_tabel(data: list): #data should have the form [word, tries, won: boolean, duration, player, 1st - 6th guess]
    sheet.append_row(data)

def load_sheet_data(): #load the data from the sheet
    data = sheet.get_all_values()
    header = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=header)

    df["tries"] = pd.to_numeric(df["tries"], errors="coerce") # correct datatypes
    df["won"] = df["won"].map({"TRUE": True, "FALSE": False})
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")

    return df

def load_properties(): #load linguistic properties
    return pd.read_pickle("../data/propertie_dict.pkl")

def analyze_game_data(save_to_file=False):  # analysis function

    df = load_sheet_data()
    df["word"] = df["word"].str.lower()

    props = load_properties()
    props = {k.lower(): v for k, v in props.items()}

    # Attach properties to the data
    df["syllables"] = df["word"].apply(
        lambda w: props.get(w, {}).get("syllables_count")
    )

    df["frequency"] = df["word"].apply(
        lambda w: props.get(w, {}).get("frequenzies")
    )

    df["pos"] = df["word"].apply(
        lambda w: props.get(w, {}).get("pos")
    )

    df["vowels"] = df["word"].apply(
    lambda w: sum(letter in "aeiou" for letter in w)
    )
    # Convert columns to numeric
    df["tries"] = pd.to_numeric(df["tries"], errors="coerce")
    df["vowels"] = pd.to_numeric(df["vowels"], errors="coerce")
    df["syllables"] = pd.to_numeric(df["syllables"], errors="coerce")
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
    # Convert won to 1 and 0
    df["won"] = df["won"].astype(str).str.lower().map({
    "true": 1,
    "false": 0
})
    results = {}

    # Average attempts
    results["avg_tries_by_pos"] = (
        df.groupby("pos")["tries"]
        .mean()
        .sort_values()
    )

    results["avg_tries_by_syllables"] = (
        df.groupby("syllables")["tries"]
        .mean()
        .sort_values()
    )

    results["avg_tries_by_vowels"] = (
        df.groupby("vowels")["tries"]
        .mean()
        .sort_values()
    )

    results["avg_tries_by_frequency"] = (
        df.groupby("frequency")["tries"]
        .mean()
        .sort_values()
    )

    # Win rate
    results["winrate_by_pos"] = (
        df.groupby("pos")["won"]
        .mean()
        .sort_values()
    )

    results["winrate_by_syllables"] = (
        df.groupby("syllables")["won"]
        .mean()
        .sort_values()
    )

    results["winrate_by_vowels"] = (
        df.groupby("vowels")["won"]
        .mean()
        .sort_values()
    )

    results["winrate_by_frequency"] = (
        df.groupby("frequency")["won"]
        .mean()
        .sort_values()
    )

    # Save analyses as separate CSV files
    if save_to_file:

        data_folder = Path(__file__).resolve().parent.parent / "data"

        for name, result in results.items():

            result.to_csv(
                data_folder / f"{name}.csv",
                index=True
        )

        print("Alle Analyse-Dateien wurden erfolgreich erstellt.")

    return results

#if __name__ == "__main__": #test
  #  analysis = analyze_game_data()
  #  for key, value in analysis.items():
   #     print("\n---", key, "---")
    #    print(value)

if __name__ == "__main__":
    analyze_game_data(save_to_file=True)
