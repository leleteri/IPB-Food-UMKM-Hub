from uuid import UUID
from pydantic import BaseModel


class DetailPesananCreate(BaseModel):
    produk_id: int
    jumlah: int
    catatan: str | None = None


class PesananCreate(BaseModel):
    toko_id: UUID
    detail_pesanan: list[DetailPesananCreate]


class ProdukCreate(BaseModel):
    nama_produk: str
    stok: int
    deskripsi: str
