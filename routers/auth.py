import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import database
from schemas.schemas import UsuarioEntrada
from security import crear_token, hash_password, verificar_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", status_code=201)
def registrar_usuario(usuario: UsuarioEntrada):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        encriptar_password = hash_password(usuario.password)

        cursor.execute(
            """
            INSERT INTO Usuario (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.telefono,
                usuario.correo,
                encriptar_password,
                "cliente",
            ),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya se encuentra registrado.",
        )
    finally:
        conexion.close()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE correo = ?", (form_data.username,))
        usuario = cursor.fetchone()
    finally:
        conexion.close()

    if not usuario or not verificar_password(form_data.password, usuario["password"]):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = crear_token(data={"sub": usuario["correo"], "rol": usuario["rol"]})
    return {"access_token": access_token, "token_type": "bearer"}
