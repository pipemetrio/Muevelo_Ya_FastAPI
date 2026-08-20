# API de Gestión de MueveloYa

API REST desarrollada con FastAPI para la prestacion de servicios de transporte de objetos y mudanzas.

El proyecto permite administrar las entidades, con operaciones CRUD, autenticación y control de permisos según el tipo de usuario.

## Integrantes

- Sebastian Ramirez Castrillon
- Joel Andrés Mendoza Buritica
- Juan Sebastian Ramirez Velez
- Andrés Felipe Vargas Metrio
- Sergio Andrés López Sepúlveda

## Tecnologías

- Python
- FastAPI
- SQLite
- JWT
- bcrypt

## Objetivo

Desarrollar una API sencilla que permita solucionar el problema de conseguir un servicio de transporte de objetos y mudanzas, facilitando la solicitud y gestion de estos.

## Diagrama Entidad-Relación
![Diagrama del Sistema](nombre_de_tu_archivo_de_imagen.png)

## Usuarios de Ejemplo

Para las pruebas de autenticación y roles, utilice las siguientes credenciales:

| Correo electrónico | Rol | Contraseña |
| :--- | :--- | :--- |
| admin@mueveloya.com | Administrador | admin123 |
| cliente@mueveloya.com | Cliente | cliente123 |

## Tabla de Endpoints

| Método | Ruta | Permiso | Descripción |
| :--- | :--- | :--- | :--- |
| POST | /auth/registro | Público | Registro de nuevos usuarios |
| POST | /auth/login | Público | Autenticación y emisión de token |
| GET | /servicios | Público | Listado general de servicios |
| POST | /servicios | Admin | Creación de nuevo servicio |
| GET | /servicios/{id}/objetos | Autenticado | Consulta relacionada (JOIN) |
| DELETE | /transportistas/{id} | Admin | Eliminación de transportistas |

## Referencias
FastAPI. (2026). *FastAPI Documentation*. https://fastapi.tiangolo.com/
SQLite. (2026). *SQLite Documentation*. https://www.sqlite.org/docs.html
