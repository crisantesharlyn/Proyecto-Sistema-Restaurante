from pydantic import BaseModel
from typing import Optional


class PlatoCrear(BaseModel):
    nombre: str
    precio: float
    emoji: Optional[str] = None


class PlatoActualizar(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    emoji: Optional[str] = None


class PlatoRespuesta(BaseModel):
    id: int
    nombre: str
    precio: float
    emoji: Optional[str] = None
