class ValidadorHorario:
    def __init__(self, apertura, cierre):
        self.apertura = apertura
        self.cierre = cierre
       
    def horario_permitido(self, hora_inicio, hora_fin):
        if hora_inicio.day != hora_fin.day:
            return False
        inicio = hora_inicio.hour + hora_inicio.minute / 60
        fin = hora_fin.hour + hora_fin.minute / 60
        return inicio >= self.apertura and fin <= self.cierre


class ValidadorHorarioNorte(ValidadorHorario):
    def __init__(self):
        super().__init__(6, 22)
 

class ValidadorHorarioSur(ValidadorHorario):
    def __init__(self):
        super().__init__(7, 23)
 

class Notificador:
    def notificar(self, solicitante, mensaje):
        raise NotImplementedError
 

class NotificadorCorreo(Notificador):
    def notificar(self, solicitante, mensaje):
        print(f"[correo institucional -> {solicitante.nombre}] {mensaje}")
 

class NotificadorSMS(Notificador):
    def notificar(self, solicitante, mensaje):
        print(f"[SMS -> {solicitante.nombre}] {mensaje}")
 

class FabricaSede:
    def crear_validador(self):
        raise NotImplementedError
 
    def crear_notificador(self):
        raise NotImplementedError
 

class FabricaCampusNorte(FabricaSede):
    def crear_validador(self):
        return ValidadorHorarioNorte()
 
    def crear_notificador(self):
        return NotificadorCorreo()
 

class FabricaCampusSur(FabricaSede):
    def crear_validador(self):
        return ValidadorHorarioSur()
 
    def crear_notificador(self):
        return NotificadorSMS()


class Sede:
    def __init__(self, id_, nombre, fabrica):
        self.id = id_
        self.nombre = nombre
        self.validador = fabrica.crear_validador()
        self.notificador = fabrica.crear_notificador()

    def horario_permitido(self, hora_inicio, hora_fin):
        return self.validador.horario_permitido(hora_inicio, hora_fin)

    def notificar(self, solicitante, mensaje):
        self.notificador.notificar(solicitante, mensaje)