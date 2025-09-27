from src.controllers import controlador_producto, controlador_movimiento
import random
# para ejecutar este archivo
# python -m unittest test/insert_product.py
#roles: admin, empleado

def inicializar_stock(id_usuario = 1):
    productos = controlador_producto.get_all_products()

    for p in productos:
        # asignar un stock inicial aleatorio entre 50 y 200
        cantidad_inicial = random.randint(50, 200)

        try:
            controlador_movimiento.registrar_movimiento(
                id_producto=p["id_producto"],
                id_usuario=id_usuario,
                tipo="inicial",
                cantidad=cantidad_inicial
            )
            print(f"✅ Stock inicial {cantidad_inicial} registrado para {p['codigo']} - {p['nombre']}")
        except Exception as e:
            print(f"❌ Error con {p['codigo']} - {p['nombre']}: {e}")


print("\n=== TEST PRODUCTOS ===")

controlador_producto.add_product("P003", "Aceite Vegetal 1L", "Botella de aceite vegetal", 8500, 1)
controlador_producto.add_product("P004", "Arroz Blanco 5kg", "Paquete de arroz blanco", 18000, 1)
controlador_producto.add_product("P005", "Fríjol Rojo 1kg", "Bolsa de fríjoles rojos", 6000, 1)
controlador_producto.add_product("P006", "Sal Refinada 1kg", "Paquete de sal", 2500, 1)

controlador_producto.add_product("P007", "Gaseosa 1.5L", "Botella de gaseosa sabor cola", 4200, 2)
controlador_producto.add_product("P008", "Jugo de Naranja 1L", "Jugo natural en caja", 5200, 2)
controlador_producto.add_product("P009", "Agua Mineral 600ml", "Botella de agua mineral", 1800, 2)
controlador_producto.add_product("P010", "Cerveza 330ml", "Botella de cerveza rubia", 3500, 2)

controlador_producto.add_product("P011", "Leche Entera 1L", "Caja de leche entera", 4200, 3)
controlador_producto.add_product("P012", "Yogurt Natural 200g", "Vaso de yogurt natural", 2500, 3)
controlador_producto.add_product("P013", "Queso Mozzarella 250g", "Bloque de queso mozzarella", 9500, 3)
controlador_producto.add_product("P014", "Mantequilla 250g", "Paquete de mantequilla", 6500, 3)

controlador_producto.add_product("P015", "Papas Fritas 150g", "Bolsa de papas fritas", 3500, 4)
controlador_producto.add_product("P016", "Chocolate Barra 100g", "Barra de chocolate", 4200, 4)
controlador_producto.add_product("P017", "Galletas Surtidas 300g", "Caja de galletas surtidas", 5600, 4)
controlador_producto.add_product("P018", "Chicle Menta 10u", "Paquete de chicles", 1500, 4)

controlador_producto.add_product("P019", "Pan Tajado 500g", "Bolsa de pan tajado", 4800, 5)
controlador_producto.add_product("P020", "Croissant 80g", "Croissant de mantequilla", 2500, 5)
controlador_producto.add_product("P021", "Pan Integral 500g", "Pan integral tajado", 5200, 5)
controlador_producto.add_product("P022", "Bollo de Arequipe 90g", "Pan relleno de arequipe", 2800, 5)

controlador_producto.add_product("P023", "Banano 1kg", "Mano de bananos frescos", 3800, 6)
controlador_producto.add_product("P024", "Manzana Roja 1kg", "Manzanas rojas frescas", 5200, 6)
controlador_producto.add_product("P025", "Tomate Chonto 1kg", "Tomates frescos", 4000, 6)
controlador_producto.add_product("P026", "Papa Criolla 1kg", "Papa criolla fresca", 3500, 6)

controlador_producto.add_product("P027", "Pechuga de Pollo 1kg", "Filete de pechuga fresca", 12500, 7)
controlador_producto.add_product("P028", "Carne Molida 1kg", "Carne molida de res", 14500, 7)
controlador_producto.add_product("P029", "Chorizo Antioqueño 500g", "Paquete de chorizos", 9800, 7)
controlador_producto.add_product("P030", "Jamón de Cerdo 250g", "Paquete de jamón rebanado", 7500, 7)

controlador_producto.add_product("P031", "Detergente Polvo 1kg", "Bolsa de detergente en polvo", 9200, 8)
controlador_producto.add_product("P032", "Jabón Líquido 1L", "Botella de jabón líquido", 10500, 8)
controlador_producto.add_product("P033", "Cloro 1L", "Botella de cloro", 2800, 8)
controlador_producto.add_product("P034", "Esponja Multiuso", "Paquete de 3 esponjas", 3500, 8)

controlador_producto.add_product("P035", "Shampoo 400ml", "Botella de shampoo", 11800, 9)
controlador_producto.add_product("P036", "Jabón de Tocador 3u", "Caja de jabones de tocador", 6200, 9)
controlador_producto.add_product("P037", "Crema Dental 100ml", "Tubo de crema dental", 5200, 9)
controlador_producto.add_product("P038", "Desodorante Roll-on", "Desodorante personal", 7800, 9)

controlador_producto.add_product("P039", "Pilas AA 4u", "Paquete de pilas alcalinas", 8900, 10)
controlador_producto.add_product("P040", "Linterna LED", "Linterna portátil de mano", 14500, 10)
controlador_producto.add_product("P041", "Cuaderno Rayado 100h", "Cuaderno escolar", 6500, 10)
controlador_producto.add_product("P042", "Bolígrafo Azul", "Paquete de 10 bolígrafos", 7200, 10)

controlador_producto.add_product("P043", "Escoba Plástica", "Escoba de cerdas plásticas", 12500, 11)
controlador_producto.add_product("P044", "Trapero Microfibra", "Trapero con paño de microfibra", 11500, 11)
controlador_producto.add_product("P045", "Balde 10L", "Balde plástico resistente", 9500, 11)
controlador_producto.add_product("P046", "Trapeador Repuesto", "Paño de repuesto para trapero", 7800, 11)

controlador_producto.add_product("P047", "Bombillo LED 12W", "Bombillo de luz blanca", 7200, 12)
controlador_producto.add_product("P048", "Extensión Eléctrica 3m", "Cable con 3 tomas", 14800, 12)
controlador_producto.add_product("P049", "Vaso de Vidrio 6u", "Juego de vasos", 16800, 12)
controlador_producto.add_product("P050", "Silla Plástica", "Silla plástica apilable", 24500, 12)

controlador_producto.add_product("P051", "Harina de Trigo 1kg", "Paquete de harina de trigo", 4200, 1)
controlador_producto.add_product("P052", "Atún en Agua 160g", "Lata de atún en agua", 5200, 1)
inicializar_stock()


