# Guía de pruebas y sustentación

## A. Pruebas desde el menú (py main.py)

| # | Menú | Acción | Resultado esperado |
|---|------|--------|--------------------|
| 1 | 1 → 2 | Listar inventario | Salen los 8 equipos |
| 2 | 1 → 1 | Registrar equipo nuevo (serial `TEST-001`) | Mensaje ✔ con el ID nuevo |
| 3 | 1 → 1 | Registrar otro con el mismo serial | ✘ "Ya existe un equipo con el serial" |
| 4 | 1 → 6 | Cambiar estado del equipo 3 | ✘ Bloqueado: está en préstamo |
| 5 | 1 → 6 | Equipo 4 → "En Mantenimiento" | ✔ y en phpMyAdmin cambia al recargar |
| 6 | 1 → 7 | Eliminar el equipo 3 | ✘ No se puede: está en préstamo |
| 7 | 1 → 7 | Eliminar el equipo 1 | ✘ Tiene historial de préstamos |
| 8 | 1 → 7 | Eliminar el equipo nuevo `TEST-001` | ✔ Eliminado |
| 9 | 2 → 1 | Registrar usuario nuevo | ✔ Registrado |
| 10 | 2 → 1 | Repetir el mismo documento | ✘ "Ya existe un usuario" |
| 11 | 2 → 2 | Historial de usuarios | Lista con cantidad de préstamos |
| 12 | 3 → 1 | Prestar el equipo 2 a un usuario | ✔ con fecha y hora; equipo "En Préstamo" |
| 13 | 3 → 1 | Prestar de nuevo el equipo 2 | ✘ No está disponible |
| 14 | 3 → 1 | Prestar con documento inexistente | ✘ No existe el usuario |
| 15 | 3 → 3 | Ver préstamos activos | Aparece el préstamo del equipo 2 |
| 16 | 3 → 2 | Devolver el equipo 2 | ✔ y el equipo vuelve a "Disponible" |
| 17 | 3 → 2 | Devolver el equipo 2 otra vez | ✘ No tiene préstamo activo |
| 18 | 3 → 4 | Historial de préstamos | Salen todos, con fecha de devolución |

Prueba también escribir letras donde se piden números: el programa debe volver a preguntar, sin caerse.

## B. Demostración en vivo (lo que pide el instructor)

1. Abre **phpMyAdmin** en una pestaña, en las tablas `Equipos` y `Prestamos`.
2. Ejecuta `py main.py` en la otra ventana.
3. Registra un préstamo y **recarga phpMyAdmin**: se ve el nuevo registro y el estado "En Préstamo".
4. Registra la devolución y **recarga**: aparece la fecha de devolución y el equipo vuelve a "Disponible".

## C. Qué explicar en la sustentación

- **Modularidad:** `conexion.py` (conexión), `controladores/` (lógica CRUD), `main.py` (menú), `utils.py` (apoyo).
- **Programación estructurada:** funciones con una sola responsabilidad, reutilizadas desde el menú.
- **Seguridad:** todas las consultas usan `%s` con parámetros. Nunca se concatenan textos en el SQL.
- **Manejo de errores:** `try-except` captura errores de MySQL (conexión, serial/documento duplicado, llave foránea) y muestra mensajes legibles.
- **Transacciones:** en `conexion.py`, si algo falla se hace `rollback`. Un préstamo guarda el registro y cambia el estado del equipo en la misma transacción.
- **Concurrencia:** `SELECT ... FOR UPDATE` bloquea el equipo mientras se presta, para que dos personas no lo presten a la vez.
- **Integridad:** llaves foráneas con `ON DELETE RESTRICT`, serial `UNIQUE`, `ENUM` para estado, tipo y rol.
- **Decisión de diseño:** el estado "En Préstamo" solo lo cambia el módulo de préstamos; el módulo de equipos solo alterna entre Disponible y En Mantenimiento.
- **Cambio sobre la guía:** se agregó la columna `modelo` a `Equipos`, porque el requerimiento funcional pide registrar el modelo.

## D. Subir el proyecto a GitHub

1. Crea una cuenta en https://github.com y un repositorio nuevo (*New repository*), por ejemplo `gestion-equipos`, sin README.
2. Instala Git desde https://git-scm.com y configura tu identidad (una sola vez):
   ```
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu_correo@ejemplo.com"
   ```
3. En la carpeta del proyecto:
   ```
   git init
   git add .
   git commit -m "Proyecto inicial: gestión y préstamo de equipos"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/gestion-equipos.git
   git push -u origin main
   ```
4. Revisa en GitHub que **no** se haya subido `config.py` (está en `.gitignore`); sí debe estar `config.example.py`.
5. Para próximos cambios: `git add .`, `git commit -m "descripción"`, `git push`.

Si trabajan en grupo, cada integrante clona el repositorio (`git clone <url>`), crea su `config.py` a partir de `config.example.py` y trabaja en una rama (`git checkout -b modulo-usuarios`).
