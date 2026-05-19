from typing import Any
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import login_services
from app.database import SessionLocal
from app import user_models


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_exists(item: Any, item_name: str = "Item"):
    if item is None:
        raise HTTPException(status_code=404, detail=f"{item_name} tidak ditemukan")

    return item


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    token: str = Depends(reusable_oauth2),
    db: AsyncSession = Depends(get_db),
):
    try:
        user_id = login_services.decode_access_token(token)

    except (JWTError, ValueError):
        raise credentials_exception

    result = await db.execute(
        select(user_models.User).where(user_models.User.user_id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


def require_role(*allowed_roles: str):
    async def role_checker(
        current_user: user_models.User = Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return role_checker
