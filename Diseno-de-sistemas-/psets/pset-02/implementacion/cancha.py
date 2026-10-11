import threading

class Cancha:
    def __init__(self, id_, nombre, tipo, sede):
        self.id = id_
        self.nombre = nombre
        self.tipo = tipo
        self.sede = sede
        self.disponible = True     
        self.horarios_ocupados = []
        self.lock = threading.Lock()

    def esta_disponible(self, hora_inicio, hora_fin):
        if not self.disponible:
            return False
        for horario in self.horarios_ocupados:
            inicio = horario[0]
            fin = horario[1]
            if hora_inicio < fin and hora_fin > inicio:
                return False
        return True

    def ocupar_horario(self, hora_inicio, hora_fin):
        self.horarios_ocupados.append((hora_inicio, hora_fin))

    def liberar_horario(self, hora_inicio, hora_fin):
        if (hora_inicio, hora_fin) in self.horarios_ocupados:
            self.horarios_ocupados.remove((hora_inicio, hora_fin))

    def verificar_y_reservar(self, hora_inicio, hora_fin):
        self.lock.acquire()
        disponible = self.esta_disponible(hora_inicio, hora_fin)
        if disponible:
            self.ocupar_horario(hora_inicio, hora_fin)
        self.lock.release()
        return disponible

    def tomar_lock(self):
        self.lock.acquire()

    def soltar_lock(self):
        self.lock.release()

    def marcar_no_disponible(self):
        self.disponible = False

    def marcar_disponible(self):
        self.disponible = True