from datetime import datetime

from solicitante import Estudiante, CapitanEquipo
from cancha import Cancha
from gestor_reservas import GestorReservas
from administrador import AdministradorComplejo
from reserva import EstadoReserva


def separador(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def main():
    gestor = GestorReservas()
    admin = AdministradorComplejo(id_="ADM-01", nombre="Carla Vega")

    separador("UC-03: Gestionar canchas (alta inicial del catalogo)")
    cancha_futbol = Cancha(id_="C-01", nombre="Cancha de Futbol 1", tipo="futbol")
    cancha_basquet = Cancha(id_="C-02", nombre="Cancha de Basquet 1", tipo="basquet")
    admin.agregar_cancha(gestor, cancha_futbol)
    admin.agregar_cancha(gestor, cancha_basquet)

    ana = Estudiante(id_="EST-01", nombre="Ana Torres")
    luis = Estudiante(id_="EST-02", nombre="Luis Paredes")
    marco = CapitanEquipo(id_="CAP-01", nombre="Marco Diaz", equipo="Halcones FC")

    separador("UC-01: Reservar cancha_caso normal (Ana, estudiante)")
    hora_solicitud_1 = datetime(2026, 9, 7, 10, 0)
    inicio_1 = datetime(2026, 9, 7, 16, 0)
    fin_1 = datetime(2026, 9, 7, 17, 0)
    reserva_ana = gestor.solicitar_reserva(ana, cancha_futbol, inicio_1, fin_1, hora_solicitud_1)

    separador("UC-01: Reservar cancha_conflicto de prioridad (Marco, capitan, antes de 18:00)")
    hora_solicitud_2 = datetime(2026, 9, 7, 10, 5)
    conflicto = gestor.solicitar_reserva(marco, cancha_futbol, inicio_1, fin_1, hora_solicitud_2)

    separador("UC-04: Resolver conflicto de reserva (el administrador reasigna a Marco)")
    admin.resolver_conflicto(gestor, conflicto, decision="reasignar")
   
    separador("UC-01: Reservar cancha_caso sin prioridad, sin conflicto (Luis, basquet)")
    hora_solicitud_3 = datetime(2026, 9, 7, 11, 0)
    inicio_3 = datetime(2026, 9, 7, 19, 0)
    fin_3 = datetime(2026, 9, 7, 20, 0)
    reserva_luis = gestor.solicitar_reserva(luis, cancha_basquet, inicio_3, fin_3, hora_solicitud_3)

    separador("UC-02: Cancelar reserva_caso normal (mas de 2 horas de anticipacion)")
    hora_actual_cancelacion_normal = datetime(2026, 9, 7, 15, 0)  
    gestor.cancelar_reserva(reserva_luis, hora_actual_cancelacion_normal)

    separador("UC-02: Cancelar reserva_caso no-show (menos de 2 horas de anticipacion)")
    hora_solicitud_4 = datetime(2026, 9, 7, 12, 0)
    inicio_4 = datetime(2026, 9, 7, 21, 0)
    fin_4 = datetime(2026, 9, 7, 22, 0)
    reserva_ana_2 = gestor.solicitar_reserva(ana, cancha_basquet, inicio_4, fin_4, hora_solicitud_4)
    hora_actual_no_show = datetime(2026, 9, 7, 20, 15)  
    gestor.cancelar_reserva(reserva_ana_2, hora_actual_no_show)

    separador("Resumen final de reservas")
    for r in gestor.reservas:
        print(r)

    separador("Resumen final de conflictos")
    for c in gestor.conflictos:
        print(c)


if __name__ == "__main__":
    main()