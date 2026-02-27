from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "API Biblioteca funcionando correctamente"}


class Usuario(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr

class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str
    autor: str
    año: int
    paginas: int = Field(..., gt=1)
    estado: str = "disponible"

    @validator("año")
    def validar_anio(cls, value):
        if value < 1450 or value > datetime.now().year:
            raise ValueError("Año inválido")
        return value

    @validator("estado")
    def validar_estado(cls, value):
        if value not in ["disponible", "prestado"]:
            raise ValueError("Estado inválido")
        return value
    
class Prestamo(BaseModel):
    id: int
    id_usuario: int
    id_libro: int
    fecha: datetime = datetime.now()

usuarios: List[Usuario] = []
libros: List[Libro] = []
prestamos: List[Prestamo] = []


#USUARI 

@app.post("/v1/usuarios/", status_code=201, tags=["Usuarios"])
async def agregar_usuario(usuario: Usuario):
    if any(u.id == usuario.id for u in usuarios):
        raise HTTPException(status_code=409, detail="El ID del usuario ya existe")
    usuarios.append(usuario)
    return {"mensaje": "Usuario registrado correctamente", "usuario": usuario}


@app.get("/v1/usuarios/", tags=["Usuarios"])
async def listar_usuarios():
    return usuarios

#libros

@app.post("/v1/libros/", status_code=201, tags=["Libros"])
async def agregar_libro(libro: Libro):
    if any(l.id == libro.id for l in libros):
        raise HTTPException(status_code=409, detail="El ID del libro ya existe")
    libros.append(libro)
    return {"mensaje": "Libro registrado correctamente", "libro": libro}


@app.get("/v1/libros/", tags=["Libros"])
async def listar_libros():
    return libros


@app.get("/v1/libros/disponibles", tags=["Libros"])
async def libros_disponibles():
    disponibles = [l for l in libros if l.estado == "disponible"]
    return disponibles


@app.get("/v1/libros/buscar/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):
    encontrados = [l for l in libros if nombre.lower() in l.nombre.lower()]
    if not encontrados:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return encontrados

#prestamos

@app.post("/v1/prestamos/", status_code=201, tags=["Prestamos"])
async def registrar_prestamo(prestamo: Prestamo):

    usuario = next((u for u in usuarios if u.id == prestamo.id_usuario), None)
    if not usuario:
        raise HTTPException(status_code=404, 
                            detail="Usuario no existe")

    libro = next((l for l in libros if l.id == prestamo.id_libro), None)
    if not libro:
        raise HTTPException(status_code=404, 
                            detail="Libro no existe")

    if libro.estado == "prestado":
        raise HTTPException(status_code=409, 
                            detail="El libro ya está prestado")

    libro.estado = "prestado"
    prestamos.append(prestamo)

    return {"mensaje": "Préstamo registrado correctamente", 
            "prestamo": prestamo}


@app.put("/v1/prestamos/devolver/{id_libro}", tags=["Prestamos"])
async def devolver_libro(id_libro: int):

    prestamo = next((p for p in prestamos if p.id_libro == id_libro), None)
    if not prestamo:
        raise HTTPException(status_code=409, 
                            detail="No existe registro de préstamo")

    libro = next((l for l in libros if l.id == id_libro), None)
    libro.estado = "disponible"

    prestamos.remove(prestamo)

    return {"mensaje": "Libro devuelto correctamente"}  # 200 OK


@app.delete("/v1/prestamos/{id_prestamo}", tags=["Prestamos"])
async def eliminar_prestamo(id_prestamo: int):

    prestamo = next((p for p in prestamos if p.id == id_prestamo), None)
    if not prestamo:
        raise HTTPException(status_code=409, 
                            detail="El préstamo no existe")

    prestamos.remove(prestamo)
    return {"mensaje": "Préstamo eliminado correctamente"}


@app.get("/v1/prestamos/", tags=["Prestamos"])
async def listar_prestamos():
    return prestamos