class AdministradorComplejo:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre

    def agregar_cancha(self, canchas, cancha):
        canchas.append(cancha)
        print(f"El administrador {self.nombre} agrega {cancha.nombre} al catalogo ({cancha.sede.nombre})")

    def resolver_conflicto(self, facade, conflicto, decision, hora_actual):
        print(f"1. El administrador {self.nombre} revisa el conflicto {conflicto.id}")
        print(f"2. El administrador decide la resolucion: '{decision}'")
        conflicto.resolver(decision, facade, hora_actual)
        print("3. El sistema actualiza el estado de las reservas involucradas")
        print("4. El sistema notifica el resultado a los solicitantes")
        if decision == "reasignar":
            vieja = conflicto.reserva_existente
            nueva = conflicto.reserva_nueva
            vieja.sede.notificar(vieja.solicitante,
                                 f"Tu reserva {vieja.id} fue anulada por conflicto de prioridad")
            nueva.sede.notificar(nueva.solicitante,
                                 f"Reserva {nueva.id} confirmada en {nueva.cancha.nombre}")
        else:
            conflicto.sede.notificar(conflicto.solicitante_nuevo,
                                     f"Tu solicitud para {conflicto.cancha.nombre} fue rechazada")

    def definir_bloqueo(self, facade, bloqueo, canchas_y_fechas, hora_actual):
        return facade.bloquear(bloqueo, canchas_y_fechas, hora_actual)