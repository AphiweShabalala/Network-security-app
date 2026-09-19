"""Manual MongoDB connectivity check; credentials are read from ``.env``."""
import os

from dotenv import load_dotenv
from pymongo import MongoClient


def check_connection() -> bool:
    load_dotenv()
    uri = os.getenv("MONGO_DB_URL")
    if not uri:
        raise RuntimeError("MONGO_DB_URL is not configured")
    client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
    client.admin.command("ping")
    return True


if __name__ == "__main__":
    print("MongoDB connection successful" if check_connection() else "Connection failed")
