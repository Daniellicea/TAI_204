from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets


#seguridad basica
security = HTTPBasic()
def verificar_peticion(credentiales: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentiales.username, "Daniel")
    contraAuth = secrets.compare_digest(credentiales.password, "1234")
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    return credentiales.username