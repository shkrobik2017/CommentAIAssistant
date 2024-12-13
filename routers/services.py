from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from db.db_models import UserModel, ArticleModel, CommentModel
from db.db_services import UUIDStr
from logger.logger import logger
from models.models import TokenData
from settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_user_auth(*, current_user: UserModel):
    if current_user is None:
        logger.error(f"User {current_user} is not authorized!")
        raise HTTPException(
            status_code=401,
            detail={"Unauthorized": "User is not authorized!"}
        )


def verify_password(*, plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(*, password: str):
    return pwd_context.hash(password)


async def get_user(*, username: str):
    if user := await UserModel.find_one(UserModel.username == username):
        return user


async def authenticate_user(*, username: str, password: str):
    user = await get_user(username=username)
    if not user:
        return False
    if not verify_password(
            plain_password=password,
            hashed_password=user.hashed_password
    ):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    return encoded_jwt


async def get_current_user(*, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except:
        logger.error(f"Invalid credentials provided: {token}")
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    *, current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if current_user.is_baned:
        logger.error(f"User: {current_user} is banned")
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_article(*, content: str, current_user: UserModel) -> ArticleModel:
    check_user_auth(current_user=current_user)
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

    return article


async def get_article(*, article_id: UUIDStr, current_user: UserModel):
    check_user_auth(current_user=current_user)
    article = await ArticleModel.get(article_id)

    return article


async def get_article_comments_from_db(*, current_user: UserModel, article_id: UUIDStr):
    check_user_auth(current_user=current_user)
    if await ArticleModel.get(article_id) is None:
        raise HTTPException(
            status_code=404,
            detail={"NotFound": "Article not found"}
        )

    comments = await CommentModel.find({"article_id": article_id}).to_list(length=None)
    return comments

