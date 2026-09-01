from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import PagoEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/", description="Roles permitidos: cliente, admin")
def listar_pagos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Pago")
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            dict_fila = dict(fila)
            dict_fila["pagado"] = bool(dict_fila["pagado"])
            resultado.append(dict_fila)

        return resultado
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: cliente, admin")
def obtener_pago(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Pago WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        dict_fila = dict(fila)
        dict_fila["pagado"] = bool(dict_fila["pagado"])
        return dict_fila
    finally:
        conexion.close()


@router.post("/", status_code=201, description="Roles permitidos: cliente, admin")
def crear_pago(
    pago: PagoEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

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
                int(pago.pagado),
                pago.fecha_pago,
                pago.servicio_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Pago registrado correctamente",
            "id": nuevo_id,
            "creado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: admin")
def actualizar_pago(
    id: int,
    pago: PagoEntrada,
    admin: dict = Depends(verificar_rol_admin),
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
                fecha_pago = ?
            WHERE id = ?
            """,
            (
                pago.valor,
                pago.metodo,
                int(pago.pagado),
                pago.fecha_pago,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        conexion.commit()
        return {
            "mensaje": "Pago actualizado correctamente",
            "modificado_por": admin["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: admin")
def eliminar_pago(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Pago WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        conexion.commit()
        return {
            "mensaje": "Pago eliminado correctamente",
            "eliminado_por": admin["nombre"],
        }
    finally:
        conexion.close()
