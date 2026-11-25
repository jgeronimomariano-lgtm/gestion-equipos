"""
controladores/equipos.py
Módulo de Equipos (Inventario): registrar, consultar, actualizar,
cambiar estado y eliminar equipos.
Todas las consultas son parametrizadas (%s) para evitar inyección SQL.
"""

from mysql.connector import Error, errorcode

import utils
from conexion import obtener_cursor

TIPOS = ["PC de escritorio", "Portátil", "Tablet", "Router"]


# -----------------------------------------------------
# Funciones de apoyo
# -----------------------------------------------------
def obtener_equipo(id_equipo):
    """Devuelve el equipo como diccionario, o None si no existe."""
    with obtener_cursor() as cursor:
        cursor.execute("SELECT * FROM Equipos WHERE id_equipo = %s", (id_equipo,))
        return cursor.fetchone()


def _mostrar_equipos(equipos):
    """Imprime una lista de equipos en formato de tabla."""
    print(f"\n{'ID':<5}{'Serial':<15}{'Tipo':<19}{'Marca':<11}{'Modelo':<18}{'Estado':<18}")
    print("-" * 86)
    for e in equipos:
        print(f"{e['id_equipo']:<5}{e['serial']:<15}{e['tipo_dispositivo']:<19}"
              f"{e['marca']:<11}{e['modelo']:<18}{e['estado']:<18}")


# -----------------------------------------------------
# Registrar
# -----------------------------------------------------
def registrar_equipo():
    print("=== REGISTRAR EQUIPO ===")
    serial = utils.pedir_texto("Serial")
    tipo = utils.elegir_opcion("Tipo de dispositivo", TIPOS)
    marca = utils.pedir_texto("Marca")
    modelo = utils.pedir_texto("Modelo")

    try:
        with obtener_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Equipos (serial, tipo_dispositivo, marca, modelo) "
                "VALUES (%s, %s, %s, %s)",
                (serial, tipo, marca, modelo),
            )
            nuevo_id = cursor.lastrowid
        utils.mensaje_exito(f"Equipo registrado con ID {nuevo_id}. Estado inicial: Disponible.")
    except Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            utils.mensaje_error(f"Ya existe un equipo con el serial '{serial}'.")
        else:
            utils.mensaje_error(f"No se pudo registrar el equipo: {e}")


# -----------------------------------------------------
# Consultar
# -----------------------------------------------------
def listar_equipos():
    print("=== INVENTARIO DE EQUIPOS ===")
    try:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM Equipos ORDER BY id_equipo")
            equipos = cursor.fetchall()
        if equipos:
            _mostrar_equipos(equipos)
        else:
            utils.mensaje_info("No hay equipos registrados.")
    except Error as e:
        utils.mensaje_error(f"No se pudo consultar el inventario: {e}")


def consultar_estado_equipo():
    print("=== CONSULTAR ESTADO DE UN EQUIPO ===")
    id_equipo = utils.pedir_entero("ID del equipo")
    try:
        equipo = obtener_equipo(id_equipo)
        if equipo is None:
            utils.mensaje_error(f"No existe un equipo con ID {id_equipo}.")
        else:
            _mostrar_equipos([equipo])
            utils.mensaje_info(f"Estado actual: {equipo['estado']}")
    except Error as e:
        utils.mensaje_error(f"No se pudo consultar el equipo: {e}")


def listar_equipos_por_estado():
    print("=== EQUIPOS POR ESTADO ===")
    estado = utils.elegir_opcion("Estado", ["Disponible", "En Préstamo", "En Mantenimiento"])
    try:
        with obtener_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Equipos WHERE estado = %s ORDER BY id_equipo", (estado,)
            )
            equipos = cursor.fetchall()
        if equipos:
            _mostrar_equipos(equipos)
        else:
            utils.mensaje_info(f"No hay equipos en estado '{estado}'.")
    except Error as e:
        utils.mensaje_error(f"No se pudo consultar: {e}")


