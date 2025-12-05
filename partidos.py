# partidos.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import SessionDep
from models import (
    Partido,
    PartidoCreate,
    PartidoRead,
    PartidoUpdate,
    ResultadoEnum,
)


router = APIRouter(prefix="/partidos", tags=["Partidos"])


# =============================
# Crear partido
# =============================
@router.post("/", response_model=PartidoRead)
async def crear_partido(data: PartidoCreate, session: SessionDep):

    nuevo = Partido.model_validate(data)
    session.add(nuevo)
    await session.commit()
    await session.refresh(nuevo)

    return nuevo


# =============================
# Listar partidos (con filtros)
# =============================
@router.get("/", response_model=list[PartidoRead])
async def listar_partidos(
    session: SessionDep,
    rival: str | None = None,
    resultado: ResultadoEnum | None = None,
    es_local: bool | None = None,
    year: int | None = None,
):
    stmt = select(Partido)

    if rival:
        stmt = stmt.where(Partido.rival.ilike(f"%{rival}%"))
    if resultado:
        stmt = stmt.where(Partido.resultado == resultado)
    if es_local is not None:
        stmt = stmt.where(Partido.es_local == es_local)
    if year:
        stmt = stmt.where(Partido.fecha.cast("text").like(f"{year}-%"))

    result = await session.exec(stmt)
    return result.all()


# =============================
# Obtener partido por ID
# =============================
@router.get("/{partido_id}", response_model=PartidoRead)
async def obtener_partido(partido_id: int, session: SessionDep):
    partido = await session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido


# =============================
# Actualizar partido
# =============================
@router.patch("/{partido_id}", response_model=PartidoRead)
async def actualizar_partido(
    partido_id: int,
    cambios: PartidoUpdate,
    session: SessionDep,
):
    partido = await session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    for campo, valor in cambios.model_dump(exclude_unset=True).items():
        setattr(partido, campo, valor)

    session.add(partido)
    await session.commit()
    await session.refresh(partido)

    return partido


# =============================
# Eliminar partido
# =============================
@router.delete("/{partido_id}")
async def eliminar_partido(partido_id: int, session: SessionDep):
    partido = await session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    await session.delete(partido)
    await session.commit()

    return {"message": "Partido eliminado correctamente"}

