from reglas_prioridad import PrioridadAntesDe18h, SinPrioridad


class Solicitante:
    def __init__(self, id_, nombre, comportamiento_prioridad):
        self.id = id_
        self.nombre = nombre
        self.comportamiento_prioridad = comportamiento_prioridad

    def tiene_prioridad(self, hora_solicitud):
        return self.comportamiento_prioridad.aplica_prioridad(hora_solicitud)


class Estudiante(Solicitante):
    def __init__(self, id_, nombre):
        sin_prioridad = SinPrioridad()
        super().__init__(id_, nombre, sin_prioridad)


class CapitanEquipo(Solicitante):
    def __init__(self, id_, nombre, equipo):
        prioridad_18h = PrioridadAntesDe18h()
        super().__init__(id_, nombre, prioridad_18h)
        self.equipo = equipo
