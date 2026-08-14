from datetime import datetime
from config.base_datos import obtener_conexion
from models.historial import Historial


class HistorialDAO:
    def obtener_todos(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM historial ORDER BY id DESC;")
        filas = cur.fetchall()
        conn.close()
        return [Historial(id=f["id"], fecha=f["fecha"], hora=f["hora"], accion=f["accion"]) for f in filas]

    def insertar(self, h: Historial):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO historial (fecha, hora, accion) VALUES (%s, %s, %s) RETURNING id;",
            (h.fecha, h.hora, h.accion),
        )
        h.id = cur.fetchone()["id"]
        conn.commit()
        conn.close()
        return h

    def registrar(self, accion: str):
        """Método centralizado: cualquier otro DAO llama a esto para dejar
        constancia de una acción, sin tener que armar fecha/hora él mismo."""
        ahora = datetime.now()
        h = Historial(
            fecha=ahora.strftime("%d/%m/%Y"),
            hora=ahora.strftime("%H:%M:%S"),
            accion=accion,
        )
        return self.insertar(h)

    def limpiar(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM historial;")
        conn.commit()
        conn.close()
