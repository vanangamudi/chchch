import sys
import pymongo
from collections import Counter
from pprint import pprint
import gzip
import json
import datetime
from tqdm import tqdm


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
    
    with gzip.open('{}-corpus.txt.gz'.format(collection), 'wt') as f:
        items = [item for item in db[collection].find()]
        for item in tqdm(items):
            del item['_id']
            
        f.write(json.dumps(items, indent=2, ensure_ascii=False, default = datetime_converter))
