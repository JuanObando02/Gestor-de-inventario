# 📦 Gestor de Inventario

Aplicación de escritorio desarrollada en **Python con Tkinter** para la gestión de inventarios.  
Permite registrar productos, categorías, movimientos de entrada y salida, así como consultar el stock actualizado.

## 🚀 Características

- ✅ Gestión de productos (crear, editar, eliminar).  
- ✅ Gestión de categorías de productos.  
- ✅ Control de stock mediante movimientos de:
  - Entrada
  - Salida
  - Inventario inicial
  - Ajustes  
- ✅ Importación de productos desde archivo **CSV**.  
- ✅ Reporte de inventario actualizado.  
- ✅ Interfaz gráfica intuitiva con **Tkinter**.  
- ✅ Base de datos local en **SQLite**.

## 🛠️ Tecnologías usadas

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interfaz gráfica
- [SQLite3](https://www.sqlite.org/index.html) - Base de datos embebida

## 📂 Estructura del proyecto
<pre>
│── MiniStock.py # Punto de entrada de la aplicación
│── src/
│ ├── controllers/ # Controladores de lógica de negocio
│ ├── database/ # Conexión y manejo de la base de datos SQLite
│ ├── models/ # Modelos de entidades
│ ├── utils/ # Utilidades y funciones auxiliares
│ └── views/ # Interfaces gráficas con Tkinter
│── data/ # Archivos de datos (ej: CSV de prueba)
│── requirements.txt # Dependencias necesarias
└── README.md # Documentación del proyecto </pre>

## ⚙️ Instalación y uso

1. Clona este repositorio:
   ```bash
   git clone https://github.com/JuanObando02/Gestor-de-inventario.git
   cd Gestor-de-inventario

2. Crea un entorno virtual (opcional, pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate   # En Linux/Mac
    venv\Scripts\activate      # En Windows

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

4. Ejecuta la aplicación:
    ```bash
    python MiniStock.py

5. Credenciales predeterminadas de Acceso:
    ```bash
    Usuario: admin
    Contraseña: 1234

- NOTA: **Tambien puedes descargar directamente el archivo MiniStock.zip que se encuentra en la carpeta /disk.**

## 📊 Formato CSV de importación

El archivo CSV debe contener las siguientes columnas:
- codigo, nombre, id_categoria, descripcion, precio, stock.

    Ejemplo:
    ```bash
    P001,Mouse Logitech,1,Mouse inalámbrico,50000,10
    P002,Teclado Redragon,1,Teclado mecánico,120000,5
## 📸 Capturas de pantalla

<p align="center">
    <img src="assets/images/Imagenes%20app/Captura%20de%20pantalla%202025-10-03%20131402.png" alt="Login" width="400">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura%20de%20pantalla%202025-10-03%20131415.png" alt="Pantalla principal" width="800">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura de pantalla 2025-10-03 132605.png" alt="Pantalla principal" width="800">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura de pantalla 2025-10-03 132621.png" alt="Pantalla principal" width="400">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura de pantalla 2025-10-03 132628.png" alt="Pantalla principal" width="400">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura de pantalla 2025-10-03 132945.png" alt="Pantalla principal" width="800">
</p>
<p align="center">
    <img src="assets/images/Imagenes%20app/Captura de pantalla 2025-10-03 132701.png" alt="Pantalla principal" width="800">
</p>

## 👨‍💻 Autores

 - Juan Sebastián Obando
 📧[GitHub](https://github.com/JuanObando02)

 - Erika Muñoz
 📧[GitHub](https://github.com/Emm3-z)

- Cristian Cifuentes
 📧[GitHub](https://github.com/CristianCifuentes01)

- Camilo Zapata
 📧[GitHub](https://github.com/juan-zapata12)