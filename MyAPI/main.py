#importaciones
from fastapi import FastAPI  #fastapi libreria
import asyncio
from typing import Optional

#instancia del servidor
#instacioa del servidor 
app = FastAPI(
   title="Mi primer API",
   description="Licea Gonzalez Eduardo Daniel",
   version="1.0"
)

#para abir y acceder debemos estar siempre en la caprta y despues correr el servidor
#comando uvicorn main:app --reload

#endpoints
@app.get("/", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}


@app.get("/holamundo", tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5)  # simulación de espera
    return {
        "mensaje": "Hola mundo",
        "status": 200
    }

#ID ficticia
usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul", "edad": 21},
]

@app.get("/V1/Usuario/{id}", tags=['Parametro obligatorio'])
async def Consultauno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "mensaje": "Usuario encontrado",
                "Usuario": usuario,
                "status": 200
            }
    return {
        "mensaje": "Usuario no encontrado",
        "status": 404
    }

@app.get("/V1/Usuarios/", tags=['Parametro opcional'])
async def Consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "mensaje": "Usuario encontrado",
                    "Usuario": usuario,
                    "status": 200
                }
        return{"mensaje": "usuario no encontrado","status":"200"}
    else:
        return{"mensaje":"No se proporciono id","status":"200"}