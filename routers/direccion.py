import sqlite3

from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import DireccionEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/direcciones", tags=["Direcciones"])


@router.get("/")
def listar_direcciones(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Direccion")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_direccion(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Direccion WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Dirección no encontrada",
            )

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_direccion(
    direccion: DireccionEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
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

        return {"mensaje": "Dirección creada correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_direccion(
    id: int,
    direccion: DireccionEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
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
            UPDATE Direccion
            SET alias = ?,
                ciudad = ?,
                barrio = ?,
                direccion = ?,
                usuario_id = ?
            WHERE id = ?
            """,
            (
                direccion.alias,
                direccion.ciudad,
                direccion.barrio,
                direccion.direccion,
                direccion.usuario_id,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Dirección no encontrada",
            )

        conexion.commit()
        return {"mensaje": "Dirección actualizada correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_direccion(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
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
        return {"mensaje": "Dirección eliminada correctamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la dirección porque está vinculada como origen o destino en uno o más servicios.",
        )
    finally:
        conexion.close()
