class Inventario:
    def verificar(self, producto):
        print(f"Verificando el stock de: {producto}")
        return True

class Pago:
    def procesar(self, monto):
        print(f"Procesando pago: {monto}")
        return True

class Envio:
    def crear_envio(self, producto):
        print(f"Preparando el encio del producto: {producto}")

class Notifiacion:
    def crear_notificacion(self, notificacion):
        print(f"Se esta enviando el correo de notificacion: {notificacion}")


class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
        self.notificacion = Notifiacion()

    def comprar(self, producto, precio, notificacion):

        if not self.inventario.verificar(producto):
            print("No hay stock")
            return
        
        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return 

        self.envio.crear_envio(producto)
        print("Se ha realizado el envio")

        self.notificacion.crear_notificacion(notificacion)
        print("Se ha enviado el correo de notificacion, felicidades por su compra")

def main():

    tienda = TiendaFacade()

    tienda.comprar("Laptop", 1500, "Se ha enviado el correo de notificacion, felicidades por su compra")       

main()