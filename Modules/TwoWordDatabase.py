import pandas as pd


class TwoWordDatabase:
    def __init__(self):
        # Have to specify pungenerator as working directory in Settings > Project > Project Structure
        self.W2_Adj_Noun_Pairs = pd.read_csv('DataSets/W2_Adj_Noun_Pairs_With_Homo.csv')

    def create_two_word_dict(self):
        phrase_dictionary = {}

        # Create a dictionary with the frequency as the key and a list of two-word phrases as the value
        for x in range(len(self.W2_Adj_Noun_Pairs)):
            if self.W2_Adj_Noun_Pairs.iloc[x, 0] in phrase_dictionary:
                phrase_dictionary[self.W2_Adj_Noun_Pairs.iloc[x, 0]].append(
                    str(self.W2_Adj_Noun_Pairs.iloc[x, 1]) + " " + str(self.W2_Adj_Noun_Pairs.iloc[x, 2]))
            else:
                phrase_dictionary[self.W2_Adj_Noun_Pairs.iloc[x, 0]] = \
                    [str(self.W2_Adj_Noun_Pairs.iloc[x, 1]) + " " + str(self.W2_Adj_Noun_Pairs.iloc[x, 2])]
        return phrase_dictionary

    def get_two_word_database(self):
        return self.W2_Adj_Noun_Pairs
