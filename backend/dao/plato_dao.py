from config.base_datos import obtener_conexion
from models.plato import Plato
from dao.historial_dao import HistorialDAO


class PlatoDAO:
    def __init__(self):
        self.__hdao = HistorialDAO()
        
    def obtener_todos(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM platos ORDER BY id_plato;")
        filas = cur.fetchall()
        conn.close()
        return [Plato(id=f["id_plato"], nombre=f["nombre"], precio=f["precio"], emoji=f["emoji"]) for f in filas]
    
    def obtener_por_id(self, id_plato: int):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM platos WHERE id_plato = %s;", (id_plato,))
        f = cur.fetchone()
        conn.close()
        return Plato(id=f["id_plato"], nombre=f["nombre"], precio=f["precio"], emoji=f["emoji"]) if f else None
    
    def insertar(self, plato: Plato):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO platos (nombre, precio, emoji) VALUES (%s, %s, %s) RETURNING id_plato;",
            (plato.nombre, plato.precio, plato.emoji)
        )
        plato.id = cur.fetchone()["id_plato"]
        conn.commit()
        conn.close()
        self.__hdao.registrar(f"Plato agregado: {plato.nombre} S/.{plato.precio:.2f} (ID={plato.id})")
        return plato
    
    def actualizar(self, id_plato: int, nombre=None, precio=None, emoji=None):
        actual = self.obtener_por_id(id_plato)
        if not actual:
            return None
        nuevo_nombre = nombre if nombre is not None else actual.nombre
        nuevo_precio = precio if precio is not None else actual.precio
        nuevo_emoji = emoji if emoji is not None else actual.emoji
        
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "UPDATE platos SET nombre = %s, precio = %s, emoji = %s WHERE id_plato = %s "
            "RETURNING id_plato, nombre, precio, emoji;",
            (nuevo_nombre, nuevo_precio, nuevo_emoji, id_plato)
        )
        f = cur.fetchone()
        conn.commit()
        conn.close()
        self.__hdao.registrar(f"Plato actualizado: {nuevo_nombre} (ID={id_plato})")
        return Plato(id=f["id_plato"], nombre=f["nombre"], precio=f["precio"], emoji=f["emoji"])
    
    def eliminar(self, id_plato: int):
        actual = self.obtener_por_id(id_plato)
        nombre = actual.nombre if actual else f"ID={id_plato}"
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM plato WHERE id_plato = %s;", (id_plato,))
        conn.commit()
        conn.close()
        self.__hdao.registrar(f"Plato eliminado: {nombre} (ID={id_plato})")
        