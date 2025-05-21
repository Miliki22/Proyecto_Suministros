from app import create_app, db   # Importa la función para crear la aplicación y la instancia de la base de datos
from app.models import User   # Importa el modelo de usuario
from werkzeug.security import generate_password_hash    # Importa la función para encriptar contraseñas

app = create_app()            # Crea una instancia de la aplicación Flask con su configuración
app.app_context().push()      # Establece un contexto de aplicación para poder interactuar con la base de datos

# --- CREACIÓN DE USUARIO ADMINISTRADOR ---

# Verifica si ya existe un usuario admin
if not User.query.filter_by(username='admin').first():       # Si no existe, crea un nuevo usuario administrador
    admin = User(
        username='admin',
        email='admin@example.com',      # Correo del admin (puede personalizarse)
        password=generate_password_hash('TokioSchool25'),  # Contraseña encriptada
        role='admin'     # Rol asignado
    )
    db.session.add(admin)   # Agrega el nuevo usuario a la sesion de la base de datos
    db.session.commit()     # Guarda los cambios en la base de datos
    print("Administrador creado con éxito.")
else:
    print("El usuario administrador ya existe.")
