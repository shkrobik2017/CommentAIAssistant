import json

from fastapi import HTTPException

from agent.agent import CommentAgent
from celery_app.config import app_celery
from db.db_models import CommentModel, ArticleModel
from db.db_setup import init_mongodb_beanie
from logger.logger import logger


@app_celery.task
def generate_comments(article_id: str, content: str) -> None:
    import asyncio
    try:
        asyncio.run(_generate_comments(article_id, content))
    except HTTPException as ex:
        logger.error("An error occurred when generate comment.")
        raise HTTPException(
            status_code=500,
            detail={"Eternal error": f"Something went wrong: {ex}"}
        )


async def _generate_comments(article_id: str, content: str) -> None:
    await init_mongodb_beanie()
    agent = CommentAgent()
    logger.info(f"Article id: {article_id}")

    try:

        result = await agent.generate_comment(content)

        json_result = json.loads(result)

        for v in json_result.values():
            await CommentModel(
                article_id=article_id,
                content=v
            ).create()

        logger.info(f"Comment generated for article {article_id}")

    except Exception as ex:
        logger.error(f"Error in _generate_comments: {ex}")
        raise ex

    article_model = await ArticleModel.find_one(
        ArticleModel.id == article_id
    )
    if article_model is not None:
        await article_model.set({"status": "Completed"})
        await article_model.save()
        logger.info(f"Article with id {article_id} status updated successfully")


