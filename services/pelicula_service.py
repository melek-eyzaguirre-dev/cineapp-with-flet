from decimal import Decimal
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "flet_peliculas_db",
    "port": 3307,
}


def obtener_conexion():
  """Establece y retorna la conexión con MySQL."""
  try:
    conexion = mysql.connector.connect(**DB_CONFIG)
    return conexion
  except Error as e:
    print(f"❌ Error al conectar con MySQL: {e}")
    return None


def obtener_todos():
  """Consulta y retorna todas las películas registradas con sus nuevos campos."""
  conexion = obtener_conexion()
  if not conexion:
    return []

  peliculas = []
  try:
    cursor = conexion.cursor(dictionary=True)
    query = """
            SELECT id, titulo, director, genero, anio_estreno, duracion_min, poster_url, comentario, puntuacion 
            FROM peliculas 
            ORDER BY id ASC
        """
    cursor.execute(query)
    peliculas = cursor.fetchall()
  except Error as e:
    print(f"❌ Error al consultar películas: {e}")
  finally:
    if conexion.is_connected():
      cursor.close()
      conexion.close()

  return peliculas


def validar_datos_pelicula(datos: dict) -> tuple[bool, str]:
  """Valida los campos requeridos y tipos de datos."""
  titulo = str(datos.get("titulo", "")).strip()
  director = str(datos.get("director", "")).strip()
  genero = str(datos.get("genero", "")).strip()
  puntuacion_raw = datos.get("puntuacion")
  anio_raw = datos.get("anio_estreno")
  duracion_raw = datos.get("duracion_min")

  if not titulo:
    return False, "El título no puede estar vacío"
  if not director:
    return False, "El director no puede estar vacío"
  if not genero:
    return False, "Debes seleccionar un género"

  try:
    puntuacion = float(str(puntuacion_raw).replace(",", "."))
    if puntuacion < 1.0 or puntuacion > 10.0:
      return False, "La puntuación debe estar entre 1.0 y 10.0"
  except (ValueError, TypeError):
    return False, "Puntuación inválida (ej: 8.5)"

  try:
    anio = int(anio_raw)
    if anio < 1888 or anio > 2030:
      return False, "Año de estreno fuera de rango (1888 - 2030)"
  except (ValueError, TypeError):
    return False, "El año debe ser un número entero"

  try:
    duracion = int(duracion_raw)
    if duracion <= 0:
      return False, "La duración debe ser mayor a 0 minutos"
  except (ValueError, TypeError):
    return False, "La duración debe ser un número entero en minutos"

  return True, ""


def crear(datos: dict) -> tuple[bool, str]:
  """Inserta una nueva película con todos los campos."""
  es_valido, error_msg = validar_datos_pelicula(datos)
  if not es_valido:
    return False, error_msg

  conexion = obtener_conexion()
  if not conexion:
    return False, "No se pudo conectar a la base de datos"

  try:
    cursor = conexion.cursor()
    query = """
            INSERT INTO peliculas (titulo, director, genero, anio_estreno, duracion_min, poster_url, comentario, puntuacion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    puntuacion_val = round(
        float(str(datos["puntuacion"]).replace(",", ".")), 1
    )
    valores = (
        datos["titulo"].strip(),
        datos["director"].strip(),
        datos["genero"].strip(),
        int(datos["anio_estreno"]),
        int(datos["duracion_min"]),
        datos.get("poster_url", "").strip(),
        datos.get("comentario", "").strip(),
        puntuacion_val,
    )
    cursor.execute(query, valores)
    conexion.commit()
    return True, "Película registrada exitosamente"
  except Error as e:
    print(f"❌ Error al registrar película: {e}")
    if conexion.is_connected():
      conexion.rollback()
    return False, f"Error en base de datos: {e.msg}"
  finally:
    if conexion.is_connected():
      cursor.close()
      conexion.close()


def obtener_por_id(pelicula_id: int):
  """Consulta una película por su ID."""
  conexion = obtener_conexion()
  if not conexion:
    return None

  pelicula = None
  try:
    cursor = conexion.cursor(dictionary=True)
    query = """
            SELECT id, titulo, director, genero, anio_estreno, duracion_min, poster_url, comentario, puntuacion 
            FROM peliculas 
            WHERE id = %s
        """
    cursor.execute(query, (pelicula_id,))
    pelicula = cursor.fetchone()
  except Error as e:
    print(f"❌ Error al consultar película por ID: {e}")
  finally:
    if conexion.is_connected():
      cursor.close()
      conexion.close()

  return pelicula


def actualizar(pelicula_id: int, datos: dict) -> tuple[bool, str]:
  """Actualiza todos los campos de una película existente."""
  es_valido, error_msg = validar_datos_pelicula(datos)
  if not es_valido:
    return False, error_msg

  conexion = obtener_conexion()
  if not conexion:
    return False, "No se pudo conectar a la base de datos"

  try:
    cursor = conexion.cursor()
    query = """
            UPDATE peliculas 
            SET titulo = %s, director = %s, genero = %s, anio_estreno = %s, 
                duracion_min = %s, poster_url = %s, comentario = %s, puntuacion = %s 
            WHERE id = %s
        """
    puntuacion_val = round(
        float(str(datos["puntuacion"]).replace(",", ".")), 1
    )
    valores = (
        datos["titulo"].strip(),
        datos["director"].strip(),
        datos["genero"].strip(),
        int(datos["anio_estreno"]),
        int(datos["duracion_min"]),
        datos.get("poster_url", "").strip(),
        datos.get("comentario", "").strip(),
        puntuacion_val,
        pelicula_id,
    )
    cursor.execute(query, valores)
    conexion.commit()
    return True, "Película actualizada exitosamente"
  except Error as e:
    print(f"❌ Error al actualizar película ID {pelicula_id}: {e}")
    if conexion.is_connected():
      conexion.rollback()
    return False, f"Error en base de datos: {e.msg}"
  finally:
    if conexion.is_connected():
      cursor.close()
      conexion.close()


def eliminar(pelicula_id: int) -> bool:
  """Elimina una película por ID."""
  conexion = obtener_conexion()
  if not conexion:
    return False

  exito = False
  try:
    cursor = conexion.cursor()
    query = "DELETE FROM peliculas WHERE id = %s"
    cursor.execute(query, (pelicula_id,))
    conexion.commit()
    exito = True
  except Error as e:
    print(f"❌ Error al eliminar película ID {pelicula_id}: {e}")
    if conexion.is_connected():
      conexion.rollback()
  finally:
    if conexion.is_connected():
      cursor.close()
      conexion.close()

  return exito
