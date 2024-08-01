from pymongo import MongoClient

# Ensure pymongo is installed: pip install pymongo

client = MongoClient("localhost", 27017)

# Access the source collection
source_collection = client["models"]["outputs_gemma-2b_1722274538_2400"]

# Access the target collection
target_collection = client["online_fine_tuning"]["outgoing"]

# Retrieve all documents from the source collection
documents = list(source_collection.find())

# Insert all documents into the target collection
if documents:
    print("hey")
    target_collection.insert_many(documents)
