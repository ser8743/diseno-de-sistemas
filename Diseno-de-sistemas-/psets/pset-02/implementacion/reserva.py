from estado_reserva import EstadoReserva
from politica_cancelacion import CancelacionAdministrativa

class Reserva:
    def __init__(self, id_, solicitante, cancha, sede, hora_inicio, hora_fin,
                 hora_solicitud, politica_cancelacion):
        self.id = id_
        self.solicitante = solicitante
        self.cancha = cancha
        self.sede = sede
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.hora_solicitud = hora_solicitud
        self.politica_cancelacion = politica_cancelacion
        self.estado = EstadoReserva.CONFIRMADA

    def esta_activa(self):
        return self.estado == EstadoReserva.CONFIRMADA

    def cancelar(self, hora_actual):
        return self.aplicar_politica(self.politica_cancelacion, hora_actual)

    def anular(self, hora_actual):
        return self.aplicar_politica(CancelacionAdministrativa(), hora_actual)

    def aplicar_politica(self, politica, hora_actual):
        if self.estado != EstadoReserva.CONFIRMADA:
            return self.estado
        self.estado = politica.evaluar(self, hora_actual)
        self.cancha.liberar_horario(self.hora_inicio, self.hora_fin)
        return self.estado

    def resumen(self):
        return (f"Reserva[{self.id}] {self.solicitante.nombre} -> {self.cancha.nombre} "
                f"({self.sede.nombre}) {self.hora_inicio} a {self.hora_fin} :: {self.estado}")

class ReservaRegular(Reserva):
    pass

class ReservaEquipoOficial(Reserva):
    def __init__(self, id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud, politica_cancelacion, equipo):
        super().__init__(id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud, politica_cancelacion)
        self.equipo = equipo