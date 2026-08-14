from fastapi import APIRouter, HTTPException
from dao.cliente_dao import ClienteDAO
from modelos.cliente import Cliente
from schemas.cliente_schema import ClienteCrear, ClienteActualizar, ClienteRespuesta

router = APIRouter(prefix="/clientes", tags=["Clientes"])
dao = ClienteDAO()


@router.get("/", response_model=list[ClienteRespuesta])
def listar_clientes():
    return [c.to_dict() for c in dao.obtener_todos()]


@router.post("/", response_model=ClienteRespuesta)
def crear_cliente(datos: ClienteCrear):
    c = dao.insertar(Cliente(nombre=datos.nombre))
    return c.to_dict()


@router.put("/{id_cliente}", response_model=ClienteRespuesta)
def actualizar_cliente(id_cliente: int, datos: ClienteActualizar):
    c = dao.actualizar(id_cliente, datos.nombre)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return c.to_dict()


@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    dao.eliminar(id_cliente)
    return {"mensaje": "Cliente eliminado"}
