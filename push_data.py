import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database_name = "NetworkSecurityData"
            self.collection_name = "NetworkLogs"
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    
    def cv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_to_mongoDb(self,records,database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len((self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        

if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'
    DATABASE ='NetworkSecurityData'
    Collection ='NetworkData'
    networkobj = NetworkDataExtract()
    networkobj.cv_to_json_converter(file_path=FILE_PATH)
    no_of_records = networkobj.insert_data_to_mongoDb(records=networkobj.cv_to_json_converter(file_path=FILE_PATH), database=DATABASE, collection=Collection)
    print(f"No of records inserted to MongoDB: {no_of_records}")