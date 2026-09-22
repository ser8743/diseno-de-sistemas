from abc import ABC, abstractmethod

class Boton(ABC):
    @abstractmethod
    def renderizar(self):
        pass
    

class Menu(ABC):
    @abstractmethod
    def renderizar(self):   
        pass    

class ChecBox(ABC):
    @abstractmethod
    def crear_CheckBox(self):
        pass

class WindowsCheckBox(ChecBox):
    def crear_CheckBox(self):
        print("Check_box estilo Windows...")

class MacCheckBox(ChecBox):
    def crear_CheckBox(self):
        print("Check_box estilo Mac...")

class BotonWindows(Boton):
    def renderizar(self):
        print("Boton estilo windows...")

class MenuWindows(Menu):
    def renderizar(self):
        print("Menu estilo Windows...")

class BotonMac(Boton):
    def renderizar(self):
        print("Boton estilo MAC...")

class MenuMac(Menu):
    def renderizar(self):
        print("Menu estilo MAC...")


class UIFactoryABC(ABC):
    @abstractmethod
    def crear_boton(self):
        pass
    def crear_menu(self):
        pass
    def crear_checkBox(self):
        pass

class WindowsFactory(UIFactoryABC):
    def crear_boton(self):
        return BotonWindows()
    def crear_menu(self):
        return MenuWindows()
    def crear_checkBox(self):
        return WindowsCheckBox()

class MacFactory(UIFactoryABC):
    def crear_boton(self):
        return BotonMac()
    def crear_menu(self):
        return MenuMac()
    def crear_checkBox(self):
        return MacCheckBox()


def crear_UI(factory: UIFactoryABC):
    boton = factory.crear_boton()
    menu = factory.crear_menu()
    checBox = factory.crear_checkBox()

    boton.renderizar()
    menu.renderizar()
    checBox.crear_CheckBox()
    

def main():

    sistema = 'Windows'

    if sistema == 'Windows':
        factory = WindowsFactory()
    elif sistema == 'Mac':
        factory = MacFactory()

    crear_UI(factory)

main()