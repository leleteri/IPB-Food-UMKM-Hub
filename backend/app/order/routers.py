import random
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from . import schemas, functions, enum

router = APIRouter(prefix="/pesanan")


@router.post("/")
async def buat_pesanan(
    pesanan: schemas.PesananCreate, db: AsyncSession = Depends(get_db)
):
    mahasiswa_id = ""

    result = await functions.buat_pesanan(
        db=db,
        mahasiswa_id=mahasiswa_id,
        pesanan_data=pesanan,
    )

    return result


async def ubah_status_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    # BAGIAN INI NANTI DIUBAH
    pesanan_id = random.randint(0, 100)
    # BAGIAN INI NANTI DIUBAH

    result = await functions.ubah_status_pesanan(db=db, pesanan_id=pesanan_id)
    return result


async def batalkan_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    # BAGIAN INI NANTI DIUBAH
    pesanan_id = random.randint(0, 100)
    # BAGIAN INI NANTI DIUBAH

    result = await functions.batalkan_pesanan(db=db, pesanan_id=pesanan_id)
    return result
