import text_processing as tp
import build_database as bd
import extract_properties_functions as epf
print("test")
token = tp.create_token() #extract abd create token from a text, lowers and filters them
lemma1 = tp.create_lemma(token) #create lemma out of the tokens, solving edge cases and remove duplicates
pos_tags = epf.pos_tagger(token) #dict of word and its pos-tag
lemma2 = tp.remove_proper_names(pos_tags) #depending on those lemmas, we will fill our database
final_lemma = []

for lemma in lemma2: #lemma1 cleans our words, since the function remove_proper_names() has the pos_tags_dict_dict as input, we loose our cleaning from lemma 1
    if lemma in lemma1: #so we create the intersection
        final_lemma.append(lemma)

word_length = epf.number_of_letters(final_lemma) #dict of word and its length
word_frequenzies = epf.extract_frequenzy("../data/first_three_chapters.txt", final_lemma) #dict of word and its frequenzy
word_syllables_count = epf.extract_syllables(final_lemma)
word_constituents_count = epf.extract_constituents(token)
properties_dict_list = [word_length, pos_tags, word_frequenzies, word_syllables_count, word_constituents_count]
propertie_dict = bd.create_propertie_dict(final_lemma, properties_dict_list)
#print(lemma) #just for testsing and visualisation
print(propertie_dict) #just for testsing and visualisation
