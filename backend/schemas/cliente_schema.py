from pydantic import BaseModel
from typing import Optional


class ClienteCrear(BaseModel):
    nombre: str


class ClienteActualizar(BaseModel):
    nombre: Optional[str] = None


class ClienteRespuesta(BaseModel):
    id: int
    nombre: str
