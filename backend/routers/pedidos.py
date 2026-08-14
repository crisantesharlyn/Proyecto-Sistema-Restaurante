from fastapi import APIRouter, HTTPException
from dao.pedido_dao import PedidoDAO
from dao.cliente_dao import ClienteDAO
from schemas.pedido_schema import PedidoCrear, PedidoEstadoActualizar, PedidoRespuesta

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
dao = PedidoDAO()
cliente_dao = ClienteDAO()


@router.get("/", response_model=list[PedidoRespuesta])
def listar_pedidos():
    return [p.to_dict() for p in dao.obtener_todos()]


@router.post("/", response_model=PedidoRespuesta)
def crear_pedido(datos: PedidoCrear):
    cliente = cliente_dao.obtener_por_id(datos.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    platos_dict = [item.model_dump() for item in datos.platos]
    try:
        p = dao.insertar(datos.id_cliente, platos_dict, nombre_cliente=cliente.nombre)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return p.to_dict()


@router.put("/{id_pedido}/estado")
def actualizar_estado(id_pedido: int, datos: PedidoEstadoActualizar):
    if datos.estado not in ("Pendiente", "En cocina", "Listo"):
        raise HTTPException(status_code=400, detail="Estado inválido")
    resultado = dao.actualizar_estado(id_pedido, datos.estado)
    if not resultado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return resultado
