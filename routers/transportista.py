from fastapi import APIRouter, HTTPException, status

from database import database
from models.schemas import TransportistaEntrada


router = APIRouter(prefix="/transportistas", tags=["Transportistas"])


@router.get("/")
def listar_transportistas():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Transportista")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_transportista(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM Transportista WHERE id = ?",
        (id,)
    )

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Transportista no encontrado"
        )

    return dict(fila)


@router.post("/", status_code=201)
def crear_transportista(transportista: TransportistaEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO Transportista
        (nombre, documento, telefono, activo)
        VALUES (?, ?, ?, ?)
        """,
        (
            transportista.nombre,
            transportista.documento,
            transportista.telefono,
            transportista.activo
        )
    )

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return {
        "mensaje": "Transportista creado correctamente",
        "id": nuevo_id
    }


@router.put("/{id}")
def actualizar_transportista(
    id: int,
    transportista: TransportistaEntrada
):
    conexion = database.obtener_conexion()
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
            id
        )
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Transportista no encontrado"
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Transportista actualizado correctamente"
    }


@router.delete("/{id}")
def eliminar_transportista(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM Transportista WHERE id = ?",
        (id,)
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Transportista no encontrado"
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Transportista eliminado correctamente"
    }