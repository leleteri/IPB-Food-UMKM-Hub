from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.auth import schemas

from .. import security
from ..dependencies import get_db
from ..user import models as user_models

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: schemas.TokenSchema)
) -> user_models.User:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        sub = payload.get("sub")

        if sub is None:
            raise credentials_exception

        user_id = UUID(sub)

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(user_models.User).where(user_models.User.user_id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
