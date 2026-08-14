class Cliente:
    def __init__(self, id=None, nombre=""):
        self.id = id
        self.nombre = nombre

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}
