from fastapi import APIRouter, Depends, HTTPException, status
from database import database
from models.schemas import AsignacionEntrada
from security import verificar_rol_admin

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


@router.get("/")
def listar_asignaciones():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Asignacion")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_asignacion(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Asignacion WHERE id = ?", (id,))
    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    return dict(fila)


@router.post("/", status_code=201, dependencies=[Depends(verificar_rol_admin)])
def crear_asignacion(asignacion: AsignacionEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar llave foranea
    cursor.execute("SELECT id FROM Servicio WHERE id = ?", (asignacion.servicio_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El servicio especificado no existe"
        )

    cursor.execute(
        "SELECT id FROM Transportista WHERE id = ?", (asignacion.transportista_id,)
    )
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El transportista especificado no existe"
        )

    cursor.execute("SELECT id FROM Vehiculo WHERE id = ?", (asignacion.vehiculo_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El vehículo especificado no existe"
        )

    cursor.execute(
        """
        INSERT INTO Asignacion (fecha_asignacion, servicio_id, transportista_id, vehiculo_id)
        VALUES (?, ?, ?, ?)
        """,
        (
            asignacion.fecha_asignacion,
            asignacion.servicio_id,
            asignacion.transportista_id,
            asignacion.vehiculo_id,
        ),
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return {"mensaje": "Asignación realizada correctamente", "id": nuevo_id}


@router.put("/{id}", dependencies=[Depends(verificar_rol_admin)])
def actualizar_asignacion(id: int, asignacion: AsignacionEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE Asignacion
        SET fecha_asignacion = ?,
            servicio_id = ?,
            transportista_id = ?,
            vehiculo_id = ?
        WHERE id = ?
        """,
        (
            asignacion.fecha_asignacion,
            asignacion.servicio_id,
            asignacion.transportista_id,
            asignacion.vehiculo_id,
            id,
        ),
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Asignación actualizada correctamente"}


@router.delete("/{id}", dependencies=[Depends(verificar_rol_admin)])
def eliminar_asignacion(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Asignacion WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Asignación eliminada correctamente"}