from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user
from app.user_models import User
from app.pesanan.models import Produk
from app.dependencies import verify_exists
from . import schemas
from .promo_models import Promo

from sqlalchemy import select


async def tambah_produk(
    form_data: schemas.ProdukCreate, current_user: User, db: AsyncSession
):
    existing_stmt = select(Produk).where(
        Produk.nama == form_data.nama, Produk.toko_id == current_user.user_id
    )
    existing_produk = await db.scalar(existing_stmt)

    if existing_produk:
        raise HTTPException(
            status_code=400, detail=f"Produk '{form_data.nama}' sudah ada di toko Anda."
        )

    new_produk = Produk(**form_data.model_dump(), toko_id=current_user.user_id)

    db.add(new_produk)
    await db.commit()
    await db.refresh(new_produk)
    return new_produk


async def hapus_produk(produk_id: int, current_user: User, db: AsyncSession):
    stmt = (
        delete(Produk)
        .where(Produk.produk_id == produk_id, Produk.toko_id == current_user.user_id)
        .returning(Produk.nama)  # <--- The Magic: Returns the name of the deleted row
    )

    result = await db.execute(stmt)
    deleted_name = result.scalar_one_or_none()  # Get the name from the deleted row

    verify_exists(deleted_name, "Produk")

    await db.commit()
    return {"message": f"{deleted_name} berhasil dihapus"}


async def ubah_detail_produk(
    produk_id: int,
    detail_data: schemas.ProdukEdit,
    current_user: User,
    db: AsyncSession,
):
    stmt = select(Produk).where(
        Produk.produk_id == produk_id,
        Produk.toko_id == current_user.user_id,
    )
    produk = verify_exists(await db.scalar(stmt), "Produk")

    update_data = detail_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(produk, key, value)

    await db.commit()
    await db.refresh(produk)

    return produk


async def add_promo(
    promo_data: schemas.PromoCreate, current_user: User, db: AsyncSession
):
    new_promo = Promo(
        **promo_data.model_dump(),
        toko_id=current_user.user_id,
        tanggal_berlaku=datetime.now(),
    )

    db.add(new_promo)

    await db.commit()
    await db.refresh(new_promo)

    return new_promo
