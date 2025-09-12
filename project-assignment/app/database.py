import motor.motor_asyncio
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)


db = mongo_client["assignment_db"]


users_collection = db["users"]
