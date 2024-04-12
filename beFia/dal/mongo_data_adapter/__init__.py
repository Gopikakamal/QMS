from os import getenv
from pymongo import MongoClient

db_connection = MongoClient(getenv("MONGO_URI"))
