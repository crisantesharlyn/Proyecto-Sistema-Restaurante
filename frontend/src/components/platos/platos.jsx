import { useState, useEffect } from "react";
import api from "../../api/axios";

function Platos() {
  const [platos, setPlatos] = useState([]);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [nombre, setNombre] = useState("");
  const [precio, setPrecio] = useState("");
  const [emoji, setEmoji] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  useEffect(() => {
    cargarPlatos();
  }, []);

  function cargarPlatos() {
    api.get("/platos/").then((res) => setPlatos(res.data));
  }

  function empezarEdicion(p) {
    setNombre(p.nombre);
    setPrecio(p.precio);
    setEmoji(p.emoji || "");
    setEditandoId(p.id);
    setMostrarForm(true);
  }

  function abrirNuevo() {
    setNombre("");
    setPrecio("");
    setEmoji("");
    setEditandoId(null);
    setMostrarForm(true);
  }

  async function guardarPlato() {
    if (editandoId) {
      const res = await api.put(`/platos/${editandoId}`, {
        nombre,
        precio: Number(precio),
        emoji,
      });
      setPlatos(platos.map((p) => (p.id === editandoId ? res.data : p)));
    } else {
      const res = await api.post("/platos/", {
        nombre,
        precio: Number(precio),
        emoji,
      });
      setPlatos([...platos, res.data]);
    }
    setMostrarForm(false);
  }

  async function eliminarPlato(id) {
    await api.delete(`/platos/${id}`);
    setPlatos(platos.filter((p) => p.id !== id));
  }

  return (
    <div>
      <div className="section-eyebrow">GESTIÓN DE PLATOS · RF01–RF04</div>
      <div className="section-title-row">
        <h1>El Menú</h1>
        <button className="btn btn-accent" onClick={abrirNuevo}>
          + Nuevo plato
        </button>
      </div>

      {mostrarForm && (
        <div className="plato-card mb-4" style={{ borderStyle: "solid" }}>
          <h6 className="mb-3">{editandoId ? "Editar plato" : "Nuevo plato"}</h6>
          <div className="row g-2">
            <div className="col-md-4">
              <input className="form-control" placeholder="Nombre"
                     value={nombre} onChange={(e) => setNombre(e.target.value)} />
            </div>
            <div className="col-md-3">
              <input className="form-control" type="number" placeholder="Precio"
                     value={precio} onChange={(e) => setPrecio(e.target.value)} />
            </div>
            <div className="col-md-2">
              <input className="form-control" placeholder="Emoji"
                     value={emoji} onChange={(e) => setEmoji(e.target.value)} />
            </div>
            <div className="col-md-3 d-flex gap-2">
              <button className="btn btn-accent flex-fill" onClick={guardarPlato}>Guardar</button>
              <button className="btn btn-outline-secondary" onClick={() => setMostrarForm(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <div className="row g-4">
        {platos.map((p, i) => (
          <div className="col-md-4" key={p.id}>
            <div className="plato-card">
              <div className="icono-plato" />
              <h5 className="mb-0">{p.nombre}</h5>
              <div className="id-plato">id_plato · {String(p.id).padStart(3, "0")}</div>
              <div className="precio">S/ {p.precio.toFixed(2)}</div>
              <div className="d-flex gap-2">
                <button className="icon-btn" onClick={() => empezarEdicion(p)}>Editar</button>
                <button className="icon-btn danger" onClick={() => eliminarPlato(p.id)}>Eliminar</button>
              </div>
            </div>
          </div>
        ))}

        <div className="col-md-4">
          <div className="add-plato-card" onClick={abrirNuevo}>
            <div className="signo-mas">+</div>
            <div>Agregar plato</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Platos;
