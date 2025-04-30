from flask import Blueprint, render_template, request, flash, redirect, url_for # Importa Blueprint para agrupar rutas, y render_template para cargar HTML
from flask_login import login_required, current_user  # Importa decoradores para requerir autenticación y obtener el usuario actual
from .models import User, Proveedor, Producto, Venta  # Importa los modelos de la base de datos
from .forms import ProductoForm  # Importa el formulario para productos
from app import db  # Importa la instancia de SQLAlchemy para interactuar con la base de datos

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
    
@main.route('/registrar_producto', methods=['GET', 'POST'])
@login_required
def registrar_producto():
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    form = ProductoForm()
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]

    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            proveedor_id=form.proveedor_id.data
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto registrado con éxito')
        return redirect(url_for('main.dashboard'))

    return render_template('registrar_producto.html', form=form)