import json
from data_updator import add

with open('qdrant_storage/new_wine.json') as wine_file:
    new_wine = json.load(wine_file)

add.delay(new_wine)
