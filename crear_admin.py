from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Verificamos si el admin ya existe
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('TokioSchool25'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado correctamente.")
    else:
        print("⚠️ El usuario 'admin' ya existe.")
