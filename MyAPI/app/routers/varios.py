import asyncio
from fastapi import APIRouter

routerV = APIRouter(
    prefix="/inicio",
    tags=["Inicio"]
)

@routerV.get("/")
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

@routerV.get("/holamundo")
async def hola():
    await asyncio.sleep(5)
    return {"mensaje": "Hola mundo"}