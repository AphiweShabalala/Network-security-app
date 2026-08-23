import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print("Mongo URL loaded:", bool(MONGO_DB_URL))

try:
    client = pymongo.MongoClient(
        MONGO_DB_URL,
        serverSelectionTimeoutMS=10000
    )

    print("Client created")

    print("Running ping...")
    result = client.admin.command("ping")

    print("MongoDB ping successful:", result)

    print("Databases:")
    print(client.list_database_names())

except Exception as e:
    print("MongoDB connection FAILED")
    print(type(e).__name__)
    print(e)