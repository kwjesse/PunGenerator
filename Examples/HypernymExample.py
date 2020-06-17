import os, sys
from Modules.HypernymConceptInquirer import *

sys.path.append(os.getcwd())

topic = input('Enter a topic: ')

ci = HypernymConceptInquirer(topic)

relationships = ci.get_PartOf_nodes()

for relation in relationships.items():
    print(relation)
