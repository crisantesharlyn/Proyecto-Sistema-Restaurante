import { useState } from "react";
import "./App.css";
import Platos from "./components/platos/Platos.jsx";
import Clientes from "./components/clientes/Clientes.jsx";
import Pedidos from "./components/pedidos/Pedidos.jsx";
import Historial from "./components/historial/Historial.jsx";

const TABS = [
  { key: "platos", label: "Menú" },
  { key: "pedidos", label: "Pedidos" },
  { key: "clientes", label: "Clientes" },
];

function App() {
  const [tab, setTab] = useState("platos");

  return (
    <div className="container">
      <nav className="navbar-restaurante">
        <div className="navbar-brand-custom">
          <div className="navbar-logo-circle">C</div>
          <div className="navbar-brand-text">
            <div className="titulo">El Arte del Buen Sabor</div>
            <div className="subtitulo">Sistema de gestión</div>
          </div>
        </div>

        <div className="navbar-tabs-custom">
          {TABS.map((t) => (
            <button
              key={t.key}
              className={tab === t.key ? "active" : ""}
              onClick={() => setTab(t.key)}
            >
              {t.label}
            </button>
          ))}
        </div>

        <span
          className="badge-admin"
          style={{ cursor: "pointer" }}
          title="Ver historial de auditoría"
          onClick={() => setTab(tab === "historial" ? "platos" : "historial")}
        >
          ADMIN
        </span>
      </nav>

      {tab === "platos" && <Platos />}
      {tab === "pedidos" && <Pedidos />}
      {tab === "clientes" && <Clientes />}
      {tab === "historial" && <Historial />}
    </div>
  );
}

export default App;
