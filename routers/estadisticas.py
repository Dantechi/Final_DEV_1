from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from models import Jugador, Partido, Estadistica
from db import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
templates = Jinja2Templates(directory="templates")


# CREAR ESTADISTICA
@router.get("/crear")
def crear_form(request: Request, session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    partidos = session.exec(select(Partido)).all()
    return templates.TemplateResponse(
        "estadisticas/crear.html",
        {"request": request, "jugadores": jugadores, "partidos": partidos}
    )


@router.post("/crear")
def crear_estadistica(
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
    jugador = session.get(Jugador, jugador_id)
    partido = session.get(Partido, partido_id)
    if not jugador or not partido:
        raise HTTPException(400, "Jugador o partido no existe")

    estadistica = Estadistica(
        jugador_id=jugador_id,
        partido_id=partido_id,
        minutos_jugados=minutos_jugados,
        goles=goles,
        faltas=faltas,
        tarjetas_amarillas=tarjetas_amarillas,
        tarjetas_rojas=tarjetas_rojas
    )
    session.add(estadistica)
    session.commit()
    return RedirectResponse(f"/jugadores/detalle/{jugador_id}", status_code=302)
