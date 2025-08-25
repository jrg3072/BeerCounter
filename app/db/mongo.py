from pymongo import MongoClient

client = MongoClient()
db = client["BeersCounter"]

user_collection = db["users"]
ranking_collection = db["ranking"]