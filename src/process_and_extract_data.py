import text_processing as tp
import build_database as bd
import extract_properties_functions as epf


token = tp.create_token() #extract abd create token from a text, lowers and filters them
pos_tags = epf.pos_tagger(token) #dict of word and its pos-tag
lemma1 = tp.create_lemma(token) #create lemma out of the tokens, solving edge cases and remove duplicates
lemma2 = tp.remove_proper_names(pos_tags) #depending on those lemmas, we will fill our database, since we do not want proper names
final_lemma = [] 

for lemma in lemma2: #lemma1 cleans our words, since the function remove_proper_names() has the pos_tags_dict_dict as input, we loose our cleaning from lemma 1
    if lemma in lemma1: #so we create the intersection
        final_lemma.append(lemma)

desired_length = [  #filter the words so we only have words between the length of 5 to 7
    w for w in final_lemma
    if 5 <= len(w) <= 7
]

final_lemma = desired_length # the words we want to get the properties of, these words are also the ones that the players have to find out


#create a dict of words ans their properties
word_length = epf.number_of_letters(final_lemma) #dict of word and its length
word_frequenzies = epf.extract_frequenzy("../data/extracted_chapters.txt", final_lemma) #dict of word and its frequenzy
word_syllables_count = epf.extract_syllables(final_lemma) #dict of words and theircounts of syllables
properties_dict_list = [word_length, pos_tags, word_frequenzies, word_syllables_count] #create a list to automaticly extract the properties from the dicts
propertie_dict = bd.create_propertie_dict(final_lemma, properties_dict_list) #create the final dict of words and their properties
#print(propertie_dict) #just for testsing and visualisation
#print(len(propertie_dict)) #just for testing and visualisation


bd.create_pickle("../data/propertie_dict.pkl",propertie_dict) # create a pickle for our propertie_dict, so we dont always have to load it
print("count of entries: " + str(len(propertie_dict))) #output to see how many word entries we got
cmu_words = " ".join(element for element in epf.return_cmu_dict() if 5 <= len(element) <= 7)
pos_tags_for_cmu_words = epf.pos_tagger(tp.tokenize(cmu_words)) #dict of word and its pos-tag
bd.create_pickle("../data/CMUdict_5_to_7.pkl", pos_tags_for_cmu_words) #store only words that are between 5 to 7 letters long, but with propn
for key in list(pos_tags_for_cmu_words.keys()): # now we remove words from the cmu dict, that get labeles as PROPN as pos-tag
    if pos_tags_for_cmu_words.get(key) == "PROPN":
        del pos_tags_for_cmu_words[key]
bd.create_pickle("../data/CMUdict_5_to_7_without_propn.pkl", pos_tags_for_cmu_words) #for our diagram, to compare the words of both dict, but without PROPN
print("done")



