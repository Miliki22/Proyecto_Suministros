from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Verifica si ya existe un usuario admin
if not User.query.filter_by(username='admin').first():
    admin = User(
        username='admin',
        email='admin@example.com',  
        password=generate_password_hash('TokioSchool25'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("Administrador creado con éxito.")
else:
    print("El usuario administrador ya existe.")
