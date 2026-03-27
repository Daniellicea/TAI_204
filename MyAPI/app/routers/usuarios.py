from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from app.data.db import get_db
from sqlalchemy.orm import Session
from app.data.usuario import Usuarios as usuarioDB

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["Usuarios"]
)

# 🔹 Obtener todos los usuarios
@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

# 🔹 Obtener un usuario por ID
@router.get("/{id}")
async def consulta_uno(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "status": "200",
        "usuario": usuario
    }

# 🔹 Crear usuario
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuario_nuevo = usuarioDB(
        nombre=usuarioP.nombre,
        edad=usuarioP.edad
    )
    
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)

    return {
        "mensaje": "usuario creado",
        "usuario": usuario_nuevo
    }

# 🔹 Actualizar usuario
@router.put("/{id}")
async def actualizar_usuario(id: int, datos: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "usuario actualizado",
        "usuario": usuario
    }

# 🔹 Eliminar usuario
@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_peticion),
    db: Session = Depends(get_db)
):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "status": "200"
    }