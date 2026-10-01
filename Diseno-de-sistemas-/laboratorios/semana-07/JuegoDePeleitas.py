from abc import ABC, abstractmethod
import random

#Datos
class Personaje():
    def __init__(self, nombre, ataque_base, vida):
        self.nombre = nombre
        self.ataque_base = ataque_base
        self.vida = vida
        self.habilidad = AtaqueNormal()

#Comportamientos
    def recibir_dano(self, dano):
        self.vida = self.vida - dano
        if(self.vida < 0 ):
            self.vida = 0

    def sigue_vivo(self):
        return self.vida > 0

    def atacar(self):
        return self.habilidad.dano(self.ataque_base)
          
    def cambiar_ataque(self, nueva_habilidad):
        self.habilidad = nueva_habilidad

#Personajes Fantasia
class Guerrero(Personaje):
    def __init__(self):
        super().__init__("Arturo", 300, 750)

class Mago(Personaje):
    def __init__(self):
        super().__init__("Alicia", 700, 550)

class Manticora(Personaje):
    def __init__(self):
        super().__init__("Manticora", 370, 600)

class Dragon(Personaje):
    def __init__(self):
        super().__init__("Dracaris", 500, 1200)

#Personajes Ciencia Ficcion
class Alien(Personaje):
    def __init__(self):
        super().__init__("Apex", 280, 900)

class Cegador(Personaje):
    def __init__(self):
        super().__init__("Cegador", 300, 400)

class Soldado(Personaje):
    def __init__(self):
        super().__init__("Aquiles Baila", 450, 650)

class Tanque(Personaje):
    def __init__(self):
        super().__init__("Zoyla Vaca", 500, 990)


#Factory
class PersonajeFactory():
    @staticmethod
    def crear(tipo):
        tipos = {
            "guerrero" : Guerrero,
            "dragon" : Dragon,
            "soldado" : Soldado,
            "alien" : Alien,
        }
        if tipo not in tipos:
            raise ValueError(f"Personaje desconocido {tipo}")
        return tipos[tipo]()


#Abstract Factory
class MundoFactory(ABC):
    @abstractmethod
    def jugador(self):
        pass
    @abstractmethod
    def enemigo(self):
        pass
    
class FantasyFactory(MundoFactory):
    def jugador(self):
        return PersonajeFactory.crear("guerrero")

    def enemigo(self):
        return PersonajeFactory.crear("dragon")

class ScifiFactory(MundoFactory):

    def jugador(self):
        return PersonajeFactory.crear("soldado")
    
    def enemigo(self):
        return PersonajeFactory.crear("alien")


#Strategy
class Ataque(ABC):
    @abstractmethod
    def dano(self, dano_base):
        pass

class AtaqueNormal(Ataque):
    def dano(self, dano_base):
        return dano_base

class AtaqueFuerte(Ataque):
    def dano(self, dano_base):
        return dano_base * 1.5

class Combate:
    def __init__(self, eficaciaAtaque):
        self.eficaciaAtaque = eficaciaAtaque

    def calcular_total_dano(self, dano):
        return self.eficaciaAtaque.dano(dano)


#Singelton 
class GameConfig():
    _objeto = None

    def __new__(configuracion):
        if configuracion._objeto is None:
            configuracion._objeto = super().__new__(configuracion)
            configuracion._objeto.dificultad = "Media"
            configuracion._objeto.turnos = 5
        return configuracion._objeto

a = GameConfig()
b = GameConfig()
a.turnos = 6

#Facade
class GameFacade:
    def __init__(self):
        self.config = GameConfig()
        self.fabrica = None
        self.jugador = None
        self.enemigo = None
 
    def crear_mundo(self):
        print("Elige un mundo:")
        print("1. Fantasia")
        print("2. Ciencia ficcion")
        while True:
            opcion = input("Opcion: ")
            if opcion == "1":
                self.fabrica = FantasyFactory()
                break
            if opcion == "2":
                self.fabrica = ScifiFactory()
                break
            print("Opcion no valida")
 
    def crear_personajes(self):
        self.jugador = self.fabrica.jugador()
        self.enemigo = self.fabrica.enemigo()
        print()
        print(f"Jugador: {self.jugador.nombre} (vida {self.jugador.vida})")
        print()
        print(f"Enemigo: {self.enemigo.nombre} (vida {self.enemigo.vida})")
 
    
    def elegir_estrategia(self):
        print("Elige tu ataque: 1. Normal  2. Fuerte")
        while True:
            opcion = input("Opcion: ")
            if opcion == "1":
                self.jugador.cambiar_ataque(AtaqueNormal())
                return
            if opcion == "2":
                self.jugador.cambiar_ataque(AtaqueFuerte())
                return
            print("Opcion no valida")
 
    def estrategia_enemigo(self):
        if self.config.dificultad == "Facil":
            return AtaqueNormal()
        if self.config.dificultad == "Dificil":
            return AtaqueFuerte()
        return random.choice([AtaqueNormal(), AtaqueFuerte()])
 
    
    def turno(self, numero):
        print()
        print(f"--- Turno {numero} ---")
        print()
 
        self.elegir_estrategia()
        dano = int(self.jugador.atacar())
        self.enemigo.recibir_dano(dano)
        print(f"{self.jugador.nombre} ataca y hace {dano} de dano. ")
        print(f"Vida de {self.enemigo.nombre}: {self.enemigo.vida}")
 
        if not self.enemigo.sigue_vivo():
            return
 
        self.enemigo.cambiar_ataque(self.estrategia_enemigo())
        dano = int(self.enemigo.atacar())
        self.jugador.recibir_dano(dano)
        print(f"{self.enemigo.nombre} responde y hace {dano} de dano. ")
        print(f"Vida de {self.jugador.nombre}: {self.jugador.vida}")
 
    def ejecutar_turnos(self):
        for numero in range(1, self.config.turnos + 1):
            self.turno(numero)
            if not self.jugador.sigue_vivo() or not self.enemigo.sigue_vivo():
                break
 

    def determinar_ganador(self):
        print()
        print("=== Fin del combate ===")
        print()

        if not self.enemigo.sigue_vivo():
            print(f"Gana {self.jugador.nombre}!")
        elif not self.jugador.sigue_vivo():
            print(f"Gana {self.enemigo.nombre}.")
        elif self.jugador.vida > self.enemigo.vida:
            print(f"Se acabaron los turnos.Gana {self.jugador.nombre} por tener mas vida.")
        elif self.jugador.vida < self.enemigo.vida:
            print(f"Se acabaron los turnos.Gana {self.enemigo.nombre} por tener mas vida.")
        else:
            print("Se acabaron los turnos.Empate.")
 
    def iniciar(self):
        self.crear_mundo()
        self.crear_personajes()
        self.ejecutar_turnos()
        self.determinar_ganador()

