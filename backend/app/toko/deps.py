from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.pesanan.models import Produk
from app.dependencies import verify_exists
from .promo_models import Promo
from app.user_models import Toko, Kantin


async def get_toko_list(db: AsyncSession):
    return await db.scalars(select(Toko))


async def get_kantin_list(db: AsyncSession):
    return await db.scalars(select(Kantin))


async def get_kantin_by_id(kantin_id, db: AsyncSession):
    kantin = select(Kantin).where(Kantin.kantin_id == kantin_id)
    return verify_exists(await db.scalar(kantin), "Kantin")


async def get_toko_by_id(toko_id: UUID, db: AsyncSession):
    produk = select(Toko).where(Toko.user_id == toko_id)
    return verify_exists(await db.scalar(produk), "Toko")


async def get_produk_by_toko(toko_id: UUID, db: AsyncSession):
    toko = await get_toko_by_id(toko_id=toko_id, db=db)

    return await db.scalars(
        select(order_models.Produk).where(Produk.toko_id == toko.user_id)
    )


async def get_promo_by_id(
    promo_id: int,
    db: AsyncSession,
):
    promo = select(Promo).where(Promo.promo_id == promo_id)
    return verify_exists(promo, "Promo")
