import json
# from bson.objectid import ObjectId
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb+srv://PythonDB:cud4BUXMwUmTI9A9@cluster0.zv0mgxq.mongodb.net/")

# db = client.hm

with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)

db = client.hm_10

for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            'author': ObjectId(author['_id'])
        })