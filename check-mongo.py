import pymongo
from collections import Counter
from pprint import pprint

client = pymongo.MongoClient("localhost", 27017)
db = client.test

counter = Counter()

counter.update([item['url'].strip() for item in db.kiruvam.find()])

duplicates = [(i, v) for i, v in counter.items() if v > 1]
duplicates = list(duplicates)
pprint(duplicates)
print('{} - {}'.format(len(counter), len(duplicates)))

with open('urls.txt', 'w') as f:
    f.write('\n'.join(sorted(counter.keys())))
