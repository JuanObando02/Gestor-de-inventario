class Producto:
    
    #Constructor de la clase Producto

    def __init__(self, codigo, nombre, descripcion, cantidad, precio_unitario):
        if not all([codigo, nombre, cantidad is not None, precio_unitario is not None]):
            raise ValueError("Todos los campos obligatorios deben tener un valor.")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero no negativo.")
        if not isinstance(precio_unitario, (int, float)) or precio_unitario < 0:
            raise ValueError("El precio debe ser un número no negativo.")
        
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
        """Agrega un producto al inventario si no existe ya un producto con el mismo código."""
        if any(p.codigo == producto.codigo for p in self.productos):
            raise ValueError(f"El producto con código '{producto.codigo}' ya existe.")
        self.productos.append(producto)

    def eliminar_producto(self, codigo):
        """Elimina un producto del inventario por su código."""
        self.productos = [p for p in self.productos if p.codigo != codigo]

    def buscar_producto(self, codigo):
        """Busca y retorna un producto por su código."""
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None