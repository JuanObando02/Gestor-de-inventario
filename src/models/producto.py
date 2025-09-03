class Producto:
    def __init__(self, producto_id, categoria_id, codigo, nombre, descripcion, precio):
        self.producto_id = producto_id
        self.categoria_id = categoria_id
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        
    def __repr__(self):
        return f"<Product {self.nombre} - {self.precio} USD>"