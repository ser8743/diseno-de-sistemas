import threading
from datetime import datetime

from sede import Sede, FabricaCampusNorte, FabricaCampusSur
from solicitante import Estudiante, CapitanEquipo
from cancha import Cancha
from facade import ReservaFacade
from administrador import AdministradorComplejo
from bloqueo import Bloqueo


def separador(titulo):
    print("\n" + "=" * 74)
    print(titulo)
    print("=" * 74)
 

def main():
    facade = ReservaFacade()
    admin = AdministradorComplejo("ADM-01", "Carla Vega")

    norte = Sede("SEDE-N", "Campus Norte", FabricaCampusNorte())
    sur = Sede("SEDE-S", "Campus Sur", FabricaCampusSur())

    canchas = []
    cancha_n1 = Cancha("C-N1", "Cancha Futbol Norte", "futbol", norte)
    cancha_s1 = Cancha("C-S1", "Cancha Basquet Sur", "basquet", sur)
    admin.agregar_cancha(canchas, cancha_n1)
    admin.agregar_cancha(canchas, cancha_s1)

    ana = Estudiante("EST-01", "Ana Torres")
    luis = Estudiante("EST-02", "Luis Paredes")
    marco = CapitanEquipo("CAP-01", "Marco Diaz", "Halcones FC")
    sofia = CapitanEquipo("CAP-02", "Sofia Reyes", "Cobras Voley")

    separador("Escenario 1: una reserva en cada sede")
    facade.reservar(ana, cancha_n1, norte,
                    datetime(2026, 11, 2, 10, 0), datetime(2026, 11, 2, 11, 0),
                    datetime(2026, 11, 1, 9, 0))
    facade.reservar(sofia, cancha_s1, sur,
                    datetime(2026, 11, 2, 8, 0), datetime(2026, 11, 2, 9, 0),
                    datetime(2026, 11, 1, 9, 5))

    separador("Escenario 2: reserva rechazada por horario fuera del rango de su sede")
    facade.reservar(luis, cancha_n1, norte,
                    datetime(2026, 11, 2, 22, 30), datetime(2026, 11, 2, 23, 30),
                    datetime(2026, 11, 1, 9, 10))

    separador("Escenario 3a: reserva recurrente exitosa (Marco, 3 semanas)")
    facade.reservar_recurrente(marco, cancha_n1, norte,
                               datetime(2026, 11, 9), 17, 18, 3,
                               datetime(2026, 11, 1, 9, 20),
                               ["balones", "chalecos"], "Entrenamiento oficial Halcones FC")

    separador("Escenario 3b: reserva recurrente rechazada por conflicto en una semana")
    facade.reservar(ana, cancha_n1, norte,
                    datetime(2026, 11, 23, 19, 0), datetime(2026, 11, 23, 20, 0),
                    datetime(2026, 11, 1, 9, 22))
    print()
    facade.reservar_recurrente(luis, cancha_n1, norte,
                               datetime(2026, 11, 16), 19, 20, 3,
                               datetime(2026, 11, 1, 9, 25))

    separador("Escenario 4a: cancelacion de estudiante a tiempo")
    r1 = facade.reservar(ana, cancha_n1, norte,
                         datetime(2026, 11, 4, 16, 0), datetime(2026, 11, 4, 17, 0),
                         datetime(2026, 11, 1, 9, 30))
    facade.cancelar(r1, datetime(2026, 11, 4, 10, 0))    

    separador("Escenario 4b: capitan cancela con menos de 24 horas -> no-show")
    r2 = facade.reservar(marco, cancha_n1, norte,
                         datetime(2026, 11, 5, 17, 0), datetime(2026, 11, 5, 18, 0),
                         datetime(2026, 11, 1, 9, 35))
    facade.cancelar(r2, datetime(2026, 11, 5, 8, 0))      

    separador("Escenario 4c: el administrador anula (sin penalidad)")
    r3 = facade.reservar(luis, cancha_s1, sur,
                         datetime(2026, 11, 6, 10, 0), datetime(2026, 11, 6, 11, 0),
                         datetime(2026, 11, 1, 9, 40))
    facade.cancelar(r3, datetime(2026, 11, 6, 9, 0), True, "mantenimiento programado")

    separador("Escenario 5: un solicitante llega a 3 no-shows y queda suspendido")
    for dia in [9, 16, 23]:
        inicio = datetime(2026, 11, dia, 20, 0)
        fin = datetime(2026, 11, dia, 21, 0)
        solicitud = datetime(2026, 11, dia - 1, 20, 0)
        r = facade.reservar(luis, cancha_s1, sur, inicio, fin, solicitud)
        facade.cancelar(r, datetime(2026, 11, dia, 19, 30))

    print()
    facade.reservar(luis, cancha_s1, sur,
                    datetime(2026, 11, 30, 10, 0), datetime(2026, 11, 30, 11, 0),
                    datetime(2026, 11, 24, 9, 0))

    separador("Escenario 6: bloqueo clonado en dos canchas (una con reserva existente)")
    facade.reservar(ana, cancha_s1, sur,
                    datetime(2026, 12, 1, 9, 0), datetime(2026, 12, 1, 10, 0),
                    datetime(2026, 11, 25, 9, 0))
    plantilla = Bloqueo("Torneo intercampus", 9, 12, ["mallas", "marcadores"])
    clones = admin.definir_bloqueo(facade, plantilla,
                                   [(cancha_n1, datetime(2026, 12, 1)),
                                    (cancha_s1, datetime(2026, 12, 1))],
                                   datetime(2026, 11, 28, 9, 0))

    clones[0].equipo_montaje.append("tarima")
    print()
    print("Prototype: equipo del clon 1 =", clones[0].equipo_montaje)
    print("Prototype: equipo del clon 2 =", clones[1].equipo_montaje)
    print("Prototype: equipo de la plantilla =", plantilla.equipo_montaje, "(no cambio)")

    separador("Escenario 7: dos hilos reservan la misma cancha y franja al mismo tiempo")
    resultados = []

    def intentar_reservar(solicitante):
        r = facade.reservar(solicitante, cancha_n1, norte,
                            datetime(2026, 12, 7, 15, 0), datetime(2026, 12, 7, 16, 0),
                            datetime(2026, 12, 1, 9, 0))
        resultados.append(r)

    hilo_a = threading.Thread(target=intentar_reservar, args=(ana,))
    hilo_b = threading.Thread(target=intentar_reservar, args=(luis,))
    hilo_a.start()
    hilo_b.start()
    hilo_a.join()
    hilo_b.join()

    confirmadas = 0
    for r in resultados:
        if r is not None:
            confirmadas = confirmadas + 1
    print()
    print("Resultado de la carrera:", confirmadas, "hilo(s) obtuvieron confirmacion")

    separador("Escenario 8 (extra, viene del PSet 1): conflicto de prioridad resuelto por el admin")
    facade.reservar(ana, cancha_n1, norte,
                    datetime(2026, 12, 9, 10, 0), datetime(2026, 12, 9, 11, 0),
                    datetime(2026, 12, 1, 9, 0))
    conflicto = facade.reservar(marco, cancha_n1, norte,
                                datetime(2026, 12, 9, 10, 0), datetime(2026, 12, 9, 11, 0),
                                datetime(2026, 12, 1, 9, 5))
    admin.resolver_conflicto(facade, conflicto, "reasignar", datetime(2026, 12, 2, 9, 0))

    separador("Resumen final de reservas")
    for r in facade.reservas:
        print(r.resumen())

    separador("Resumen final de conflictos")
    for c in facade.conflictos:
        print("ConflictoReserva", c.id, "en", c.cancha.nombre, "->", c.resolucion)

    separador("Resumen de suspensiones")
    for s in [ana, luis, marco, sofia]:
        if s.suspendido_hasta is None:
            print(s.nombre + ": sin suspension")
        else:
            print(s.nombre + ": suspendido hasta", s.suspendido_hasta)


if __name__ == "__main__":
    main()