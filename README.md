# API de Gestión de MueveloYa

API REST desarrollada con FastAPI para la prestación de servicios de transporte de objetos y mudanzas.

El proyecto permite administrar las entidades principales del negocio mediante operaciones CRUD, consultas relacionales, autenticación JWT y control de permisos por roles.

---

## Objetivo y Alcance

Desarrollar una API que solucione la logística de Obtención y gestión de servicios de transporte de objetos y mudanzas, facilitando la solicitud, asignación y seguimiento de los mismos de forma segura.

---

## Integrantes

- Sebastian Ramirez Castrillon
- Joel Andrés Mendoza Buritica
- Juan Sebastian Ramirez Velez
- Andrés Felipe Vargas Metrio
- Sergio Andrés López Sepúlveda

---

## Tecnologías

- Python
- FastAPI
- SQLite
- PyJWT
- bcrypt / Passlib

---

## Requisitos Previos

Antes de comenzar, asegúrate de contar con lo siguiente instalado en tu sistema:

- **Python:** Versión 3.10 o superior (`python --version` o `python3 --version`).
- **Pip:** Administrador de paquetes de Python (`pip --version`).
- **Git:** Control de versiones para clonar el repositorio (`git --version`).

---

## Instalación y Ejecución

Para ejecutar el proyecto en un entorno local sigue estos pasos:

### 1. Clonar el repositorio

```bash
git clone https://github.com/pipemetrio/Muevelo_Ya_FastAPI.git
cd Muevelo_Ya_FastAPI
```

### 2. Crear y activar un entorno virtual

```Bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Instalar las dependencias

```Bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación

Ejecuta el servidor de desarrollo con Uvicorn:

```Bash
uvicorn main:app --reload
```

Al iniciar la aplicación por primera vez, las tablas y los datos de prueba (sembrado de datos) se crearán de forma automática en la base de datos SQLite.
El servidor estará disponible en: http://127.0.0.1:8000

### 5. Acceder a la documentación interactiva

Abre tu navegador web y visita:

Swagger UI: http://127.0.0.1:8000/docs

---

## Usuarios de Ejemplo

Para las pruebas de autenticación y permisos, utiliza las siguientes credenciales (sembradas por defecto):

| Correo electrónico    | Rol                             | Contraseña       |
| --------------------- | ------------------------------- | ---------------- |
| admin@mueveloya.com   | Administrador (`admin`)         | admin123         |
| cliente@mueveloya.com | Cliente (`cliente`)             | cliente123       |
| driver1@mueveloya.com | Transportista (`transportista`) | transportista123 |

---

## Diagrama Entidad-Relación

## ![Diagrama del Sistema](evidence/Diagrama_MER_FastAPI.drawio.png)

---

## Tabla de Endpoints

