from typing import List
from unittest import result
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import enum
from app.dependencies import get_db, require_role
from app.user_models import User
from . import deps, schemas, services

router = APIRouter(prefix="/toko", tags=["toko"])


@router.get("/", response_model=list[schemas.TokoResponse])
async def list_toko(db: AsyncSession = Depends(get_db)):
    return await deps.get_toko_list(db=db)


@router.patch("/me")
async def ubah_detail_toko(
    form_data: schemas.TokoEdit,
    current_user: User = Depends(require_role(enum.ROLE_TOKO)),
    db: AsyncSession = Depends(get_db),
):
    return await services.ubah_detail_toko(
        form_data=form_data, current_user=current_user, db=db
    )


@router.get("/{toko_id}", response_model=schemas.TokoResponse)
async def lihat_toko(toko_id: UUID, db: AsyncSession = Depends(get_db)):
    return await deps.get_toko_by_id(toko_id=toko_id, db=db)


@router.get("/{toko_id}/produk", response_model=list[schemas.ProdukResponse])
async def lihat_produk(toko_id: UUID, db: AsyncSession = Depends(get_db)):
    return await deps.get_produk_by_toko(toko_id=toko_id, db=db)


@router.post("/produk")
async def tambah_produk(
    form_data: schemas.ProdukCreate,
    current_user: User = Depends(require_role(enum.ROLE_TOKO)),
    db: AsyncSession = Depends(get_db),
):
    return await services.tambah_produk(
        form_data=form_data, current_user=current_user, db=db
    )


@router.post("/promo")
async def tambah_promo(
    promo_data: schemas.PromoCreate,
    current_user: User = Depends(require_role(enum.ROLE_TOKO)),
    db: AsyncSession = Depends(get_db),
):
    return await services.tambah_promo(
        promo_data=promo_data, current_user=current_user, db=db
    )


@router.get("/promo")
async def lihat_promo(
    promo_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await deps.get_promo_by_id(promo_id=promo_id, db=db)


@router.patch("/produk/{produk_id}")
async def ubah_detail_produk(
    produk_id: int,
    detail_data: schemas.ProdukEdit,
    current_user: User = Depends(require_role(enum.ROLE_TOKO)),
    db: AsyncSession = Depends(get_db),
):
    return await services.ubah_detail_produk(
        produk_id=produk_id, detail_data=detail_data, current_user=current_user, db=db
    )


@router.delete("/produk/{produk_id}")
async def hapus_produk(
    produk_id: int,
    current_user: User = Depends(require_role(enum.ROLE_TOKO)),
    db: AsyncSession = Depends(get_db),
):
    return await services.hapus_produk(
        produk_id=produk_id,
        current_user=current_user,
        db=db,
    )
