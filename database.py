from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Url = "sqlite:///datos.db"

# se supone que aquí se dice dónde el motor va a guardar el archivo de la base de datos
engine = create_engine(Url, connect_args={"check_same_thread": False}, echo=True)

# Este es el código de la sesión que es donde se irán anotando los cambios y guardando o descartando
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Se va a definir la base que luego pueden heredar sus especificaciones
Base = declarative_base()

#Crea una sesión para cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()