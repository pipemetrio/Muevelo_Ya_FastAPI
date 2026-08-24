from contextlib import asynccontextmanager
from fastapi import FastAPI
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
    return {"mensaje": "API MuéveloYa funcionando. Visita http://127.0.0.1:8000/docs"}
