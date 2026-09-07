psets/pset-01/
├── README.md
├── diagramas/
│   ├── Requerimientos.pdf              (Entregable 1)
│   ├── ModeloDominio.pdf               (Entregable 2)
│   ├── Casos de Uso.pdf                (Entregable 3 — diagrama de casos de uso)
│   └── *.png                           (versiones en imagen de los diagramas, de respaldo)
└── implementacion/
    ├── Diagrama de Flujo_Casos de Uso.pdf  (Entregable 4 — flujo de cada caso de uso)
    ├── solicitante.py        # Solicitante, Estudiante, CapitanEquipo
    ├── reglas_prioridad.py   # ComportamientoPrioridad, PrioridadAntesDe18h, SinPrioridad
    ├── cancha.py             # Cancha
    ├── reserva.py            # Reserva, EstadoReserva
    ├── conflicto.py          # ConflictoReserva
    ├── gestor_reservas.py    # GestorReservas (orquestador)
    ├── administrador.py      # AdministradorComplejo
    ├── simulacion.py         # Script principal de simulación
    └── Dockerfile