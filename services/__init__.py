"""Paquete de servicios para la lógica de negocio y base de datos."""

from .pelicula_service import (
    obtener_conexion,
    obtener_todos,
    crear,
    obtener_por_id,
    actualizar,
    eliminar  # [NUEVO]
)

__all__ = [
    "obtener_conexion",
    "obtener_todos",
    "crear",
    "obtener_por_id",
    "actualizar",
    "eliminar"  # [MODIFICADO]
]