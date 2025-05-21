# 🚀 **Proyecto de Gestión de Suministros Informáticos**

Aplicación web desarrollada con **Python, Flask y SQLite** para gestionar productos, ventas y proveedores de una empresa de suministros informáticos. El sistema incluye autenticación de usuarios (administradores y clientes), gráficas de ventas, y manejo de inventario.

## 📌 Características principales

### 1. Gestión de productos
- Alta, baja y modificación de productos.
- Visualización de lista con stock, precio y descripción.
- Relación con proveedores.

### 2. Control de stock
- Inventariado actualizado.
- Aviso de reposición cuando el stock está al 90%.

### 3. Autenticación y roles
- Registro y login con protección de contraseñas.
- Roles: usuario cliente y administrador.
- Vistas restringidas según rol.

### 4. Ventas
- Registro de ventas con selección de producto y cantidad.
- Historial de compras para usuarios.

### 5. Proveedores
- Registro de proveedores con nombre, email, teléfono, dirección, CIF, IVA y descuento.
- Eliminación y visualización en tabla.

### 6. Estadísticas y gráficas (solo administrador)
- 📊 **Ventas por producto**: gráfico de barras.
- 📈 **Ventas mensuales**: gráfico por mes.
- 📉 **Comparativa de beneficios**: grafico de beneficio segun precio de venta y costo proveedor.

### 7. Experiencia de usuario
- Interfaz intuitiva y responsiva.
- Mensajes de validación y confirmación.
- Navegación sencilla entre secciones.

## 🛠️ Tecnologías utilizadas
- Python 3
- Flask + Jinja2
- SQLite3 + SQLAlchemy ORM
- Matplotlib y Pandas
- HTML + CSS con uiGradients y Animate.css

## 🗂️ Estructura del proyecto
```plaintext
Proyecto_Suministros/
├── app/
│   ├── templates/            # HTML templates
│   ├── static/               # Archivos estáticos y gráficas
│   ├── routes.py             # Rutas principales
│   ├── auth.py               # Autenticación
│   ├── forms.py              # Formularios Flask-WTF
│   ├── models.py             # Modelos SQLAlchemy
├── config/                   # Configuraciones
├── instance/tienda.db        # Base de datos SQLite
├── crear_admin.py            # Script para crear admin inicial
├── db.py                     # Inicializa la base de datos
├── main.py                   # Lanza la app Flask
├── requirements.txt
└── README.md
```

## 🚀 Instalación
```plaintext
python3 -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
python db.py
python crear_admin.py
flask run
```
## 📝 Pendientes / por implementar
- Buscador de productos.
- Exportación de datos a CSV.

---

### 🎨 Mejora visual: Ilustración en la pantalla de inicio

Se agregó una imagen ilustrativa en la página principal (`index.html`) para transmitir visualmente el propósito de la aplicación (gestión de suministros informáticos).  
La imagen combina elementos tecnológicos como computadoras, gráficos y periféricos, manteniendo la armonía con el fondo degradado del sitio.

🔧 **Archivo modificado:**
- `app/templates/index.html`

📁 **Nuevo recurso:**
- `app/static/img_inicio.png`


© 2025 - Proyecto educativo y de práctica profesional en desarrollo web con Python.
