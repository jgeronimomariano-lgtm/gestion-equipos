"""
utils.py
Funciones de apoyo para la consola: limpiar pantalla, mensajes
y validación de lo que escribe el usuario.
"""

import os


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para continuar...")


def mensaje_exito(texto):
    print(f"\n✔ {texto}")


def mensaje_error(texto):
    print(f"\n✘ {texto}")


def mensaje_info(texto):
    print(f"\nℹ {texto}")


def pedir_texto(etiqueta, obligatorio=True):
    """Pide un texto y valida que no esté vacío."""
    while True:
        valor = input(f"{etiqueta}: ").strip()
        if valor or not obligatorio:
            return valor
        mensaje_error("Este campo no puede estar vacío.")


def pedir_entero(etiqueta):
    """Pide un número entero y repite hasta que sea válido."""
    while True:
        valor = input(f"{etiqueta}: ").strip()
        try:
            return int(valor)
        except ValueError:
            mensaje_error("Debe ingresar un número entero.")


def pedir_documento(etiqueta="Documento"):
    """Valida que el documento tenga solo dígitos (entre 5 y 15)."""
    while True:
        valor = input(f"{etiqueta}: ").strip()
        if valor.isdigit() and 5 <= len(valor) <= 15:
            return valor
        mensaje_error("El documento debe tener solo números (5 a 15 dígitos).")


def elegir_opcion(titulo, opciones):
    """
    Muestra una lista numerada y devuelve la opción elegida.
    Ejemplo: elegir_opcion("Tipo de dispositivo", ["Portátil", "Tablet"])
    """
    print(f"\n{titulo}:")
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion}")
    while True:
        numero = pedir_entero("Elija una opción")
        if 1 <= numero <= len(opciones):
            return opciones[numero - 1]
        mensaje_error(f"Elija un número entre 1 y {len(opciones)}.")


def confirmar(pregunta):
    """Pide confirmación (s/n). Devuelve True si responde 's'."""
    while True:
        respuesta = input(f"{pregunta} (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        mensaje_error("Responda 's' para sí o 'n' para no.")
