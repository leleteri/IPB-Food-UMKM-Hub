from datetime import datetime
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base


class Promo(Base):
    __tablename__ = "promo"

    promo_id: Mapped[int] = mapped_column(primary_key=True)
    toko_id: Mapped[UUID] = mapped_column(ForeignKey("toko.user_id"))
    minimum_harga: Mapped[int] = mapped_column()
    nominal_potongan: Mapped[int] = mapped_column()
    tanggal_berlaku: Mapped[datetime] = mapped_column()
    tanggal_musnah: Mapped[datetime] = mapped_column()
