from flask import Blueprint, render_template   # Importa Blueprint para agrupar rutas, y render_template para cargar HTML
from flask_login import login_required, current_user  # Importa decoradores para requerir autenticación y obtener el usuario actual

main = Blueprint('main', __name__)   # Crea un Blueprint llamado 'main' para agrupar las rutas principales de la aplicación (no de autenticación)

@main.route('/')   # Define la ruta principal de la aplicación
def index():
    return render_template('index.html')   # Renderiza la plantilla index.html

@main.route('/dashboard')   # Define la ruta para el dashboard (panel de control), protegida con login_required
@login_required   # Requiere que el usuario esté autenticado para acceder a esta ruta
def dashboard():
    # Verifica el rol del usuario actual y renderiza la plantilla correspondiente
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')  # Renderiza la plantilla admin_dashboard.html si el usuario es administrador
    else:
        return render_template('user_dashboard.html')   # Renderiza la plantilla user_dashboard.html si el usuario es un usuario normal 
    