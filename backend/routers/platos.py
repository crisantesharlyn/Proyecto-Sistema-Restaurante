from fastapi import APIRouter, HTTPException
from dao.plato_dao import PlatoDAO
from models.plato import Plato
from schemas.plato_schema import PlatoCrear, PlatoActualizar, PlatoRespuesta
   
router = APIRouter(prefix="/platos", tags=["Platos"])
dao = PlatoDAO()


@router.get("/", response_model=list[PlatoRespuesta])
def listar_platos():
    return [p.to_dict() for p in dao.obtener_todos()]


@router.post("/", response_model=PlatoRespuesta)
def crear_plato(datos: PlatoCrear):
    p = dao.insertar(Plato(nombre=datos.nombre, precio=datos.precio, emoji=datos.emoji))
    return p.to_dict()


@router.put("/{id_plato}", response_model=PlatoRespuesta)
def actualizar_plato(id_plato: int, datos: PlatoActualizar):
    p = dao.actualizar(id_plato, nombre=datos.nombre, precio=datos.precio, emoji=datos.emoji)
    if not p:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    return p.to_dict()


@router.delete("/{id_plato}")
def eliminar_plato(id_plato: int):
    try:
        dao.eliminar(id_plato)
    except ValueError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
    return {"mensaje": "Plato eliminado"}