| Método     | Ruta                         | Permiso                       | Descripción                                 |
| ---------- | ---------------------------- | ----------------------------- | ------------------------------------------- |
| **POST**   | `/auth/registro`             | Público                       | Registro inicial de usuarios                |
| **POST**   | `/auth/login`                | Público                       | Login y emisión de Token JWT                |
| **GET**    | `/usuarios`                  | Admin                         | Listar todos los usuarios                   |
| **GET**    | `/usuarios/{id}`             | Cliente, Transportista, Admin | Obtener usuario por ID                      |
| **GET**    | `/usuarios/{id}/direcciones` | Cliente, Admin                | Obtener direcciones de un usuario           |
| **POST**   | `/usuarios`                  | Admin                         | Crear usuario directamente                  |
| **PUT**    | `/usuarios/{id}`             | Cliente, Transportista, Admin | Actualizar datos de usuario                 |
| **DELETE** | `/usuarios/{id}`             | Admin                         | Eliminar usuario                            |
| **GET**    | `/transportistas`            | Admin                         | Listar transportistas                       |
| **GET**    | `/transportistas/{id}`       | Transportista, Admin          | Obtener transportista por ID                |
| **POST**   | `/transportistas`            | Admin                         | Registrar transportista                     |
| **PUT**    | `/transportistas/{id}`       | Admin                         | Actualizar transportista                    |
| **DELETE** | `/transportistas/{id}`       | Admin                         | Eliminar transportista                      |
| **GET**    | `/vehiculos`                 | Transportista, Admin          | Listar vehículos                            |
| **GET**    | `/vehiculos/{id}`            | Transportista, Admin          | Obtener vehículo por ID                     |
| **POST**   | `/vehiculos`                 | Admin                         | Registrar vehículo                          |
| **PUT**    | `/vehiculos/{id}`            | Admin                         | Actualizar vehículo                         |
| **DELETE** | `/vehiculos/{id}`            | Admin                         | Eliminar vehículo                           |
| **GET**    | `/direcciones`               | Cliente, Admin                | Listar direcciones                          |
| **GET**    | `/direcciones/{id}`          | Cliente, Admin                | Obtener dirección por ID                    |
| **POST**   | `/direcciones`               | Cliente, Admin                | Crear dirección                             |
| **PUT**    | `/direcciones/{id}`          | Cliente, Admin                | Actualizar dirección                        |
| **DELETE** | `/direcciones/{id}`          | Cliente, Admin                | Eliminar dirección                          |
| **GET**    | `/servicios`                 | Cliente, Transportista, Admin | Listar todos los servicios                  |
| **GET**    | `/servicios/{id}`            | Cliente, Transportista, Admin | Obtener servicio por ID                     |
| **GET**    | `/servicios/{id}/objetos`    | Cliente, Transportista, Admin | Obtener objetos de un servicio              |
| **POST**   | `/servicios`                 | Cliente, Admin                | Solicitar nuevo servicio                    |
| **PUT**    | `/servicios/{id}`            | Cliente, Admin                | Actualizar servicio o estado                |
| **DELETE** | `/servicios/{id}`            | Cliente, Admin                | Eliminar o cancelar servicio                |
| **GET**    | `/objetos-transporte`        | Cliente, Transportista, Admin | Listar todos los objetos de transporte      |
| **GET**    | `/objetos-transporte/{id}`   | Cliente, Transportista, Admin | Obtener objeto por ID                       |
| **POST**   | `/objetos-transporte`        | Cliente, Admin                | Registrar objeto en un servicio             |
| **PUT**    | `/objetos-transporte/{id}`   | Cliente, Admin                | Actualizar datos de un objeto               |
| **DELETE** | `/objetos-transporte/{id}`   | Cliente, Admin                | Eliminar objeto de transporte               |
| **GET**    | `/asignaciones`              | Transportista, Admin          | Listar todas las asignaciones               |
| **GET**    | `/asignaciones/{id}`         | Transportista, Admin          | Obtener asignación por ID                   |
| **POST**   | `/asignaciones`              | Admin                         | Asignar servicio a transportista o vehículo |
| **PUT**    | `/asignaciones/{id}`         | Admin                         | Actualizar asignación logística             |
| **DELETE** | `/asignaciones/{id}`         | Admin                         | Cancelar o eliminar asignación              |
| **GET**    | `/pagos`                     | Cliente, Admin                | Listar pagos                                |
| **GET**    | `/pagos/{id}`                | Cliente, Admin                | Obtener pago por ID                         |
| **POST**   | `/pagos`                     | Cliente, Admin                | Registrar pago de servicio                  |
| **PUT**    | `/pagos/{id}`                | Admin                         | Actualizar estado del pago                  |
| **DELETE** | `/pagos/{id}`                | Admin                         | Anular pago                                 |

---

## Referencias

- FastAPI. (2026). _FastAPI Documentation_. https://fastapi.tiangolo.com/
- SQLite. (2026). _SQLite Documentation_. https://www.sqlite.org/docs.html
