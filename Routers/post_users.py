from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from clases import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Usuarios - Creación"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)): 
    db_user = User(nombre=user.nombre, edad=user.edad, region=user.region, email=user.email)  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user