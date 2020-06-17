from Modules.TwoWordDatabase import *

phrase_database = TwoWordDatabase()

phrases = phrase_database.get_two_word_database()
print(phrases.head(10))
(phrases.tail(10))

phrase_dict = phrase_database.create_two_word_dict()

# Check that the dictionary begins at the first word
print(sorted(phrase_dict.keys(), reverse=True))

print(phrase_dict[1030])


print(phrase_dict[phrases['Frequency'].max()])

print(phrase_dict[phrases['Frequency'].min()])