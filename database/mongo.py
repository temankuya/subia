from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

if not MONGO_URL:
    raise ValueError("MONGO_URL belum disetel di config.env")

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.fsub
usersdb = mongodb.user


async def is_served_user(user_id: int) -> bool:
    return await usersdb.find_one({"user_id": user_id}) is not None


async def get_served_users() -> list[int]:
    return [user["user_id"] async for user in usersdb.find({"user_id": {"$gt": 0}})]


async def add_served_user(user_id: int):
    if await is_served_user(user_id):
        return
    result = await usersdb.insert_one({"user_id": user_id})
    return result.inserted_id
