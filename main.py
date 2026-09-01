from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import crear_tablas, sembrar_datos
from routers import (
    auth,
    usuario,
    transportista,
    vehiculo,
    direccion,
    servicio,
    objeto_transporte,
    asignacion,
    pago,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    sembrar_datos()
    yield


app = FastAPI(
    title="API MuéveloYa",
    description="API RESTful para la gestión logística de servicios de carga y mudanzas",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Usamos cualquier origen debido ya que MuéveloYa es un proyecto de transporte y puede ser utilizado desde distintos dispositivos o plataformas para gestionar los servicios.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(transportista.router)
app.include_router(vehiculo.router)
app.include_router(direccion.router)
app.include_router(servicio.router)
app.include_router(objeto_transporte.router)
app.include_router(asignacion.router)
app.include_router(pago.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "API MuéveloYa funcionando. Visita https://muevelo-ya-fastapi.onrender.com/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    return {"estado": "ok"}
