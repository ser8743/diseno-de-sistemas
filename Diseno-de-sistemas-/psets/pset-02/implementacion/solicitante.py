from datetime import timedelta
from configuracion import ConfiguracionReglas
from reglas_prioridad import SinPrioridad, PrioridadAntesDe18h
from politica_cancelacion import CancelacionEstudiante, CancelacionCapitan


class Solicitante:
    def __init__(self, id_, nombre, comportamiento_prioridad, politica_cancelacion):
        self.id = id_
        self.nombre = nombre
        self.comportamiento_prioridad = comportamiento_prioridad
        self.politica_cancelacion = politica_cancelacion
        self.fechas_no_shows = []
        self.suspendido_hasta = None

    def tiene_prioridad(self, hora_inicio):
        return self.comportamiento_prioridad.aplica_prioridad(hora_inicio)

    def esta_suspendido(self, ahora):
        if self.suspendido_hasta is None:
            return False
        return ahora < self.suspendido_hasta

    def registrar_no_show(self, fecha):
        self.fechas_no_shows.append(fecha)
        config = ConfiguracionReglas.obtener_instancia()

        cantidad_del_mes = 0
        for f in self.fechas_no_shows:
            if f.year == fecha.year and f.month == fecha.month:
                cantidad_del_mes = cantidad_del_mes + 1

        if cantidad_del_mes >= config.limite_no_shows_mes and not self.esta_suspendido(fecha):
            self.suspendido_hasta = fecha + timedelta(days=config.dias_suspension)
            return True
        return False


class Estudiante(Solicitante):
    def __init__(self, id_, nombre):
        sin_prioridad = SinPrioridad()
        cancelacion = CancelacionEstudiante()
        super().__init__(id_, nombre, sin_prioridad, cancelacion)


class CapitanEquipo(Solicitante):
    def __init__(self, id_, nombre, equipo):
        prioridad_18h = PrioridadAntesDe18h()
        cancelacion = CancelacionCapitan()
        super().__init__(id_, nombre, prioridad_18h, cancelacion)
        self.equipo = equipo