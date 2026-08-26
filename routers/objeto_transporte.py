from database import database
from fastapi import APIRouter, HTTPException, Depends
from schemas.schemas import ObjetoTransporteEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/objetos-transporte", tags=["Objetos de Transporte"])


@router.get("/", description="Roles permitidos: cliente, transportista, admin")
def listar_objetos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ObjetoTransporte")
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            dict_fila = dict(fila)
            dict_fila["fragil"] = bool(dict_fila["fragil"])
            resultado.append(dict_fila)

        return resultado
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: cliente, transportista, admin")
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

        dict_fila = dict(fila)
        dict_fila["fragil"] = bool(dict_fila["fragil"])
        return dict_fila
    finally:
        conexion.close()


@router.post("/", status_code=201, description="Roles permitidos: cliente, admin")
def crear_objeto(
    objeto: ObjetoTransporteEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

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
                int(objeto.fragil),
                objeto.servicio_id,
            ),
        )

        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Objeto de transporte creado correctamente",
            "id": nuevo_id,
            "creado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: cliente, admin")
def actualizar_objeto(
    id: int,
    objeto: ObjetoTransporteEntrada,
    usuario_actual: dict = Depends(obtener_usuario_actual),
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE ObjetoTransporte
            SET nombre = ?,
                cantidad = ?,
                peso = ?,
                fragil = ?
            WHERE id = ?
            """,
            (
                objeto.nombre,
                objeto.cantidad,
                objeto.peso,
                int(objeto.fragil),
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Objeto de transporte no encontrado"
            )

        conexion.commit()
        return {
            "mensaje": "Objeto de transporte actualizado correctamente",
            "modificado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: cliente, admin")
def eliminar_objeto(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ObjetoTransporte WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Objeto de transporte no encontrado"
            )

        conexion.commit()
        return {
            "mensaje": "Objeto de transporte eliminado correctamente",
            "eliminado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()
