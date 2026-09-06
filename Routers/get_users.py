from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from clases import UserResponse

# Se mantiene tu prefix y tag
router = APIRouter(prefix="/users", tags=["Usuarios - Lectura"])

@router.get("/", response_model=list[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100,
    # Parámetros opcionales para buscar por columnas específicas
    nombre: Optional[str] = None,
    region: Optional[str] = None,
    email: Optional[str] = None,
    solo_activos: bool = True,  # Filtra usuarios que no hayan sufrido borrado lógico
    db: Session = Depends(get_db)
):
    # 1. Creamos la consulta base
    query = db.query(User)
    
    # 2. Filtrar solo los usuarios activos si solo_activos es True
    if solo_activos:
        query = query.filter(User.is_active == True)
        
    # 3. Aplicar filtros dinámicos por palabra clave si el cliente los envía
    if nombre:
        query = query.filter(User.nombre.ilike(f"%{nombre}%"))
        
    if region:
        query = query.filter(User.region.ilike(f"%{region}%"))
        
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
        
    # 4. Retornamos los resultados paginados
    return query.offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:   
        raise HTTPException(status_code=404, detail="User not found")
    return user