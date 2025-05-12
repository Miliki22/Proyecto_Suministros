from flask import Blueprint, render_template, redirect, url_for, request, flash  # Importa las funciones necesarias de Flask
from werkzeug.security import check_password_hash, generate_password_hash  # Importa la función para verificar contraseñas hasheadas (encriptadas)
from flask_login import login_user, logout_user  # Importa las funciones para manejar la sesión de usuario
from .models import User   # Importa el modelo User (usuario) desde models.py
from app import db  # Importa la instancia de SQLAlchemy para interactuar con la base de datos
from .forms import RegistroForm  # Importa el formulario de registro desde forms.py

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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()

    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Las contraseñas no coinciden.")
            return render_template('register.html', form=form)

        usuario_existente = User.query.filter_by(username=form.username.data).first()
        if usuario_existente:
            flash("El nombre de usuario ya está registrado.")
            return render_template('register.html', form=form)

        nuevo_usuario = User(
            username=form.username.data,
            email=form.email.data,  
            password=generate_password_hash(form.password.data),
            role='user'
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)
