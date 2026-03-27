#immportaciones 

from sqlalchemy.orm import Session
from sqlalchemy import Column,Integer,String

from app.data.db import Base

#la U mayuscula es para diferenicra la clase del archivo
class Usuarios(Base):
    __tablename__="tb-usuarios"
    # el campo es de tipo entero con llave primaria y es autoincrementable
    id = Column(Integer, primary_key=True,index=True)
    nombre = Column(String)
    edad = Column(Integer)
    

   
    