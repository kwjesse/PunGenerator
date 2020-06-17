import nltk
from nltk.corpus import wordnet

"""
Use Thesaurus.com to get Synonyms
Example: Synonym for scream is shout

https://www.nltk.org/howto/wordnet.html <br/>
https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
"""


class SynonymsThesaurus:
    def __init__(self):
        pass

    def find_synonyms_antonyms(self, word):
        synonyms = []
        antonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        return set(synonyms), set(antonyms)
