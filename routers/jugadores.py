from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select
from database import get_session
from models import Jugador
from enums.states import States
from enums.positions import Position
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def lista_jugadores(request: Request, session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return templates.TemplateResponse("jugadores/lista.html", {"request": request, "jugadores": jugadores})


@router.get("/crear")
def formulario_crear(request: Request):
    return templates.TemplateResponse("jugadores/crear.html", {
        "request": request,
        "positions": list(Position),
        "states": list(States)
    })


@router.post("/crear")
def crear_jugador(
    request: Request,
    nombre: str = Form(...),
    numero_camiseta: int = Form(...),
    fecha_nacimiento: str = Form(...),
    nacionalidad: str = Form(...),
    altura_cm: int = Form(...),
    peso_kg: int = Form(...),
    pie_dominante: str = Form(...),
    posicion: Position = Form(...),
    valor_jugador: int = Form(...),
    anio_club: int = Form(...),
    session: Session = Depends(get_session)
):
    existe = session.exec(select(Jugador).where(Jugador.numero_camiseta == numero_camiseta)).first()
    if existe:
        raise HTTPException(status_code=400, detail="Número de camiseta duplicado")

    jugador = Jugador(
        nombre=nombre,
        numero_camiseta=numero_camiseta,
        fecha_nacimiento=fecha_nacimiento,
        nacionalidad=nacionalidad,
        altura_cm=altura_cm,
        peso_kg=peso_kg,
        pie_dominante=pie_dominante,
        posicion=posicion,
        valor_jugador=valor_jugador,
        anio_club=anio_club,
    )
    session.add(jugador)
    session.commit()
    return RedirectResponse("/jugadores", status_code=303)
