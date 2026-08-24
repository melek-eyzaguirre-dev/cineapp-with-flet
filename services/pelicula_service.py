import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "flet_peliculas_db",
    "port": 3307
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
    """Consulta y retorna todas las películas registradas."""
    conexion = obtener_conexion()
    if not conexion:
        return []

    peliculas = []
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, director, puntuacion FROM peliculas ORDER BY id ASC")
        peliculas = cursor.fetchall()
    except Error as e:
        print(f"❌ Error al consultar películas: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    return peliculas


def validar_datos_pelicula(datos: dict) -> tuple[bool, str]:  # [NUEVO]
    """Valida la integridad de los datos antes de operar en la base de datos."""  # [NUEVO]
    titulo = str(datos.get("titulo", "")).strip()  # [NUEVO]
    director = str(datos.get("director", "")).strip()  # [NUEVO]
    puntuacion_raw = datos.get("puntuacion")  # [NUEVO]

    if not titulo:  # [NUEVO]
        return False, "El título no puede estar vacío"  # [NUEVO]
    if not director:  # [NUEVO]
        return False, "El director no puede estar vacío"  # [NUEVO]

    try:  # [NUEVO]
        # Validar entero estricto o numérico exacto  # [NUEVO]
        puntuacion = int(puntuacion_raw)  # [NUEVO]
        if puntuacion < 1 or puntuacion > 10:  # [NUEVO]
            return False, "La puntuación debe ser un número entero entre 1 y 10"  # [NUEVO]
    except (ValueError, TypeError):  # [NUEVO]
        return False, "La puntuación debe ser un número entero válido"  # [NUEVO]

    return True, ""  # [NUEVO]


def crear(datos: dict) -> tuple[bool, str]:  # [MODIFICADO]
    """Inserta una nueva película en la base de datos con validaciones."""  # [MODIFICADO]
    es_valido, error_msg = validar_datos_pelicula(datos)  # [NUEVO]
    if not es_valido:  # [NUEVO]
        return False, error_msg  # [NUEVO]

    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo establecer conexión con la base de datos"  # [MODIFICADO]

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO peliculas (titulo, director, puntuacion) VALUES (%s, %s, %s)"
        valores = (datos["titulo"].strip(), datos["director"].strip(), int(datos["puntuacion"]))  # [MODIFICADO]
        cursor.execute(query, valores)
        conexion.commit()
        return True, "Película registrada exitosamente"  # [MODIFICADO]
    except Error as e:
        print(f"❌ Error al registrar película: {e}")
        if conexion.is_connected():
            conexion.rollback()
        return False, f"Error en base de datos: {e.msg}"  # [MODIFICADO]
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def obtener_por_id(pelicula_id: int):
    """Consulta y retorna una sola película por su ID o None si no existe."""
    conexion = obtener_conexion()
    if not conexion:
        return None

    pelicula = None
    try:
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT id, titulo, director, puntuacion FROM peliculas WHERE id = %s"
        cursor.execute(query, (pelicula_id,))
        pelicula = cursor.fetchone()
    except Error as e:
        print(f"❌ Error al consultar película por ID: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    return pelicula


def actualizar(pelicula_id: int, datos: dict) -> tuple[bool, str]:  # [MODIFICADO]
    """Actualiza los datos de una película existente con validaciones previas."""  # [MODIFICADO]
    es_valido, error_msg = validar_datos_pelicula(datos)  # [NUEVO]
    if not es_valido:  # [NUEVO]
        return False, error_msg  # [NUEVO]

    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo establecer conexión con la base de datos"  # [MODIFICADO]

    try:
        cursor = conexion.cursor()
        query = """
            UPDATE peliculas 
            SET titulo = %s, director = %s, puntuacion = %s 
            WHERE id = %s
        """
        valores = (datos["titulo"].strip(), datos["director"].strip(), int(datos["puntuacion"]),
                   pelicula_id)  # [MODIFICADO]
        cursor.execute(query, valores)
        conexion.commit()
        return True, "Película actualizada exitosamente"  # [MODIFICADO]
    except Error as e:
        print(f"❌ Error al actualizar película ID {pelicula_id}: {e}")
        if conexion.is_connected():
            conexion.rollback()
        return False, f"Error en base de datos: {e.msg}"  # [MODIFICADO]
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def eliminar(pelicula_id: int) -> bool:
    """Elimina una película por su ID."""
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