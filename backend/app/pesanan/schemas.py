from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DetailPesananCreate(BaseModel):
    produk_id: int
    jumlah: int
    catatan: str | None = None


class PesananCreate(BaseModel):
    detail_pesanan: list[DetailPesananCreate]


class PesananResponse(BaseModel):
    pesanan_id: int
    mahasiswa_id: UUID
    toko_id: UUID
    tanggal: datetime
    total_harga: int
    total_bayar: int
    status: str
