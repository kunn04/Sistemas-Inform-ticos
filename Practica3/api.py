from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['practica3']