from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError

import os
from loguru import logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from another_fastapi_jwt_auth import AuthJWT

from src.auth.models import UserModel
from src.auth.schemas import UserSchema
from src.auth.utils import hash_password

from src.auth.config import JWTConfig


# Logger config
os.makedirs("logs", exist_ok=True)

logger.add(
    "logs/auth_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    enqueue=True,
)


@AuthJWT.load_config
def get_config():
    return JWTConfig()


async def register_user(user_schema: UserSchema, db: AsyncSession):
    try:
        valid = validate_email(user_schema.email)
        email_normalized = valid.email
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user_in_db = await db.execute(
        select(UserModel).where(email_normalized == UserModel.email)
    )
    user = user_in_db.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    hashed_password = hash_password(user_schema.password)
    new_user = UserModel(email=email_normalized, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"New user registered: {new_user.email}. User ID: {new_user.id}")
    return {"status": status.HTTP_200_OK}


async def login_user(user_schema: UserSchema, db: AsyncSession, Authorize: AuthJWT):
    try:
        valid = validate_email(user_schema.email)
        email_normalized = valid.email
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user_in_db = await db.execute(
        select(UserModel).where(email_normalized == UserModel.email)
    )
    user = user_in_db.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    access_token = Authorize.create_access_token(subject=str(user.id))

    logger.info(f"User entered in account. User ID: {user.id}")
    return {"access_token": access_token}


async def get_current_user(db: AsyncSession, Authorize: AuthJWT):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    user_in_db = await db.execute(select(UserModel).where(int(user_id) == UserModel.id))
    user = user_in_db.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"user": {"id": user.id, "email": user.email}}
