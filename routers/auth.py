from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from db.db_models import UserModel
from logger.logger import logger
from models.models import Token
from routers.services import authenticate_user, create_access_token, get_current_active_user, get_user, \
    get_password_hash
from settings import settings

router = APIRouter()


@router.post(
    path="/signup"
)
async def signup(user: UserModel) -> dict:
    if await get_user(username=user.username) is not None:
        logger.error(f"User {user.username} already registered")
        raise HTTPException(
            status_code=400,
            detail={"Bad Request": f"User {user.username} already registered"}
        )

    try:
        hashed_pass = get_password_hash(password=user.password)
    except Exception as ex:
        logger.error("An error occurred in hashing password")
        raise ex

    new_user = UserModel(
        username=user.username,
        hashed_password=hashed_pass,
        email=user.email
    )

    await new_user.create()
    logger.info(f"New user registered successfully: {new_user}")

    return {"Success": f"User {user.username} registered successfully."}


@router.post(
    path="/token",
    response_model=Token
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        logger.error("Incorrect input username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    try:
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        logger.info(f"Access token for user: {form_data.username} created successfully")

        return Token(access_token=access_token, token_type="bearer")
    except Exception as ex:
        logger.error(f"An error occurred in creating access token: {ex}")
        raise ex


@router.get(
    path="/users/me/",
    response_model=UserModel
)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user


@router.get(
    path="/users/me/items/"
)
async def read_own_items(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