# -----------------------------------------------------
# Actualizar características
# -----------------------------------------------------
def actualizar_equipo():
    print("=== ACTUALIZAR EQUIPO ===")
    id_equipo = utils.pedir_entero("ID del equipo a actualizar")
    try:
        equipo = obtener_equipo(id_equipo)
        if equipo is None:
            utils.mensaje_error(f"No existe un equipo con ID {id_equipo}.")
            return

        _mostrar_equipos([equipo])
        print("\nPresione Enter para conservar el valor actual.")

        serial = input(f"Serial [{equipo['serial']}]: ").strip() or equipo["serial"]
        marca = input(f"Marca [{equipo['marca']}]: ").strip() or equipo["marca"]
        modelo = input(f"Modelo [{equipo['modelo']}]: ").strip() or equipo["modelo"]
        tipo = equipo["tipo_dispositivo"]
        if utils.confirmar(f"¿Cambiar el tipo de dispositivo (actual: {tipo})?"):
            tipo = utils.elegir_opcion("Nuevo tipo", TIPOS)

        with obtener_cursor() as cursor:
            cursor.execute(
                "UPDATE Equipos SET serial = %s, tipo_dispositivo = %s, "
                "marca = %s, modelo = %s WHERE id_equipo = %s",
                (serial, tipo, marca, modelo, id_equipo),
            )
        utils.mensaje_exito("Equipo actualizado correctamente.")
    except Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            utils.mensaje_error("Ese serial ya pertenece a otro equipo.")
        else:
            utils.mensaje_error(f"No se pudo actualizar el equipo: {e}")


# -----------------------------------------------------
# Cambiar estado (Disponible <-> En Mantenimiento)
# -----------------------------------------------------
def cambiar_estado_equipo():
    """
    Solo permite pasar entre 'Disponible' y 'En Mantenimiento'.
    'En Préstamo' lo controla únicamente el módulo de préstamos.
    """
    print("=== CAMBIAR ESTADO DE UN EQUIPO ===")
    id_equipo = utils.pedir_entero("ID del equipo")
    try:
        equipo = obtener_equipo(id_equipo)
        if equipo is None:
            utils.mensaje_error(f"No existe un equipo con ID {id_equipo}.")
            return

        _mostrar_equipos([equipo])

        if equipo["estado"] == "En Préstamo":
            utils.mensaje_error("El equipo está en préstamo. Primero debe registrarse su devolución.")
            return

        nuevo_estado = utils.elegir_opcion("Nuevo estado", ["Disponible", "En Mantenimiento"])
        if nuevo_estado == equipo["estado"]:
            utils.mensaje_info(f"El equipo ya está '{nuevo_estado}'.")
            return

        with obtener_cursor() as cursor:
            cursor.execute(
                "UPDATE Equipos SET estado = %s WHERE id_equipo = %s",
                (nuevo_estado, id_equipo),
            )
        utils.mensaje_exito(f"Estado actualizado a '{nuevo_estado}'.")
    except Error as e:
        utils.mensaje_error(f"No se pudo cambiar el estado: {e}")


# -----------------------------------------------------
# Eliminar (dar de baja)
# -----------------------------------------------------
def eliminar_equipo():
    print("=== ELIMINAR EQUIPO (DAR DE BAJA) ===")
    id_equipo = utils.pedir_entero("ID del equipo a eliminar")
    try:
        equipo = obtener_equipo(id_equipo)
        if equipo is None:
            utils.mensaje_error(f"No existe un equipo con ID {id_equipo}.")
            return

        _mostrar_equipos([equipo])

        if equipo["estado"] == "En Préstamo":
            utils.mensaje_error("No se puede eliminar un equipo que está en préstamo.")
            return

        if not utils.confirmar("¿Seguro que desea eliminar este equipo?"):
            utils.mensaje_info("Operación cancelada.")
            return

        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM Equipos WHERE id_equipo = %s", (id_equipo,))
        utils.mensaje_exito("Equipo eliminado correctamente.")
    except Error as e:
        if e.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            utils.mensaje_error(
                "No se puede eliminar: el equipo tiene préstamos en su historial."
            )
        else:
            utils.mensaje_error(f"No se pudo eliminar el equipo: {e}")
