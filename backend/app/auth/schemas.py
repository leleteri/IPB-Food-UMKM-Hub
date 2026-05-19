from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nama: str
    foto: str | None = None
    nomor_telepon: str


class MahasiswaCreate(UserCreate):
    nim: str
    fakultas: str


class TokoCreate(UserCreate):
    kantin_id: int | None = 0


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
