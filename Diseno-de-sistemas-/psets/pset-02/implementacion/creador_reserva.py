from reserva import ReservaRegular, ReservaEquipoOficial
from solicitante import CapitanEquipo

class CreadorReserva:
    def crear_reserva(self, id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud):
        raise NotImplementedError
 

class CreadorReservaEstudiante(CreadorReserva):
    def crear_reserva(self, id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud):
        return ReservaRegular(id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud, solicitante.politica_cancelacion)
 

class CreadorReservaCapitan(CreadorReserva):
    def crear_reserva(self, id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud):
        return ReservaEquipoOficial(id_, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud, solicitante.politica_cancelacion, solicitante.equipo)
 

def obtener_creador(solicitante):
    if isinstance(solicitante, CapitanEquipo):
        return CreadorReservaCapitan()
    return CreadorReservaEstudiante()