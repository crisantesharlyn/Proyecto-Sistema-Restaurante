from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import platos, clientes, pedidos, historial

app = FastAPI(title="Sistema de Restaurante")

# CORS: permite que React (Vite, puerto 5173) llame a esta API (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(platos.router)
app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(historial.router)


@app.get("/")
def read_root():
    return {"message": "Backend levantado correctamente 🚀"}

