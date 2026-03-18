
#modelo de Pydantic de validacion
from pydantic import BaseModel, Field


class crear_usuario(BaseModel):
    id: int = Field (..., gt=0, description = "indentificador de usuario")
    nombre: str= Field(...,min_length=3, max_length = 50, example= "Juanito doe")
    edad: int = Field(..., ge=0, description="Edad validad entre 1 y 125")


