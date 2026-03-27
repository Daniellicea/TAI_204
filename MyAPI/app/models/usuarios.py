from pydantic import BaseModel, Field
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan Doe")
    edad: int = Field(..., gt=0, le=125, description="Edad válida entre 1 y 125")

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, example="Juan Doe")
    edad: Optional[int] = Field(None, gt=0, le=125, description="Edad válida entre 1 y 125")