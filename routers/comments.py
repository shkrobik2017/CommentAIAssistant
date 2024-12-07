from fastapi import APIRouter, status, HTTPException, Depends
from db.db_models import ArticleModel, CommentModel, UserModel
from db.db_services import UUIDStr
from models.response_models import GetCommentsResponseModel
from routers.services import get_current_user

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
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail={"Unauthorized": "User is not authorized"}
        )
    if await ArticleModel.get(article_id) is None:
        raise HTTPException(
            status_code=404,
            detail={"NotFound": "Article not found"}
        )

    comments = await CommentModel.find({"article_id": article_id}).to_list(length=None)

    return GetCommentsResponseModel(comments=comments)

