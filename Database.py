from pymongo import MongoClient

class Database(object):

    def __init__(self,database,collection,uri):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def show_all_entries(self):
        return self.collection.find()

    def find(self,query):
        return self.collection.find(query)

    def find_one(self,query):
        return self.collection.find_one(query)

    def insert(self,query):
        self.collection.insert(query)

    def delete(self,query):
        self.collection.delete_many(query)

    def update(self,id,updated_data):
        self.collection.update(id, updated_data, upsert=False)


