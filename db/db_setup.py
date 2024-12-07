from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from db.db_models import ArticleModel, CommentModel, UserModel
from settings import settings

MONGODB_MODELS = [
    ArticleModel,
    CommentModel,
    UserModel
]


async def init_mongodb_beanie() -> None:
    client = AsyncIOMotorClient(settings.MONGODB_URI)

    await init_beanie(database=client.db_name, document_models=MONGODB_MODELS)
