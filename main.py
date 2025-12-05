# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from routers import jugadores, partidos, estadisticas
from db import create_db_and_tables, get_session, SessionDep
from models import Jugador

@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_db_and_tables()
    yield



app = FastAPI(
    lifespan=lifespan,
    title="Sigmotoa FC API",
    version="1.0.0",
    description="API REST para gestionar jugadores, partidos y estadísticas de Sigmotoa FC",
)

# CORS (útil durante desarrollo; ajustar orígenes en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de la API (JSON)
app.include_router(jugadores.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)

# Endpoint raíz (API)
@app.get("/", tags=["api"])
async def root():
    return {
        "app": "Sigmotoa FC API",
        "version": "1.0.0",
        "description": "API para gestionar jugadores, partidos y estadísticas. Revisa /docs para la documentación OpenAPI."
    }

# Ejemplo de endpoint para debug / sanity (opcional)
@app.get("/health", tags=["api"])
async def health():
    return {"status": "ok"}

# Manejo global de HTTPException para devolver JSON con detalle (comportamiento parecido al ejemplo HTML)
from fastapi import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Devuelve un JSON consistente para errores HTTP.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        },
    )



@app.get("/api/ref/resumen", tags=["api"])
async def resumen_refugios(session: SessionDep):
    """
    Endpoint de ejemplo que muestra un resumen simple - se puede eliminar luego.
    """
    result = await session.exec(select(Jugador))
    jugadores = result.all()
    return {"total_jugadores": len(jugadores)}

# Para ejecutar con uvicorn:
# uvicorn main:app --reload
