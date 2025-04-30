import os

basedir = os.path.abspath(os.path.dirname(__file__))   # Obtiene la ruta absoluta del directorio actual
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(basedir), 'instance', 'tienda.db') # Cambia esto por la URI de mi base de datos
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva la advertencia de modificaciones de objetos
SECRET_KEY = os.urandom(24)   # Cambia esto por una clave secreta más segura en producción, Sirve para la seguridad de sesiones/cookies en Flask.
