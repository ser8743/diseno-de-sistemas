class ConfiguracionReglas:
    instancia = None

    def __init__(self):
        self.hora_limite_prioridad = 18
        self.ventana_cancelacion_estudiante_horas = 2
        self.ventana_cancelacion_capitan_horas = 24
        self.limite_no_shows_mes = 3
        self.dias_suspension = 7

    @staticmethod
    def obtener_instancia():
        if ConfiguracionReglas.instancia is None:
            ConfiguracionReglas.instancia = ConfiguracionReglas()
        return ConfiguracionReglas.instancia
 