from datetime import datetime, timedelta

class ReservaRecurrente:
    def __init__(self):
        self.cancha = None
        self.fecha_inicio = None
        self.hora_inicio = None
        self.hora_fin = None
        self.solicitante = None
        self.numero_semanas = None
        self.equipo_prestado = None
        self.notas = None
        self.reservas = []

    def fechas_semanas(self):
        franjas = []
        for i in range(self.numero_semanas):
            dia = self.fecha_inicio + timedelta(weeks=i)
            inicio = datetime(dia.year, dia.month, dia.day, self.hora_inicio, 0)
            fin = datetime(dia.year, dia.month, dia.day, self.hora_fin, 0)
            franjas.append((inicio, fin))
        return franjas


class ReservaRecurrenteBuilder:
    def __init__(self):
        self.reserva = ReservaRecurrente()

    def para(self, cancha, fecha_inicio, hora_inicio, hora_fin, solicitante):
        self.reserva.cancha = cancha
        self.reserva.fecha_inicio = fecha_inicio
        self.reserva.hora_inicio = hora_inicio
        self.reserva.hora_fin = hora_fin
        self.reserva.solicitante = solicitante

    def con_numero_semanas(self, numero):
        if numero < 2 or numero > 8:
            raise ValueError("El numero de semanas debe estar entre 2 y 8")
        self.reserva.numero_semanas = numero

    def con_equipo_prestado(self, equipo):
        self.reserva.equipo_prestado = equipo

    def con_notas(self, notas):
        self.reserva.notas = notas

    def construir(self):
        if self.reserva.cancha is None or self.reserva.numero_semanas is None:
            raise ValueError("Faltan datos obligatorios: cancha o numero de semanas")
        return self.reserva