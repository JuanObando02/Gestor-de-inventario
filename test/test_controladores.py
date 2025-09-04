from src.controllers import controlador_usuario, controlador_producto 

# para ejecutar este archivo
# python -m unittest test/test_controladores.py

#roles: admin, empleado
# 🔹 1. Probar inserción de un usuario
print("=== TEST USUARIOS ===")
controlador_usuario.insert_user("admin", "1234", "empleado")

user = controlador_usuario.get_user("admin")
print("Usuario recuperado:", user)

valid = controlador_usuario.validate_login("admin", "1234")
print("Login válido:", valid)

invalid = controlador_usuario.validate_login("admin", "mala_clave")
print("Login inválido:", invalid)

# 🔹 2. Probar inserción de productos
#codigo,nombre,descripcion,precio,categoria

print("\n=== TEST PRODUCTOS ===")
controlador_producto.add_product("P001", "Arroz 500g", "Paquete de arroz", 2500, 1)
controlador_producto.add_product("P002", "Azúcar 1kg", "Paquete de azúcar", 3000, 1)

productos = controlador_producto.get_all_products()
print("Productos en inventario:")
for p in productos:
    print(p)