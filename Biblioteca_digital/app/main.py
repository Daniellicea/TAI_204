from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    version="1.0.0"
)

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