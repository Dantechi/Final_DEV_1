# routers/partidos.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from models import Partido
from db import get_session

router = APIRouter(prefix="/partidos", tags=["Partidos"])


@router.get("/")
def lista_partidos(request: Request, session: Session = Depends(get_session)):
    partidos = session.exec(select(Partido)).all()
    return TemplateResponse("partidos/lista.html", {"request": request, "partidos": partidos})


@router.get("/crear")
def crear_partido_form(request: Request):
    return TemplateResponse("partidos/crear.html", {"request": request})


@router.post("/crear")
def crear_partido(
    request: Request,
    rival: str = Form(...),
    fecha: str = Form(...),
    es_local: bool = Form(...),
    goles_sigmoto: int = Form(...),
    goles_rival: int = Form(...),
    session: Session = Depends(get_session)
):

    if goles_sigmoto > goles_rival:
        resultado = "Victoria"
    elif goles_sigmoto < goles_rival:
        resultado = "Derrota"
    else:
        resultado = "Empate"

    partido = Partido(
        rival=rival,
        fecha=fecha,
        es_local=es_local,
        goles_sigmoto=goles_sigmoto,
        goles_rival=goles_rival,
        resultado=resultado
    )

    session.add(partido)
    session.commit()

    return RedirectResponse("/partidos", status_code=302)


@router.get("/detalle/{partido_id}")
def detalle_partido(partido_id: int, request: Request, session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(404, "Partido no encontrado")

    return TemplateResponse("partidos/detalle.html", {"request": request, "partido": partido})
