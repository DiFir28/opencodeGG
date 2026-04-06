import json

with open('borders.json', 'r', encoding='utf-8') as file:
     borders = json.load(file)

print(borders)

