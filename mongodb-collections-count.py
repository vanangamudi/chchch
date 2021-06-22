import pymongo
from collections import Counter
from pprint import pprint

client = pymongo.MongoClient("localhost", 27017)
db = client.test

for dbobj in client.list_databases():
    dbname = dbobj['name']
    db = client[dbname]
    for cname in db.list_collection_names():
        print('{}/{}: {}'.format(dbname, cname, db[cname].estimated_document_count()))
