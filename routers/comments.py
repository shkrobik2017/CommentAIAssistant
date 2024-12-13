from fastapi import APIRouter, status, HTTPException, Depends
from db.db_models import ArticleModel, CommentModel, UserModel
from db.db_services import UUIDStr
from models.response_models import GetCommentsResponseModel
from routers.services import get_current_user, get_article_comments_from_db

router = APIRouter()


@router.get(
    path="/{article_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=GetCommentsResponseModel
)
async def get_article_comments(
        article_id: UUIDStr,
        current_user: UserModel = Depends(get_current_user)
) -> GetCommentsResponseModel:
    comments = await get_article_comments_from_db(
        current_user=current_user,
        article_id=article_id
    )

    return GetCommentsResponseModel(comments=comments)

