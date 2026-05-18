from typing import Any
from fastapi import HTTPException
from .database import SessionLocal


def verify_exists(item: Any, item_name: str = "Item"):
    if item is None:
        raise HTTPException(status_code=404, detail=f"{item_name} tidak ditemukan")

    return item


async def get_db():
    async with SessionLocal() as session:
        yield session
