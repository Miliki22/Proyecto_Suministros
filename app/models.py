from . import db  # Importa la instancia de SQLAlchemy desde __init__.py
from flask_login import UserMixin  # Importa UserMixin para manejar la autenticación de usuarios

class User(UserMixin, db.Model):  # # Modelo de la tabla 'User' en la base de datos, hereda de SQLAlchemy y UserMixin
    id = db.Column(db.Integer, primary_key=True) # ID único del usuario (clave primaria)
    username = db.Column(db.String(150), nullable=False, unique=True)  # Nombre de usuario único, obligatorio y con un máximo de 150 caracteres
    password = db.Column(db.String(150), nullable=False)  # Contraseña del usuario, obligatoria y con un máximo de 150 caracteres
    role = db.Column(db.String(50), nullable=False)  # Rol de usuario ('admin' o 'user')
