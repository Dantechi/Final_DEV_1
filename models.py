# models/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum


# -------- ENUMS -------- #

class States(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    LESIONADO = "LESIONADO"
    AMONESTADO = "AMONESTADO"


class Positions(str, Enum):
    ARQUERO = "ARQUERO"
    DEFENSA_C = "DEFENSA_C"
    DEFENSA_L = "DEFENSA_L"
    VOLANTE_D = "VOLANTE_D"
    VOLANTE_O = "VOLANTE_O"
    VOLANTE_C = "VOLANTE_C"
    VOLANTE_E = "VOLANTE_E"
    DELANTERO_C = "DELANTERO_C"
    DELANTERO_P = "DELANTERO_P"


# -------- MODELO JUGADOR -------- #

class JugadorBase(SQLModel):
    nombre: str
    numero_camiseta: int = Field(index=True)
    fecha_nacimiento: str
    nacionalidad: str
    altura_cm: int
    peso_kg: int
    pie_dominante: str
    posicion: Positions
    valor_jugador: Optional[int] = 0
    anio_club: Optional[int] = 0
    estado_activo: bool = True
    estado_suspendido: bool = False
    estado: States = States.ACTIVO


class Jugador(JugadorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    estadisticas: List["Estadistica"] = Relationship(back_populates="jugador")


# -------- MODELO PARTIDO -------- #

class PartidoBase(SQLModel):
    rival: str
    fecha: str
    es_local: bool
    goles_sigmoto: int
    goles_rival: int
    resultado: str = "Pendiente"


class Partido(PartidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    estadisticas: List["Estadistica"] = Relationship(back_populates="partido")


# -------- MODELO ESTADISTICA -------- #

class EstadisticaBase(SQLModel):
    minutos_jugados: int
    goles: int
    faltas: int
    tarjetas_amarillas: int
    tarjetas_rojas: int


class Estadistica(EstadisticaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    jugador_id: int = Field(foreign_key="jugador.id")
    partido_id: int = Field(foreign_key="partido.id")

    jugador: Jugador = Relationship(back_populates="estadisticas")
    partido: Partido = Relationship(back_populates="estadisticas")
