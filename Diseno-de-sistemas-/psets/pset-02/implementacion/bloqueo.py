import copy
from datetime import datetime

class Bloqueo:
    def __init__(self, motivo, hora_inicio, hora_fin, equipo_montaje):
        self.motivo = motivo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.equipo_montaje = equipo_montaje
        self.cancha = None
        self.fecha = None

    def clonar(self, cancha, fecha):
        nuevo = copy.deepcopy(self)
        nuevo.cancha = cancha
        nuevo.fecha = fecha
        return nuevo

    def inicio(self):
        return datetime(self.fecha.year, self.fecha.month, self.fecha.day, self.hora_inicio, 0)

    def fin(self):
        return datetime(self.fecha.year, self.fecha.month, self.fecha.day, self.hora_fin, 0)