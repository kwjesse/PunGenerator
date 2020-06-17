import Levenshtein
import pandas as pd

"""
Find Homophones from the CMU dictionary
Example: A homophone for screen is scream
"""
class HomophoneFinder:
    def __init__(self):
        # Import the CMU dictionary
        self.cmu_dict = pd.read_csv('http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict.0.7a',
                                    sep='delimiter', header=None, engine='python')
        self.phonetic_dictionary = self.create_phonetic_dict()

    def create_phonetic_dict(self):
        phonetic_dictionary = {}

        # Create a dictionary with the word as the key and the phonetic spelling as the value
        for x in range(118, 133336):
            line = str(self.cmu_dict[x:x + 1][0])
            line = line.split("\n")
            line = line[0].split(" ")
            line = line[4:]
            phonetic_dictionary[line[0]] = " ".join(line[i] for i in range(2, len(line)))
        return phonetic_dictionary

    # Finds homophones that are 1 edit distance away
    def find_homophones(self, word):
        homophones = {}
        if word in self.phonetic_dictionary:
            phonetic_val = self.phonetic_dictionary[word]
            for key, value in self.phonetic_dictionary.items():
                dist = Levenshtein.distance(phonetic_val, value)
                if dist <= 1:
                    if key != word:
                        homophones[key] = value
        # Point to change: To increase the probability that the word does rhyme
        if len(homophones) >= 3:
            return homophones
        else:
            homophones = {}
            return homophones
