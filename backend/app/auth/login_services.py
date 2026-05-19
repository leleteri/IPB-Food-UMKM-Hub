from datetime import timedelta, datetime, timezone
from uuid import UUID
from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Uuid, select

from . import schemas
from .. import security
from app.user_models import User
from app.dependencies import get_db


async def auth_user(
    form_data: schemas.TokenRequest, db: AsyncSession = Depends(get_db)
):
    user = await db.scalar(select(User).where(User.email == form_data.email))

    if user is None:
        return None

    if not security.verify_password(form_data.password, user.password):
        return None

    return user


def create_access_token(user_id: UUID, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))

    payload = {"sub": str(user_id), "exp": expire}

    return jwt.encode(payload, security.SECRET_KEY, algorithm=security.ALGORITHM)


def decode_access_token(token: str):
    payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])

    sub = payload.get("sub")

    if sub is None:
        raise JWTError("Missing Subject")

    return Uuid(sub)
