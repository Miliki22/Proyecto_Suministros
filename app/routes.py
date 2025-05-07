from flask import Blueprint, render_template, request, flash, redirect, url_for # Importa Blueprint para agrupar rutas, y render_template para cargar HTML
from flask_login import login_required, current_user  # Importa decoradores para requerir autenticación y obtener el usuario actual
from .models import User, Proveedor, Producto, Venta  # Importa los modelos de la base de datos
from .forms import ProductoForm, ProveedorForm, VentaForm # Importa el formulario para productos
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

@main.route('/productos')
@login_required
def listar_productos():
    productos = Producto.query.all()
    return render_template('listar_productos.html', productos=productos)

    
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

@main.route('/eliminar_producto/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash(f'Producto "{producto.nombre}" eliminado correctamente.')
    return redirect(url_for('main.listar_productos'))

@main.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)  # Rellena el formulario con los datos existentes

    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.precio = form.precio.data
        producto.stock = form.stock.data
        producto.proveedor_id = form.proveedor_id.data

        db.session.commit()
        flash(f'Producto "{producto.nombre}" actualizado correctamente.')
        return redirect(url_for('main.listar_productos'))

    return render_template('editar_producto.html', form=form, producto=producto)

@main.route('/proveedores')
@login_required
def listar_proveedores():
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    proveedores = Proveedor.query.all()
    return render_template('listar_proveedores.html', proveedores=proveedores)

@main.route('/registrar_proveedor', methods=['GET', 'POST'])
@login_required
def registrar_proveedor():
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_proveedor = Proveedor(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor registrado correctamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('registrar_proveedor.html', form=form)

@main.route('/eliminar_proveedor/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    proveedor = Proveedor.query.get_or_404(id)
    if proveedor.productos:
        flash("No se puede eliminar el proveedor porque tiene productos asociados.")
    else:
        db.session.delete(proveedor)
        db.session.commit()
        flash('Proveedor eliminado correctamente.')

    return redirect(url_for('main.listar_proveedores'))


@main.route('/realizar_venta', methods=['GET', 'POST'])
@login_required
def realizar_venta():
    form = VentaForm()
    form.producto_id.choices = [(p.id, p.nombre) for p in Producto.query.all()]

    if form.validate_on_submit():
        producto = Producto.query.get(form.producto_id.data)

        if not producto:
            flash('Producto no válido.')
            return redirect(url_for('main.realizar_venta'))

        if form.cantidad.data > producto.stock:
            flash('Stock insuficiente para realizar la venta.')
            return redirect(url_for('main.realizar_venta'))

        total = producto.precio * form.cantidad.data

        nueva_venta = Venta(
            producto_id=producto.id,
            usuario_id=current_user.id,
            cantidad=form.cantidad.data,
            total=total
        )

        producto.stock -= form.cantidad.data  # Descontar stock
        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta realizada con éxito.')
        return redirect(url_for('main.dashboard'))

    return render_template('realizar_venta.html', form=form)

@main.route('/ventas')
@login_required
def listar_ventas():
    if current_user.role != 'admin':
        flash('Acceso denegado')
        return redirect(url_for('main.dashboard'))

    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('listar_ventas.html', ventas=ventas)


@main.route('/mis_compras')
@login_required
def mis_compras():
    ventas = Venta.query.filter_by(usuario_id=current_user.id).order_by(Venta.fecha.desc()).all()
    return render_template('mis_compras.html', ventas=ventas)
