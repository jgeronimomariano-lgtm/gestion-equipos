"""
conexion.py
Capa de acceso a la base de datos.
Ofrece un gestor de contexto que abre la conexión, entrega un cursor,
confirma (commit) si todo sale bien y deshace (rollback) si hay un error.
"""

from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


@contextmanager
def obtener_cursor(como_diccionario=True):
    """
    Uso:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM Equipos WHERE id_equipo = %s", (1,))
            fila = cursor.fetchone()
    """
    conexion = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=como_diccionario)
        try:
            yield cursor
            conexion.commit()      # todo salió bien: guardar cambios
        except Error:
            conexion.rollback()    # algo falló: deshacer cambios
            raise
        finally:
            cursor.close()
    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


def probar_conexion():
    """Devuelve True si se puede conectar a la base de datos."""
    try:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM Equipos")
            total = cursor.fetchone()["total"]
        print(f"Conexión exitosa. Equipos registrados: {total}")
        return True
    except Error as e:
        print(f"Error de conexión: {e}")
        return False


if __name__ == "__main__":
    probar_conexion()
