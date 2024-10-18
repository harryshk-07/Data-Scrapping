from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    
    db = client['scrapingDB']
    collection = db['scrapedData']

    client.server_info() 
    print("Successfully connected to MongoDB!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
