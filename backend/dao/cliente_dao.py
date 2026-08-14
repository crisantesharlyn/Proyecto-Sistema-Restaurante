from config.base_datos import obtener_conexion
from models.cliente import Cliente
from dao.historial_dao import HistorialDAO
import psycopg2

class ClienteDAO:
    def __init__(self):
        self.__hdao = HistorialDAO()

    def obtener_todos(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cliente ORDER BY id_cliente;")
        filas = cur.fetchall()
        conn.close()
        return [Cliente(id=f["id_cliente"], nombre=f["nombre"]) for f in filas]

    def obtener_por_id(self, id_cliente: int):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cliente WHERE id_cliente = %s;", (id_cliente,))
        f = cur.fetchone()
        conn.close()
        return Cliente(id=f["id_cliente"], nombre=f["nombre"]) if f else None

    def insertar(self, cliente: Cliente):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cliente (nombre) VALUES (%s) RETURNING id_cliente;",
            (cliente.nombre,),
        )
        cliente.id = cur.fetchone()["id_cliente"]
        conn.commit()
        conn.close()
        self.__hdao.registrar(f"Cliente agregado: {cliente.nombre} (ID={cliente.id})")
        return cliente

    def actualizar(self, id_cliente: int, nombre: str = None):
        actual = self.obtener_por_id(id_cliente)
        if not actual:
            return None
        nuevo_nombre = nombre if nombre is not None else actual.nombre

        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cliente SET nombre = %s WHERE id_cliente = %s RETURNING id_cliente, nombre;",
            (nuevo_nombre, id_cliente),
        )
        f = cur.fetchone()
        conn.commit()
        conn.close()
        self.__hdao.registrar(f"Cliente actualizado: {nuevo_nombre} (ID={id_cliente})")
        return Cliente(id=f["id_cliente"], nombre=f["nombre"])

    def eliminar(self, id_cliente: int):
        actual = self.obtener_por_id(id_cliente)
        nombre = actual.nombre if actual else f"ID={id_cliente}"
        conn = obtener_conexion()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM cliente WHERE id_cliente = %s;", (id_cliente,))
            conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise ValueError(f"No se puede eliminar '{nombre}': tiene pedidos asociados.")
        finally:
            conn.close()
        self.__hdao.registrar(f"Cliente eliminado: {nombre} (ID={id_cliente})")
