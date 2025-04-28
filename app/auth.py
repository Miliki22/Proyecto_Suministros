from flask import Blueprint, render_template, redirect, url_for, request, flash  # Importa las funciones necesarias de Flask
from werkzeug.security import check_password_hash  # Importa la función para verificar contraseñas hasheadas (encriptadas)
from flask_login import login_user, logout_user  # Importa las funciones para manejar la sesión de usuario
from .models import User   # Importa el modelo User (usuario) desde models.py

# Crea el Blueprint 'auth' para agrupar las rutas de autenticación
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])  # Define la ruta para el login, acepta métodos GET y POST
def login():
    if request.method == 'POST':  # Si el método es POST, significa que se está enviando el formulario de login
        username = request.form.get('username')    # Obtiene el nombre de usuario del formulario
        password = request.form.get('password')    # Obtiene la contraseña del formulario

        user = User.query.filter_by(username=username).first()   # Busca el usuario en la base de datos por su nombre de usuario
        if user and check_password_hash(user.password, password):  # Verifica si el usuario existe y si la contraseña es correcta
            login_user(user)   # Inicia la sesión del usuario
            return redirect(url_for('main.dashboard'))   # Redirige al dashboard (panel de control) después de iniciar sesión
        else:
            flash('Credenciales incorrectas')  # Muestra un mensaje de error si las credenciales son incorrectas

    return render_template('login.html')   # Renderiza la plantilla de login.html

@auth.route('/logout')   # Define la ruta para el logout(cerrar sesión)
def logout():
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('main.index'))  # Redirige a la página principal después de cerrar sesión (index)


