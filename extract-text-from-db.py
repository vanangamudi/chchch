import pymongo
from collections import Counter
from pprint import pprint
import gzip
import json

from tqdm import tqdm

client = pymongo.MongoClient("localhost", 27017)
db = client.test

counter = Counter()

with gzip.open('corpus.txt.gz', 'wt') as f:
    items = [item for item in db.kiruvam.find()]
    for item in tqdm(items):
        del item['_id']
    f.write(json.dumps(items, indent=2, ensure_ascii=False))
