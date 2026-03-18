from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario = secrets.compare_digest(credentials.username, "Daniel")
    password = secrets.compare_digest(credentials.password, "1234")

    if not (usuario and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username