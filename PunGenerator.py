"""
Pun Generator (PAUL BOT-puns are usually lame, but occasionally terrific)

Example:
What do you call a shout that has a pixel?
A computer scream
"""

import numpy as np
import pandas as pd
import csv
import os
import sys
import re
from wordfreq import zipf_frequency
from Modules.HomophoneFinder import *
from Modules.HypernymConceptInquirer import *
from Modules.SynonymsThesaurus import *
from Modules.TwoWordDatabase import *
from Modules.TemplateDatabase import *
import nltk

class PunGenerator:
    def __init__(self):
        self.thesaurus = SynonymsThesaurus()
        self.homophone = HomophoneFinder()
        self.phrase_database = TwoWordDatabase()
        self.templates = TemplateDatabase()

    # Global variables
    two_word_phrase = ""
    question = ""
    answer = ""
    nonhomophone_word = ""
    homophone_word = ""
    homophone_freq = 0.0
    hypernym_word = ""
    hypernym_freq = 0.0
    synonym_word = ""
    synonym_freq = 0.0
    antonym_word = ""
    antonym_freq = 0.0
    isSynonym = True

    def FindFrequency(self, word):
        return zipf_frequency(word, 'en', 'best', minimum=0.0)

    def FindAnswer(self):
        global nonhomophone_word
        global homophone_word
        global homophone_freq
        global answer
        global two_word_phrase

        # Initialize variable to null
        two_word_phrase = ""
        answer = ""
        nonhomophone_word = ""
        homophone_word = ""
        homophone_freq = 0.0

        while (True):
            # Randomly pick a two word phrase
            phrase_database = self.phrase_database.get_two_word_database()
            row = phrase_database.sample()
            two_word_phrase = row.iloc[0]['Adjective-Noun Pair']
            split = two_word_phrase.split(" ")
            first_word = split[0]
            second_word = split[1]
            # Checks for high Frequency of initial phrase
            first_word_freq = self.FindFrequency(first_word)
            second_word_freq = self.FindFrequency(second_word)
            if first_word_freq and second_word_freq < 3.0:
                break
            # Find a two word phrase with a homophone
            first_word_homo = self.homophone.find_homophones(first_word.upper())
            second_word_homo = self.homophone.find_homophones(second_word.upper())
            # Point to change and vs or
            if len(first_word_homo) != 0 or len(second_word_homo) != 0:
                # Create the Answer
                if len(first_word_homo) > len(second_word_homo):
                    # Get the the homophone words
                    keys = first_word_homo.keys()
                    count = 0
                    for key in keys:
                        homo_lowercase = key.lower()
                        # Get the parts of speech
                        tokenized_homo = nltk.word_tokenize(homo_lowercase)
                        tokenized_homo_tag = nltk.pos_tag(tokenized_homo)
                        if 'JJ' in tokenized_homo_tag[0][1]:
                            # If the first adjective, initialize homophone_word and homophone_feq
                            if count == 0:
                                homophone_freq = self.FindFrequency(homo_lowercase)
                                homophone_word = homo_lowercase
                                count += 1
                            else:
                                # Pick the word with the best frequency
                                freq = self.FindFrequency(homo_lowercase)
                                if freq > homophone_freq:
                                    homophone_freq = freq
                                    homophone_word = homo_lowercase
                                    count += 1
                    # Point change: threshold of frequency
                    if homophone_freq >= 3.0:
                        nonhomophone_word = second_word.lower()
                        answer = homophone_word + " " + nonhomophone_word
                        break
                    # Set variables back to zero and repeat while loop
                    else:
                        nonhomophone_word = ""
                        homophone_word = ""
                        homophone_freq = 0.0
                        answer = ""
                else:
                    # Get the the homophone words
                    keys = second_word_homo.keys()
                    for key in keys:
                        homo_lowercase = key.lower()
                        count = 0
                        # Get the parts of speech
                        tokenized_homo = nltk.word_tokenize(homo_lowercase)
                        tokenized_homo_tag = nltk.pos_tag(tokenized_homo)
                        if 'NN' in tokenized_homo_tag[0][1]:
                            # If the first noun, initialize homophone_word and homophone_feq
                            if count == 0:
                                homophone_freq = self.FindFrequency(homo_lowercase)
                                homophone_word = homo_lowercase
                                count += 1
                            # Pick the word with the best frequency
                            else:
                                freq = self.FindFrequency(homo_lowercase)
                                if freq > homophone_freq:
                                    homophone_freq = freq
                                    homophone_word = homo_lowercase
                                    count += 1
                    # Point change: threshold of frequency
                    if homophone_freq >= 3.0:
                        nonhomophone_word = first_word.lower()
                        answer = nonhomophone_word + " " + homophone_word
                        break
                    # Set variables back to zero and repeat while loop
                    else:
                        nonhomophone_word = ""
                        homophone_word = ""
                        homophone_freq = 0.0
                        answer = ""

    # Hypernym relationship test function
    def FindHypernym(self, topic):
        global hypernym_word
        global hypernym_freq
        global nonhomophone_word
        relation_list = []
        # Create a list of hypernyms
        ci = HypernymConceptInquirer(topic)
        relationships = ci.get_PartOf_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_IsA_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_HasA_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_AtLocation_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_CapableOf_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_Causes_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_FormOf_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_HasSubevent_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_RelatedTo_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        relationships = ci.get_UsedFor_nodes()
        for relation in relationships.items():
            relation_list.append(relation)
        count = 0
        # For every hypernym
        for rel in relation_list:
            rel_lower = rel[0].lower()
            # Determine if the hypernym is more than one word
            split = re.split(" -_", rel_lower)
            # If the hypernym is only one word
            if len(split) == 1:
                # If hypernym is not the starting word
                if rel_lower != nonhomophone_word:
                    # initialize hypernym_word and hypernym_feq
                    if count == 0:
                        hypernym_freq = self.FindFrequency(rel_lower)
                        hypernym_word = rel_lower
                        count += 1
                    # Pick the word with the best frequency
                    else:
                        freq = self.FindFrequency(rel_lower)
                        if freq > hypernym_freq:
                            hypernym_freq = freq
                            hypernym_word = rel_lower
                            count += 1


    def FindSynonymOrAntonym(self):
        global homophone_word
        global hypernym_word
        global synonym_word
        global antonym_word
        global hypernym_freq
        global synonym_freq
        global antonym_freq
        global question
        global isSynonym

        question = ""
        hypernym_word = ""
        hypernym_freq = 0.0
        synonym_word = ""
        synonym_freq = 0.0
        antonym_word = ""
        antonym_freq = 0.0

        # Find synonyms and antonyms
        count = 0
        synonyms, antonyms = self.thesaurus.find_synonyms_antonyms(homophone_word)
        for syn in synonyms:
            syn_lower = syn.lower()
            # If synonym is not the starting word
            if syn_lower != homophone_word:
                # initialize synonym_word and synonym_feq
                if count == 0:
                    synonym_freq = self.FindFrequency(syn_lower)
                    synonym_word = syn_lower
                    count += 1
                # Pick the word with the best frequency
                else:
                    freq = self.FindFrequency(syn_lower)
                    if freq > synonym_freq:
                        synonym_freq = freq
                        synonym_word = syn_lower
                        count += 1
        isSynonym = True
        if len(antonyms) > 0:
            count = 0
            for ant in antonyms:
                ant_lower = ant.lower()
                # If antonym is not the starting word
                if ant_lower != homophone_word:
                    # initialize antonym_word and antonym_feq
                    if count == 0:
                        antonym_freq = self.FindFrequency(ant_lower)
                        antonym_word = ant_lower
                        count += 1
                    # Pick the word with the best frequency
                    else:
                        freq = self.FindFrequency(ant_lower)
                        if freq > synonym_freq:
                            antonym_freq = freq
                            antonym_word = ant_lower
                            count += 1
            # Use the antonym if the frequency is higher than the synonym
            if antonym_freq > synonym_freq:
                isSynonym = False
            else:
                isSynonym = True

    def FindQuestion(self):
        global homophone_word
        global nonhomophone_word
        global hypernym_word
        global synonym_word
        global antonym_word
        global hypernym_freq
        global synonym_freq
        global antonym_freq
        global question
        global isSynonym

        question = ""
        hypernym_word = ""
        hypernym_freq = 0.0
        synonym_word = ""
        synonym_freq = 0.0
        antonym_word = ""
        antonym_freq = 0.0

        self.FindSynonymOrAntonym()
        self.FindHypernym(nonhomophone_word)

        tokenized_hyper_tag = []
        tokenized_syn_ant_tag = []
        is_hyper_NN_JJ = False
        is_syn_ant_NN_JJ = False
        is_hyper_V = False
        is_syn_ant_V = False

        # If a synonym or antonym was picked
        if synonym_word or antonym_word:
            # Get the parts of speech
            tokenized_hyper = nltk.word_tokenize(hypernym_word)
            tokenized_hyper_tag = nltk.pos_tag(tokenized_hyper)

            # Get parts of speech if the synonym was picked
            if isSynonym:
                tokenized_syn = nltk.word_tokenize(synonym_word)
                tokenized_syn_ant_tag = nltk.pos_tag(tokenized_syn)
            # Get parts of speech if the antonym was picked
            else:
                tokenized_ant = nltk.word_tokenize(antonym_word)
                tokenized_syn_ant_tag = nltk.pos_tag(tokenized_ant)

            # Determine if hypernym is noun, adjective of verb
            if 'NN' in tokenized_hyper_tag[0][1] or 'JJ' in tokenized_hyper_tag[0][1]:
                is_hyper_NN_JJ = True
            elif "V" in tokenized_hyper_tag[0][1]:
                is_hyper_V = True
            # Else start over
            else:
                hypernym_word = ""
                hypernym_freq = 0.0
                synonym_word = ""
                synonym_freq = 0.0
                antonym_word = ""
                antonym_freq = 0.0

            # Determine if synonym/antonym is noun, adjective of verb
            if 'NN' in tokenized_syn_ant_tag[0][1] or 'JJ' in tokenized_syn_ant_tag[0][1]:
                is_syn_ant_NN_JJ = True
            elif "V" in tokenized_syn_ant_tag[0][1]:
                is_syn_ant_V = True
            # Else start over
            else:
                hypernym_word = ""
                hypernym_freq = 0.0
                synonym_word = ""
                synonym_freq = 0.0
                antonym_word = ""
                antonym_freq = 0.0
        # If right parts of speech
        if (synonym_word or antonym_word) and hypernym_word:
            templates = self.templates.get__templates()

            # Filter for negative and positive templates
            neg_templates = templates[templates.iloc[:]["Is_Negative"] == True]
            pos_templates = templates[templates.iloc[:]["Is_Negative"] == False]

            # Pick template
            # If need a positive template
            if isSynonym:
                if is_hyper_NN_JJ and is_syn_ant_NN_JJ:
                    pos_templates_NN_JJ = pos_templates[pos_templates.iloc[:]["First_Parts_Of_Speech"] == "NN/JJ"]
                    question = pos_templates_NN_JJ.iloc[0][0]
                else:
                    pos_templates_V = pos_templates[pos_templates.iloc[:]["First_Parts_Of_Speech"] != "NN/JJ"]
                    question = pos_templates_V.iloc[0][0]
            # If need a negative template
            else:
                if is_hyper_NN_JJ and is_syn_ant_NN_JJ:
                    neg_templates_NN_JJ = neg_templates[neg_templates.iloc[:]["First_Parts_Of_Speech"] == "NN/JJ"]
                    question = neg_templates_NN_JJ.iloc[0][0]
                else:
                    neg_templates_V = neg_templates[neg_templates.iloc[:]["First_Parts_Of_Speech"] != "NN/JJ"]
                    question = neg_templates_V.iloc[0][0]

            vowels = ["a", "e", "i", "o", "u"]

            # If an noun add an article
            if 'NN' in tokenized_hyper_tag[0][1]:
                isVowel = False
                for vowel in vowels:
                    # If this vowel, add 'an' to word
                    if hypernym_word[0] == vowel:
                        hypernym_word = "an " + hypernym_word
                        isVowel = True
                        break
                # If not a vowel, add 'a' to word
                if not isVowel:
                    hypernym_word = "a " + hypernym_word

            # If an noun add an article
            if 'NN' in tokenized_syn_ant_tag[0][1]:
                if isSynonym:
                    isVowel = False
                    for vowel in vowels:
                        # If this vowel, add 'an' to word
                        if synonym_word[0] == vowel:
                            synonym_word = "an " + synonym_word
                            isVowel = True
                            break
                    # If not a vowel, add 'a' to word
                    if not isVowel:
                        synonym_word = "a " + synonym_word
                else:
                    isVowel = False
                    for vowel in vowels:
                        # If this vowel, add 'an' to word
                        if antonym_word[0] == vowel:
                            antonym_word = "an " + antonym_word
                            isVowel = True
                            break
                    # If not a vowel, add 'a' to word
                    if not isVowel:
                        antonym_word = "a " + antonym_word

            # Add hypernym and synonym/antonym to sentence structure
            if is_hyper_V and isSynonym:
                question = question.replace("_", hypernym_word, 1)
                question = question.replace("_", synonym_word, 1)
            elif is_hyper_V and not isSynonym:
                question = question.replace("_", hypernym_word, 1)
                question = question.replace("_", antonym_word, 1)
            elif is_syn_ant_V and isSynonym:
                question = question.replace("_", synonym_word, 1)
                question = question.replace("_", hypernym_word, 1)
            elif is_syn_ant_V and not isSynonym:
                question = question.replace("_", antonym_word, 1)
                question = question.replace("_", hypernym_word, 1)
            elif is_syn_ant_NN_JJ and is_hyper_NN_JJ and isSynonym:
                question = question.replace("_", hypernym_word, 1)
                question = question.replace("_", synonym_word, 1)
            elif is_syn_ant_NN_JJ and is_hyper_NN_JJ and not isSynonym:
                question = question.replace("_", hypernym_word, 1)
                question = question.replace("_", antonym_word, 1)

    def PunGeneratorSolver(self):
        global nonhomophone_word
        global homophone_word
        global homophone_freq
        global answer
        global two_word_phrase
        global hypernym_word
        global synonym_word
        global hypernym_freq
        global synonym_freq
        global antonym_word
        global antonym_freq
        global question
        global isSynonym

        synonym_word = ""
        antonym_word = ""
        hypernym_word = ""

        while (not synonym_word and not antonym_word) or not hypernym_word:
            self.FindAnswer()
            self.FindQuestion()

        """print("The two word phrase is " + two_word_phrase)
        print("The answer is " + answer)
        print("Homophone is " + homophone_word + " with a frequency of " + str(homophone_freq))
        print("Nonhomophone is " + nonhomophone_word)
        if isSynonym:
            print("The synonym is " + synonym_word + " with a frequency of " + str(synonym_freq))
        else:
            print("The antonym is " + antonym_word + " with a frequency of " + str(antonym_freq))
        print("Hypernym is " + hypernym_word + " with a frequency of " + str(hypernym_freq))"""
        print(question)
        print(answer)

        """"
        # Path to Artefacts.csv
        artefact_path = os.path.join(os.getcwd(), 'DataSets', 'Artefacts_v2.csv')
        # Row to add to UserEvaluation.csv (Example for now)
        toAdd = [question, answer]

        # Writes toAdd to Artefacts.csv
        with open(artefact_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(toAdd)
        """

puns = PunGenerator()
puns.PunGeneratorSolver()
