from pydantic import BaseModel


class UsuarioEntrada(BaseModel):
    nombre: str
    telefono: str
    correo: str


class TransportistaEntrada(BaseModel):
    nombre: str
    documento: str
    telefono: str
    activo: bool


class VehiculoEntrada(BaseModel):
    placa: str
    tipo: str
    capacidad_kg: float
    disponible: bool


class DireccionEntrada(BaseModel):
    alias: str
    ciudad: str
    barrio: str
    direccion: str
    cliente_id: int


class ServicioEntrada(BaseModel):
    fecha: str
    estado: str
    descripcion: str
    cliente_id: int
    direccion_origen_id: int
    direccion_destino_id: int


class ObjetoTransporteEntrada(BaseModel):
    nombre: str
    cantidad: int
    peso: float
    fragil: bool
    servicio_id: int


class AsignacionEntrada(BaseModel):
    fecha_asignacion: str
    servicio_id: int
    transportista_id: int
    vehiculo_id: int


class PagoEntrada(BaseModel):
    valor: float
    metodo: str
    pagado: bool
    fecha_pago: str
    servicio_id: int
