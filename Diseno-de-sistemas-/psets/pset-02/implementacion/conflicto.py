from creador_reserva import obtener_creador

class ConflictoReserva:
    def __init__(self, id_, reserva_existente, solicitante_nuevo, cancha, sede,
                 hora_inicio, hora_fin, hora_solicitud):
        self.id = id_
        self.reserva_existente = reserva_existente
        self.solicitante_nuevo = solicitante_nuevo
        self.cancha = cancha
        self.sede = sede
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.hora_solicitud = hora_solicitud
        self.reserva_nueva = None
        self.resuelto = False
        self.resolucion = None

    def resolver(self, decision, facade, hora_actual):
        if decision == "reasignar":
            self.reserva_existente.anular(hora_actual)
            creador = obtener_creador(self.solicitante_nuevo)
            self.reserva_nueva = creador.crear_reserva(
                facade.siguiente_id(), self.solicitante_nuevo, self.cancha, self.sede,
                self.hora_inicio, self.hora_fin, self.hora_solicitud)
            self.cancha.ocupar_horario(self.hora_inicio, self.hora_fin)
            facade.reservas.append(self.reserva_nueva)
        elif decision != "mantener":
            raise ValueError("Decision de conflicto no reconocida")
        self.resuelto = True
        self.resolucion = decision