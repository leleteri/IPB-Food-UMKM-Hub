import random
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from . import schemas, services, enum

router = APIRouter(prefix="/pesanan")


@router.post("/")
async def buat_pesanan(
    pesanan: schemas.PesananCreate, db: AsyncSession = Depends(get_db)
):
    mahasiswa_id = ""

    result = await services.buat_pesanan(
        mahasiswa_id=mahasiswa_id,
        pesanan_data=pesanan,
        db=db,
    )

    return result


async def ubah_status_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    # BAGIAN INI NANTI DIUBAH
    pesanan_id = random.randint(0, 100)
    # BAGIAN INI NANTI DIUBAH

    result = await services.ubah_status_pesanan(pesanan_id=pesanan_id, db=db)
    return result


async def batalkan_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    # BAGIAN INI NANTI DIUBAH
    pesanan_id = random.randint(0, 100)
    # BAGIAN INI NANTI DIUBAH

    result = await services.batalkan_pesanan(pesanan_id=pesanan_id, db=db)
    return result
