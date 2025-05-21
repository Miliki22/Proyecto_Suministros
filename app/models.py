from . import db
from flask_login import UserMixin
from datetime import datetime

# Tabla de usuarios con roles (admin o user)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)        
    username = db.Column(db.String(100), nullable=False, unique=True)   # Nombre del usuario unico   
    email = db.Column(db.String(150), nullable=False, unique=True)      # Email unico
    password = db.Column(db.String(200), nullable=False)                # Contraseña hasheada
    role = db.Column(db.String(10), nullable=False, default='user')     # Rol del Usuario (user o admin)
    ventas = db.relationship('Venta', backref='usuario', lazy=True)     # Relacion con ventas realizadas por el usuario

    def __repr__(self):
        return f"<User {self.username}>"

# Tabla de proveedores
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    cif = db.Column(db.String(50))
    porcentaje_descuento = db.Column(db.Float)
    iva = db.Column(db.Float)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)  #  # Relación con productos del proveedor

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"

# Tabla de productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)             # Precio de venta
    costo_proveedor = db.Column(db.Float, nullable=False)    # Costo del proveedor
    stock = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False)     # Umbral para alertas de reposicion
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)    # Relacion con proveedor

    # Relación con ventas
    ventas = db.relationship('Venta', backref='producto', lazy=True)      # Relacion con ventas del producto


    def __repr__(self):
        return f"<Producto {self.nombre}>"

# Tabla de ventas
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)    # Producto vendido
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)         # Usuario que realizo la compra
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)                                          # Total de la venta
    fecha = db.Column(db.DateTime, default=datetime.utcnow)                              # Fecha y hora de la venta
    
    def __repr__(self):
        return f"<Venta {self.id} - Producto {self.producto_id} - Usuario {self.usuario_id}>"
