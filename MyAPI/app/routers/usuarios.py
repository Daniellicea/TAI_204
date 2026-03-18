from fastapi import status, HTTPException, Depends, APIRouter
from typing import Optional
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["Usuarios"]
)

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
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    
    nuevo = usuario.model_dump()
    usuarios.append(nuevo)
    return {"usuario": nuevo}

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