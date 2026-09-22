import copy

class Computadora:
    def __inti__(self):
        self.cpu = None
        self.ram = None
        self.disco = None
        self.gpu = None
        self.wifi = None


    def mostrar(self):
        print("CPU: ", self.cpu)
        print("Ram: ", self.ram)
        print("Disco: ", self.disco)
        print("GPU: ", self.gpu)
        print("Wifi: ", self.wifi)

    def clonar(self): 
        return copy.deepcopy(self)

class ComputadoraBuilder:
    def __init__(self):
        self.computadora = Computadora()

    def add_cpu(self, cpu):
        self.computadora.cpu = cpu
        return self

    def add_ram(self, ram):
        self.computadora.ram = ram
        return self 

    def add_disco(self, disco):
        self.computadora.disco = disco
        return self

    def add_gpu(self, gpu):
        self.computadora.gpu = gpu
        return self

    def add_wifi(self, wifi):
        self.computadora.wifi= wifi
        return self

    def builder(self):
        return self.computadora


def main():

    pc_builder = ComputadoraBuilder()

    pc_builder = pc_builder.add_ram(4).add_gpu(18).add_wifi(2)

    pc_gaming = pc_builder.add_disco(1).add_cpu(20).builder()

    pc_gaming.mostrar()

    pc_work = pc_gaming.clonar()

    pc_work.ram = 64

    pc_work.mostrar()

main()    