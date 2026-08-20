from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database
from routers.usuario import router as usuario
from routers.transportista import router as transportista
from routers.direccion import router as direccion


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.crear_tablas()
    database.sembrar_datos()
    yield


app = FastAPI(title="API MuéveloYa", lifespan=lifespan)
app.include_router(usuario)
app.include_router(transportista)
app.include_router(direccion)



@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API MueveloYa funcionando. Visita /docs"}

