"""
Database insertion and retrieval
"""
from pymongo import MongoClient

class Mongodb:
    def __init__(self, client_name="testclient"):
        self.name = client_name
        self.client = None
        self.data = None
        self.collection = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.name, 27017)

    def set_data(self, data_name):
        self.data = self.client[data_name]

    def set_collection(self, collection_name):
        self.collection = self.data[collection_name]

    def list_rows(self):
        return list(self.collection.find())

    def f_field(self, fields):
        _dict = {}
        for i in fields:
            _dict[i] = 1
        _dict["_id"] = 0

        rows = []
        for i in self.collection.find({}, _dict):
            rows.append(i)
        return rows

    def search_for_head(self, fields, k):
        _dict = {}
        for i in fields:
            _dict[i] = 1
        _dict["_id"] = 0

        return list(self.collection.find({}, _dict).sort("km").limit(k))
