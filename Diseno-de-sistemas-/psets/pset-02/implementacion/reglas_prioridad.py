from configuracion import ConfiguracionReglas

class ComportamientoPrioridad:
    def aplica_prioridad(self, hora_inicio):
        raise NotImplementedError


class PrioridadAntesDe18h(ComportamientoPrioridad):
    def aplica_prioridad(self, hora_inicio):
        limite = ConfiguracionReglas.obtener_instancia().hora_limite_prioridad
        return hora_inicio.hour < limite


class SinPrioridad(ComportamientoPrioridad):
    def aplica_prioridad(self, hora_inicio):
        return False