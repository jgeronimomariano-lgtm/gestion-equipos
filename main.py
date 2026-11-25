"""
main.py
Menú principal del Sistema de Gestión y Préstamo de Equipos de Cómputo.
Solo se encarga de la interacción; la lógica vive en /controladores.
"""

from conexion import probar_conexion
from controladores import equipos, prestamos, usuarios
from utils import limpiar_pantalla, mensaje_error, pausar


def ejecutar(accion):
    """Limpia la pantalla, ejecuta una acción y espera a que el usuario lea."""
    limpiar_pantalla()
    try:
        accion()
    except Exception as e:  # red de seguridad: el programa nunca debe colapsar
        mensaje_error(f"Ocurrió un error inesperado: {e}")
    pausar()


def mostrar_menu(titulo, opciones):
    """
    Muestra un menú. 'opciones' es una lista de (texto, función).
    La opción 0 siempre es volver/salir. Devuelve el texto escrito.
    """
    limpiar_pantalla()
    print("=" * 50)
    print(f"  {titulo}")
    print("=" * 50)
    for i, (texto, _) in enumerate(opciones, start=1):
        print(f"  {i}. {texto}")
    print("  0. Volver / Salir")
    return input("\nElija una opción: ").strip()


def ejecutar_menu(titulo, opciones, es_principal=False):
    """
    Repite un menú hasta que el usuario elija 0.
    En el menú principal las opciones son submenús, que no necesitan pausa.
    """
    while True:
        eleccion = mostrar_menu(titulo, opciones)
        if eleccion == "0":
            return
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            accion = opciones[int(eleccion) - 1][1]
            if es_principal:
                accion()
            else:
                ejecutar(accion)
        else:
            mensaje_error("Opción no válida.")
            pausar()


def menu_equipos():
    ejecutar_menu("MÓDULO DE EQUIPOS", [
        ("Registrar equipo", equipos.registrar_equipo),
        ("Ver inventario completo", equipos.listar_equipos),
        ("Consultar equipo por ID", equipos.consultar_estado_equipo),
        ("Consultar equipos por estado", equipos.listar_equipos_por_estado),
        ("Actualizar características", equipos.actualizar_equipo),
        ("Cambiar estado (Disponible / Mantenimiento)", equipos.cambiar_estado_equipo),
        ("Eliminar equipo (dado de baja)", equipos.eliminar_equipo),
    ])


def menu_usuarios():
    ejecutar_menu("MÓDULO DE USUARIOS", [
        ("Registrar usuario", usuarios.registrar_usuario),
        ("Ver usuarios registrados", usuarios.listar_usuarios),
    ])


def menu_prestamos():
    ejecutar_menu("PRÉSTAMOS Y DEVOLUCIONES", [
        ("Registrar préstamo", prestamos.prestar_equipo),
        ("Registrar devolución", prestamos.devolver_equipo),
        ("Ver préstamos activos", prestamos.listar_prestamos_activos),
        ("Ver historial de préstamos", prestamos.historial_prestamos),
    ])


def main():
    limpiar_pantalla()
    if not probar_conexion():
        print("\nRevise que MySQL esté iniciado en XAMPP y los datos de config.py.")
        return
    pausar()

    ejecutar_menu("SISTEMA DE GESTIÓN DE EQUIPOS DE CÓMPUTO", [
        ("Equipos (inventario)", menu_equipos),
        ("Usuarios", menu_usuarios),
        ("Préstamos y devoluciones", menu_prestamos),
    ], es_principal=True)
    limpiar_pantalla()
    print("Hasta luego.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma cerrado por el usuario.")