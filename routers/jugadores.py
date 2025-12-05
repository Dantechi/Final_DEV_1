from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from models import Jugador, Positions, States, Estadistica
from db import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])

templates = Jinja2Templates(directory="templates")


# LISTA DE JUGADORES
@router.get("/")
def lista_jugadores(request: Request, session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return templates.TemplateResponse("jugadores/lista.html", {"request": request, "jugadores": jugadores})


# CREAR JUGADOR
@router.get("/crear")
def crear_jugador_form(request: Request):
    return templates.TemplateResponse("jugadores/crear.html", {"request": request, "posiciones": list(Positions), "estados": list(States)})


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
    posicion: Positions = Form(...),
    session: Session = Depends(get_session)
):
    # Validación número de camiseta
    if session.exec(select(Jugador).where(Jugador.numero_camiseta == numero_camiseta)).first():
        raise HTTPException(status_code=400, detail="Número de camiseta duplicado")

    jugador = Jugador(
        nombre=nombre,
        numero_camiseta=numero_camiseta,
        fecha_nacimiento=fecha_nacimiento,
        nacionalidad=nacionalidad,
        altura_cm=altura_cm,
        peso_kg=peso_kg,
        pie_dominante=pie_dominante,
        posicion=posicion
    )
    session.add(jugador)
    session.commit()
    return RedirectResponse("/jugadores", status_code=302)


# DETALLE JUGADOR + ESTADISTICAS
@router.get("/detalle/{jugador_id}")
def detalle_jugador(jugador_id: int, request: Request, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")

    total_goles = sum(e.goles for e in jugador.estadisticas)
    total_partidos = len(jugador.estadisticas)
    promedio_goles = total_goles / total_partidos if total_partidos else 0
    total_minutos = sum(e.minutos_jugados for e in jugador.estadisticas)
    total_tarjetas = sum(e.tarjetas_amarillas + e.tarjetas_rojas for e in jugador.estadisticas)

    return templates.TemplateResponse(
        "jugadores/detalle.html",
        {
            "request": request,
            "jugador": jugador,
            "total_goles": total_goles,
            "total_partidos": total_partidos,
            "promedio_goles": promedio_goles,
            "total_minutos": total_minutos,
            "total_tarjetas": total_tarjetas
        }
    )


# EDITAR JUGADOR
@router.get("/editar/{jugador_id}")
def editar_jugador_form(jugador_id: int, request: Request, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")
    return templates.TemplateResponse(
        "jugadores/editar.html",
        {"request": request, "jugador": jugador, "posiciones": list(Positions), "estados": list(States)}
    )


@router.post("/editar/{jugador_id}")
def editar_jugador(
    jugador_id: int,
    request: Request,
    nombre: str = Form(...),
    numero_camiseta: int = Form(...),
    fecha_nacimiento: str = Form(...),
    nacionalidad: str = Form(...),
    altura_cm: int = Form(...),
    peso_kg: int = Form(...),
    pie_dominante: str = Form(...),
    posicion: Positions = Form(...),
    estado: States = Form(...),
    session: Session = Depends(get_session)
):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")

    jugador.nombre = nombre
    jugador.numero_camiseta = numero_camiseta
    jugador.fecha_nacimiento = fecha_nacimiento
    jugador.nacionalidad = nacionalidad
    jugador.altura_cm = altura_cm
    jugador.peso_kg = peso_kg
    jugador.pie_dominante = pie_dominante
    jugador.posicion = posicion
    jugador.estado = estado

    session.add(jugador)
    session.commit()
    return RedirectResponse(f"/jugadores/detalle/{jugador_id}", status_code=302)
