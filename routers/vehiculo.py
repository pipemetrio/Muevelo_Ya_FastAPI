from fastapi import APIRouter, HTTPException, status
from database import database
from models.schemas import VehiculoEntrada

router = APIRouter(prefix="/vehiculos", tags=["Vehiculos"])


@router.get("/")
def listar_vehiculos():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Vehiculo")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_vehiculo(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Vehiculo WHERE id = ?", (id,))
    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return dict(fila)


@router.post("/", status_code=201)
def crear_vehiculo(vehiculo: VehiculoEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO Vehiculo (placa, tipo, capacidad_kg, disponible)
        VALUES (?, ?, ?, ?)
        """,
        (vehiculo.placa, vehiculo.tipo, vehiculo.capacidad_kg, vehiculo.disponible),
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return {"mensaje": "Vehículo creado correctamente", "id": nuevo_id}


@router.put("/{id}")
def actualizar_vehiculo(id: int, vehiculo: VehiculoEntrada):
    conexion = database.obtener_conexion()
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
        (vehiculo.placa, vehiculo.tipo, vehiculo.capacidad_kg, vehiculo.disponible, id),
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Vehículo actualizado correctamente"}


@router.delete("/{id}")
def eliminar_vehiculo(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Vehiculo WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Vehículo eliminado correctamente"}
