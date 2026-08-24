from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import ObjetoTransporteEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/objetos-transporte", tags=["Objetos de Transporte"])


@router.get("/")
def listar_objetos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ObjetoTransporte")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}")
def obtener_objeto(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ObjetoTransporte WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(
                status_code=404, detail="Objeto de transporte no encontrado"
            )

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201)
def crear_objeto(
    objeto: ObjetoTransporteEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM Servicio WHERE id = ?", (objeto.servicio_id,))
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El servicio indicado no existe"
            )

        cursor.execute(
            """
            INSERT INTO ObjetoTransporte (nombre, cantidad, peso, fragil, servicio_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                objeto.nombre,
                objeto.cantidad,
                objeto.peso,
                objeto.fragil,
                objeto.servicio_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Objeto de transporte creado correctamente",
            "id": nuevo_id,
        }
    finally:
        conexion.close()


@router.put("/{id}")
def actualizar_objeto(
    id: int,
    objeto: ObjetoTransporteEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE ObjetoTransporte
            SET nombre = ?,
                cantidad = ?,
                peso = ?,
                fragil = ?,
                servicio_id = ?
            WHERE id = ?
            """,
            (
                objeto.nombre,
                objeto.cantidad,
                objeto.peso,
                objeto.fragil,
                objeto.servicio_id,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Objeto de transporte no encontrado"
            )

        conexion.commit()
        return {"mensaje": "Objeto de transporte actualizado correctamente"}
    finally:
        conexion.close()


@router.delete("/{id}")
def eliminar_objeto(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ObjetoTransporte WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Objeto de transporte no encontrado"
            )

        conexion.commit()
        return {"mensaje": "Objeto de transporte eliminado correctamente"}
    finally:
        conexion.close()
