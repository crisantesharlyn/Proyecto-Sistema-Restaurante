import axios from "axios";

// Instancia centralizada: cualquier componente importa esto en vez de
// escribir la URL del backend en cada archivo. Si el backend cambia de
// puerto o dominio, solo se actualiza aquí.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export default api;
