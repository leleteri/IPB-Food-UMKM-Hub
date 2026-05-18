from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric

from app.database import Base


class Produk(Base):
    __tablename__ = "produk"

    produk_id: Mapped[int] = mapped_column(primary_key=True)
    toko_id: Mapped[UUID] = mapped_column(ForeignKey("toko.user_id"))
    nama: Mapped[str] = mapped_column(nullable=False)
    deskripsi: Mapped[str] = mapped_column(String(100))
    harga: Mapped[int] = mapped_column(nullable=False)
    stok: Mapped[int] = mapped_column(default=0)
    foto: Mapped[str] = mapped_column()
    kategori: Mapped[str] = mapped_column()
    diskon_berlaku: Mapped[int] = mapped_column()

    detail_pesanan: Mapped[list["DetailPesanan"]] = relationship(
        back_populates="produk"
    )


class Pesanan(Base):
    __tablename__ = "pesanan"

    pesanan_id: Mapped[int] = mapped_column(primary_key=True)
    mahasiswa_id: Mapped[UUID] = mapped_column(ForeignKey("mahasiswa.user_id"))
    toko_id: Mapped[UUID] = mapped_column(ForeignKey("toko.user_id"))
    tanggal: Mapped[datetime] = mapped_column()
    total_harga: Mapped[int] = mapped_column(default=0)
    total_bayar: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(nullable=False)

    detail_pesanan: Mapped[list["DetailPesanan"]] = relationship(
        back_populates="pesanan"
    )


class DetailPesanan(Base):
    __tablename__ = "detail_pesanan"

    dp_id: Mapped[int] = mapped_column(primary_key=True)
    pesanan_id: Mapped[int] = mapped_column(ForeignKey("pesanan.pesanan_id"))
    produk_id: Mapped[int] = mapped_column(ForeignKey("produk.produk_id"))
    harga_satuan: Mapped[int] = mapped_column()
    jumlah_beli: Mapped[int] = mapped_column(default=0)
    subtotal_harga: Mapped[int] = mapped_column()
    catatan: Mapped[str] = mapped_column(String(100))

    pesanan: Mapped["Pesanan"] = relationship(back_populates="detail_pesanan")
    produk: Mapped["Produk"] = relationship(back_populates="detail_pesanan")
