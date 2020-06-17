from Modules.SynonymsThesaurus import *

thesaurus = SynonymsThesaurus()

synonyms, antonyms = thesaurus.find_synonyms_antonyms("scream")
print(synonyms)
