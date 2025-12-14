from fastapi import FastAPI, HTTPException
from src.infrastructure.postgres_repository import PostgresRepository
from src.core.schemas import UsuarioCreate, UsuarioLogin, UsuarioOut

app = FastAPI(title="Control Car API")
repo = PostgresRepository()

# -------------------------------
# Endpoints de Usuarios
# -------------------------------

@app.post("/usuarios/registro")
def registrar_usuario(usuario: UsuarioCreate):
    """
    Registrar un nuevo usuario en el sistema.
    """
    try:
        repo.registrar_usuario(usuario.nombre, usuario.correo, usuario.contrasena, usuario.rol)
        return {"message": "Usuario registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {str(e)}")


@app.post("/usuarios/login", response_model=UsuarioOut)
def login(usuario: UsuarioLogin):
    """
    Autenticar usuario con correo y contraseña.
    """
    user = repo.autenticar_usuario(usuario.correo, usuario.contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return user

# -------------------------------
# Endpoints de Vehículos
# -------------------------------

@app.get("/vehicles")
def get_vehicles():
    """
    Obtener lista de vehículos registrados.
    """
    vehicles = repo.get_vehicles()
    return [{"id": v[0], "placa": v[1], "modelo": v[2], "anio": v[3]} for v in vehicles]


@app.post("/vehicles")
def add_vehicle(placa: str, modelo: str, anio: int):
    """
    Agregar un nuevo vehículo.
    """
    try:
        repo.add_vehicle(placa, modelo, anio)
        return {"message": "Vehículo agregado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al agregar vehículo: {str(e)}")

