from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:

    def __init__(self, url: str, database_name: str):
        self.client = AsyncIOMotorClient(url)
        self.database_name = database_name
