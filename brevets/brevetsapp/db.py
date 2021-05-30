"""
Database helper functions
"""
from pymongo import MongoClient

class Mongodb:

    def __init__(self, client_name="testclient"):
        self.name = client_name
        self.client = None
        self.data = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.name, 27017)

    def set_data(self, name):
        self.data = self.client[name]

    def insert(self, data_base, row):
        self.data[data_base].insert_one(row)

    def delete_rows(self, data_base):
        self.data[data_base].delete_many({})

    def list_rows(self, data_base):
        return list(self.data[data_base].find())