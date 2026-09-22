class Estudiante:
    def __init__(self, nombre):    
        self.nombre = nombre

class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre

class ReservaRegular:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante

    def confirmar(self):
        return "Reserva confirmada para: " + self.fecha

class ReservaPrioridad:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
            self.cancha = cancha
            self.fecha = fecha
            self.hora_inicio = hora_inicio
            self.hora_fin = hora_fin
            self.solicitante = solicitante

    def confirmar(self):
        return "Reserva con Prioridad confirmada para: " + self.fecha
    

class CreadorDeReservas():
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        raise NotImplementedError

class CreadorDeReservaRegular(CreadorDeReservas):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaRegular(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class CreadorDeReservaPrioritaria(CreadorDeReservas):
    def cear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaPrioridad(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class FabricaDeReservas():
    @staticmethod
    def elegir_creador(solicitante):
        if isinstance(solicitante, Estudiante):
            return CreadorDeReservaRegular()
        elif isinstance(solicitante, EquipoOficial):
            return CreadorDeReservaPrioritaria()

def reservar_desde_web(cancha, fecha, hora_inicio, hora_fin, solicitante):

        creador = FabricaDeReservas.elegir_creador(solicitante)
        reserva = creador.crear_reserva(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

        return reserva

def main():
    reserva_1 = reservar_desde_web(
        'Cancha de futbol',
        '2026-09-17',
        '18:00',
        '19:00',
        Estudiante ('Sergio')
    )

    print(reserva_1.confirmar())

    reserva_2 = reservar_desde_web(
        'Cancha de futbol',
        '2026-09-17',
        '18:00',
        '19:00',
        EquipoOficial ('Dragones')
    )

    print(reserva_2.confirmar())

if __name__ == "__main__":
    main()
