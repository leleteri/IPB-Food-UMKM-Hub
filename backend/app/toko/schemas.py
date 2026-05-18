from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class KantinBase(BaseModel):
    nama: str
    alamat: str

    model_config = ConfigDict(from_attributes=True)


class TokoBase(BaseModel):
    nama: str
    foto: str
    status_buka: str
    jenis_toko: str
    rating_count: int
    rating_avg: Decimal

    model_config = ConfigDict(from_attributes=True)


class KantinResponse(KantinBase):
    kantin_id: int
    daftar_toko: list[TokoBase]


class TokoResponse(TokoBase):
    user_id: UUID
    kantin_id: int
    kantin: KantinBase


class ProdukBase(BaseModel):
    nama: str
    deskripsi: str | None = None
    harga: int
    stok: int | None = 0
    foto: str | None = None
    diskon_berlaku: int | None = 0


class ProdukCreate(ProdukBase):
    pass


class ProdukEdit(BaseModel):
    nama: str | None = None
    deskripsi: str | None = None
    harga: int | None = None
    stok: int | None = None
    foto: str | None = None
    diskon_berlaku: int | None = None


class ProdukResponse(ProdukBase):
    produk_id: int

    model_config = ConfigDict(from_attributes=True)
