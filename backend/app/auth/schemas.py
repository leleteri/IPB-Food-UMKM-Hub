from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    nama: str
    nomor_telepon: str
    password: str


class MahasiswaCreate(UserCreate):
    nim: str
    fakultas: str


class TokoCreate(UserCreate):
    kantin: str
