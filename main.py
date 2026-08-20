from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database

from routers.usuario import router as usuario
from routers.transportista import router as transportista
from routers.vehiculo import router as vehiculo
from routers.objeto_transporte import router as objeto_transporte
from routers.asignacion import router as asignacion
from routers.pago import router as pago
from routers.servicio import router as servicio


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.crear_tablas()
    database.sembrar_datos()
    yield


app = FastAPI(title="API MuéveloYa", lifespan=lifespan)
app.include_router(usuario)
app.include_router(transportista)
app.include_router(vehiculo)
app.include_router(objeto_transporte)
app.include_router(asignacion)
app.include_router(pago)
app.include_router(servicio)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API MueveloYa funcionando. Visita /docs"}
