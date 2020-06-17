from Modules.HomophoneFinder import *
from wordfreq import zipf_frequency

# Find the homophones for SCREEN
homophone = HomophoneFinder()
found_homophones = homophone.find_homophones("TURTLE")
print(found_homophones)
for words in found_homophones:
    print(zipf_frequency(words, 'en', 'best', minimum=0.0))
