import pymongo 
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://max:ILoveFortnite333@cluster0.ppz7t.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB database End-to-End-IoT!")
except Exception as e:
    print(e)
