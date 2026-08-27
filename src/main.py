import text_processing as tp
import build_database as bd
import extract_properties_functions as epf

token = tp.create_token()
lemma = tp.create_lemma(token)
word_length = epf.number_of_letters
pos_tags = epf.pos_tagger(token)
lemma = tp.remove_proper_names(pos_tags)
word_frequenzies = epf.extract_frequenzy("../data/first_three_chapters.txt", lemma)
word_syllables_count = "" #has do bes done
word_constituents_count = "" #has to be done

print(lemma)

