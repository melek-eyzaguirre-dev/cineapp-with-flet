import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Cargar variables de entorno desde el archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construcción de la URL de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creación de motor, sesión y modelo base
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Bloque de prueba de conexión al ejecutar directamente el archivo
if __name__ == "__main__":
    try:
        with engine.connect() as conexion:
            resultado = conexion.execute(text("SELECT 1"))
            print("==================================================")
            print("✅ ¡Conexión exitosa a la base de datos MySQL!")
            print(f"📊 Base conectada: {DB_NAME} en {DB_HOST}:{DB_PORT}")
            print("==================================================")
    except Exception as e:
        print("==================================================")
        print("❌ Error al conectar con la base de datos:")
        print(e)
        print("==================================================")