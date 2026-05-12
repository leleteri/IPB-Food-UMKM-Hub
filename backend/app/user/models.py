from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric

from datetime import datetime
from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    nama: Mapped[str] = mapped_column(nullable=False)
    nomor_telepon: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "user",
    }


class Mahasiswa(User):
    __tablename__ = "mahasiswa"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    nim: Mapped[str] = mapped_column(unique=True, nullable=False)
    fakultas: Mapped[str] = mapped_column()

    __mapper_args__ = {"polymorphic_identity": "mahasiswa"}


class Toko(User):
    __tablename__ = "toko"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    kantin_id: Mapped[UUID] = mapped_column(ForeignKey("kantin.kantin_id"))
    tanggal_diajukan: Mapped[datetime] = mapped_column()
    tanggal_diterima: Mapped[datetime] = mapped_column()
    status_buka: Mapped[bool] = mapped_column()
    jenis_toko: Mapped[str] = mapped_column(String(20))
    rating_count: Mapped[int] = mapped_column(default=0)
    rating_avg: Mapped[Decimal] = mapped_column(Numeric(2, 1))

    __mapper_args__ = {"polymorphic_identity": "toko"}


class Kantin(Base):
    __tablename__ = "kantin"

    kantin_id: Mapped[UUID] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column()
    alamat: Mapped[str] = mapped_column()
