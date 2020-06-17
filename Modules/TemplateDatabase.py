import pandas as pd


class TemplateDatabase:
    def __init__(self):
        # Have to specify pungenerator as working directory in Settings > Project > Project Structure
        self.Templates = pd.read_csv('DataSets/Templates.csv')

    def get__templates(self):
        return  self.Templates
