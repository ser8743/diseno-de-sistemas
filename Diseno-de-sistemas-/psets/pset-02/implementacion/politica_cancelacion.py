from datetime import timedelta
from configuracion import ConfiguracionReglas
from estado_reserva import EstadoReserva

class PoliticaCancelacion:
    etiqueta = ""

    def evaluar(self, reserva, hora_actual):
        raise NotImplementedError


class CancelacionEstudiante(PoliticaCancelacion):
    etiqueta = "2a"

    def evaluar(self, reserva, hora_actual):
        horas = ConfiguracionReglas.obtener_instancia().ventana_cancelacion_estudiante_horas
        falta = reserva.hora_inicio - hora_actual
        if falta < timedelta(hours=horas):
            return EstadoReserva.NO_SHOW
        return EstadoReserva.CANCELADA


class CancelacionCapitan(PoliticaCancelacion):
    etiqueta = "2b"

    def evaluar(self, reserva, hora_actual):
        horas = ConfiguracionReglas.obtener_instancia().ventana_cancelacion_capitan_horas
        falta = reserva.hora_inicio - hora_actual
        if falta < timedelta(hours=horas):
            return EstadoReserva.NO_SHOW
        return EstadoReserva.CANCELADA


class CancelacionAdministrativa(PoliticaCancelacion):
    etiqueta = "2c"

    def evaluar(self, reserva, hora_actual):
        return EstadoReserva.ANULADA