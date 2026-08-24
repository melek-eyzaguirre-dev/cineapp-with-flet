import os
import sys

from alembic import command

import alembic
from dotenv import load_dotenv
from alembic.config import Config
import alembic
from sqlalchemy import text
from peliculas_flet.database import engine

load_dotenv()

def limpiar_version_corrupta():
    """Limpia la tabla alembic_version si quedó en un estado huérfano."""
    try:
        # usar begin() para que la operación se ejecute dentro de una transacción y se auto-commit
        with engine.begin() as conexion:
            conexion.execute(text("DROP TABLE IF EXISTS alembic_version;"))
        print("🧹 Tabla alembic_version verificada/limpiada.")
    except Exception as e:
        print(f"⚠️ Aviso al limpiar versión previa: {e}")

def ejecutar_migracion():
    print("==================================================")
    print("🚀 INICIANDO MIGRACIÓN AUTOMÁTICA CON ALEMBIC")
    print("==================================================")

    # Resolver ruta de alembic.ini relativa al proyecto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    alembic_ini = os.path.join(base_dir, "alembic.ini")
    alembic_cfg = Config(alembic_ini)

    try:
        print("🔍 1. Detectando cambios en los modelos...")
        command.revision(alembic_cfg, message="crear_tabla_peliculas", autogenerate=True)
        print("✅ Revisión generada con éxito.")

        print("⚡ 2. Aplicando cambios en MySQL...")
        command.upgrade(alembic_cfg, "head")
        print("==================================================")
        print("✅ ¡MIGRACIÓN COMPLETADA CON ÉXITO!")
        print("📊 La tabla 'peliculas' ha sido creada en flet_peliculas_db")
        print("==================================================")

    except Exception as e:
        print("==================================================")
        print("❌ Error durante la migración:")
        print(e)
        print("==================================================")

if __name__ == "__main__":
    limpiar_version_corrupta()
    ejecutar_migracion()