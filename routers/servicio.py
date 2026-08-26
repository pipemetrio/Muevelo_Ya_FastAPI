import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from database import database
from schemas.schemas import ServicioEntrada
from security import obtener_usuario_actual

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("/", description="Roles permitidos: cliente, transportista, admin")
def listar_servicios(usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                s.id, s.fecha, s.estado, s.descripcion,
                u.id AS usuario_id, u.nombre AS usuario_nombre, u.telefono AS usuario_telefono, u.correo AS usuario_correo,
                do.id AS orig_id, do.alias AS orig_alias, do.ciudad AS orig_ciudad, do.barrio AS orig_barrio, do.direccion AS orig_direccion,
                dd.id AS dest_id, dd.alias AS dest_alias, dd.ciudad AS dest_ciudad, dd.barrio AS dest_barrio, dd.direccion AS dest_direccion
            FROM Servicio s
            INNER JOIN Usuario u ON s.usuario_id = u.id
            INNER JOIN Direccion do ON s.direccion_origen_id = do.id
            INNER JOIN Direccion dd ON s.direccion_destino_id = dd.id
            """)
        filas = cursor.fetchall()

        resultado = []
        for fila in filas:
            resultado.append(
                {
                    "id": fila["id"],
                    "fecha": fila["fecha"],
                    "estado": fila["estado"],
                    "descripcion": fila["descripcion"],
                    "usuario": {
                        "id": fila["usuario_id"],
                        "nombre": fila["usuario_nombre"],
                        "telefono": fila["usuario_telefono"],
                        "correo": fila["usuario_correo"],
                    },
                    "direccion_origen": {
                        "id": fila["orig_id"],
                        "alias": fila["orig_alias"],
                        "ciudad": fila["orig_ciudad"],
                        "barrio": fila["orig_barrio"],
                        "direccion": fila["orig_direccion"],
                    },
                    "direccion_destino": {
                        "id": fila["dest_id"],
                        "alias": fila["dest_alias"],
                        "ciudad": fila["dest_ciudad"],
                        "barrio": fila["dest_barrio"],
                        "direccion": fila["dest_direccion"],
                    },
                }
            )
        return resultado
    finally:
        conexion.close()


@router.get("/{id}", description="Roles permitidos: cliente, transportista, admin")
def obtener_servicio(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT 
                s.id, s.fecha, s.estado, s.descripcion,
                u.id AS usuario_id, u.nombre AS usuario_nombre, u.telefono AS usuario_telefono, u.correo AS usuario_correo,
                do.id AS orig_id, do.alias AS orig_alias, do.ciudad AS orig_ciudad, do.barrio AS orig_barrio, do.direccion AS orig_direccion,
                dd.id AS dest_id, dd.alias AS dest_alias, dd.ciudad AS dest_ciudad, dd.barrio AS dest_barrio, dd.direccion AS dest_direccion
            FROM Servicio s
            INNER JOIN Usuario u ON s.usuario_id = u.id
            INNER JOIN Direccion do ON s.direccion_origen_id = do.id
            INNER JOIN Direccion dd ON s.direccion_destino_id = dd.id
            WHERE s.id = ?
            """,
            (id,),
        )
        fila = cursor.fetchone()

        if fila is None:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        return {
            "id": fila["id"],
            "fecha": fila["fecha"],
            "estado": fila["estado"],
            "descripcion": fila["descripcion"],
            "usuario": {
                "id": fila["usuario_id"],
                "nombre": fila["usuario_nombre"],
                "telefono": fila["usuario_telefono"],
                "correo": fila["usuario_correo"],
            },
            "direccion_origen": {
                "id": fila["orig_id"],
                "alias": fila["orig_alias"],
                "ciudad": fila["orig_ciudad"],
                "barrio": fila["orig_barrio"],
                "direccion": fila["orig_direccion"],
            },
            "direccion_destino": {
                "id": fila["dest_id"],
                "alias": fila["dest_alias"],
                "ciudad": fila["dest_ciudad"],
                "barrio": fila["dest_barrio"],
                "direccion": fila["dest_direccion"],
            },
        }
    finally:
        conexion.close()


@router.get(
    "/{id}/objetos", description="Roles permitidos: cliente, transportista, admin"
)
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


@router.post("/", status_code=201, description="Roles permitidos: cliente, admin")
def crear_servicio(
    servicio: ServicioEntrada, usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

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
        return {
            "mensaje": "Servicio creado correctamente",
            "id": nuevo_id,
            "creado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.put("/{id}", description="Roles permitidos: cliente, admin")
def actualizar_servicio(
    id: int,
    servicio: ServicioEntrada,
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
            UPDATE Servicio
            SET fecha = ?,
                estado = ?,
                descripcion = ?
            WHERE id = ?
            """,
            (
                servicio.fecha,
                servicio.estado,
                servicio.descripcion,
                id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        conexion.commit()
        return {
            "mensaje": "Servicio actualizado correctamente",
            "modificado_por": usuario_actual["nombre"],
        }
    finally:
        conexion.close()


@router.delete("/{id}", description="Roles permitidos: cliente, admin")
def eliminar_servicio(id: int, usuario_actual: dict = Depends(obtener_usuario_actual)):
    if usuario_actual["rol"] not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=403, detail="No tienes permisos para realizar esta acción"
        )

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Servicio WHERE id = ?", (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        conexion.commit()
        return {
            "mensaje": "Servicio eliminado correctamente",
            "eliminado_por": usuario_actual["nombre"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el servicio porque tiene pagos, asignaciones o paquetes de transporte asociados.",
        )
    finally:
        conexion.close()
