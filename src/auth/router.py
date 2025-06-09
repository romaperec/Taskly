from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.auth.service import register_user
from src.auth.schemas import UserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user_schema: UserSchema, db: AsyncSession = Depends(get_session)):
    return await register_user(user_schema, db)
