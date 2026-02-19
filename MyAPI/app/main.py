#importaciones
from fastapi import FastAPI  #fastapi libreria
import asyncio
from typing import Optional
from fastapi import HTTPException, status



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
        return {
            "mensaje": "Usuario no encontrado",
            "status": 404
        }
    else:
        # Devuelve la lista completa de usuarios
        return {
            "mensaje": "Lista de usuarios",
            "Usuarios": usuarios,
            "status": 200
        }


# agregar usuario (POST)
@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def agregar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID ya existe"
            )

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuario,
        "status": 200
    }


# actualizar usuario (PUT)
@app.put("/v1/usuarios/", tags=["CRUD HTTP"])
async def actualizar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usr,
                "status": 200
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# eliminar usuario (DELETE)
@app.delete("/v1/usuarios/", tags=["CRUD HTTP"])
async def eliminar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "usuario": usr,
                "status": 200
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
