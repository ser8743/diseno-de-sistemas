from enum import Enum
from datetime import datetime, timedelta


class EstadoReserva(Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    NO_SHOW = "NO_SHOW"


class Reserva:
    LIMITE_NO_SHOW = timedelta(hours=2)

    def __init__(self, id_: str, solicitante, cancha, hora_inicio: datetime,
                 hora_fin: datetime, hora_solicitud: datetime):
        self.id = id_
        self.solicitante = solicitante
        self.cancha = cancha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.hora_solicitud = hora_solicitud
        self.estado = EstadoReserva.CONFIRMADA

    def confirmar(self):
        self.estado = EstadoReserva.CONFIRMADA

    def esta_activa(self) -> bool:
        return self.estado == EstadoReserva.CONFIRMADA

    def cancelar(self, hora_actual: datetime):
        
        tiempo_restante = self.hora_inicio - hora_actual
        if tiempo_restante < self.LIMITE_NO_SHOW:
            self.estado = EstadoReserva.NO_SHOW
        else:
            self.estado = EstadoReserva.CANCELADA
        self.cancha.liberar_horario(self.hora_inicio, self.hora_fin)
        return self.estado

    def __str__(self):
        return (f"Reserva[{self.id}] {self.solicitante.nombre} -> "
                f"{self.cancha.nombre} {self.hora_inicio.strftime('%H:%M')}-"
                f"{self.hora_fin.strftime('%H:%M')} :: {self.estado.value}")
