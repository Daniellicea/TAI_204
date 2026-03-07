from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta


# CONFIGURACIÓN DE SEGURIDAD
CLAVE_SECRETA = "Daniel"   #usuario de prueba
ALGORITMO = "HS256"
TIEMPO_EXPIRACION_TOKEN = 1  # minutos

# Endpoint donde se obtiene el token
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="API con Seguridad OAuth2 + JWT",
    description="Licea Gonzalez Eduardo Daniel",
    version="1.0"
)


# MODELOS
class Token(BaseModel):
    access_token: str
    token_type: str

class Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del usuario")
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=0)

# -----------------------------
# BASE DE DATOS SIMULADA
# -----------------------------

usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul", "edad": 21},
]

# usuario de prueba
base_usuarios = {
    "admin": "12345"
}

# ------------
# FUNCIONES JWT

def crear_token(datos: dict):
    """Genera un token JWT con expiración"""
    datos_copia = datos.copy()

    expiracion = datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION_TOKEN)

    datos_copia.update({"exp": expiracion})

    token = jwt.encode(datos_copia, CLAVE_SECRETA, algorithm=ALGORITMO)

    return token


async def verificar_token(token: str = Depends(oauth2_esquema)):
    """Verifica que el token sea válido"""
    
    excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        usuario = datos.get("sub")

        if usuario is None:
            raise excepcion

        return usuario

    except JWTError:
        raise excepcion


# AUTENTICACIÓN
@app.post("/token", response_model=Token, tags=["Seguridad"])
async def login(datos: OAuth2PasswordRequestForm = Depends()):
    """Permite obtener el token JWT"""

    password = base_usuarios.get(datos.username)

    if not password or datos.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    token_acceso = crear_token(datos={"sub": datos.username})

    return {
        "access_token": token_acceso,
        "token_type": "bearer"
    }


# ENDPOINTS PROTEGIDOS

@app.put("/v1/usuarios/", tags=["CRUD PROTEGIDO"])
async def actualizar_usuario(usuario: Usuario, usuario_actual: str = Depends(verificar_token)):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            usr.update(usuario.dict())

            return {
                "mensaje": f"Usuario actualizado por {usuario_actual}",
                "usuario": usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/v1/usuarios/{id}", tags=["CRUD PROTEGIDO"])
async def eliminar_usuario(id: int, usuario_actual: str = Depends(verificar_token)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)

            return {
                "mensaje": f"Usuario eliminado por {usuario_actual}"
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# ENDPOINTS PÚBLICOS

@app.get("/", tags=["Inicio"])
async def inicio():
    return {
        "mensaje": "Bienvenido a la API con seguridad OAuth2 + JWT"
    }


@app.get("/v1/usuarios/", tags=["CRUD PUBLICO"])
async def consultar_usuarios(id: Optional[int] = None):

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}

        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"usuarios": usuarios}