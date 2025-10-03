class Recurso:
    def __init__(self, nombre, tipo, ubicacion):
        self.nombre = nombre
        self.tipo = tipo          # 'archivo', 'proceso', 'servicio', 'memoria'
        self.ubicacion = ubicacion

class SIN:
    def __init__(self):
        self.registry = {}  # nombre -> recurso

    def registrar(self, recurso):
        self.registry[recurso.nombre] = recurso
        print(f"[SIN] Recurso registrado: {recurso.nombre} ({recurso.tipo}) en {recurso.ubicacion}")

    def resolver(self, nombre):
        if nombre in self.registry:
            r = self.registry[nombre]
            print(f"[SIN] Recurso encontrado: {r.nombre} ({r.tipo}) en {r.ubicacion}")
            return r
        else:
            print(f"[SIN] Recurso {nombre} no encontrado")
            return None

if __name__ == "__main__":
    sin = SIN()

    # Registrar recursos
    sin.registrar(Recurso("archivo1", "archivo", "/mnt/data/archivo1.txt"))
    sin.registrar(Recurso("proceso1", "proceso", "PID:1234"))
    sin.registrar(Recurso("servicio_db", "servicio", "server1:3306"))

    # Resolver recursos
    sin.resolver("archivo1")
    sin.resolver("proceso1")
    sin.resolver("servicio_db")
    sin.resolver("recurso_no_existente")
