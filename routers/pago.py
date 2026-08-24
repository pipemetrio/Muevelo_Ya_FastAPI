from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import PagoEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/")
def listar_pagos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Pago")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_pago(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Pago WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_pago(
    pago: PagoEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM Servicio WHERE id = ?", (pago.servicio_id,))
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El servicio indicado no existe"
            )

        cursor.execute(
            """
            INSERT INTO Pago (valor, metodo, pagado, fecha_pago, servicio_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                pago.valor,
                pago.metodo,
                pago.pagado,
                pago.fecha_pago,
                pago.servicio_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Pago registrado correctamente", "id": nuevo_id}
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_pago(
    id: int, pago: PagoEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE Pago
            SET valor = ?,
                metodo = ?,
                pagado = ?,
                fecha_pago = ?,
                servicio_id = ?
            WHERE id = ?
            """,
            (
                pago.valor,
                pago.metodo,
                pago.pagado,
                pago.fecha_pago,
                pago.servicio_id,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        conexion.commit()
        return {"mensaje": "Pago actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_pago(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Pago WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        conexion.commit()
        return {"mensaje": "Pago eliminado correctamente"}
    finally:
        conexion.close()
