class Historial:
    def __init__(self, id=None, fecha="", hora="", accion=""):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.accion = accion

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "hora": self.hora,
            "accion": self.accion,
        }
