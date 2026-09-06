from fastapi import FastAPI
from database import engine, Base
from controlls import router as user_router
import os
from dotenv import load_dotenv

load_dotenv()

# Lee la variable de entorno mediante os.getenv()
# Puedes pasar un segundo argumento como valor por defecto en caso de que no exista
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./datos.db")
SECRET_KEY = os.getenv("SECRET_KEY")

print(f"Conectado a la base de datos en: {DATABASE_URL}")

# 1. Genera las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# 2. Instancia principal de FastAPI
app = FastAPI()

# 3. Registra el enrutador de usuarios en la aplicación
app.include_router(user_router)