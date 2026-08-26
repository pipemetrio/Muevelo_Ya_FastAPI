import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import VehiculoEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.get("/", description="Roles permitidos: transportista, admin")
def listar_vehiculos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["transportista", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para acceder a esta información"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Vehiculo")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: transportista, admin")
def obtener_vehiculo(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["transportista", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para acceder a esta información"
        )

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


@router.post("/", status_code=201, description="Roles permitidos: admin")
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
                int(vehiculo.disponible),
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Vehículo creado correctamente",
            "id": nuevo_id,
            "creado_por": admin["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="La placa ingresada ya se encuentra registrada.",
        )
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: admin")
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
                int(vehiculo.disponible),
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        conexion.commit()
        return {
            "mensaje": "Vehículo actualizado correctamente",
            "modificado_por": admin["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: admin")
def eliminar_vehiculo(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Vehiculo WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        conexion.commit()
        return {
            "mensaje": "Vehículo eliminado correctamente",
            "eliminado_por": admin["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el vehículo porque tiene asignaciones logísticas registradas.",
        )
    finally:
        conexion.close()
