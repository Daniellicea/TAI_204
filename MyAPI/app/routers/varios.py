import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.usuario import Usuarios as usuarioDB
from app.models.usuarios import UsuarioCreate, UsuarioUpdate

routerV = APIRouter(
    prefix="/inicio",
    tags=["Inicio"]
)

# endpoint principal
@routerV.get("/")
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

# endpoint con espera
@routerV.get("/holamundo")
async def hola():
    await asyncio.sleep(5)
    return {
        "mensaje": "Hola mundo",
        "status": "200"
    }

# obtener usuario por id
@routerV.get("/usuario/{id}")
async def consulta_uno(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    return {
        "mensaje": "usuario encontrado",
        "usuario": usuario
    }

# buscar usuarios
@routerV.get("/buscar")
async def consulta_todos(id: Optional[int] = None, db: Session = Depends(get_db)):

    if id is not None:
        usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="usuario no encontrado")

        return {
            "mensaje": "usuario encontrado",
            "usuario": usuario
        }

    usuarios = db.query(usuarioDB).all()

    return {
        "mensaje": "lista de usuarios",
        "total": len(usuarios),
        "usuarios": usuarios
    }

# crear usuario
@routerV.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = usuarioDB(
        nombre=datos.nombre,
        edad=datos.edad
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "usuario creado",
        "usuario": nuevo
    }

# actualizar usuario completo
@routerV.put("/usuario/{id}")
async def actualizar_usuario(id: int, datos: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "usuario actualizado",
        "usuario": usuario
    }

# actualizar usuario parcial
@routerV.patch("/usuario/{id}")
async def actualizar_parcial(id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    if datos.nombre is not None:
        usuario.nombre = datos.nombre

    if datos.edad is not None:
        usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "usuario actualizado parcialmente",
        "usuario": usuario
    }

# eliminar usuario
@routerV.delete("/usuario/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": "usuario eliminado",
        "status": "200"
    }