from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
import asyncio

# --- CONFIGURACIONES (a) ---
SECRET_KEY = "Daniel" # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Límite solicitado: 1 minuto

# Define el endpoint para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Mi primer API - Seguridad JWT",
    description="Licea Gonzalez Eduardo Daniel - Control de Acceso",
    version="1.2"
)

# --- MODELOS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanito doe")
    edad: int = Field(..., ge=0, description="Edad válida entre 1 y 125")

# --- BASE DE DATOS FICTICIA ---
usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul", "edad": 21},
]
# Credenciales de prueba: Usuario 'admin' Password '12345'
USER_DB = {"admin": "12345"}

# --- LÓGICA DE JWT (b y c) ---

def create_access_token(data: dict):
    """Generación de Token con límite de 1 minuto"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validación de Token y protección de rutas"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token no válido o ha expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# --- ENDPOINT PARA AUTENTICACIÓN ---

@app.post("/token", response_model=Token, tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Paso para obtener el token mediante usuario y contraseña"""
    user_password = USER_DB.get(form_data.username)
    if not user_password or form_data.password != user_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario o contraseña incorrectos"
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ENDPOINTS PROTEGIDOS (d) ---

@app.put("/v1/usuarios/", tags=["CRUD PROTEGIDO"])
async def actualizar_usuario(usuario: dict, user: str = Depends(get_current_user)):
    """Protegido con JWT: Solo accesible con token válido"""
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario)
            return {
                "mensaje": f"Usuario actualizado por {user}",
                "usuario": usr,
                "status": 200
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=["CRUD PROTEGIDO"])
async def eliminar_usuario(id: int, user: str = Depends(get_current_user)):
    """Protegido con JWT: Solo accesible con token válido"""
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {"mensaje": f"Usuario eliminado por {user}"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- ENDPOINTS PÚBLICOS ---

@app.get("/", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI con seguridad JWT activa (1 min)"}

@app.get("/V1/Usuarios/", tags=['CRUD HTTP'])
async def Consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario": usuario, "status": 200}
        return {"mensaje": "No encontrado", "status": 404}
    return {"Usuarios": usuarios, "status": 200}