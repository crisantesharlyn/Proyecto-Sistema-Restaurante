class Pedido:
    """
    platos: lista de dicts {"id_plato": int, "cantidad": int}
    Representa la tabla intermedia pedido_plato en memoria.
    """
    def __init__(self, id=None, id_cliente=None, total=0.0,
                 estado="Pendiente", fecha=None, platos=None):
        self.id = id
        self.id_cliente = id_cliente
        self.total = total
        self.estado = estado
        self.fecha = fecha
        self.platos = platos or []

    def to_dict(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "total": float(self.total),
            "estado": self.estado,
            "fecha": str(self.fecha) if self.fecha else None,
            "platos": self.platos,
        }
