import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import DireccionEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/direcciones", tags=["Direcciones"])


@router.get("/", description="Roles permitidos: cliente, admin")
def listar_direcciones(usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para acceder a esta información"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                d.id,
                d.alias,
                d.ciudad,
                d.barrio,
                d.direccion,
                d.usuario_id,
                u.nombre AS usuario_nombre,
                u.telefono AS usuario_telefono,
                u.correo AS usuario_correo
            FROM Direccion d
            INNER JOIN Usuario u ON d.usuario_id = u.id
            """)
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            resultado.append(
                {
                    "id": fila["id"],
                    "alias": fila["alias"],
                    "ciudad": fila["ciudad"],
                    "barrio": fila["barrio"],
                    "direccion": fila["direccion"],
                    "usuario_id": fila["usuario_id"],
                    "usuario": {
                        "nombre": fila["usuario_nombre"],
                        "telefono": fila["usuario_telefono"],
                        "correo": fila["usuario_correo"],
                    },
                }
            )
        return resultado
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: cliente, admin")
def obtener_direccion(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para acceder a esta información"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                d.id,
                d.alias,
                d.ciudad,
                d.barrio,
                d.direccion,
                d.usuario_id,
                u.nombre AS usuario_nombre,
                u.telefono AS usuario_telefono,
                u.correo AS usuario_correo
            FROM Direccion d
            INNER JOIN Usuario u ON d.usuario_id = u.id
            WHERE d.id = ?
            """,
            (id,),
        )
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Dirección no encontrada",
            )

        return {
            "id": fila["id"],
            "alias": fila["alias"],
            "ciudad": fila["ciudad"],
            "barrio": fila["barrio"],
            "direccion": fila["direccion"],
            "usuario_id": fila["usuario_id"],
            "usuario": {
                "nombre": fila["usuario_nombre"],
                "telefono": fila["usuario_telefono"],
                "correo": fila["usuario_correo"],
            },
        }
    finally:
        conexion.close()


@router.post("/", status_code=201, description="Roles permitidos: cliente, admin")
def crear_direccion(
    direccion: DireccionEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        # Verificar existencia del usuario
        cursor.execute("SELECT id FROM Usuario WHERE id = ?", (direccion.usuario_id,))
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400,
                detail="El usuario indicado no existe",
            )

        cursor.execute(
            """
            INSERT INTO Direccion (alias, ciudad, barrio, direccion, usuario_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                direccion.alias,
                direccion.ciudad,
                direccion.barrio,
                direccion.direccion,
                direccion.usuario_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid

        return {
            "mensaje": "Dirección creada correctamente",
            "id": nuevo_id,
            "creado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: cliente, admin")
def actualizar_direccion(
    id: int,
    direccion: DireccionEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE Direccion
            SET alias = ?,
                ciudad = ?,
                barrio = ?,
                direccion = ?
            WHERE id = ?
            """,
            (
                direccion.alias,
                direccion.ciudad,
                direccion.barrio,
                direccion.direccion,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Dirección no encontrada",
            )

        conexion.commit()
        return {
            "mensaje": "Dirección actualizada correctamente",
            "modificado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: cliente, admin")
def eliminar_direccion(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Direccion WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Dirección no encontrada",
            )

        conexion.commit()
        return {
            "mensaje": "Dirección eliminada correctamente",
            "eliminado_por": usuario_actual["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la dirección porque está vinculada como origen o destino en uno o más servicios.",
        )
    finally:
        conexion.close()
