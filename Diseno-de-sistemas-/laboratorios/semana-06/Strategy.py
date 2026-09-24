from abc import ABC, abstractmethod

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass

class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base

class DescuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.80

class DescuentoaEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.95

class DescuentoEmpelado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.25

class Compra:
    def __init__(self, estrategiaDescuento):
        self.estrategiaDescuento = estrategiaDescuento

    def calcular_total(self, precio):
        return self.estrategiaDescuento.aplicar(precio)

def main():

    sin_descuento = SinDescuento()
    Vip_descuento = DescuentoVIP()
    estud_descuento = DescuentoaEstudiante()
    emplea_descuento = DescuentoEmpelado()

    compra_1 = Compra(sin_descuento)
    print(compra_1.calcular_total(100))

    compra_2 = Compra(Vip_descuento)
    print(compra_2.calcular_total(85))

    compra_3 = Compra(estud_descuento)
    print(compra_3.calcular_total(65))

    compra_4 = Compra(emplea_descuento)
    print(compra_4.calcular_total(78))

main()