from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.security import get_password_hash
from app.user_models import Mahasiswa, Toko
from app import enum
from . import schemas
from .deps import ensure_email_not_registered


async def create_mahasiswa(
    db: AsyncSession,
    data: schemas.MahasiswaCreate,
):
    await ensure_email_not_registered(
        db,
        data.email,
    )

    mahasiswa = Mahasiswa(
        email=data.email,
        password=get_password_hash(data.password),
        nama=data.nama,
        foto=data.foto,
        nomor_telepon=data.nomor_telepon,
        role=enum.ROLE_MAHASISWA,
        nim=data.nim,
        fakultas=data.fakultas,
    )

    db.add(mahasiswa)

    await db.commit()

    return mahasiswa


async def create_toko(
    db: AsyncSession,
    data: schemas.TokoCreate,
):
    await ensure_email_not_registered(
        db,
        data.email,
    )

    toko = Toko(
        email=data.email,
        password=get_password_hash(data.password),
        nama=data.nama,
        foto=data.foto,
        nomor_telepon=data.nomor_telepon,
        role=enum.ROLE_TOKO_PENDING,
        kantin_id=data.kantin_id,
        tanggal_diajukan=datetime.now(),
        status_buka=enum.TOKO_TUTUP,
    )

    db.add(toko)

    await db.commit()

    return toko
