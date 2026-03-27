import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException

from app.data.database import usuarios

routerV = APIRouter(
    prefix="/inicio",
    tags=["Inicio"]
)

# 🔹 Endpoint principal
@routerV.get("/")
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

# 🔹 Endpoint con espera simulada
@routerV.get("/holamundo")
async def hola():
    await asyncio.sleep(5)
    return {
        "mensaje": "Hola mundo",
        "status": "200"
    }

# 🔹 Obtener usuario por ID (ruta dinámica corregida)
@routerV.get("/usuario/{id}")
async def consulta_uno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "mensaje": "usuario encontrado",
                "usuario": usuario,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )

# 🔹 Buscar usuario con query param
@routerV.get("/buscar")
async def consulta_todos(id: Optional[int] = None):
    
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "mensaje": "usuario encontrado",
                    "usuario": usuario,
                    "status": "200"
                }
        
        raise HTTPException(
            status_code=404,
            detail="usuario no encontrado"
        )

    # Si no mandan ID, regresamos todos
    return {
        "mensaje": "lista de usuarios",
        "usuarios": usuarios,
        "total": len(usuarios)
    }