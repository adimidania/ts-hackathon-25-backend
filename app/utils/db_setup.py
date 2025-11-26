from gym import Env
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URL)
db = client.db

# Helper to convert ObjectId to str
def obj_id(id):
    return str(id)
