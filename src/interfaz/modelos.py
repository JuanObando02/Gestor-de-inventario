class Producto:
    def __init__(self, codigo, nombre, descripcion, cantidad, precio_unitario):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def calcular_valor_total(self):
        return self.cantidad * self.precio_unitario


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        if any(p.codigo == producto.codigo for p in self.productos):
            raise ValueError("Código duplicado.")
        self.productos.append(producto)

    def eliminar_producto(self, codigo):
        self.productos = [p for p in self.productos if p.codigo != codigo]

    def buscar_por_codigo(self, codigo):
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def calcular_valor_total(self):
        return sum(p.calcular_valor_total() for p in self.productos)
