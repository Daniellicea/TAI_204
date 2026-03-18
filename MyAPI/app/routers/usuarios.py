
from fastapi import status, HTTPException, Depends, APIRouter
from pyparsing import Optional
from app.data import usuarios
from app.models.usuarios import crear_usuario   
from app.security.auth import verificar_peticion

Router = APIRouter(
    prefijo="/v1/usuarios",
    tags=["Usuarios"]
)



@Router.get("/{id}", tags=['Parametro obligatorio'])
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

@Router.get(tags=['CRUD HTTP'])
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
@Router.post("/", tags=["CRUD HTTP"])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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
@Router.put("/", tags=["CRUD HTTP"])
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
@Router.delete("/{id}", tags=["CRUD HTTP"],status_code=status.HTTP_201_CREATED)
async def eliminar_usuario(id: int,usuarioAuth: str = Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
