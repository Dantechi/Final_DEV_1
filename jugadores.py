# jugadores.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import SessionDep
from models import (
    Jugador,
    JugadorCreate,
    JugadorRead,
    JugadorUpdate,
    PosicionEnum,
    EstadoJugadorEnum,
)


router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


# =============================
# Crear jugador
# =============================
@router.post("/", response_model=JugadorRead)
async def crear_jugador(jugador: JugadorCreate, session: SessionDep):

    # Verificar número duplicado
    stmt = select(Jugador).where(
        Jugador.numero == jugador.numero,
        Jugador.eliminado == False
    )
    result = await session.exec(stmt)
    existe = result.first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail=f"El número {jugador.numero} ya está asignado a otro jugador."
        )

    nuevo = Jugador.model_validate(jugador)
    session.add(nuevo)
    await session.commit()
    await session.refresh(nuevo)
    return nuevo


# =============================
# Listar jugadores (con filtros)
# =============================
@router.get("/", response_model=list[JugadorRead])
async def listar_jugadores(
    session: SessionDep,
    nombre: str | None = None,
    posicion: PosicionEnum | None = None,
    estado: EstadoJugadorEnum | None = None,
    nacionalidad: str | None = None,
    club_previo: str | None = None,
):
    stmt = select(Jugador).where(Jugador.eliminado == False)

    if nombre:
        stmt = stmt.where(Jugador.nombre.ilike(f"%{nombre}%"))
    if posicion:
        stmt = stmt.where(Jugador.posicion == posicion)
    if estado:
        stmt = stmt.where(Jugador.estado == estado)
    if nacionalidad:
        stmt = stmt.where(Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))
    if club_previo:
        stmt = stmt.where(Jugador.club_previo.ilike(f"%{club_previo}%"))

    result = await session.exec(stmt)
    return result.all()


# =============================
# Obtener jugador por ID
# =============================
@router.get("/{jugador_id}", response_model=JugadorRead)
async def obtener_jugador(jugador_id: int, session: SessionDep):
    jugador = await session.get(Jugador, jugador_id)
    if not jugador or jugador.eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


# =============================
# Actualizar jugador
# =============================
@router.patch("/{jugador_id}", response_model=JugadorRead)
async def actualizar_jugador(
    jugador_id: int,
    cambios: JugadorUpdate,
    session: SessionDep
):
    jugador = await session.get(Jugador, jugador_id)
    if not jugador or jugador.eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    for campo, valor in cambios.model_dump(exclude_unset=True).items():
        setattr(jugador, campo, valor)

    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador


# =============================
# Borrado lógico (soft delete)
# =============================
@router.delete("/{jugador_id}")
async def eliminar_jugador(jugador_id: int, session: SessionDep):
    jugador = await session.get(Jugador, jugador_id)
    if not jugador or jugador.eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.eliminado = True
    session.add(jugador)
    await session.commit()

    return {"message": "Jugador eliminado correctamente"}


# =============================
# Restaurar jugador eliminado
# =============================
@router.post("/{jugador_id}/restaurar")
async def restaurar_jugador(jugador_id: int, session: SessionDep):
    jugador = await session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.eliminado = False
    session.add(jugador)
    await session.commit()

    return {"message": "Jugador restaurado correctamente"}
