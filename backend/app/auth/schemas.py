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


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
