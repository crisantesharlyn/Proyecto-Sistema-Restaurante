import { useState, useEffect } from "react";
import api from "../../api/axios";

const CLASE_ESTADO = {
  Pendiente: "pendiente",
  "En cocina": "en-cocina",
  Listo: "listo",
};

function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [platosDisponibles, setPlatosDisponibles] = useState([]);
  const [idCliente, setIdCliente] = useState("");
  const [itemsPedido, setItemsPedido] = useState([]); // [{id_plato, cantidad}]

  useEffect(() => {
    cargarPedidos();
    api.get("/clientes/").then((res) => setClientes(res.data));
    api.get("/platos/").then((res) => setPlatosDisponibles(res.data));
  }, []);

  function cargarPedidos() {
    api.get("/pedidos/").then((res) => setPedidos(res.data));
  }

  function agregarItem(idPlato) {
    if (itemsPedido.find((i) => i.id_plato === idPlato)) return;
    setItemsPedido([...itemsPedido, { id_plato: idPlato, cantidad: 1 }]);
  }

  function cambiarCantidad(idPlato, delta) {
    setItemsPedido(
      itemsPedido
        .map((i) => (i.id_plato === idPlato ? { ...i, cantidad: i.cantidad + delta } : i))
        .filter((i) => i.cantidad > 0)
    );
  }

  function nombrePlato(id) {
    return platosDisponibles.find((p) => p.id === id)?.nombre || `#${id}`;
  }
  function precioPlato(id) {
    return platosDisponibles.find((p) => p.id === id)?.precio || 0;
  }
  function nombreCliente(id) {
    return clientes.find((c) => c.id === id)?.nombre || `#${id}`;
  }

  const totalActual = itemsPedido.reduce(
    (sum, i) => sum + precioPlato(i.id_plato) * i.cantidad,
    0
  );

  async function guardarPedido() {
    if (!idCliente || itemsPedido.length === 0) return;
    await api.post("/pedidos/", {
      id_cliente: Number(idCliente),
      platos: itemsPedido,
    });
    setItemsPedido([]);
    setIdCliente("");
    cargarPedidos();
  }

  async function cambiarEstado(id, siguiente) {
    await api.put(`/pedidos/${id}/estado`, { estado: siguiente });
    cargarPedidos();
  }

  const ORDEN_ESTADOS = ["Pendiente", "En cocina", "Listo"];
  function siguienteEstado(actual) {
    const idx = ORDEN_ESTADOS.indexOf(actual);
    return ORDEN_ESTADOS[(idx + 1) % ORDEN_ESTADOS.length];
  }

  return (
    <div>
      <div className="section-eyebrow">GESTIÓN DE PEDIDOS · RF06–RF08, RF10</div>
      <div className="section-title-row">
        <h1>Nuevo Pedido</h1>
        <button className="btn btn-accent" onClick={guardarPedido}>
          Guardar pedido
        </button>
      </div>

      <div className="row g-4">
        {/* Columna izquierda: formulario del pedido */}
        <div className="col-md-7">
          <div className="panel-pedido">
            <div className="section-eyebrow">CLIENTE</div>
            <select
              className="form-select mb-4"
              value={idCliente}
              onChange={(e) => setIdCliente(e.target.value)}
            >
              <option value="">-- selecciona --</option>
              {clientes.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.nombre} — id_cliente {String(c.id).padStart(3, "0")}
                </option>
              ))}
            </select>

            <div className="section-eyebrow">PLATOS DEL PEDIDO</div>
            {itemsPedido.map((i) => (
              <div className="line-item" key={i.id_plato}>
                <div className="d-flex align-items-center gap-2">
                  <div className="icono-plato" style={{ width: 28, height: 28 }} />
                  {nombrePlato(i.id_plato)}
                </div>
                <div className="qty-box">
                  <button onClick={() => cambiarCantidad(i.id_plato, -1)}>−</button>
                  {i.cantidad}
                  <button onClick={() => cambiarCantidad(i.id_plato, 1)}>+</button>
                </div>
                <div>S/ {(precioPlato(i.id_plato) * i.cantidad).toFixed(2)}</div>
              </div>
            ))}

            <select
              className="form-select mt-3"
              value=""
              onChange={(e) => e.target.value && agregarItem(Number(e.target.value))}
            >
              <option value="">+ Agregar plato al pedido</option>
              {platosDisponibles
                .filter((p) => !itemsPedido.find((i) => i.id_plato === p.id))
                .map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.emoji} {p.nombre} — S/ {p.precio.toFixed(2)}
                  </option>
                ))}
            </select>

            <div className="total-pedido">
              <span>Total del pedido</span>
              <span className="monto">S/ {totalActual.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Columna derecha: historial de pedidos */}
        <div className="col-md-5">
          <div className="panel-pedido">
            <div className="section-eyebrow">HISTORIAL DE PEDIDOS</div>
            {pedidos
              .slice()
              .reverse()
              .map((pe) => (
                <div className="order-history-item" key={pe.id}>
                  <div className="d-flex justify-content-between align-items-start">
                    <div>
                      <div className="fw-semibold">{nombreCliente(pe.id_cliente)}</div>
                      <div className="id-plato">
                        id_pedido {String(pe.id).padStart(4, "0")} · {pe.fecha?.slice(0, 10)}
                      </div>
                    </div>
                    <div className="text-end">
                      <div className="fw-bold">S/ {pe.total.toFixed(2)}</div>
                      <span
                        className={`status-tag ${CLASE_ESTADO[pe.estado]}`}
                        style={{ cursor: "pointer" }}
                        title="Clic para avanzar el estado"
                        onClick={() => cambiarEstado(pe.id, siguienteEstado(pe.estado))}
                      >
                        {pe.estado}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Pedidos;
