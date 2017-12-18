import json
import datetime

file = open('../news/links/100/' + str(datetime.date.today()) + '.json', 'r', encoding='utf-8')
test = json.loads(file.read())

for link in test['links']:
    print(link)