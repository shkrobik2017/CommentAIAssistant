from fastapi import APIRouter, status, HTTPException, Depends
from celery_app.tasks import generate_comments
from db.db_models import ArticleModel, UserModel
from db.db_services import UUIDStr
from logger.logger import logger
from models.response_models import ArticleResponseModel
from routers.services import get_current_user, create_article, get_article, check_user_auth

router = APIRouter()


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleResponseModel
)
async def upload_articles(
        content: str,
        current_user: UserModel = Depends(get_current_user)
) -> ArticleResponseModel:
    article = await create_article(
        content=content,
        current_user=current_user
    )
    logger.info(f"Article created successfully: {article}")

    generate_comments.delay(str(article.id), content)

    response = ArticleResponseModel(
        id=article.id,
        content=content,
        status=article.status
    )
    return response


@router.get(
    path="/{article_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=ArticleResponseModel
)
async def get_article_status(
        article_id: UUIDStr,
        current_user: UserModel = Depends(get_current_user)
) -> ArticleResponseModel:

    article = await get_article(
        article_id=article_id,
        current_user=current_user
    )
    if article is not None:
        response = ArticleResponseModel(
            id=article.id,
            content=article.content,
            status=article.status
        )

        return response
    else:
        logger.error(f"Article with id: {article_id} not found")
        raise HTTPException(
            status_code=404,
            detail={"Not found": "Article not found"}
        )
