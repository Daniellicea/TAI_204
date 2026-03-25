from fastapi import status, HTTPException, Depends, APIRouter
from typing import Optional
from MyAPI.app.models import usuario
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from app.data.db import get_db
from sqlalchemy.orm import Session
from app.data.db import SessionLocal
from app.data import Usuario as usuarioDB


router = APIRouter(
    prefix="/v1/usuarios",
    tags=["Usuarios"]
)

@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    querryUsuario = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(querryUsuario),
        "usuarios": querryUsuario
        }



@router.get("/{id}")
async def consulta_uno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return {"usuario": usuario}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/")
async def consulta_todos(id: Optional[int] = None):
    if id:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"usuarios": usuarios}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuarionuevo = usuarioDB(
        nombre = usuarioP.nombre,
        edad = usuarioP.edad
    )
    db.add(usuarionuevo)
    db.commit()
    db.refresh(usuarionuevo)
    return {"mensaje": "usuario creado",
            "usuario": usuarioP
            }


@router.put("/")
async def actualizar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario)
            return {"usuario": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_peticion)
):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(i)
            return {"mensaje": f"Eliminado por {usuarioAuth}"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")