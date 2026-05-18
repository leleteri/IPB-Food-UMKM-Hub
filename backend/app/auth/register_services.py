from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import security
from ..user import models as users
from . import schemas


async def ensure_email_not_registered(
    db: AsyncSession,
    email: str,
) -> None:
    existing_user = await db.scalar(select(users.User).where(users.User.email == email))

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar",
        )


async def create_mahasiswa(
    db: AsyncSession,
    data: schemas.MahasiswaCreate,
) -> users.Mahasiswa:
    await ensure_email_not_registered(
        db,
        data.email,
    )

    mahasiswa = users.Mahasiswa(
        email=data.email,
        nama=data.nama,
        password=security.get_password_hash(data.password),
        nomor_telepon=data.nomor_telepon,
        role="mahasiswa",
        nim=data.nim,
        fakultas=data.fakultas,
    )

    db.add(mahasiswa)

    await db.commit()
    await db.refresh(mahasiswa)

    return mahasiswa


async def create_toko(
    db: AsyncSession,
    data: schemas.TokoCreate,
) -> users.Toko:
    await ensure_email_not_registered(
        db,
        data.email,
    )

    toko = users.Toko(
        email=data.email,
        nama=data.nama,
        password=security.get_password_hash(data.password),
        nomor_telepon=data.nomor_telepon,
        role="toko",
        kantin=data.kantin,
    )

    db.add(toko)

    await db.commit()
    await db.refresh(toko)

    return toko
