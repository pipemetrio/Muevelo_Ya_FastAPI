import sqlite3

from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import VehiculoEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.get("/")
def listar_vehiculos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Vehiculo")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_vehiculo(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Vehiculo WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_vehiculo(
    vehiculo: VehiculoEntrada, admin: dict = Depends(verificar_rol_admin)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO Vehiculo (placa, tipo, capacidad_kg, disponible)
            VALUES (?, ?, ?, ?)
            """,
            (
                vehiculo.placa,
                vehiculo.tipo,
                vehiculo.capacidad_kg,
                vehiculo.disponible,
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Vehículo creado correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_vehiculo(
    id: int, vehiculo: VehiculoEntrada, admin: dict = Depends(verificar_rol_admin)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Vehiculo
            SET placa = ?,
                tipo = ?,
                capacidad_kg = ?,
                disponible = ?
            WHERE id = ?
            """,
            (
                vehiculo.placa,
                vehiculo.tipo,
                vehiculo.capacidad_kg,
                vehiculo.disponible,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        conexion.commit()
        return {"mensaje": "Vehículo actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_vehiculo(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Vehiculo WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        conexion.commit()
        return {"mensaje": "Vehículo eliminado correctamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el vehículo porque tiene asignaciones logísticas registradas.",
        )
    finally:
        conexion.close()
