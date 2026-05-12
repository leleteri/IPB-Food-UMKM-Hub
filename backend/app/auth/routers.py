from hmac import new
from types import new_class
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import schemas
from app.user import models as users
from app import security

router = APIRouter(prefix="/auth")


@router.post(path="/register/mahasiswa")
async def mahasiswa_register(db: AsyncSession, form_data: schemas.MahasiswaCreate):
    existing_user = await db.scalar(
        select(users.User).where(users.User.email == form_data.email)
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    new_mahasiswa = users.Mahasiswa(
        email=form_data.email,
        nama=form_data.nama,
        password=security.get_password_hash(form_data.password),
        nomor_telepon=form_data.nomor_telepon,
        role="mahasiswa",
        nim=form_data.nim,
        fakultas=form_data.fakultas,
    )

    db.add(new_mahasiswa)

    await db.commit()
    await db.refresh(new_mahasiswa)

    return {
        "message": "Berhasil membuat akun",
        "user_id": str(new_mahasiswa.user_id),
        "email": new_mahasiswa.email,
        "nim": new_mahasiswa.nim,
        "fakultas": new_mahasiswa.fakultas,
    }


@router.post(path="/register/toko")
async def toko_register(db: AsyncSession, form_data: schemas.TokoCreate):
    existing_user = await db.scalar(
        select(users.User).where(users.User.email == form_data.email)
    )

    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    new_toko = users.Toko(
        email=form_data.email,
        nama=form_data.nama,
        password=security.get_password_hash(form_data.password),
        nomor_telepon=form_data.nomor_telepon,
        role="toko",
        kantin=form_data.kantin,
    )

    db.add(new_toko)

    await db.commit()
    await db.refresh(new_toko)

    return {
        "message": "Berhasil membuat akun toko",
        "user_id": str(new_toko.user_id),
        "kantin": new_toko.kantin,
        "email": new_toko.email,
    }
