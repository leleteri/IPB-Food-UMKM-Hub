from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.user_models import User


async def ensure_email_not_registered(
    db: AsyncSession,
    email: str,
):
    existing_user = await db.scalar(select(User).where(User.email == email))

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar",
        )
