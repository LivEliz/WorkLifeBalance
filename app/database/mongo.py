from pymongo import MongoClient

# MongoDB connection URL
MONGO_URL = "mongodb://localhost:27017"

# Create client
client = MongoClient(MONGO_URL)

# Create / connect to database
db = client["worklife_balance_db"]

# Collections
users_collection = db["users"]
weekly_logs_collection = db["weekly_logs"]
recommendations_collection = db["recommendations"]