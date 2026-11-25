"""
config.py
Datos de conexión a la base de datos.
Si cambias el puerto o la contraseña de XAMPP, solo editas este archivo.
"""

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,            # usa 3307 si cambiaste el puerto de XAMPP
    "user": "root",
    "password": "",          # XAMPP trae la contraseña vacía por defecto
    "database": "gestion_equipos",
    "charset": "utf8mb4",
    "use_pure": True,        # usa el conector 100% Python (evita el cierre silencioso)
}