from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import schemas, login_services
from app.user import models as users
from .. import security
from ..dependencies import get_db

router = APIRouter(prefix="/auth")


@router.post(path="/register/mahasiswa")
async def mahasiswa_register(
    form_data: schemas.MahasiswaCreate, db: AsyncSession = Depends(get_db)
):
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
async def toko_register(
    form_data: schemas.TokoCreate, db: AsyncSession = Depends(get_db)
):
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


@router.post(path="/login")
async def login(credentials: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await login_services.auth_user(form_data=credentials, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNATHORIZED, detail="Invalid email or password"
        )

    access_token = login_services.create_access_token(user_id=user.user_id)

    return schemas.TokenResponse(access_token=access_token, token_type="bearer")
