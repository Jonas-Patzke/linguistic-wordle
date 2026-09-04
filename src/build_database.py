import pickle

def create_propertie_dict(words, dicts: list):
    final_dict = {}
    for word in words:
        word_properties = {}
        word_properties.update({"length": dicts[0].get(word), "pos": dicts[1].get(word), "frequenzies": dicts[2].get(word), "syllables_count": dicts[3].get(word)})
        final_dict.update({word: word_properties})
    return final_dict




