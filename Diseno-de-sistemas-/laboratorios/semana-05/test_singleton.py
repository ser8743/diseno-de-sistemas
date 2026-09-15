from singleton import GestorDeConfiguracion, reservar_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert reservar_permitida(config) is False

def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()

    assert reservar_permitida(config) is False 

# Singleton es una variable global entonces para que esta prueba pase se tiene que cambiar de vuelta a false el modo_mantenimiento