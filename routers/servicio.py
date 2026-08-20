from fastapi import APIRouter, HTTPException, status
from database import database
from models.schemas import ServicioEntrada

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("/")
def listar_servicios():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Servicio")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_servicio(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Servicio WHERE id = ?", (id,))
    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    return dict(fila)


@router.post("/", status_code=201)
def crear_servicio(servicio: ServicioEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar llave foranea
    cursor.execute("SELECT id FROM Usuario WHERE id = ?", (servicio.cliente_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El usuario/cliente especificado no existe"
        )

    cursor.execute(
        "SELECT id FROM Direccion WHERE id = ?", (servicio.direccion_origen_id,)
    )
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="La dirección de origen no existe")

    cursor.execute(
        "SELECT id FROM Direccion WHERE id = ?", (servicio.direccion_destino_id,)
    )
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="La dirección de destino no existe")

    cursor.execute(
        """
        INSERT INTO Servicio (fecha, estado, descripcion, cliente_id, direccion_origen_id, direccion_destino_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            servicio.fecha,
            servicio.estado,
            servicio.descripcion,
            servicio.cliente_id,
            servicio.direccion_origen_id,
            servicio.direccion_destino_id,
        ),
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return {"mensaje": "Servicio creado correctamente", "id": nuevo_id}


@router.put("/{id}")
def actualizar_servicio(id: int, servicio: ServicioEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE Servicio
        SET fecha = ?,
            estado = ?,
            descripcion = ?,
            cliente_id = ?,
            direccion_origen_id = ?,
            direccion_destino_id = ?
        WHERE id = ?
        """,
        (
            servicio.fecha,
            servicio.estado,
            servicio.descripcion,
            servicio.cliente_id,
            servicio.direccion_origen_id,
            servicio.direccion_destino_id,
            id,
        ),
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Servicio actualizado correctamente"}


@router.delete("/{id}")
def eliminar_servicio(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar registros con dependencias antes de eliminar
    cursor.execute("SELECT id FROM ObjetoTransporte WHERE servicio_id = ?", (id,))
    if cursor.fetchone() is not None:
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el servicio porque tiene objetos de transporte asociados",
        )

    cursor.execute("DELETE FROM Servicio WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Servicio eliminado correctamente"}
