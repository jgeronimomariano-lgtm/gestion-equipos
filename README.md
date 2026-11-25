# Sistema de Gestión y Préstamo de Equipos de Cómputo

Aplicación de consola en Python con MySQL para administrar el inventario
tecnológico y controlar el préstamo y la devolución de equipos a usuarios
(aprendices e instructores).

Proyecto del Técnico en Programación de Software (SENA) - Retos de Programación.

## Requisitos

- Python 3.x
- MySQL / MariaDB (por ejemplo, con XAMPP)
- Librería `mysql-connector-python`

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/TU_USUARIO/gestion_equipos.git
   cd gestion_equipos
   ```
2. Instalar la dependencia:
   ```
   pip install -r requirements.txt
   ```
3. Iniciar **MySQL** desde el panel de XAMPP (botón *Start*).
4. Crear la base de datos: abrir `http://localhost/phpmyadmin`, ir a la pestaña
   **Importar**, seleccionar el archivo `database.sql` y pulsar **Continuar**.
   (El script crea la base `gestion_equipos`, las tablas y los datos de prueba.)
5. Revisar `config.py`: si cambiaste el puerto o la contraseña de MySQL,
   ajústalos ahí (por defecto: `localhost`, puerto `3306`, usuario `root`,
   sin contraseña).

## Ejecución

```
python main.py
```

## Estructura del proyecto

```
gestion_equipos/
├── main.py              # Menú principal (interacción con el usuario)
├── conexion.py          # Conexión a MySQL (commit / rollback automáticos)
├── config.py            # Datos de conexión
├── utils.py             # Limpiar pantalla, mensajes y validación de entradas
├── database.sql         # Creación de la BD, tablas y datos de prueba
├── requirements.txt
└── controladores/
    ├── equipos.py       # CRUD de equipos
    ├── usuarios.py      # Registro y consulta de usuarios
    └── prestamos.py     # Préstamos y devoluciones
```

## Funcionalidades

- **Equipos:** registrar, consultar (por ID o por estado), actualizar,
  cambiar estado (Disponible / En Mantenimiento) y eliminar.
- **Usuarios:** registrar (documento, nombre completo y rol) y consultar.
- **Préstamos:** prestar un equipo 'Disponible' registrando fecha y hora
  exactas, procesar la devolución (el equipo vuelve a 'Disponible') y
  consultar préstamos activos e historial.

## Aspectos técnicos

- Consultas parametrizadas (`%s`) para evitar inyección SQL.
- Manejo de errores con `try-except` (conexión a MySQL y datos inválidos).
- Préstamo y devolución en una sola transacción: se guardan ambos cambios o ninguno.
- Código modular: conexión, controladores y menú en archivos separados.

## Modelo de datos

- **Equipos** (`id_equipo` PK, `serial`, `tipo_dispositivo`, `marca`, `modelo`, `estado`)
- **Usuarios** (`documento` PK, `nombre_completo`, `rol`)
- **Prestamos** (`id_prestamo` PK, `documento_usuario` FK, `id_equipo` FK,
  `fecha_salida`, `fecha_devolucion`)

## Autores

- Velery Donado
- Julián Gerónimo
