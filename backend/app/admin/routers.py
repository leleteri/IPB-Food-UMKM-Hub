from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import enum
from app.dependencies import get_db, require_role
from . import services

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_role(enum.ROLE_ADMIN))],
    tags=["Admin"],
)


@router.get("/")
async def root():
    return {"status": "ok"}


@router.patch("/toko/{toko_id}")
async def approve_toko(toko_id: UUID, db: AsyncSession = Depends(get_db)):
    return await services.approve_toko(toko_id=toko_id, db=db)


@router.delete("/toko/{toko_id}")
async def hapus_toko(toko_id: UUID, db: AsyncSession = Depends(get_db)):
    return await services.hapus_toko(toko_id=toko_id, db=db)
