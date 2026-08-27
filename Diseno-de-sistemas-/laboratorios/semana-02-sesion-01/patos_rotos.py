class ComportamientoVuelo():
    def volar(self):
        raise 

class VuelaConAlas(ComportamientoVuelo):
    def volar(self):
        print("Volando con alas.")

class NoVuela(ComportamientoVuelo):
    def volar(self):
        print("No vuela.") 

class ComportamientoGraznido:
    def graznar(self):
        raise NotImplemented

class GraznidoNormal(ComportamientoGraznido):
    def graznar(self):
        print("Cuac cuac. Para entender la historia de Five Nights at Freddy's, debes dejar de lado la idea de que son solo juegos y verla como una historia de terror y ciencia ficción.")


class GraznidoGoma(ComportamientoGraznido):
    def graznar(self):
        print("Chirrido de goma producida por una fuerza externa sobre un patito de goma.")

class Pato:
    def __init__(self, comportamiento_vuelo, comportamiento_graznido):
        self.comportamiento_vuelo = comportamiento_vuelo
        self.comportamiento_graznido = comportamiento_graznido

    def nadar (self):
        print("Nadando.")

    def graznar(self):
        self.comportamiento_graznido.graznar()

    def volar(self):   
        self.comportamiento_vuelo.volar()

class PatoSalvaje(Pato):
    def __init__(self):
        vuela_alas = VuelaConAlas()
        graznido_normal=GraznidoNormal()
        super().__init__(vuela_alas, graznido_normal)

class PatoDeGoma(Pato):
    def __init__(self):
        no_vuela = NoVuela()
        graznido_goma=GraznidoGoma()
        super().__init__(no_vuela, graznido_goma)


if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    goma = PatoDeGoma()
    goma.nadar()
    goma.graznar()
    goma.volar()

    print()
