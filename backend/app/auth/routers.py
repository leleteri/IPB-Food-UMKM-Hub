from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, login_services, register_services
from ..dependencies import get_db

router = APIRouter(prefix="/auth")


@router.post(path="/register/mahasiswa")
async def mahasiswa_register(
    form_data: schemas.MahasiswaCreate,
    db: AsyncSession = Depends(get_db),
):
    mahasiswa = await register_services.create_mahasiswa(
        db=db,
        data=form_data,
    )

    return {
        "message": "Berhasil membuat akun",
        "user_id": str(mahasiswa.user_id),
        "email": mahasiswa.email,
        "nim": mahasiswa.nim,
        "fakultas": mahasiswa.fakultas,
    }


@router.post(path="/register/toko")
async def toko_register(
    form_data: schemas.TokoCreate,
    db: AsyncSession = Depends(get_db),
):
    toko = await register_services.create_toko(
        db=db,
        data=form_data,
    )

    return {
        "message": "Berhasil membuat akun toko",
        "user_id": str(toko.user_id),
        "kantin": toko.kantin,
        "email": toko.email,
    }


@router.post(path="/login")
async def login(credentials: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await login_services.auth_user(form_data=credentials, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = login_services.create_access_token(user_id=user.user_id)

    return schemas.TokenResponse(access_token=access_token, token_type="bearer")
