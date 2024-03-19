from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb+srv://PythonDB:cud4BUXMwUmTI9A9@cluster0.zv0mgxq.mongodb.net/")

    db = client.hm_10
    return db