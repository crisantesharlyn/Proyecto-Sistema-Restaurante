import { useState, useEffect } from "react";
import api from "../../api/axios";

function Historial() {
  const [historial, setHistorial] = useState([]);

  useEffect(() => {
    cargar();
  }, []);

  function cargar() {
    api.get("/historial/").then((res) => setHistorial(res.data));
  }

  async function limpiarHistorial() {
    await api.delete("/historial/");
    setHistorial([]);
  }

  return (
    <div>
      <div className="d-flex justify-content-between mb-3">
        <h5>Registro de actividad</h5>
        <button className="btn btn-outline-danger btn-sm" onClick={limpiarHistorial}>
          Limpiar historial
        </button>
      </div>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          {historial.map((h) => (
            <tr key={h.id}>
              <td>{h.fecha}</td>
              <td>{h.hora}</td>
              <td>{h.accion}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Historial;
