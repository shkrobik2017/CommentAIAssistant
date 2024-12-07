from fastapi import APIRouter, status, HTTPException, Depends
from celery_app.tasks import generate_comments
from db.db_models import ArticleModel, UserModel
from db.db_services import UUIDStr
from logger.logger import logger
from models.response_models import ArticleResponseModel
from routers.services import get_current_user

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
    if len(content) == 0:
        logger.error(f"Uploaded article not found: {content}")
        raise HTTPException(
            status_code=400,
            detail={"BadRequest": f"Article not found"}
        )

    article = ArticleModel(
        user_id=current_user.id,
        content=content
    )
    await article.create()
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
    if current_user is None:
        logger.error(f"User {current_user} is not authorized!")
        raise HTTPException(
            status_code=401,
            detail={"Unauthorized": "User is not authorized!"}
        )
    article = await ArticleModel.get(article_id)
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
