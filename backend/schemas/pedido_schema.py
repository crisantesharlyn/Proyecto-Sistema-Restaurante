from pydantic import BaseModel
from typing import Optional, List


class PedidoItem(BaseModel):
    id_plato: int
    cantidad: int


class PedidoCrear(BaseModel):
    id_cliente: int
    platos: List[PedidoItem]


class PedidoEstadoActualizar(BaseModel):
    estado: str  # 'Pendiente' | 'En cocina' | 'Listo'


class PedidoRespuesta(BaseModel):
    id: int
    id_cliente: int
    total: float
    estado: str
    fecha: Optional[str] = None
    platos: List[PedidoItem] = []
