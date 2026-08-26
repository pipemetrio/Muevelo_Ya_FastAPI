from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import AsignacionEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


@router.get("/", description="Roles permitidos: transportista, admin")
def listar_asignaciones(usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["transportista", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Asignacion")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: transportista, admin")
def obtener_asignacion(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["transportista", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Asignacion WHERE id = ?", (id,))
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")

        return dict(fila)
    finally:
        conexion.close()


@router.post("/", status_code=201, description="Roles permitidos: admin")
def crear_asignacion(
    asignacion: AsignacionEntrada,
    admin: dict = Depends(verificar_rol_admin),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM Servicio WHERE id = ?", (asignacion.servicio_id,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El servicio indicado no existe"
            )

        cursor.execute(
            "SELECT id FROM Transportista WHERE id = ?",
            (asignacion.transportista_id,),
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El transportista indicado no existe"
            )

        cursor.execute(
            "SELECT id FROM Vehiculo WHERE id = ?", (asignacion.vehiculo_id,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El vehículo indicado no existe"
            )

        cursor.execute(
            """
            INSERT INTO Asignacion (
                fecha_asignacion,
                servicio_id,
                transportista_id,
                vehiculo_id
            )
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
        return {
            "mensaje": "Asignación creada correctamente",
            "id": nuevo_id,
            "creado_por": admin["nombre"],
        }
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: admin")
def actualizar_asignacion(
    id: int,
    asignacion: AsignacionEntrada,
    admin: dict = Depends(verificar_rol_admin),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM Transportista WHERE id = ?",
            (asignacion.transportista_id,),
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El transportista indicado no existe"
            )

        cursor.execute(
            "SELECT id FROM Vehiculo WHERE id = ?", (asignacion.vehiculo_id,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400, detail="El vehículo indicado no existe"
            )

        cursor.execute(
            """
            UPDATE Asignacion
            SET fecha_asignacion = ?,
                transportista_id = ?,
                vehiculo_id = ?
            WHERE id = ?
            """,
            (
                asignacion.fecha_asignacion,
                asignacion.transportista_id,
                asignacion.vehiculo_id,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")

        conexion.commit()
        return {
            "mensaje": "Asignación actualizada correctamente",
            "modificado_por": admin["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: admin")
def eliminar_asignacion(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Asignacion WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")

        conexion.commit()
        return {
            "mensaje": "Asignación eliminada correctamente",
            "eliminado_por": admin["nombre"],
        }
    finally:
        conexion.close()
