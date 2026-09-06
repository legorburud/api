from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import User
from database import get_db
from clases import UserCreate, UserResponse, UserUpdate

# sin esta funcion existe un error de importación circular, ya que data.py importa de clases.py y clases.py importa de data.py  
router = APIRouter()

# se define un endpost
@router.post("/users/", response_model=UserResponse)  #se define el formato de respuesta
def create_user(user: UserCreate, db: Session = Depends(get_db)): 
    db_user = User(nombre=user.nombre, edad=user.edad, region=user.region, email=user.email)  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:   
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
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

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user
