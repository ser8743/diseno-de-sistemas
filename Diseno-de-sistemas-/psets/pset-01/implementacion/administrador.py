class AdministradorComplejo:
    def __init__(self, id_: str, nombre: str):
        self.id = id_
        self.nombre = nombre

    def agregar_cancha(self, gestor, cancha):
        print(f"1. El administrador {self.nombre} solicita agregar la cancha {cancha.nombre}")
        print("2. El sistema valida los datos de la cancha")
        gestor.agregar_cancha(cancha)
        print("3. El sistema actualiza el catalogo de canchas")
        print(f"4. El sistema confirma que {cancha.nombre} fue agregada")

    def resolver_conflicto(self, gestor, conflicto, decision: str):
        print(f"1. El administrador {self.nombre} revisa el conflicto {conflicto.id}")
        print(f"2. El administrador decide la resolucion: '{decision}'")
        conflicto.resolver(decision, gestor)
        print("3. El sistema actualiza el estado de las reservas involucradas")
        print("4. El sistema notifica el resultado a los solicitantes")