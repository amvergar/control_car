from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: str  # admin / operador

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str
