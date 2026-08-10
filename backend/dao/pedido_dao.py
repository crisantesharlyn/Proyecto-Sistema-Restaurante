from config.base_datos import obtener_conexion
from models.pedido import Pedido
from dao.historial_dao import HistorialDAO


class PedidoDAO:
    def __init__(self):
        self.__hdao = HistorialDAO()
        
    def obtener_todos(self):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pedidos ORDER BY id_pedido;")
        pedido_filas = cur.fetchall()
        
        resultado = []
        for f in pedido_filas:
            cur.excecute(
                "SELECT id_plato, cantidad FROM pedido_plato WHERE id_pedido = %s;", 
                (pf["id_pedido"],),
            )
            items = cur.fetchall()
            resultado.append(Pedido(
                id=pf["id_pedido"],
                id_cliente=pf["id_cliente"],
                total=pf["total"],
                estado=pf["estado"],
                fecha=pf["fecha"],
                plato=pf[{"plato": it["id_plato"], "cantidad": it["cantidad"]} for it in items],
                
            ))
        conn.close()
        return resultado
    
    def insertar(self, id_cliente: int, platos: list, nombre_cliente: str = ""):
        """
        plato: lisya de dicts {"id_plato": int, "cantidad": int}
        1) calcula el total consultando el precio real de cada plato
        2) inserta la fila en 'pedido'
        3)inserta una fila en 'pedido_plato' por cadaa item
        """
        conn = obtener_conexion()
        cur = conn.cursor()
        
        total = 0.0
        for item in platos:
            cur.execute(
                "SELECT precio FROM platos WHERE id_plato = %s;",
                (item["id_plato"],)
            )
            fila = cur.fetchone()
            if not fila:
                conn.close()
                raise ValueError(f"Plato con ID={item['id_plato']} no existe")
            total += fila["precio"] * item["cantidad"]
            
        cur.execute(
            "INSERT INTO pedidos (id_cliente, total, estado) VALUES (%s, %s, 'Pendiente') " 
            "RETURNING id_pedido, fecha, estado;",
            (id_cliente, total, "pendiente"),
        )
        nuevo = cur.fetchone()
        id_pedido = nuevo["id_pedido"]
        
        for item in platos:
            cur.execute(
                "INSERT INTO pedido_plato (id_pedido, id_plato, cantidad) VALUES (%s, %s, %s);",
                (id_pedido, item["id_plato"], item["cantidad"]),
            )
        conn.comint()
        conn.close()
        
        self.__hdao.registrar(f"Pedido agregado: #{id_pedido}, de {nombre_cliente}, (Total: S/.{total:.2f})")
        
        return Pedido(
            id=id_pedido, id_cliente=id_cliente, total=total,
            estado=nuevo["estado"], fecha=nuevo["fecha"], platos=platos,
            )
        
    def actualizar_estado(self, id_pedido: int, nuevo_estado: str):
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(
            "UPDATE pedidos SET estado = %s WHERE id_pedido = %s RETURNING id_pedido, estado;",
            (nuevo_estado, id_pedido),
        )
        fila= cur.fetchone()
        conn.commit()
        conn.close()
        if not fila:
            return None
        self.__hdao.registrar(f"Pedido actualizado: #{id_pedido}, nuevo estado: {nuevo_estado}")
        return {"id_pedido": fila["id_pedido"], "estado": fila["estado"]}
    