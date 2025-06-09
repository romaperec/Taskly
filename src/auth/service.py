from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import UserModel
from src.auth.schemas import UserSchema
from src.auth.utils import hash_password


async def register_user(user_schema: UserSchema, db: AsyncSession):
    user_in_db = await db.execute(
        select(UserModel).where(user_schema.email == UserModel.email)
    )
    user = user_in_db.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    hashed_password = hash_password(user_schema.password)
    new_user = UserModel(email=user_schema.email, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"status": status.HTTP_200_OK}
