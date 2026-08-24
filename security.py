import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
from database import database

# Configuración del JWT
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_muevelo_ya")
ALGORITHM = "HS256"
TIEMPO_EXPIRACION_MINUTOS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- Funciones de Hash para Contraseñas ---
def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


def verificar_password(password_plana: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_plana.encode("utf-8"), password_hash.encode("utf-8"))


# --- Funciones de Token JWT ---
def crear_token(data: dict) -> str:
    datos = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=TIEMPO_EXPIRACION_MINUTOS
    )
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


# --- Middleware de Autenticación y Autorización ---
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    error_autenticacion = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo = payload.get("sub")
        if not isinstance(correo, str) or not correo:
            raise error_autenticacion
    except InvalidTokenError:
        raise error_autenticacion

    conexion = database.obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
    finally:
        conexion.close()

    if usuario is None:
        raise error_autenticacion

    return dict(usuario)


def verificar_rol_admin(usuario: dict = Depends(obtener_usuario_actual)) -> dict:
    if usuario.get("rol") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de administrador",
        )
    return usuario
