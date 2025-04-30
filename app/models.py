from . import db  # Importa la instancia de SQLAlchemy desde __init__.py
from flask_login import UserMixin  # Importa UserMixin para manejar la autenticación de usuarios
from datetime import datetime  # Importa datetime para manejar fechas y horas

# Modelo de la tabla 'User' en la base de datos, hereda de SQLAlchemy y UserMixin
class User(UserMixin, db.Model):  # # Modelo de la tabla 'User' en la base de datos, hereda de SQLAlchemy y UserMixin
    id = db.Column(db.Integer, primary_key=True) # ID único del usuario (clave primaria)
    username = db.Column(db.String(150), nullable=False, unique=True)  # Nombre de usuario único, obligatorio y con un máximo de 150 caracteres
    password = db.Column(db.String(150), nullable=False)  # Contraseña del usuario, obligatoria y con un máximo de 150 caracteres
    role = db.Column(db.String(50), nullable=False)  # Rol de usuario ('admin' o 'user')
    
    def __repr__(self):
        return f"<User {self.username}>"

# Tabla de proveedores
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(50))

    productos = db.relationship('Producto', backref='proveedor', lazy=True)

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"

# Tabla de productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
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

    def __repr__(self):
        return f"<Venta {self.id} - Producto {self.producto_id} - Usuario {self.usuario_id}>"
