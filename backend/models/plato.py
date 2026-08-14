class Plato:
    def __init__(self, id=None, nombre="", precio=0.0, emoji=""):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.emoji = emoji

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": float(self.precio),
            "emoji": self.emoji,
        }
