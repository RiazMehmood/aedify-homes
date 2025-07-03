from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
import os

MONGO_URI = "mongodb+srv://devloop110:AGIbWZKYa14TwTCe@realestate.uwrwi7x.mongodb.net/?retryWrites=true&w=majority&appName=realestate"

def check_mongo_connection(uri):
    client = None
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        server_info = client.server_info()
        print("✅ Connected to MongoDB!")
        print(f"MongoDB Version: {server_info['version']}")
    except ServerSelectionTimeoutError as e:
        print("❌ Server selection timed out. Check internet or DNS.")
        print(f"Error: {e}")
    except ConfigurationError as e:
        print("❌ Configuration error in MONGO_URI.")
        print(f"Error: {e}")
    except ConnectionFailure as e:
        print("❌ Could not connect to MongoDB.")
        print(f"Error: {e}")
    except Exception as e:
        print("❌ Unknown error occurred.")
        print(f"Error: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    check_mongo_connection(MONGO_URI)

