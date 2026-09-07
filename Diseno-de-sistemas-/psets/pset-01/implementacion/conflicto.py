class ConflictoReserva:
    def __init__(self, id_: str, reserva_existente, solicitante_nuevo,
                 cancha, hora_inicio, hora_fin):
        self.id = id_
        self.reserva_existente = reserva_existente
        self.solicitante_nuevo = solicitante_nuevo
        self.cancha = cancha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.resuelto = False
        self.resolucion = None

    def resolver(self, decision: str, gestor):
        if decision == "mantener":
            gestor.rechazar_solicitud(self.solicitante_nuevo, self.cancha,
                                       self.hora_inicio, self.hora_fin)
        elif decision == "reasignar":
            self.reserva_existente.cancelar(self.reserva_existente.hora_solicitud)
            gestor.confirmar_reserva_directa(self.solicitante_nuevo, self.cancha,
                                              self.hora_inicio, self.hora_fin,
                                              self.reserva_existente.hora_solicitud)
        else:
            raise ValueError("Decision de conflicto no reconocida")
        self.resuelto = True
        self.resolucion = decision

    def __str__(self):
        return (f"ConflictoReserva[{self.id}] {self.cancha.nombre} "
                f"{self.hora_inicio.strftime('%H:%M')} :: "
                f"existente={self.reserva_existente.solicitante.nombre} vs "
                f"nuevo={self.solicitante_nuevo.nombre} -> "
                f"{'resuelto:' + self.resolucion if self.resuelto else 'pendiente'}")