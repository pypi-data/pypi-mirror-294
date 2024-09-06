
import pandas as pd
import json
from pymongo.mongo_client import MongoClient
class mongo_crud_operations:
    def __init__(self, client_uri: str, db_name:str, coll_name:str):
        self.client= self.create_client(client_uri)
        self.db = self.create_database(db_name)
        self.collection = self.create_collection(coll_name)

    def create_client(self,uri):
        return MongoClient(uri)
    
    def create_database(self,name):
        return self.client[name]
    
    def create_collection(self,name):
        return self.db[name]
    
    def insert_one_record(self,data):
        if type(data) == list:
            for d in data:
                if type(d) != dict:
                    raise ValueError("data should be in dict")
            self.collection.insert_many(data)
        elif type(data) == dict:
            self.collection.insert_one(data)
        else:
            raise ValueError('data should be in dict format')
        
    def find_all_records(self):
        records = list(self.collection.find())
        for r in records:
            print(r)
    
    def insert_in_bulk(self,datafile:str):
        self.path = datafile

        if self.path.endswith(".json"):
            with open(self.path, "r") as file:
                data = json.load(file)
        elif self.path.endswith(".csv"):
            data = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith('.xlsx'):
            data = pd.read_excel(self.path, encoding='utf-8')

        datajson = json.loads(data.to_json(orient='records'))
        self.collection.insert_many(datajson)