from pydantic import BaseModel

#Función post
class UserCreate(BaseModel):
    nombre: str
    edad: int
    region: str
    email: str

#Función get
class UserResponse(BaseModel):
    id: int
    nombre: str
    edad: int
    region: str
    email: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nombre: str | None = None
    edad: int | None = None
    region: str | None = None
    email: str | None = None

