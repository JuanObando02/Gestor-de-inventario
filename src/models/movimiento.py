class Movimiento:
    def __init__(self, movimiento_id, producto_id, tipo, cantidad, fecha, usuario_id):
        self.movimiento_id = movimiento_id
        self.producto_id = producto_id
        self.tipo = tipo  # "entrada" o "salida"
        self.cantidad = cantidad
        self.fecha = fecha
        self.usuario_id = usuario_id

    def __repr__(self):
        return f"<Movement {self.tipo} {self.cantidad} producto {self.producto_id}>"
