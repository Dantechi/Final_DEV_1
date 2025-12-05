from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import jugadores, partidos, estadisticas
from database import create_db_and_tables

app = FastAPI(title="Sistema de Futbol Sigmoto FC")

app.include_router(jugadores.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    create_db_and_tables()
