#importaciones
from fastapi import FastAPI,APIRouter  #fastapi libreria
from MyAPI.app.models import usuarios
from app.routers import usuarios, varios  


app = FastAPI(
   title="Mi primer API",
   description="Licea Gonzalez Eduardo Daniel",
   version="1.0"
)

# router de endpoints disponibles
app.include_router(usuarios.router)
app.include_router(varios.routerV) 
