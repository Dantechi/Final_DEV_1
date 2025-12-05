from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from models import Partido
from database import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/partidos", tags=["Partidos"])
templates = Jinja2Templates(directory="templates")


def calcular_resultado(g_sigmoto, g_rival):
    if g_sigmoto > g_rival:
        return "Victoria"
    if g_sigmoto < g_rival:
        return "Derrota"
    return "Empate"


@router.get("/")
def lista_partidos(request: Request, session: Session = Depends(get_session)):
    partidos = session.query(Partido).all()
    return templates.TemplateResponse("partidos/lista.html", {"request": request, "partidos": partidos})


@router.get("/crear")
def formulario_crear(request: Request):
    return templates.TemplateResponse("partidos/crear.html", {"request": request})


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
    resultado = calcular_resultado(goles_sigmoto, goles_rival)

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
    return RedirectResponse("/partidos", status_code=303)
