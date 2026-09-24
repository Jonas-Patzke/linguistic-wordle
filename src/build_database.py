import pickle
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #change the working directory to find our txt


def create_propertie_dict(words, dicts: list):
    final_dict = {}
    for word in words:
        word_properties = {}
        word_properties.update({"length": dicts[0].get(word), "pos": dicts[1].get(word), "frequenzies": dicts[2].get(word), "syllables_count": dicts[3].get(word)})
        final_dict.update({word: word_properties})
    return final_dict

def create_pickle(file_path,content): #our content sould be the propertie dict, from this dict we will pick a random word
    with open(file_path, "wb") as pickle_outfile:
        pickle.dump(content, pickle_outfile)

def read_pickle(file_path):
    with open("../data/propertie_dict.pkl", "rb") as pickle_infile:
        return pickle.load(pickle_infile)

    






