from fastapi import APIRouter, HTTPException, status
from database import database
from models.schemas import ObjetoTransporteEntrada

router = APIRouter(prefix="/objetos-transporte", tags=["Objetos de Transporte"])


@router.get("/")
def listar_objetos():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM ObjetoTransporte")
    filas = cursor.fetchall()

    conexion.close()

    return [dict(fila) for fila in filas]


@router.get("/{id}")
def obtener_objeto(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM ObjetoTransporte WHERE id = ?", (id,))
    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404, detail="Objeto de transporte no encontrado"
        )

    return dict(fila)


@router.post("/", status_code=201)
def crear_objeto(objeto: ObjetoTransporteEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar llave foranea
    cursor.execute("SELECT id FROM Servicio WHERE id = ?", (objeto.servicio_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El servicio especificado no existe"
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
    conexion.close()

    return {"mensaje": "Objeto agregado al servicio correctamente", "id": nuevo_id}


@router.put("/{id}")
def actualizar_objeto(id: int, objeto: ObjetoTransporteEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    # Validar llave foranea
    cursor.execute("SELECT id FROM Servicio WHERE id = ?", (objeto.servicio_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="El servicio especificado no existe"
        )

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
        conexion.close()
        raise HTTPException(
            status_code=404, detail="Objeto de transporte no encontrado"
        )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Objeto de transporte actualizado correctamente"}


@router.delete("/{id}")
def eliminar_objeto(id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM ObjetoTransporte WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(
            status_code=404, detail="Objeto de transporte no encontrado"
        )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Objeto de transporte eliminado correctamente"}
