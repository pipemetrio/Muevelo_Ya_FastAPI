import sqlite3

from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import TransportistaEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/transportistas", tags=["Transportistas"])


@router.get("/")
def listar_transportistas(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Transportista")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_transportista(
    id: int, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Transportista WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_transportista(
    transportista: TransportistaEntrada, admin: dict = Depends(verificar_rol_admin)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO Transportista (nombre, documento, telefono, activo)
            VALUES (?, ?, ?, ?)
            """,
            (
                transportista.nombre,
                transportista.documento,
                transportista.telefono,
                transportista.activo,
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Transportista creado correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_transportista(
    id: int,
    transportista: TransportistaEntrada,
    admin: dict = Depends(verificar_rol_admin),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Transportista
            SET nombre = ?,
                documento = ?,
                telefono = ?,
                activo = ?
            WHERE id = ?
            """,
            (
                transportista.nombre,
                transportista.documento,
                transportista.telefono,
                transportista.activo,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        conexion.commit()
        return {"mensaje": "Transportista actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_transportista(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Transportista WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        conexion.commit()
        return {"mensaje": "Transportista eliminado correctamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el transportista porque tiene servicios asignados en el historial.",
        )
    finally:
        conexion.close()
