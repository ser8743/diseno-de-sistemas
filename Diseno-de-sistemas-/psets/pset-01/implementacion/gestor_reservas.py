from reserva import Reserva, EstadoReserva
from conflicto import ConflictoReserva


class GestorReservas:
    def __init__(self):
        self.canchas = []
        self.reservas = []
        self.conflictos = []
        self._contador_reserva = 0
        self._contador_conflicto = 0

    def agregar_cancha(self, cancha):
        self.canchas.append(cancha)

    def eliminar_cancha(self, cancha):
        if cancha in self.canchas:
            self.canchas.remove(cancha)

    def solicitar_reserva(self, solicitante, cancha, hora_inicio, hora_fin, hora_solicitud):
        print(f"1. {solicitante.nombre} solicita reservar {cancha.nombre} "
              f"de {hora_inicio.strftime('%H:%M')} a {hora_fin.strftime('%H:%M')}")

        disponible = cancha.esta_disponible(hora_inicio, hora_fin)
        print(f"2. El sistema verifica disponibilidad de {cancha.nombre}: "
              f"{'disponible' if disponible else 'no disponible'}")

        if disponible:
            print("3. El sistema evalua la regla de prioridad del solicitante "
                  f"({'tiene prioridad' if solicitante.tiene_prioridad(hora_solicitud.time()) else 'sin prioridad'})")
            reserva = self._crear_reserva(solicitante, cancha, hora_inicio, hora_fin, hora_solicitud)
            return reserva

        reserva_en_conflicto = self._buscar_reserva_solapada(cancha, hora_inicio, hora_fin)
        tiene_prioridad = solicitante.tiene_prioridad(hora_solicitud.time())

        if reserva_en_conflicto is not None and tiene_prioridad and \
                not reserva_en_conflicto.solicitante.tiene_prioridad(reserva_en_conflicto.hora_solicitud.time()):
            print("3. El sistema evalua la regla de prioridad del solicitante: "
                  "tiene prioridad -> se genera conflicto")
            print("3a. El sistema genera un ConflictoReserva y lo deriva al administrador")
            self._contador_conflicto += 1
            conflicto = ConflictoReserva(
                id_=f"CFL-{self._contador_conflicto:03d}",
                reserva_existente=reserva_en_conflicto,
                solicitante_nuevo=solicitante,
                cancha=cancha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
            )
            self.conflictos.append(conflicto)
            return conflicto

        print("2a. El sistema informa la indisponibilidad de la cancha")
        return None

    def _buscar_reserva_solapada(self, cancha, hora_inicio, hora_fin):
        for r in self.reservas:
            if r.cancha is cancha and r.esta_activa():
                if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                    return r
        return None

    def _crear_reserva(self, solicitante, cancha, hora_inicio, hora_fin, hora_solicitud):
        self._contador_reserva += 1
        reserva = Reserva(
            id_=f"RES-{self._contador_reserva:03d}",
            solicitante=solicitante,
            cancha=cancha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            hora_solicitud=hora_solicitud,
        )
        cancha.ocupar_horario(hora_inicio, hora_fin)
        self.reservas.append(reserva)
        print(f"4. El sistema crea la reserva {reserva.id}")
        print(f"5. El sistema confirma la reserva a {solicitante.nombre}")
        return reserva

    def confirmar_reserva_directa(self, solicitante, cancha, hora_inicio, hora_fin, hora_solicitud):
        """Usado por ConflictoReserva.resolver('reasignar')."""
        return self._crear_reserva(solicitante, cancha, hora_inicio, hora_fin, hora_solicitud)

    def rechazar_solicitud(self, solicitante, cancha, hora_inicio, hora_fin):
        print(f"El sistema informa a {solicitante.nombre} que la solicitud para "
              f"{cancha.nombre} fue rechazada tras la resolucion del conflicto")

    def cancelar_reserva(self, reserva: Reserva, hora_actual):
        print(f"1. {reserva.solicitante.nombre} solicita cancelar la reserva {reserva.id}")
        tiempo_restante = reserva.hora_inicio - hora_actual
        print(f"2. El sistema calcula el tiempo restante hasta el inicio: {tiempo_restante}")
        print("3. El sistema determina el tipo de cancelacion segun la regla de 2 horas")
        estado_resultante = reserva.cancelar(hora_actual)
        etiqueta = "4a. NO_SHOW" if estado_resultante == EstadoReserva.NO_SHOW else "4b. CANCELADA"
        print(f"{etiqueta}: el sistema marca la reserva {reserva.id} como {estado_resultante.value}")
        print(f"5. El sistema confirma la cancelacion a {reserva.solicitante.nombre}")
        return estado_resultante
