import sqlite3

from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import ServicioEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("/")
def listar_servicios(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                s.id,
                s.fecha,
                s.estado,
                s.descripcion,
                u.nombre AS cliente,
                d_orig.direccion AS origen,
                d_dest.direccion AS destino
            FROM Servicio s
            JOIN Usuario u ON s.usuario_id = u.id
            JOIN Direccion d_orig ON s.direccion_origen_id = d_orig.id
            JOIN Direccion d_dest ON s.direccion_destino_id = d_dest.id
            """)
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_servicio(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                s.id,
                s.fecha,
                s.estado,
                s.descripcion,
                s.usuario_id,
                s.direccion_origen_id,
                s.direccion_destino_id,
                u.nombre AS cliente,
                d_orig.direccion AS origen,
                d_dest.direccion AS destino
            FROM Servicio s
            JOIN Usuario u ON s.usuario_id = u.id
            JOIN Direccion d_orig ON s.direccion_origen_id = d_orig.id
            JOIN Direccion d_dest ON s.direccion_destino_id = d_dest.id
            WHERE s.id = ?
            """,
            (id,),
        )
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        return dict(fila)
    finally:
        conexion.close()


@router.get("/{id}/objetos")
def obtener_objetos_servicio(
    id: int, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        # Validar si el servicio existe
        cursor.execute("SELECT id FROM Servicio WHERE id = ?", (id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        cursor.execute("SELECT * FROM ObjetoTransporte WHERE servicio_id = ?", (id,))
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_servicio(
    servicio: ServicioEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        # Validar existencia de llaves foráneas
        cursor.execute("SELECT id FROM Usuario WHERE id = ?", (servicio.usuario_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=400, detail="El usuario indicado no existe")

        cursor.execute(
            "SELECT id FROM Direccion WHERE id = ?",
            (servicio.direccion_origen_id,),
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400,
                detail="La dirección de origen indicada no existe",
            )

        cursor.execute(
            "SELECT id FROM Direccion WHERE id = ?",
            (servicio.direccion_destino_id,),
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400,
                detail="La dirección de destino indicada no existe",
            )

        cursor.execute(
            """
            INSERT INTO Servicio (
                fecha,
                estado,
                descripcion,
                usuario_id,
                direccion_origen_id,
                direccion_destino_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                servicio.fecha,
                servicio.estado,
                servicio.descripcion,
                servicio.usuario_id,
                servicio.direccion_origen_id,
                servicio.direccion_destino_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Servicio creado correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_servicio(
    id: int,
    servicio: ServicioEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE Servicio
            SET fecha = ?,
                estado = ?,
                descripcion = ?,
                usuario_id = ?,
                direccion_origen_id = ?,
                direccion_destino_id = ?
            WHERE id = ?
            """,
            (
                servicio.fecha,
                servicio.estado,
                servicio.descripcion,
                servicio.usuario_id,
                servicio.direccion_origen_id,
                servicio.direccion_destino_id,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        conexion.commit()
        return {"mensaje": "Servicio actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_servicio(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Servicio WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        conexion.commit()
        return {"mensaje": "Servicio eliminado correctamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el servicio porque tiene pagos, asignaciones o paquetes de transporte asociados.",
        )
    finally:
        conexion.close()
