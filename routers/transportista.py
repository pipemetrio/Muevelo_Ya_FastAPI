import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import TransportistaEntrada
from security import obtener_usuario_actual, verificar_rol_admin

router = APIRouter(prefix="/transportistas", tags=["Transportistas"])


@router.get("/", description="Roles permitidos: admin")
def listar_transportistas(admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                t.id,
                t.documento,
                t.activo,
                t.usuario_id,
                u.nombre AS usuario_nombre,
                u.telefono AS usuario_telefono,
                u.correo AS usuario_correo
            FROM Transportista t
            INNER JOIN Usuario u ON t.usuario_id = u.id
            """)
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            resultado.append(
                {
                    "id": fila["id"],
                    "documento": fila["documento"],
                    "activo": bool(fila["activo"]),
                    "usuario_id": fila["usuario_id"],
                    "usuario": {
                        "nombre": fila["usuario_nombre"],
                        "telefono": fila["usuario_telefono"],
                        "correo": fila["usuario_correo"],
                    },
                }
            )
        return resultado
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: transportista, admin")
def obtener_transportista(
    id: int, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] not in ["transportista", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para ver esta información"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                t.id,
                t.documento,
                t.activo,
                t.usuario_id,
                u.nombre AS usuario_nombre,
                u.telefono AS usuario_telefono,
                u.correo AS usuario_correo
            FROM Transportista t
            INNER JOIN Usuario u ON t.usuario_id = u.id
            WHERE t.id = ?
            """,
            (id,),
        )
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        return {
            "id": fila["id"],
            "documento": fila["documento"],
            "activo": bool(fila["activo"]),
            "usuario_id": fila["usuario_id"],
            "usuario": {
                "nombre": fila["usuario_nombre"],
                "telefono": fila["usuario_telefono"],
                "correo": fila["usuario_correo"],
            },
        }
    finally:
        conexion.close()


@router.post("/", status_code=201, description="Roles permitidos: admin")
def crear_transportista(
    transportista: TransportistaEntrada, admin: dict = Depends(verificar_rol_admin)
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO Transportista (documento, activo, usuario_id)
            VALUES (?, ?, ?)
            """,
            (
                transportista.documento,
                int(transportista.activo),
                transportista.usuario_id,
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {
            "mensaje": "Transportista creado correctamente",
            "id": nuevo_id,
            "creado_por": admin["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El documento o el usuario_id ya están registrados en otro transportista.",
        )
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: admin")
def actualizar_transportista(
    id: int,
    transportista: TransportistaEntrada,
    admin: dict = Depends(verificar_rol_admin),
):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Transportista
            SET documento = ?,
                activo = ?
            WHERE id = ?
            """,
            (
                transportista.documento,
                int(transportista.activo),
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        conexion.commit()
        return {
            "mensaje": "Transportista actualizado correctamente",
            "modificado_por": admin["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: admin")
def eliminar_transportista(id: int, admin: dict = Depends(verificar_rol_admin)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Transportista WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transportista no encontrado")

        conexion.commit()
        return {
            "mensaje": "Transportista eliminado correctamente",
            "eliminado_por": admin["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el transportista porque tiene servicios asignados en el historial.",
        )
    finally:
        conexion.close()
