from fastapi import APIRouter, HTTPException, status
from database import database
from models.schemas import PagoEntrada

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/")
def listar_pagos():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Pago")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_pago(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Pago WHERE id = ?", (id,))
    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return dict(fila)


@router.post("/", status_code=201)
def crear_pago(pago: PagoEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar si el servicio existe
    cursor.execute("SELECT id FROM Servicio WHERE id = ?", (pago.servicio_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El servicio especificado no existe"
        )

    cursor.execute(
        """
        INSERT INTO Pago (valor, metodo, pagado, fecha_pago, servicio_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (pago.valor, pago.metodo, pago.pagado, pago.fecha_pago, pago.servicio_id),
    )

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return {"mensaje": "Pago registrado correctamente", "id": nuevo_id}


@router.put("/{id}")
def actualizar_pago(id: int, pago: PagoEntrada):
    conexion = database.obtener_conexion()
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
        (pago.valor, pago.metodo, pago.pagado, pago.fecha_pago, pago.servicio_id, id),
    )

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Pago actualizado correctamente"}


@router.delete("/{id}")
def eliminar_pago(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Pago WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    conexion.commit()
    conexion.close()

    return {"mensaje": "Pago eliminado correctamente"}
