from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_models import Toko
from app import enum
from app.dependencies import verify_exists


async def approve_toko(toko_id: UUID, db: AsyncSession):
    stmt = select(Toko).where(Toko.user_id == toko_id)
    toko = verify_exists(await db.scalar(stmt), "Toko")

    if toko.role != enum.ROLE_TOKO_PENDING:
        raise HTTPException(
            status_code=400, detail="Toko sudah di approve atau bukan toko"
        )

    toko.role = enum.ROLE_TOKO

    await db.commit()

    return toko


async def hapus_toko(toko_id: UUID, db: AsyncSession):
    toko = select(Toko.nama).where(Toko.user_id == toko_id)
    nama_toko = verify_exists(await db.scalar(toko), "Toko")

    del_stmt = delete(Toko).where(Toko.user_id == toko_id)

    await db.execute(del_stmt)
    await db.commit()

    return {"message": f"Toko {nama_toko} berhasil dihapus dari sistem"}
