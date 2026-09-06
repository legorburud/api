from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from clases import UserResponse

router = APIRouter(prefix="/users", tags=["Usuarios - Eliminación"])

# Borrado Lógico
@router.delete("/{user_id}", response_model=UserResponse)
def soft_delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

# Borrado Total / Físico
@router.delete("/{user_id}/hard", status_code=status.HTTP_200_OK)
def hard_delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"Usuario {user_id} eliminado permanentemente"}