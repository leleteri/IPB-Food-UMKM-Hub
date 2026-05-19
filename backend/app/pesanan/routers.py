from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_models import User
from app.dependencies import get_db, require_role
from . import schemas, services, deps

router = APIRouter(prefix="/pesanan")


@router.post("/buat")
async def checkout(
    toko_id: UUID,
    pesanan: schemas.PesananCreate,
    current_user: User = Depends(require_role("Mahasiswa")),
    db: AsyncSession = Depends(get_db),
):
    mahasiswa_id = current_user.user_id

    return await services.buat_pesanan(
        toko_id=toko_id,
        mahasiswa_id=mahasiswa_id,
        pesanan_data=pesanan,
        db=db,
    )


@router.get("/{pesanan_id}", response_model=schemas.PesananResponse)
async def lihat_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    return await deps.get_pesanan(pesanan_id=pesanan_id, db=db)


@router.patch("/{pesanan_id}")
async def ubah_status_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    result = await services.ubah_status_pesanan(pesanan_id=pesanan_id, db=db)
    return result


async def batalkan_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    result = await services.batalkan_pesanan(pesanan_id=pesanan_id, db=db)
    return result
