from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from . import schemas
from .models import Pesanan, DetailPesanan, Produk
from app import enum


async def buat_pesanan(
    mahasiswa_id: UUID,
    toko_id: UUID,
    pesanan_data: schemas.PesananCreate,
    db: AsyncSession,  # Remove Depends here, move to router
):
    product_ids = [item.produk_id for item in pesanan_data.detail_pesanan]

    result = await db.execute(select(Produk).where(Produk.produk_id.in_(product_ids)))
    produk_map = {p.produk_id: p for p in result.scalars().all()}

    new_pesanan = Pesanan(
        mahasiswa_id=mahasiswa_id,
        toko_id=toko_id,
        tanggal=datetime.now(),
        status=enum.STATUS_DIBUAT,  # Use Enums consistently
    )
    db.add(new_pesanan)
    await db.flush()  # Get the new_pesanan.pesanan_id

    total_harga = 0

    for item in pesanan_data.detail_pesanan:
        produk = produk_map.get(item.produk_id)

        if not produk:
            raise HTTPException(404, f"Produk {item.produk_id} tidak ditemukan")
        if produk.toko_id != toko_id:
            raise HTTPException(400, f"Produk {produk.nama} bukan milik toko ini")
        if produk.stok < item.jumlah:
            raise HTTPException(400, f"Stok {produk.nama} tidak cukup")

        harga_satuan = produk.harga - (produk.diskon_berlaku or 0)
        subtotal = harga_satuan * item.jumlah

        detail = DetailPesanan(
            pesanan_id=new_pesanan.pesanan_id,
            produk_id=produk.produk_id,
            harga_satuan=harga_satuan,
            jumlah_beli=item.jumlah,
            subtotal_harga=subtotal,
            catatan=item.catatan,
        )
        db.add(detail)

        produk.stok -= item.jumlah  # Reserve stock
        total_harga += subtotal

    new_pesanan.total_harga = total_harga
    new_pesanan.total_bayar = total_harga  # Adjust if there's an app fee or discount

    await db.commit()
    await db.refresh(new_pesanan)
    return new_pesanan


async def ubah_status_pesanan(pesanan_id: int, db: AsyncSession):
    stmt = select(Pesanan).where(Pesanan.pesanan_id == pesanan_id)
    pesanan = await db.scalar(stmt)

    if not pesanan:
        raise HTTPException(404, "Pesanan tidak ditemukan")

    # Use Enum for everything
    if pesanan.status == enum.STATUS_DIBUAT:
        pesanan.status = enum.STATUS_DIPROSES
    elif pesanan.status == enum.STATUS_DIPROSES:
        pesanan.status = enum.STATUS_SELESAI
    else:
        raise HTTPException(400, f"Status {pesanan.status} tidak dapat diubah lagi")

    await db.commit()
    return pesanan


async def batalkan_pesanan(pesanan_id: int, db: AsyncSession):
    stmt = (
        select(Pesanan)
        .where(Pesanan.pesanan_id == pesanan_id)
        .options(
            selectinload(Pesanan.detail_pesanan).selectinload(DetailPesanan.produk)
        )
    )
    pesanan = await db.scalar(stmt)

    if not pesanan:
        raise HTTPException(404, "Pesanan tidak ditemukan")

    if pesanan.status != enum.STATUS_DIBUAT:
        raise HTTPException(400, "Hanya pesanan baru yang bisa dibatalkan")

    # RESTORE STOCK
    for detail in pesanan.detail_pesanan:
        detail.produk.stok += detail.jumlah_beli

    pesanan.status = enum.STATUS_DIBATALKAN
    await db.commit()
    return pesanan
