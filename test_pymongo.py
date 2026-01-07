from pymongo.mongo_client import MongoClient

uri = 'mongodb+srv://abhishekbirhade97_db_user:nbysTJ01AM3zR7CX@cluster0.azmeclf.mongodb.net/?appName=Cluster0'

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print('Pinged your deployment. You successfully connected to MongoDB!')
except Exception as e:
    print(e)