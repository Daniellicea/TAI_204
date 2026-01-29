#importaciones
from fastapi import FastAPI  #fastapi libreria
import asyncio

#instancia del servidor
app= FastAPI()


#endpoints
@app.get("/")

async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"
    }

@app.get("/holamundo")

async def Hola():
    await asyncio.sleep(5)#peticion, consulta, archivo
    return {"mensaje":"Hola mundo",
            "status":"200"
    }
