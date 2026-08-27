import text_processing as tp
import build_database as bd
import extract_properties_functions as epf

token = tp.create_token() #extract abd create token from a text, lowers and filters them
lemma = tp.create_lemma(token) #create lemma out of the tokens, solving edge cases and remove duplicates
word_length = epf.number_of_letters #dict of word and its length
pos_tags = epf.pos_tagger(token) #dict of word and its pos-tag
lemma = tp.remove_proper_names(pos_tags) #depending on those lemmas, we will fill our database
word_frequenzies = epf.extract_frequenzy("../data/first_three_chapters.txt", lemma) #dict of word and its frequenzy
word_syllables_count = "" #has do bes done
word_constituents_count = "" #has to be done

print(lemma) #just for testsing and visualisation

