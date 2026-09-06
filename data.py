from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()
Url = "sqlite:///datos.db"

# se supone que aquí se dice dónde el motor va a guardar el archivo de la base de datos
engine = create_engine(Url, connect_args={"check_same_thread": False}, echo=True)

# Este es el código de la sesión que es donde se irán anotando los cambios y guardando o descartando
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Se va a definir la base que luego pueden heredar sus especificaciones
Base = declarative_base()


# Hay que definir los modelos de datos a guardar
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30), index=True)
    edad = Column(Integer, index=True)
    region = Column(String(100), index=True)
    email = Column(String(30), unique=True, index=True)


Base.metadata.create_all(bind=engine)

#Crea una sesión para cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# se define un endpost
@app.post("/users/", response_model=UserResponse)  #se define el formato de respuesta
def create_user(user: UserCreate, db: Session = Depends(get_db)): 
    db_user = User(nombre=user.nombre, edad=user.edad, region=user.region, email=user.email)  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:   
        raise HTTPException(status_code=404, detail="User not found")
    return user

class UserUpdate(BaseModel):
    nombre: str | None = None
    edad: int | None = None
    region: str | None = None
    email: str | None = None

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends
(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.nombre is not None:
        db_user.nombre = user_update.nombre
    if user_update.edad is not None:
        db_user.edad = user_update.edad
    if user_update.region is not None:
        db_user.region = user_update.region
    if user_update.email is not None:
        db_user.email = user_update.email
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user