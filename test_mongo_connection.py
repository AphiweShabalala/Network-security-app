import os
import pymongo
from dotenv import load_dotenv

def check_connection() -> bool:
    """Ping MongoDB when run manually; importing this module has no side effects."""
    load_dotenv()
    mongo_db_url = os.getenv("MONGO_DB_URL")
    if not mongo_db_url:
        raise RuntimeError("MONGO_DB_URL is not configured")

    client = pymongo.MongoClient(mongo_db_url, serverSelectionTimeoutMS=10_000)
    client.admin.command("ping")
    return True


if __name__ == "__main__":
    print("MongoDB connection successful" if check_connection() else "Connection failed")
