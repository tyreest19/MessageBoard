from pymongo import MongoClient

class Database(object):

    def __init__(self,database,collection,uri):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def show_all_entries(self):
        '''returns a list of all entries'''
        entries = [entries for entries in self.collection.find()]
        return entries

    def find(self,query):
        entries = [entries for entries in self.collection.find(query)]
        return entries

    def find_one(self, query, verify_new_user=False):
        if verify_new_user== True:
            return self.collection.find_one(query)
        entries = [entries for entries in self.collection.find(query)]
        return entries[0]

    def insert(self,query):
        self.collection.insert(query)

    def delete(self,query):
        self.collection.delete_many(query)

    def update(self,id,updated_data):
        self.collection.update(id, updated_data, upsert=False)


