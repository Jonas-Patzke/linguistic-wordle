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
sheet1 = client.open_by_url( #the data table for our linguistic wordle
"https://docs.google.com/spreadsheets/d/1A2AqtIRgllnj0LVhDF0N7CrbK-haPZxRQNYx09a9gTQ/edit?gid=0#gid=0"
).sheet1

sheet2 = client.open_by_url( #the data for the wordle without hints
"https://docs.google.com/spreadsheets/d/1h02HEgTMySWGgAWkalbT35zez5A9_lhq0dfTx997jG4/edit?gid=0#gid=0"
).sheet1


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

def write_data_tabel(sheet, data: list): #data should have the form [word, tries, won: boolean, duration, player, 1st - 6th guess]
    sheet.append_row(data)

def load_sheet_data(): #load the data from the sheet
    data = sheet1.get_all_values()
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
        lambda w: props.get(w, {}).get("syllables_count"))

    df["frequency"] = df["word"].apply(
        lambda w: props.get(w, {}).get("frequenzies"))

    df["pos"] = df["word"].apply(
        lambda w: props.get(w, {}).get("pos"))

    df["vowels"] = df["word"].apply(
    lambda w: sum(letter in "aeiou" for letter in w))

    # Convert columns to numeric
    df["tries"] = pd.to_numeric(df["tries"], errors="coerce")
    df["vowels"] = pd.to_numeric(df["vowels"], errors="coerce")
    df["syllables"] = pd.to_numeric(df["syllables"], errors="coerce")
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
    # Convert won to 1 and 0
    df["won"] = df["won"].astype(str).str.lower().map({
    "true": 1,
    "false": 0})
    results = {}

    # Average attempts
    results["avg_tries_by_pos"] = (
        df.groupby("pos")["tries"]
        .mean()
        .sort_values())

    results["avg_tries_by_syllables"] = (
        df.groupby("syllables")["tries"]
        .mean()
        .sort_values())

    results["avg_tries_by_vowels"] = (
        df.groupby("vowels")["tries"]
        .mean()
        .sort_values())

    results["avg_tries_by_frequency"] = (
        df.groupby("frequency")["tries"]
        .mean()
        .sort_values())

    # Win rate
    results["winrate_by_pos"] = (
        df.groupby("pos")["won"]
        .mean()
        .sort_values())

    results["winrate_by_syllables"] = (
        df.groupby("syllables")["won"]
        .mean()
        .sort_values())

    results["winrate_by_vowels"] = (
        df.groupby("vowels")["won"]
        .mean()
        .sort_values())

    results["winrate_by_frequency"] = (
        df.groupby("frequency")["won"]
        .mean()
        .sort_values())

    # Save analyses as separate CSV files
    if save_to_file:

        data_folder = Path(__file__).resolve().parent.parent / "data" / "tables_and_charts"

        for name, result in results.items():

            result.to_csv(
                data_folder / f"{name}.csv",
                index=True)
            
        combined = pd.concat(results, axis=1) #a file with all values
        combined.to_csv(data_folder / "analysis_all.csv", index=True)

        print("Alle Analyse-Dateien wurden erfolgreich erstellt.")

    return results

if __name__ == "__main__":
   analyze_game_data(save_to_file=True)

def top_5_first_letters(file):
    words = bd.read_pickle(file) #load words

    if isinstance(words, dict):
        word_list = list(words.keys())
    else:
        word_list = words

    first_letters = [w[0].lower() for w in word_list if isinstance(w, str) and len(w) > 0] #extract first letters

    df = pd.DataFrame(first_letters, columns=["first_letter"]) #calculate frequency
    counts = df["first_letter"].value_counts()
    percentages = df["first_letter"].value_counts(normalize=True) * 100

    top5 = pd.DataFrame({ #pick top 5
        "count": counts.head(5),
        "percent": percentages.head(5).round(2)
    })
    
    plt.figure(figsize=(10, 6)) #creates diagramm
    plt.bar(top5.index, top5["percent"], color="skyblue")
    plt.title("Top 5 initial letter – Percentage")
    plt.xlabel("Letter")
    plt.ylabel("Percent (%)")
    plt.tight_layout()

    data_folder = Path(__file__).resolve().parent.parent / "data" #saves diagramm
    plt.savefig(data_folder / "top5_first_letters.png")
    plt.close()

    print("Diagramm 'top5_first_letters.png' wurde erstellt.")

    return top5

