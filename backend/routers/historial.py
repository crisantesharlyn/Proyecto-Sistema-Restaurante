from fastapi import APIRouter
from dao.historial_dao import HistorialDAO
from schemas.historial_schema import HistorialRespuesta

router = APIRouter(prefix="/historial", tags=["Historial"])
dao = HistorialDAO()


@router.get("/", response_model=list[HistorialRespuesta])
def listar_historial():
    return [h.to_dict() for h in dao.obtener_todos()]


@router.delete("/")
def limpiar_historial():
    dao.limpiar()
    return {"mensaje": "Historial limpiado"}
