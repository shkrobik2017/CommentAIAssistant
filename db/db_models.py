from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field

from db.db_services import get_uuid4_id, UUIDStr


class CommonModel(BaseModel):
    id: UUIDStr = Field(default_factory=get_uuid4_id, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)


class UserModel(CommonModel, Document):
    username: str
    hashed_password: str
    email: str
    is_baned: bool = Field(default=False)


class ArticleModel(CommonModel, Document):
    user_id: UUIDStr
    content: str
    status: str = Field(default="In Progress")


class CommentModel(CommonModel, Document):
    article_id: UUIDStr
    content: str
