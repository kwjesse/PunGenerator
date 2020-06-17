import csv
import os

# Path to Artefacts.csv
artefact_path = os.path.join(os.getcwd(), '..', 'DataSets', 'Artefacts.csv')
# Row to add to UserEvaluation.csv (Example for now)
toAdd = ['What do you call _ _?', '_ _', '1']

# Writes toAdd to Artefact.csv
with open(artefact_path, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(toAdd)