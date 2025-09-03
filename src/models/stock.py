class Stock:
    def __init__(self, stock_id, producto_id, cantidad_actual):
        self.stock_id = stock_id
        self.producto_id = producto_id
        self.cantidad_actual = cantidad_actual

    def __repr__(self):
        return f"<Stock Producto {self.producto_id}: {self.cantidad_actual}>"