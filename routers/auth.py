from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import sqlite3
from database import database
from models.schemas import UsuarioRegistroEntrada
from security import obtener_password_hash, verificar_password, crear_token_acceso

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", status_code=201)
def registrar_usuario(usuario: UsuarioRegistroEntrada):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    password_hash = obtener_password_hash(usuario.password)

    try:
        cursor.execute(
            """
            INSERT INTO Usuario (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nombre, usuario.telefono, usuario.correo, password_hash, "cliente")
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )
    finally:
        conexion.close()

    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE correo = ?", (form_data.username,))
    usuario = cursor.fetchone()
    conexion.close()

    if not usuario or not verificar_password(form_data.password, usuario["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = crear_token_acceso(data={"sub": usuario["correo"], "rol": usuario["rol"]})
    return {"access_token": access_token, "token_type": "bearer"}