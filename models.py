# models.py
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

# Importamos tus enums reales
from utils.positions import Position
from utils.states import States


# =========================
# ENUM resultado del partido
# =========================
class ResultadoEnum(str, Enum):
    VICTORIA = "VICTORIA"
    EMPATE = "EMPATE"
    DERROTA = "DERROTA"


# =========================
# MODELO JUGADOR
# =========================

class JugadorBase(SQLModel):
    nombre: str
    numero: int = Field(ge=1, le=99)
    edad: int = Field(ge=15, le=50)
    estatura_cm: int = Field(ge=140, le=220)
    peso_kg: float = Field(ge=40, le=150)
    nacionalidad: str

    # ENUMS actualizados
    posicion: Position
    estado: States = States.ACTIVO

    # Información adicional
    contrato: Optional[str] = None
    club_previo: Optional[str] = None
    valor_mercado_usd: Optional[float] = Field(default=0, ge=0)


class Jugador(JugadorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)
    eliminado: bool = Field(default=False)

    estadisticas: List["EstadisticaJugador"] = Relationship(back_populates="jugador")


class JugadorCreate(JugadorBase):
    pass


class JugadorRead(JugadorBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime


class JugadorUpdate(SQLModel):
    nombre: Optional[str] = None
    numero: Optional[int] = None
    edad: Optional[int] = None
    estatura_cm: Optional[int] = None
    peso_kg: Optional[float] = None
    nacionalidad: Optional[str] = None
    posicion: Optional[Position] = None
    estado: Optional[States] = None
    contrato: Optional[str] = None
    club_previo: Optional[str] = None
    valor_mercado_usd: Optional[float] = None


# =========================
# MODELO PARTIDO
# =========================

class PartidoBase(SQLModel):
    fecha: date
    rival: str
    es_local: bool
    goles_a_favor: int = Field(ge=0)
    goles_en_contra: int = Field(ge=0)
    resultado: ResultadoEnum


class Partido(PartidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    estadisticas: List["EstadisticaJugador"] = Relationship(back_populates="partido")


class PartidoCreate(PartidoBase):
    pass


class PartidoRead(PartidoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime


class PartidoUpdate(SQLModel):
    fecha: Optional[date] = None
    rival: Optional[str] = None
    es_local: Optional[bool] = None
    goles_a_favor: Optional[int] = None
    goles_en_contra: Optional[int] = None
    resultado: Optional[ResultadoEnum] = None


# =========================
# MODELO ESTADÍSTICA JUGADOR
# =========================

class EstadisticaBase(SQLModel):
    minutos_jugados: int = Field(ge=0, le=120)
    gols: int = Field(default=0, ge=0)
    asistencias: int = Field(default=0, ge=0)
    faltas: int = Field(default=0, ge=0)
    tarjetas_amarillas: int = Field(default=0, ge=0)
    tarjetas_rojas: int = Field(default=0, ge=0)
    goles_recibidos: Optional[int] = Field(default=None, ge=0)


class EstadisticaJugador(EstadisticaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    jugador_id: int = Field(foreign_key="jugador.id")
    partido_id: int = Field(foreign_key="partido.id")

    creado_en: datetime = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    jugador: Optional["Jugador"] = Relationship(back_populates="estadisticas")
    partido: Optional["Partido"] = Relationship(back_populates="estadisticas")


class EstadisticaCreate(EstadisticaBase):
    jugador_id: int
    partido_id: int


class EstadisticaRead(EstadisticaBase):
    id: int
    jugador_id: int
    partido_id: int
    creado_en: datetime
    actualizado_en: datetime


class EstadisticaUpdate(SQLModel):
    minutos_jugados: Optional[int] = None
    gols: Optional[int] = None
    asistencias: Optional[int] = None
    faltas: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    goles_recibidos: Optional[int] = None
