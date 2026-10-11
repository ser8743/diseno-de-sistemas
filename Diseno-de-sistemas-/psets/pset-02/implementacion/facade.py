from estado_reserva import EstadoReserva
from creador_reserva import obtener_creador
from reserva_recurrente import ReservaRecurrenteBuilder
from conflicto import ConflictoReserva

class ReservaFacade:
    def __init__(self):
        self.reservas = []
        self.conflictos = []
        self.bloqueos_aplicados = []
        self.contador_reserva = 0
        self.contador_conflicto = 0

    def siguiente_id(self):
        self.contador_reserva = self.contador_reserva + 1
        return "RES-" + str(self.contador_reserva)

    def buscar_reserva_solapada(self, cancha, hora_inicio, hora_fin):
        for r in self.reservas:
            if r.cancha is cancha and r.esta_activa():
                if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                    return r
        return None

    def reservar(self, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud):
        print(f"1. {solicitante.nombre} solicita reservar {cancha.nombre} ({sede.nombre}) "
              f"de {hora_inicio} a {hora_fin}")

        if solicitante.esta_suspendido(hora_solicitud):
            print(f"1a. Rechazada: {solicitante.nombre} esta suspendido hasta {solicitante.suspendido_hasta}")
            return None

        if not sede.horario_permitido(hora_inicio, hora_fin):
            print(f"1b. Rechazada: el horario queda fuera del rango permitido en {sede.nombre}")
            return None

        print(f"2. El sistema verifica disponibilidad de {cancha.nombre} en {sede.nombre}")
        disponible = cancha.verificar_y_reservar(hora_inicio, hora_fin)

        if not disponible:
            existente = self.buscar_reserva_solapada(cancha, hora_inicio, hora_fin)
            hay_conflicto = False
            if existente is not None:
                yo_tengo_prioridad = solicitante.tiene_prioridad(hora_inicio)
                el_tiene_prioridad = existente.solicitante.tiene_prioridad(existente.hora_inicio)
                if yo_tengo_prioridad and not el_tiene_prioridad:
                    hay_conflicto = True

            if hay_conflicto:
                self.contador_conflicto = self.contador_conflicto + 1
                conflicto = ConflictoReserva("CFL-" + str(self.contador_conflicto), existente, solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud)
                self.conflictos.append(conflicto)
                print("2b. Conflicto de prioridad: el sistema lo deriva al administrador (UC-04)")
                return conflicto

            print("2a. Rechazada: la cancha no esta disponible en ese horario")
            return None

        creador = obtener_creador(solicitante)
        reserva = creador.crear_reserva(self.siguiente_id(), solicitante, cancha, sede, hora_inicio, hora_fin, hora_solicitud)
        self.reservas.append(reserva)
        print(f"3. El sistema crea la reserva {reserva.id}")
        print(f"4. El sistema confirma y notifica la reserva a {solicitante.nombre}")
        sede.notificar(solicitante, f"Reserva {reserva.id} confirmada en {cancha.nombre}")
        return reserva

    def reservar_recurrente(self, solicitante, cancha, sede, fecha_inicio, hora_inicio, hora_fin, numero_semanas, hora_solicitud, equipo_prestado=None, notas=None):
        print(f"1. {solicitante.nombre} solicita una reserva recurrente de {cancha.nombre}")
        print(f"({numero_semanas} semanas, de {hora_inicio}:00 a {hora_fin}:00)")

        if solicitante.esta_suspendido(hora_solicitud):
            print(f"Precondicion no cumplida: {solicitante.nombre} esta suspendido")
            return None

        print("2. El sistema arma la solicitud con el Builder")
        builder = ReservaRecurrenteBuilder()
        builder.para(cancha, fecha_inicio, hora_inicio, hora_fin, solicitante)
        builder.con_numero_semanas(numero_semanas)
        if equipo_prestado is not None:
            builder.con_equipo_prestado(equipo_prestado)
        if notas is not None:
            builder.con_notas(notas)
        recurrente = builder.construir()

        print("3. El sistema verifica disponibilidad semana por semana")
        franjas = recurrente.fechas_semanas()

        cancha.tomar_lock()
        semana_en_conflicto = 0
        numero = 1
        for franja in franjas:
            if cancha.esta_disponible(franja[0], franja[1]):
                print(f"3.{numero} semana {numero} ({franja[0]}): disponible")
            else:
                print(f"3.{numero} semana {numero} ({franja[0]}): EN CONFLICTO")
                semana_en_conflicto = numero
                break
            numero = numero + 1

        if semana_en_conflicto > 0:
            cancha.soltar_lock()
            print(f"3a. El sistema NO registra ninguna reserva de la serie e indica ")
            print(f"la semana en conflicto: semana {semana_en_conflicto}")
            return None

        print("4. El sistema registra TODAS las reservas de la serie")
        for franja in franjas:
            cancha.ocupar_horario(franja[0], franja[1])
        cancha.soltar_lock()

        creador = obtener_creador(solicitante)
        for franja in franjas:
            reserva = creador.crear_reserva(self.siguiente_id(), solicitante, cancha, sede, franja[0], franja[1], hora_solicitud)
            self.reservas.append(reserva)
            recurrente.reservas.append(reserva)

        print(f"5. El sistema confirma y notifica la reserva recurrente a {solicitante.nombre} ")
        print(f"({len(recurrente.reservas)} semanas)")
        sede.notificar(solicitante, f"Reserva recurrente confirmada en {cancha.nombre} ({numero_semanas} semanas)")
        return recurrente

    def cancelar(self, reserva, hora_actual, administrativa=False, motivo=""):
        if administrativa:
            print(f"1. El administrador anula la reserva {reserva.id} ({motivo})")
        else:
            print(f"1. {reserva.solicitante.nombre} solicita cancelar la reserva {reserva.id}")

        print("2. El sistema aplica la politica de cancelacion correspondiente")
        if administrativa:
            estado = reserva.anular(hora_actual)
            print("2c. Estado = ANULADA (nunca penaliza)")
        else:
            estado = reserva.cancelar(hora_actual)
            if estado == EstadoReserva.NO_SHOW:
                print(reserva.politica_cancelacion.etiqueta + ". Estado = NO_SHOW")
            else:
                print("   Estado = CANCELADA")

        print("3. El sistema libera el horario de la cancha")

        if estado == EstadoReserva.NO_SHOW:
            print(f"3a. {reserva.solicitante.nombre} acumula un no-show del mes")
            suspendido = reserva.solicitante.registrar_no_show(hora_actual)
            if suspendido:
                print(f"3a-i. El sistema suspende a {reserva.solicitante.nombre} 7 dias ")
                print(f"(hasta {reserva.solicitante.suspendido_hasta})")

        print(f"4. El sistema notifica el resultado a {reserva.solicitante.nombre}")
        reserva.sede.notificar(reserva.solicitante, f"Tu reserva {reserva.id} quedo en estado {estado}")
        return estado

    def bloquear(self, plantilla, canchas_y_fechas, hora_actual):
        print(f"1. El administrador define el bloqueo {plantilla.motivo}")
        print(f"(motivo, franja, equipo: {plantilla.equipo_montaje})")
        print(f"2. El administrador indica las canchas y fechas donde replicarlo")
        print(f"({len(canchas_y_fechas)})")

        aplicados = []
        numero = 1
        for par in canchas_y_fechas:
            cancha = par[0]
            fecha = par[1]
            clon = plantilla.clonar(cancha, fecha)
            inicio = clon.inicio()
            fin = clon.fin()
            print(f"2.{numero} El sistema clona la plantilla para {cancha.nombre} el {fecha} (Prototype)")

            cancha.tomar_lock()
            for r in self.reservas:
                if r.cancha is cancha and r.esta_activa() and inicio < r.hora_fin and fin > r.hora_inicio:
                    print(f"2a. Hay una reserva existente en esa franja: {r.id} de {r.solicitante.nombre}")
                    r.anular(hora_actual)
                    print(f"2a-i. El sistema anula {r.id} (sin penalidad) y notifica al afectado")
                    r.sede.notificar(r.solicitante, f"Tu reserva {r.id} fue anulada por el bloqueo '{clon.motivo}'")
            cancha.ocupar_horario(inicio, fin)
            cancha.soltar_lock()

            print(f"3. El sistema aplica el bloqueo en {cancha.nombre} el {fecha}")
            self.bloqueos_aplicados.append(clon)
            aplicados.append(clon)
            numero = numero + 1

        print("4. El sistema confirma el bloqueo completo")
        return aplicados