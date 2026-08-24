import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import UsuarioEntrada
from security import hash_password, obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
def listar_usuarios(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, telefono, correo, rol FROM Usuario")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_usuario(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                u.id AS usuario_id,
                u.nombre,
                u.telefono,
                u.correo,
                u.rol,
                d.id AS direccion_id,
                d.alias,
                d.ciudad,
                d.barrio,
                d.direccion
            FROM Usuario u
            LEFT JOIN Direccion d ON u.id = d.usuario_id
            WHERE u.id = ?
            """,
            (id,),
        )
        filas = cursor.fetchall()

        if not filas:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario = {
            "id": filas[0]["usuario_id"],
            "nombre": filas[0]["nombre"],
            "telefono": filas[0]["telefono"],
            "correo": filas[0]["correo"],
            "rol": filas[0]["rol"],
            "direcciones": [],
        }

        for fila in filas:
            if fila["direccion_id"] is not None:
                usuario["direcciones"].append(
                    {
                        "id": fila["direccion_id"],
                        "alias": fila["alias"],
                        "ciudad": fila["ciudad"],
                        "barrio": fila["barrio"],
                        "direccion": fila["direccion"],
                    }
                )

        return usuario
    finally:
        conexion.close()


@router.get("/{id}/direcciones")
def obtener_direcciones_usuario(
    id: int, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        # Validar si el usuario existe
        cursor.execute("SELECT id FROM Usuario WHERE id = ?", (id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        cursor.execute("SELECT * FROM Direccion WHERE usuario_id = ?", (id,))
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_usuario(usuario: UsuarioEntrada, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        password_hash = hash_password(usuario.password)

        cursor.execute(
            """
            INSERT INTO Usuario (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.telefono,
                usuario.correo,
                password_hash,
                "cliente",
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Usuario creado correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_usuario(
    id: int,
    usuario: UsuarioEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        password_hash = hash_password(usuario.password)

        cursor.execute(
            """
            UPDATE Usuario
            SET nombre = ?,
                telefono = ?,
                correo = ?,
                password = ?
            WHERE id = ?
            """,
            (
                usuario.nombre,
                usuario.telefono,
                usuario.correo,
                password_hash,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        conexion.commit()
        return {"mensaje": "Usuario actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_usuario(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        conexion.commit()
        return {"mensaje": "Usuario eliminado correctamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el usuario porque tiene direcciones registradas o historial de servicios asociados.",
        )
    finally:
        conexion.close()
