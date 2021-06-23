import sys
import pymongo
from collections import Counter
from pprint import pprint
import gzip
import json
import datetime
from tqdm import tqdm

CHUNK_SIZE = 500000

def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

if __name__ == '__main__':

    assert len(sys.argv) > 1, 'usage: {} <db>/<collection>'.format(sys.argv[0])

    operand = sys.argv[1]
    assert len(operand.split('/')) == 2, 'db and collection names are must!!'
    dbname, collection = operand.split('/')
    
    client = pymongo.MongoClient("localhost", 27017)
    db = client[dbname]
    
    counter = Counter()
    items = [item for item in db[collection].find()]

    for item in tqdm(items):
        del item['_id']

    for i in range(len(items) // CHUNK_SIZE + 1):
        start_index, end_index = i * CHUNK_SIZE, (i+1) * CHUNK_SIZE
        print('writing chunk {}-{}'.format(start_index, end_index))
        with gzip.open('{}-corpus--chunk-{}-{}.json.gz'.format(collection, start_index, end_index), 'wt') as f:
            f.write(json.dumps(items[start_index: end_index], indent=2, ensure_ascii=False, default = datetime_converter))
