# Vehiculo --> mueva --> mover()

# Auto --> mueve por carretera
# Bote --> mueve por mar
# Avion --> mueve por aire 

class ComportamientoVehiculo():
    def movimiento(self):
        raise

class seMueveTierra(ComportamientoVehiculo):
    def movimiento(self):
        print("Conduciendo por carretera.")

class seMueveMar(ComportamientoVehiculo):
    def movimiento(self):
        print("Navegando por agua.")

class seMueveAire(ComportamientoVehiculo):
    def movimiento(self):
        print("Volando por aire.")

class Vehiculo():
    def __init__(self, comportamiento_vehiculo):
        self.comportamiento_vehiculo = comportamiento_vehiculo

    def movimiento(self):
        self.comportamiento_vehiculo.movimiento()

class Carro(Vehiculo):
    def __init__(self):
        conduce_tierra = seMueveTierra()
        super().__init__(conduce_tierra)

class Bote(Vehiculo):
    def __init__(self):
        conduce_mar = seMueveMar()
        super().__init__(conduce_mar)

class Avion(Vehiculo):
    def __init__(self):
        conduce_aire = seMueveAire()
        super().__init__(conduce_aire)

if __name__ == "__main__":
    tierra=Carro()
    tierra.movimiento()

    print()

    mar=Bote()
    mar.movimiento()

    print()

    aire=Avion()
    aire.movimiento()

    print()