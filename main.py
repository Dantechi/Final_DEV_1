from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import create_db_and_tables
from routers import jugadores, partidos, estadisticas
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Sistema de Gestión de Fútbol")

templates = Jinja2Templates(directory="templates")

app.include_router(jugadores.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "API de Gestión de Fútbol funcionando. Visita /docs"}
