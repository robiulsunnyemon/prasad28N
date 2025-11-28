from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie
from src.prasad.auth.model.user import UserModel
import os
from src.prasad.images.model.image_model import ImageModel



load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017/poetry_prasad")
DB_NAME = os.getenv("DATABASE_NAME", "poetry_prasad")



async def init_db():
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DETAILS)
    database: AsyncIOMotorDatabase = client.get_database(DB_NAME)

    # Beanie init
    await init_beanie(
        database=database,
        document_models=[
            UserModel,
            ImageModel
        ],
    )


async def drop_user_collection():
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DETAILS)
    database: AsyncIOMotorDatabase = client.get_database()
    await database.drop_collection("drone_service_order")

