from datetime import time


class ComportamientoPrioridad:
    def aplica_prioridad(self, hora_solicitud):
        raise NotImplementedError


class PrioridadAntesDe18h(ComportamientoPrioridad):
    def aplica_prioridad(self, hora_solicitud):
        return hora_solicitud < time(18, 0)


class SinPrioridad(ComportamientoPrioridad):
    def aplica_prioridad(self, hora_solicitud):
        return False
