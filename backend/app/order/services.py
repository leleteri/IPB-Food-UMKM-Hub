from datetime import datetime
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas, enum
from ..dependencies import get_db


async def buat_pesanan(
    mahasiswa_id,
    pesanan_data: schemas.PesananCreate,
    db: AsyncSession = Depends(get_db),
):
    new_pesanan = models.Pesanan(
        mahasiswa_id=mahasiswa_id,
        toko_id=pesanan_data.toko_id,
        tanggal=datetime.now(),
        status="pesanan dibuat",
    )

    db.add(new_pesanan)

    await db.flush()

    total_harga = 0

    for item in pesanan_data.detail_pesanan:
        produk = await db.scalar(
            select(models.Produk).where(models.Produk.produk_id == item.produk_id)
        )

        if not produk:
            raise HTTPException(
                status_code=404, detail=f"Produk {item.produk_id} tidak ditemukan"
            )

        if produk.toko_id != pesanan_data.toko_id:
            raise HTTPException(status_code=400, detail="Produk tidak ada di toko")

        if produk.stok < item.jumlah:
            raise HTTPException(
                status_code=400,
                detail=f"Jumlah item {produk.nama} melebihi stok tersisa",
            )

        harga_satuan = produk.harga - produk.diskon_berlaku
        subtotal = harga_satuan * item.jumlah

        detail = models.DetailPesanan(
            pesanan_id=new_pesanan.pesanan_id,
            produk_id=produk.produk_id,
            harga_satuan=harga_satuan,
            jumlah_beli=item.jumlah,
            subtotal_harga=subtotal,
            catatan=item.catatan,
        )

        db.add(detail)

        produk.stok -= item.jumlah

        total_harga += subtotal

    new_pesanan.total_harga = total_harga
    new_pesanan.total_bayar = total_harga - 0

    await db.commit()
    await db.refresh(new_pesanan)

    return new_pesanan


async def ubah_status_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    pesanan = await db.scalar(
        select(models.Pesanan).where(models.Pesanan.pesanan_id == pesanan_id)
    )

    if not pesanan:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

    if (
        pesanan.status == enum.STATUS_DIBATALKAN
        or pesanan.status == enum.STATUS_SELESAI
    ):
        raise HTTPException(status_code=400, detail="status pesanan tidak dapat diubah")

    if pesanan.status == enum.STATUS_DIBUAT:
        pesanan.status = enum.STATUS_DIPROSES

    if pesanan.status == enum.STATUS_DIPROSES:
        pesanan.status = enum.STATUS_SELESAI

    await db.commit()

    return pesanan


async def batalkan_pesanan(pesanan_id: int, db: AsyncSession = Depends(get_db)):
    pesanan = await db.scalar(
        select(models.Pesanan).where(models.Pesanan.pesanan_id == pesanan_id)
    )

    if not pesanan:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

    if not pesanan.status == "Pesanan dibuat":
        raise HTTPException(
            status_code=400, detail="Pesanan sudah tidak dapat dibatalkan"
        )

    pesanan.status = enum.STATUS_DIBATALKAN

    await db.commit()

    return pesanan


async def tambah_produk(
    produk_data: schemas.ProdukCreate, tokto_id, db: AsyncSession = Depends(get_db)
):
    new_produk = models.Produk(
        nama=produk_data.nama_produk,
        deskripsi=produk_data.deskripsi,
    )
