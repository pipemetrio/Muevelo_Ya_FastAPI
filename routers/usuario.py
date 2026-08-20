from fastapi import APIRouter, Depends, HTTPException, status

from database import database
from models.schemas import UsuarioEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
def listar_usuarios(usuario_admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Usuario")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]

@router.get("/{id}/direcciones")
def obtener_usuario_direcciones(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            Usuario.id AS usuario_id,
            Usuario.nombre,
            Usuario.telefono,
            Usuario.correo,
            Usuario.rol,
            Direccion.id AS direccion_id,
            Direccion.alias,
            Direccion.ciudad,
            Direccion.barrio,
            Direccion.direccion
        FROM Usuario
        LEFT JOIN Direccion
        ON Usuario.id = Direccion.usuario_id
        WHERE Usuario.id = ?
        """,
        (id,)
    )

    filas = cursor.fetchall()

    conexion.close()

    if not filas:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario = {
        "id": filas[0]["usuario_id"],
        "nombre": filas[0]["nombre"],
        "telefono": filas[0]["telefono"],
        "correo": filas[0]["correo"],
        "rol": filas[0]["rol"],
        "direcciones": []
    }

    for fila in filas:
        if fila["direccion_id"] is not None:
            usuario["direcciones"].append({
                "id": fila["direccion_id"],
                "alias": fila["alias"],
                "ciudad": fila["ciudad"],
                "barrio": fila["barrio"],
                "direccion": fila["direccion"]
            })

    return usuario

@router.get("/{id}")
def obtener_usuario(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id,))

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return dict(fila)


@router.post("/", status_code=201)
def crear_usuario(usuario: UsuarioEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO Usuario
        (nombre, telefono, correo, rol)
        VALUES (?, ?, ?, ?)
        """,
        (usuario.nombre, usuario.telefono, usuario.correo, "cliente"),
    )

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return {"mensaje": "Usuario creado correctamente", "id": nuevo_id}


@router.put("/{id}")
def actualizar_usuario(id: int, usuario: UsuarioEntrada, usuario_admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE Usuario
        SET nombre = ?,
            telefono = ?,
            correo = ?,
            rol = ?
        WHERE id = ?
        """,
        (usuario.nombre, usuario.telefono, usuario.correo, usuario.rol, id),
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete("/{id}")
def eliminar_usuario(id: int, usuario_admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Usuario eliminado correctamente"}