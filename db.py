from app import create_app, db  # Importa la función create_app y la instancia de la base de datos (db) desde el módulo app

app = create_app()   # Crea la instancia de la aplicación Flask 

with app.app_context():   # Crea un contexto de aplicación para ejecutar operaciones relacionadas con la base de datos
    db.create_all()  # Crea todas las tablas definidas en models.py (si no existen) en la base de datos
    print("Base de datos creada correctamente.")  # Imprime un mensaje de confirmación en la consola