if __name__ == "__main__":
    print(top_5_first_letters("../data/CMUdict_5_to_7_without_propn.pkl")) #prints top 5 from wordle dick
    print(top_5_first_letters("../data/CMUdict_5_to_7_without_propn.pkl"))

def avg_syllables_by_length_with_plot(file):

    words = bd.read_pickle(file) #load words

    if isinstance(words, dict): #takes key and values
        df = pd.DataFrame([
            {"word": w, 
             "length": len(w), 
             "syllables": words[w].get("syllables_count")}
            for w in words.keys()
        ])
    else:
        raise ValueError("The dictionary must be a dict (like propertie_dict.pkl).")

    df["syllables"] = pd.to_numeric(df["syllables"], errors="coerce") #make syllables to numbers

    result = df.groupby("length")["syllables"].mean().round(3) #calculate average

    plt.figure(figsize=(10, 6)) #creates diagramm
    plt.bar(result.index, result.values, color="skyblue")
    plt.title("Average number of syllables per word")
    plt.xlabel("Word length (number of letters)")
    plt.ylabel("Average syllables")
    plt.tight_layout()

    data_folder = Path(__file__).resolve().parent.parent / "data" #save diagramm
    plt.savefig(data_folder / "avg_syllables_by_length.png")
    plt.close()

    print("Diagramm 'avg_syllables_by_length.png' wurde erstellt.")
    return result

if __name__ == "__main__":
    print(avg_syllables_by_length_with_plot("../data/propertie_dict.pkl"))

def avg_vowels_with_plot(file, length=None):

    words = bd.read_pickle(file) #load words

    if isinstance(words, dict): #takes keys and values
        df = pd.DataFrame([
            {"word": w,
             "length": len(w),
             "vowels": sum(ch in "aeiou" for ch in w.lower())}
            for w in words.keys()
        ])
    else:
        raise ValueError("The dictionary must be a dict (like propertie_dict.pkl).")

    if length is not None: #filters if we search a specific length
        df = df[df["length"] == length]

        if df.empty:
            print(f"Keine Wörter mit Länge {length} gefunden.")
            return None

    result = df.groupby("length")["vowels"].mean().round(3) #calculate avergae

    plt.figure(figsize=(10, 6)) #creates diagramm
    plt.bar(result.index, result.values, color="skyblue")
    plt.title("Average number of vowels per word length")
    plt.xlabel("Word length (number of letters)")
    plt.ylabel("Average number of vowels")
    plt.tight_layout()

    data_folder = Path(__file__).resolve().parent.parent / "data" #saves diagramm
    plt.savefig(data_folder / "avg_vowels_by_length.png")
    plt.close()

    print("Diagramm 'avg_vowels_by_length.png' wurde erstellt.")
    return result

if __name__ == "__main__":
    print(avg_vowels_with_plot("../data/propertie_dict.pkl"))
    print(avg_vowels_with_plot("../data/propertie_dict.pkl", length=6)) #if we want to look at a spezific length

def top_10_words_with_plot(file):

    words = bd.read_pickle(file) #load words

    if not isinstance(words, dict):
        raise ValueError("The dictionary must be a dict (like propertie_dict.pkl).")

    df = pd.DataFrame([ #builds dataframe
        {
            "word": w,
            "frequenzy": words[w].get("frequenzies"),
            #"daily": words[w].get("daily_frequenzy")  #if we want the daily usage
        }
        for w in words.keys()
    ])

    df["frequenzy"] = pd.to_numeric(df["frequenzy"], errors="coerce") #frequency to numbers
    #df["daily"] = pd.to_numeric(df["daily"], errors="coerce")

    top10 = df.sort_values("frequenzy", ascending=False).head(10) #top10 most frequent words

    plt.figure(figsize=(10, 6)) #creates diagramm
    plt.bar(top10["word"], top10["frequenzy"], color="skyblue")
    plt.title("Top 10 most frequent words in the text")
    plt.xlabel("Word")
    plt.ylabel("Frequent")
    plt.xticks(rotation=45)
    plt.tight_layout()

    data_folder = Path(__file__).resolve().parent.parent / "data" #saves diagramm
    plt.savefig(data_folder / "top10_words.png")
    plt.close()

    print("Diagramm 'top10_words.png' wurde erstellt.")
    return top10

if __name__ == "__main__":
    print(top_10_words_with_plot("../data/propertie_dict.pkl"))
