# Sistema de Restaurante — FastAPI + PostgreSQL + React (Vite)

Proyecto terminado, siguiendo el mismo patrón que usa el profesor en
`PASOS_CONEXION_REACT.md`: FastAPI + schemas Pydantic + DAO + Historial
de auditoría, conectado a un frontend en React con Vite.

## Estructura

```
proyecto-final/
├── backend/
│   ├── config/base_datos.py      → conexión a PostgreSQL (obtener_conexion())
│   ├── modelos/                  → clases Python planas (Plato, Cliente, Pedido, Historial)
│   ├── schemas/                  → validación con Pydantic (Crear/Actualizar/Respuesta)
│   ├── dao/                      → todo el SQL vive aquí, uno por tabla
│   ├── routers/                  → endpoints FastAPI, delegan al DAO
│   ├── schema.sql                → DDL + datos base de PostgreSQL
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py                   → punto de entrada (uvicorn main:app)
└── frontend/
    ├── src/
    │   ├── api/axios.js          → cliente HTTP centralizado
    │   ├── components/           → Platos, Clientes, Pedidos, Historial
    │   ├── App.jsx
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── .env.example
```

## Cómo correrlo

### 1. Base de datos
```bash
psql -U postgres -f backend/schema.sql
# luego, ya conectado a la base 'restaurante', corre el resto del schema.sql
```

### 2. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # y edita con tu password real
uvicorn main:app --reload
```
Abre `http://127.0.0.1:8000/docs` — ahí puedes probar cada endpoint sin
tocar React todavía.

### 3. Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Abre `http://localhost:5173`.

## Endpoints disponibles

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/platos/` | lista platos |
| POST | `/platos/` | crea plato |
| PUT | `/platos/{id}` | edita plato |
| DELETE | `/platos/{id}` | elimina plato |
| GET | `/clientes/` | lista clientes |
| POST | `/clientes/` | crea cliente |
| PUT | `/clientes/{id}` | edita cliente |
| DELETE | `/clientes/{id}` | elimina cliente |
| GET | `/pedidos/` | lista pedidos (con sus platos) |
| POST | `/pedidos/` | crea pedido (calcula el total automáticamente) |
| PUT | `/pedidos/{id}/estado` | cambia estado (Pendiente/En cocina/Listo) |
| GET | `/historial/` | lista el registro de auditoría |
| DELETE | `/historial/` | limpia el historial |

Cada creación/edición/eliminación en `platos`, `clientes` y `pedidos`
queda registrada automáticamente en `historial`, vía `HistorialDAO.registrar()`.
