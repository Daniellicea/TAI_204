from fastapi import FastAPI
from app.routers import usuarios, varios

app = FastAPI(
    title="Mi primer API",
    description="Licea Gonzalez Eduardo Daniel",
    version="1.0"
)

# incluir routers
app.include_router(usuarios.router)
app.include_router(varios.routerV)

