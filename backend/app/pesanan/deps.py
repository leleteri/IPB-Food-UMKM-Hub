from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Pesanan
from app.dependencies import verify_exists


async def get_pesanan(pesanan_id: int, db: AsyncSession):
    pesanan = select(Pesanan).where(Pesanan.pesanan_id == pesanan_id)
    return verify_exists(await db.scalar(pesanan), "Pesanan")
