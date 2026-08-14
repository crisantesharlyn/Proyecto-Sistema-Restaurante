import { useState, useEffect } from "react";
import api from "../../api/axios";

function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [nombre, setNombre] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  useEffect(() => {
    cargarClientes();
  }, []);

  function cargarClientes() {
    // pedidos y total consumido se calculan del lado del cliente a partir
    // de /pedidos/, así la tabla replica "Pedidos realizados" y "Total consumido"
    Promise.all([api.get("/clientes/"), api.get("/pedidos/")]).then(
      ([resClientes, resPedidos]) => {
        const pedidos = resPedidos.data;
        const conDatos = resClientes.data.map((c) => {
          const propios = pedidos.filter((p) => p.id_cliente === c.id);
          return {
            ...c,
            pedidosRealizados: propios.length,
            totalConsumido: propios.reduce((sum, p) => sum + p.total, 0),
          };
        });
        setClientes(conDatos);
      }
    );
  }

  function abrirNuevo() {
    setNombre("");
    setEditandoId(null);
    setMostrarForm(true);
  }

  function empezarEdicion(c) {
    setNombre(c.nombre);
    setEditandoId(c.id);
    setMostrarForm(true);
  }

  async function guardarCliente() {
    if (editandoId) {
      await api.put(`/clientes/${editandoId}`, { nombre });
    } else {
      await api.post("/clientes/", { nombre });
    }
    setMostrarForm(false);
    cargarClientes();
  }

  async function eliminarCliente(id) {
    await api.delete(`/clientes/${id}`);
    cargarClientes();
  }

  return (
    <div>
      <div className="section-eyebrow">GESTIÓN DE CLIENTES · RF05, RF09</div>
      <div className="section-title-row">
        <h1>Clientes</h1>
        <button className="btn btn-accent" onClick={abrirNuevo}>
          + Registrar cliente
        </button>
      </div>

      {mostrarForm && (
        <div className="plato-card mb-4" style={{ borderStyle: "solid" }}>
          <h6 className="mb-3">{editandoId ? "Editar cliente" : "Nuevo cliente"}</h6>
          <div className="row g-2">
            <div className="col-md-6">
              <input className="form-control" placeholder="Nombre del cliente"
                     value={nombre} onChange={(e) => setNombre(e.target.value)} />
            </div>
            <div className="col-md-4 d-flex gap-2">
              <button className="btn btn-accent flex-fill" onClick={guardarCliente}>Guardar</button>
              <button className="btn btn-outline-secondary" onClick={() => setMostrarForm(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <table className="table table-cantina">
        <thead>
          <tr>
            <th>CLIENTE</th>
            <th>ID</th>
            <th>PEDIDOS REALIZADOS</th>
            <th>TOTAL CONSUMIDO</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((c) => (
            <tr key={c.id}>
              <td>
                <span className="avatar-cliente">{c.nombre[0]}</span>
                {c.nombre}
              </td>
              <td className="id-plato">id_cliente · {String(c.id).padStart(3, "0")}</td>
              <td>{c.pedidosRealizados}</td>
              <td className="fw-bold">S/ {c.totalConsumido.toFixed(2)}</td>
              <td className="text-end">
                <button className="icon-btn me-2" onClick={() => empezarEdicion(c)}>Editar</button>
                <button className="icon-btn danger" onClick={() => eliminarCliente(c.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Clientes;
