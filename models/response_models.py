from enum import Enum
from pydantic import BaseModel
from db.db_models import CommentModel
from db.db_services import UUIDStr


class ArticleResponseModel(BaseModel):

    class StatusEnum(str, Enum):
        completed = "Completed"
        in_progress = "In Progress"

    id: UUIDStr
    content: str
    status: StatusEnum


class GetCommentsResponseModel(BaseModel):
    comments: list[CommentModel]
