from config.base_datos import obtener_conexion
from models.cliente import Cliente
from dao.historial_dao import HistorialDAO


class ClienteDAO:
    def __init__(self):
        self.historial_dao = HistorialDAO()
        
    def obtener_todos(self):
        conn  = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY id_cliente;")
        filas = cursor.fetchall()
        conn.close()
        return [Cliente(id=f["id_cliente"], nombre=f["nombre"]) for f in filas]
    
    def obtener_por_id(self, id_cliente: int):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE id_cliente = %s;", (id_cliente,))
        f = cur.fetchone()
        conn.close()
        return Cliente(id=f["id_cliente"], nombre=f["nombre"]) if f else None
        
    def insertar(self, cliente: Cliente):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clientes (nombre) VALUES (%s) RETURING id_clienttes;",
            (cliente.nombre,)
        )
        cliente.id = cur.fetchone()["id_cliente"]
        conn.commit()
        conn.close()
        self.__hdao.resgistrar(f"Cliente agregado: {cliente.nombre} (ID={cliente.id})") 
        return cliente
    
    def actualizar(self, id_cliente: int, nombre: str):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "UPDATE clientes SET nombre = %s WHERE id_cliente = %s RETURNING id_cliente, nombre;",
            (nombre, id_cliente),
            )
        f  = cur.fetchone()
        conn.commit()
        conn.close()
        if not f:
            return None
        self.__hdao.resgistrar(f"Cliente actualizado: {nombre} (ID={id_cliente})")
        return Cliente(id=f["id_cliente"], nombre=f["nombre"])
    
    def eliminar(self, id_cliente: int):
        actual = self.obtener_por_id(id_cliente)
        nombre = actual.nombre if actual else f"ID={id_cliente}"
        conn = obtener_conexion()
        cur.execute("DELETE FROM clientes WHERE id_cliente = %s;", (id_cliente,))
        conn.commit()
        conn.close()
        self.__hdao.resgistrar(f"Cliente eliminado: {nombre} (ID={id_cliente})")
        