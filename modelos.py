from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enums.states import States
from enums.positions import Position


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    numero_camiseta: int = Field(gt=0, lt=100)
    fecha_nacimiento: str
    nacionalidad: str
    altura_cm: int
    peso_kg: int
    pie_dominante: str
    posicion: Position
    valor_jugador: int
    anio_club: int
    estado: States = Field(default=States.ACTIVO)
    estado_suspendido: bool = False

    estadisticas: List["Estadistica"] = Relationship(back_populates="jugador")


class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rival: str
    fecha: str
    es_local: bool
    goles_sigmoto: int
    goles_rival: int
    resultado: Optional[str] = None

    estadisticas: List["Estadistica"] = Relationship(back_populates="partido")


class Estadistica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    minutos_jugados: int
    goles: int
    faltas: int
    tarjetas_amarillas: int
    tarjetas_rojas: int

    jugador_id: int = Field(foreign_key="jugador.id")
    partido_id: int = Field(foreign_key="partido.id")

    jugador: Jugador = Relationship(back_populates="estadisticas")
    partido: Partido = Relationship(back_populates="estadisticas")
