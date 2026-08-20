from fastapi import APIRouter, HTTPException

from database import database
from models.schemas import DireccionEntrada


router = APIRouter(prefix="/direcciones", tags=["Direcciones"])


@router.get("/")
def listar_direcciones():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Direccion")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_direccion(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM Direccion WHERE id = ?",
        (id,)
    )

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Direccion no encontrada"
        )

    return dict(fila)


@router.post("/", status_code=201)
def crear_direccion(direccion: DireccionEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Verificar que el usuario exista
    cursor.execute(
        "SELECT * FROM Usuario WHERE id = ?",
        (direccion.usuario_id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="El usuario indicado no existe"
        )

    # Crear direccion
    cursor.execute(
        """
        INSERT INTO Direccion
        (alias, ciudad, barrio, direccion, usuario_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            direccion.alias,
            direccion.ciudad,
            direccion.barrio,
            direccion.direccion,
            direccion.usuario_id
        )
    )

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return {
        "mensaje": "Direccion creada correctamente",
        "id": nuevo_id
    }


@router.put("/{id}")
def actualizar_direccion(id: int, direccion: DireccionEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Verificar que el usuario exista
    cursor.execute(
        "SELECT * FROM Usuario WHERE id = ?",
        (direccion.usuario_id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail="El usuario indicado no existe"
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
            id
        )
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Direccion no encontrada"
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Direccion actualizada correctamente"
    }


@router.delete("/{id}")
def eliminar_direccion(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM Direccion WHERE id = ?",
        (id,)
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Direccion no encontrada"
        )

    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Direccion eliminada correctamente"
    }