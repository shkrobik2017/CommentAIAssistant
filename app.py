from fastapi import FastAPI
from routers.articles import router as articles_router
from routers.comments import router as comments_router
from routers.auth import router as auth_router
from db.db_setup import init_mongodb_beanie

app = FastAPI(title="AI comments Assistant")

app.include_router(articles_router, tags=["Articles Router"])
app.include_router(comments_router, tags=["Comments Router"])
app.include_router(auth_router, tags=["Authentication Router"])


@app.on_event("startup")
async def startup_event() -> None:
    await init_mongodb_beanie()
