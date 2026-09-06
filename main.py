import os
from dotenv import load_dotenv
from fastapi import FastAPI
from database import engine, Base

# Importamos cada router modularizado desde la carpeta Routers/
from Routers.get_users import router as get_user_router
from Routers.post_users import router as post_user_router
from Routers.put_users import router as put_user_router
from Routers.delete_users import router as delete_user_router

# Carga variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./datos.db")
SECRET_KEY = os.getenv("SECRET_KEY")

print(f"Conectado a la base de datos en: {DATABASE_URL}")

# 1. Instancia principal de FastAPI
app = FastAPI(title="CRUD de Usuarios Modularizado por Métodos HTTP")

# 2. Genera las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# 3. Registra cada enrutador individualmente en la aplicación
app.include_router(post_user_router)
app.include_router(get_user_router)
app.include_router(put_user_router)
app.include_router(delete_user_router)
