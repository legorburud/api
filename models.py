from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from database import Base

# Hay que definir los modelos de datos a guardar
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30), index=True)
    edad = Column(Integer, index=True)
    region = Column(String(100), index=True)
    email = Column(String(30), unique=True, index=True)
