import json
from modelos import Producto, Inventario


class Persistencia:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo

    def guardar(self, inventario: Inventario):
        data = [p.__dict__ for p in inventario.productos]
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self):
        inventario = Inventario()
        try:
            with open(self.archivo, "r") as f:
                data = json.load(f)
                for item in data:
                    inventario.agregar_producto(
                        Producto(**item)
                    )
        except FileNotFoundError:
            pass
        return inventario
