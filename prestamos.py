"""
controladores/prestamos.py
Módulo de Transacciones: préstamos y devoluciones.
Cada operación se hace en UNA sola transacción (insert/update de
Prestamos + update de Equipos): o se guardan ambos cambios o ninguno.
"""

from mysql.connector import Error

from conexion import obtener_cursor
from utils import (
    mensaje_error,
    mensaje_exito,
    mensaje_info,
    pedir_documento,
    pedir_entero,
)


def _formato_fecha(fecha):
    """Convierte un datetime a texto legible (o 'Pendiente' si es None)."""
    return fecha.strftime("%Y-%m-%d %H:%M:%S") if fecha else "Pendiente"


def prestar_equipo():
    """Presta un equipo 'Disponible' a un usuario y registra fecha y hora."""
    print("=== REGISTRAR PRÉSTAMO ===")
    try:
        documento = pedir_documento("Documento del usuario")
        id_equipo = pedir_entero("ID del equipo")

        with obtener_cursor() as cursor:
            # 1. El usuario debe existir
            cursor.execute(
                "SELECT nombre_completo FROM Usuarios WHERE documento = %s",
                (documento,),
            )
            usuario = cursor.fetchone()
            if usuario is None:
                mensaje_error("No existe un usuario con ese documento.")
                return

            # 2. El equipo debe existir; FOR UPDATE lo bloquea durante la transacción
            cursor.execute(
                "SELECT serial, marca, modelo, estado FROM Equipos "
                "WHERE id_equipo = %s FOR UPDATE",
                (id_equipo,),
            )
            equipo = cursor.fetchone()
            if equipo is None:
                mensaje_error("No existe un equipo con ese ID.")
                return

            # 3. Validar que esté 'Disponible'
            if equipo["estado"] != "Disponible":
                mensaje_error(
                    f"El equipo no se puede prestar: está '{equipo['estado']}'."
                )
                return

            # 4. Registrar el préstamo con fecha y hora exactas (NOW())
            cursor.execute(
                "INSERT INTO Prestamos (documento_usuario, id_equipo, fecha_salida) "
                "VALUES (%s, %s, NOW())",
                (documento, id_equipo),
            )
            id_prestamo = cursor.lastrowid

            # 5. Cambiar el estado del equipo
            cursor.execute(
                "UPDATE Equipos SET estado = 'En Préstamo' WHERE id_equipo = %s",
                (id_equipo,),
            )

            cursor.execute(
                "SELECT fecha_salida FROM Prestamos WHERE id_prestamo = %s",
                (id_prestamo,),
            )
            fecha = cursor.fetchone()["fecha_salida"]

        mensaje_exito(
            f"Préstamo #{id_prestamo} registrado: {equipo['marca']} "
            f"{equipo['modelo']} ({equipo['serial']}) para "
            f"{usuario['nombre_completo']}.\n  Fecha y hora de salida: "
            f"{_formato_fecha(fecha)}"
        )
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")


def devolver_equipo():
    """Procesa la devolución: cierra el préstamo y deja el equipo 'Disponible'."""
    print("=== REGISTRAR DEVOLUCIÓN ===")
    try:
        id_equipo = pedir_entero("ID del equipo a devolver")

        with obtener_cursor() as cursor:
            # Buscar el préstamo activo (sin fecha de devolución) de ese equipo
            cursor.execute(
                "SELECT id_prestamo, documento_usuario FROM Prestamos "
                "WHERE id_equipo = %s AND fecha_devolucion IS NULL FOR UPDATE",
                (id_equipo,),
            )
            prestamo = cursor.fetchone()
            if prestamo is None:
                mensaje_error("Ese equipo no tiene un préstamo activo.")
                return

            cursor.execute(
                "UPDATE Prestamos SET fecha_devolucion = NOW() "
                "WHERE id_prestamo = %s",
                (prestamo["id_prestamo"],),
            )
            cursor.execute(
                "UPDATE Equipos SET estado = 'Disponible' WHERE id_equipo = %s",
                (id_equipo,),
            )

            cursor.execute(
                "SELECT fecha_devolucion FROM Prestamos WHERE id_prestamo = %s",
                (prestamo["id_prestamo"],),
            )
            fecha = cursor.fetchone()["fecha_devolucion"]

        mensaje_exito(
            f"Devolución registrada (préstamo #{prestamo['id_prestamo']}). "
            f"El equipo quedó 'Disponible'.\n  Fecha y hora de devolución: "
            f"{_formato_fecha(fecha)}"
        )
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")


def _imprimir_prestamos(filas):
    print(
        f"\n{'ID':<5}{'Documento':<13}{'Usuario':<28}{'Equipo':<24}"
        f"{'Salida':<21}{'Devolución'}"
    )
    print("-" * 105)
    for p in filas:
        equipo = f"{p['marca']} {p['modelo']}"
        print(
            f"{p['id_prestamo']:<5}{p['documento_usuario']:<13}"
            f"{p['nombre_completo'][:26]:<28}{equipo[:22]:<24}"
            f"{_formato_fecha(p['fecha_salida']):<21}"
            f"{_formato_fecha(p['fecha_devolucion'])}"
        )


_CONSULTA_BASE = (
    "SELECT p.id_prestamo, p.documento_usuario, u.nombre_completo, "
    "e.marca, e.modelo, p.fecha_salida, p.fecha_devolucion "
    "FROM Prestamos p "
    "JOIN Usuarios u ON u.documento = p.documento_usuario "
    "JOIN Equipos e ON e.id_equipo = p.id_equipo "
)


def listar_prestamos_activos():
    """Muestra los préstamos que aún no se han devuelto."""
    print("=== PRÉSTAMOS ACTIVOS ===")
    try:
        with obtener_cursor() as cursor:
            cursor.execute(
                _CONSULTA_BASE
                + "WHERE p.fecha_devolucion IS NULL ORDER BY p.fecha_salida"
            )
            filas = cursor.fetchall()
        if not filas:
            mensaje_info("No hay préstamos activos.")
            return
        _imprimir_prestamos(filas)
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")


def historial_prestamos():
    """Muestra el historial completo de préstamos y devoluciones."""
    print("=== HISTORIAL DE PRÉSTAMOS ===")
    try:
        with obtener_cursor() as cursor:
            cursor.execute(_CONSULTA_BASE + "ORDER BY p.fecha_salida DESC")
            filas = cursor.fetchall()
        if not filas:
            mensaje_info("Aún no hay préstamos registrados.")
            return
        _imprimir_prestamos(filas)
    except Error as e:
        mensaje_error(f"Error de base de datos: {e}")
