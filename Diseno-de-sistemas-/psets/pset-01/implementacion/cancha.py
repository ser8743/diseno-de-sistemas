class Cancha:
    def __init__(self, id_: str, nombre: str, tipo: str, disponible: bool = True):
        self.id = id_
        self.nombre = nombre
        self.tipo = tipo
        self.disponible = disponible
        self._horarios_ocupados = []  

    def esta_disponible(self, hora_inicio, hora_fin) -> bool:
        if not self.disponible:
            return False
        for (ini, fin) in self._horarios_ocupados:
            if hora_inicio < fin and hora_fin > ini:
                return False
        return True

    def ocupar_horario(self, hora_inicio, hora_fin):
        self._horarios_ocupados.append((hora_inicio, hora_fin))

    def liberar_horario(self, hora_inicio, hora_fin):
        if (hora_inicio, hora_fin) in self._horarios_ocupados:
            self._horarios_ocupados.remove((hora_inicio, hora_fin))

    def marcar_no_disponible(self):
        self.disponible = False

    def marcar_disponible(self):
        self.disponible = True

    def __str__(self):
        return f"Cancha {self.nombre} ({self.tipo})"