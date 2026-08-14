from pydantic import BaseModel


class HistorialRespuesta(BaseModel):
    id: int
    fecha: str
    hora: str
    accion: str
