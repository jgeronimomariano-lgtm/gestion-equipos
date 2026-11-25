"""
controladores/usuarios.py
Módulo de Usuarios (Aprendices / Instructores):
registrar usuarios y consultar el historial de usuarios registrados.
"""

from mysql.connector import Error, IntegrityError

from conexion import obtener_cursor
from utils import (
    elegir_opcion,
    mensaje_error,
    mensaje_exito,
    mensaje_info,
    pedir_documento,
    pedir_texto,
)

ROLES = ["Aprendiz", "Instructor"]


def registrar_usuario():
    """Registra un usuario con documento, nombre completo y rol."""
    print("=== REGISTRAR USUARIO ===")
    try:
        documento = pedir_documento()
        nombre = pedir_texto("Nombre completo")
        rol = elegir_opcion("Rol", ROLES)

        with obtener_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Usuarios (documento, nombre_completo, rol) "
                "VALUES (%s, %s, %s)",
                (documento, nombre, rol),
            )
        mensaje_exito(f"Usuario '{nombre}' registrado como {rol}.")
    except IntegrityError as e:
        if e.errno == 1062:  # llave primaria duplicada
            mensaje_error("Ya existe un usuario con ese documento.")
        else:
            mensaje_error(f"No se pudo registrar el usuario: {e}")
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")


def listar_usuarios():
    """Muestra todos los usuarios registrados."""
    print("=== USUARIOS REGISTRADOS ===")
    try:
        with obtener_cursor() as cursor:
            cursor.execute(
                "SELECT documento, nombre_completo, rol FROM Usuarios "
                "ORDER BY nombre_completo"
            )
            usuarios = cursor.fetchall()

        if not usuarios:
            mensaje_info("No hay usuarios registrados.")
            return

        print(f"\n{'Documento':<14}{'Nombre completo':<36}{'Rol'}")
        print("-" * 62)
        for u in usuarios:
            print(f"{u['documento']:<14}{u['nombre_completo']:<36}{u['rol']}")
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")
