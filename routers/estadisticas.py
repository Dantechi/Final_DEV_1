from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from db import get_session
from models import Estadistica, Jugador, Partido

router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])
templates = Jinja2Templates(directory="templates")


@router.get("/crear")
def formulario(request: Request, session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    partidos = session.exec(select(Partido)).all()
    return templates.TemplateResponse("estadisticas/crear.html", {
        "request": request,
        "jugadores": jugadores,
        "partidos": partidos
    })


@router.post("/crear")
def crear(
    request: Request,
    jugador_id: int = Form(...),
    partido_id: int = Form(...),
    minutos_jugados: int = Form(...),
    goles: int = Form(...),
    faltas: int = Form(...),
    tarjetas_amarillas: int = Form(...),
    tarjetas_rojas: int = Form(...),
    session: Session = Depends(get_session)
):
    estad = Estadistica(
        jugador_id=jugador_id,
        partido_id=partido_id,
        minutos_jugados=minutos_jugados,
        goles=goles,
        faltas=faltas,
        tarjetas_amarillas=tarjetas_amarillas,
        tarjetas_rojas=tarjetas_rojas,
    )
    session.add(estad)
    session.commit()
    return RedirectResponse("/estadisticas/lista", status_code=303)


@router.get("/lista")
def lista(request: Request, session: Session = Depends(get_session)):
    estads = session.exec(select(Estadistica)).all()
    return templates.TemplateResponse("estadisticas/lista.html", {"request": request, "estadisticas": estads})
