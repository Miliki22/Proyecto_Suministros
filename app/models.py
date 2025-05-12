from . import db
from flask_login import UserMixin
from datetime import datetime

# Tabla de usuarios con roles (admin o user)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')  # user o admin
    ventas = db.relationship('Venta', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Tabla de proveedores
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"

# Tabla de productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    costo_proveedor = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

# Tabla de ventas
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    producto = db.relationship('Producto', backref='ventas')

    def __repr__(self):
        return f"<Venta {self.id} - Producto {self.producto_id} - Usuario {self.usuario_id}>"
