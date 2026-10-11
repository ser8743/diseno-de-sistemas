psets/pset-02/
├── README.md
├── diagramas/
│   ├── Requerimientos.pdf        (entregable 1)
│   ├── ModeloDeDominio.pdf       (entregable 2)
│   ├── CasosdeUso.pdf            (entregable 3: diagrama de casos de uso)
│   ├── DiagramasDeFlujo.pdf      (entregable 3: flujos de UC-01, UC-02, UC-05 y UC-06)
│   ├── DiagramaRobustez.pdf      (entregable 4: Cancelar una reserva)
│   ├── DiagramaSecuencia.pdf     (entregable 5: Reservar una cancha)
│   ├── DiagramaActividad.pdf     (entregable 6: Reservar de forma recurrente)
│   └── MaquinaDeEstados.pdf      (entregable 7: estados de Reserva)
└── implementacion/
    ├── simulacion.py        # script con los 7 escenarios (+1 extra de UC-04)
    ├── facade.py            # ReservaFacade: reservar, reservar_recurrente, cancelar, bloquear
    ├── configuracion.py     # Singleton ConfiguracionReglas
    ├── sede.py              # Abstract Factory (FabricaCampusNorte / FabricaCampusSur)
    ├── creador_reserva.py   # Factory Method
    ├── reserva.py           # Reserva, ReservaRegular, ReservaEquipoOficial
    ├── estado_reserva.py    # EstadoReserva (CONFIRMADA, CANCELADA, NO_SHOW, ANULADA)
    ├── reserva_recurrente.py# Builder
    ├── bloqueo.py           # Prototype
    ├── politica_cancelacion.py  # Strategy (cancelación)
    ├── reglas_prioridad.py  # Strategy (prioridad)
    ├── solicitante.py, cancha.py, conflicto.py, administrador.py
    └── Dockerfile