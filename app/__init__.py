from flask import Flask  # Importa Flask para crear la aplicación web
from flask_sqlalchemy import SQLAlchemy  # Importa SQLAlchemy para manejar la base de datos
from flask_login import LoginManager  # Importa LoginManager para manejar la autenticación de usuarios

db = SQLAlchemy()  # Inicializa la extensión SQLAlchemy (ORM)
login_manager = LoginManager()  # Inicializa la extensión LoginManager (manejo de sesiones de usuario)
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."  # Mensaje de error para redirigir al login

def create_app():
    app = Flask(__name__)   # Crea una instancia de la aplicación Flask
    app.config.from_object("config.config")  # Carga la configuración desde el archivo config/config.py

    db.init_app(app)  # Inicializa la base de datos con la aplicación Flask
    login_manager.init_app(app)  # Inicializa el manejador de login con la aplicación Flask
    login_manager.login_view = 'auth.login'   # Define la vista de login (ruta a redirigir si no hay sesión)

    from .models import User # Importa el modelo User (usuario)

    @login_manager.user_loader  # Decorador para cargar un usuario por su ID
    def load_user(user_id):
        return User.query.get(int(user_id))   # Busca el usuario en la base de datos por su ID

    # importa y registra los blueprints (módulos de rutas) de la aplicación
    from . import routes   
    from . import auth
    app.register_blueprint(routes.main)  # Registra el blueprint de rutas principales  
    app.register_blueprint(auth.auth)   # Registra el blueprint de autenticación(login/logout)

    return app  # Devuelve la instancia de la aplicación Flask configurada y lista para usar

