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
print('listar_productos')

    
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
            costo_proveedor=form.costo_proveedor.data,
            stock=form.stock.data,
            stock_maximo=form.stock_maximo.data,
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

    if producto.ventas:  # Verifica si el producto tiene ventas asociadas
        flash('No se puede eliminar el producto porque tiene ventas registradas.')
        return redirect(url_for('main.listar_productos'))

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
        producto.costo_proveedor = form.costo_proveedor.data
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
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            cif=form.cif.data,
            porcentaje_descuento=form.porcentaje_descuento.data,
            iva=form.iva.data
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

@main.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    if form.validate_on_submit():
        proveedor.nombre = form.nombre.data
        proveedor.email = form.email.data
        proveedor.telefono = form.telefono.data
        proveedor.direccion = form.direccion.data
        proveedor.cif = form.cif.data
        proveedor.porcentaje_descuento = form.porcentaje_descuento.data
        proveedor.iva = form.iva.data
        db.session.commit()
        flash("Proveedor actualizado correctamente.")
        return redirect(url_for('main.listar_proveedores'))
    return render_template('registrar_proveedor.html', form=form, editar=True)

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

@main.route('/eliminar_compra/<int:id>', methods=['POST'])
@login_required
def eliminar_compra(id):
    compra = Venta.query.get_or_404(id)
    if compra.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar esta compra.")
        return redirect(url_for('main.mis_compras'))

    db.session.delete(compra)
    db.session.commit()
    flash("Compra eliminada correctamente.")
    return redirect(url_for('main.mis_compras'))


import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar un backend no interactivo para matplotlib
import matplotlib.pyplot as plt
import os
from flask import current_app
from datetime import datetime

@main.route('/estadisticas')
@login_required
def estadisticas():
    ventas = db.session.query(Venta).all()
    if not ventas:
        flash("No hay ventas registradas aún.")
        return redirect(url_for('main.dashboard'))

    # Datos para el gráfico
    productos = []
    cantidades = []

    for venta in ventas:
        productos.append(venta.producto.nombre)
        cantidades.append(venta.cantidad)

    df = pd.DataFrame({'producto': productos, 'cantidad': cantidades})
    resumen = df.groupby('producto')['cantidad'].sum()

    # Limpiar gráficos viejos
    for archivo in os.listdir('app/static'):
        if archivo.startswith('ventas_por_producto_') and archivo.endswith('.png'):
           os.remove(os.path.join('app/static', archivo))

    # Nombre de archivo dinámico con timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f'ventas_por_producto_{timestamp}.png'
    ruta_grafico = os.path.join('app', 'static', nombre_archivo)
    
    # Generar gráfico
    fig, ax = plt.subplots(figsize=(6, 4))
    resumen.plot(kind='bar', color='goldenrod', ax=ax)
    ax.set_title('Ventas por producto')
    ax.set_xlabel('Producto')
    ax.set_ylabel('Cantidad vendida')
    plt.tight_layout()
    plt.savefig(ruta_grafico)
    plt.close()

    return render_template('estadisticas.html', grafico=nombre_archivo)

@main.route('/estadisticas/beneficios')
@login_required
def estadisticas_beneficios():
    productos = Producto.query.all()

    if not productos:
        flash("No hay productos registrados aún.")
        return redirect(url_for('main.dashboard'))

    nombres = []
    precios = []
    costos = []

    for p in productos:
        nombres.append(p.nombre)
        precios.append(p.precio)
        costos.append(p.costo_proveedor)

    df = pd.DataFrame({
        'Producto': nombres,
        'Precio Venta': precios,
        'Costo Proveedor': costos
    })

    # Eliminar gráficos viejos
    for archivo in os.listdir('app/static'):
        if archivo.startswith('comparativa_beneficios_') and archivo.endswith('.png'):
            os.remove(os.path.join('app/static', archivo))

    # Crear gráfico
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_grafico = f'comparativa_beneficios_{timestamp}.png'
    ruta_grafico = os.path.join('app', 'static', nombre_grafico)

    fig, ax = plt.subplots(figsize=(7, 4))
    df.set_index('Producto')[['Precio Venta', 'Costo Proveedor']].plot(kind='bar', ax=ax)
    ax.set_title('Comparativa de Precios vs Costos')
    ax.set_ylabel('Valor ($)')
    plt.tight_layout()
    plt.savefig(ruta_grafico)
    plt.close()

    return render_template('estadisticas_beneficios.html', grafico=nombre_grafico)

@main.route('/mis_estadisticas')
@login_required
def mis_estadisticas():
    ventas = Venta.query.filter_by(usuario_id=current_user.id).all()

    if not ventas:
        flash("Aún no realizaste compras.")
        return redirect(url_for('main.dashboard'))

    productos = [v.producto.nombre for v in ventas]
    cantidades = [v.cantidad for v in ventas]
    totales = [v.total for v in ventas]

    df = pd.DataFrame({
        'producto': productos,
        'cantidad': cantidades,
        'total': totales
    })

    resumen = df.groupby('producto')['cantidad'].sum()

    # Borrar gráficos viejos
    for archivo in os.listdir('app/static'):
        if archivo.startswith('mis_estadisticas_') and archivo.endswith('.png'):
            os.remove(os.path.join('app/static', archivo))

    # Guardar gráfico con nombre único
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_grafico = f'mis_estadisticas_{timestamp}.png'
    ruta_grafico = os.path.join('app', 'static', nombre_grafico)

    # Generar gráfico
    fig, ax = plt.subplots(figsize=(6, 4))
    resumen.plot(kind='bar', color='royalblue', ax=ax)
    ax.set_title('Mis compras por producto')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Producto')
    plt.tight_layout()
    plt.savefig(ruta_grafico)
    plt.close()

    total_gastado = df['total'].sum()
    cantidad_productos = df['producto'].nunique()

    return render_template(
        'mis_estadisticas.html',
        grafico=nombre_grafico,
        total=total_gastado,
        cantidad=cantidad_productos
    )

@main.route('/estadisticas_mensuales')
@login_required
def estadisticas_mensuales():
    if current_user.role != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('main.dashboard'))

    ventas = db.session.query(Venta).all()
    if not ventas:
        flash("No hay ventas registradas aún.")
        return redirect(url_for('main.dashboard'))

    # Agrupar por mes
    fechas = []
    cantidades = []
    for venta in ventas:
        fechas.append(venta.fecha.strftime('%Y-%m'))
        cantidades.append(venta.cantidad)

    df = pd.DataFrame({'mes': fechas, 'cantidad': cantidades})
    resumen = df.groupby('mes')['cantidad'].sum().sort_index()

    # Ruta y nombre del gráfico dinámico
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f'ventas_mensuales_{timestamp}.png'
    ruta_grafico = os.path.join('app', 'static', nombre_archivo)

    # Eliminar gráficos anteriores de esta ruta
    for archivo in os.listdir(os.path.join('app', 'static')):
        if archivo.startswith('ventas_mensuales_'):
            os.remove(os.path.join('app', 'static', archivo))

    # Generar gráfico de líneas
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')  # fondo blanco
    resumen.plot(kind='bar', color='teal', ax=ax)  # barras más delgadas
    ax.set_title('Ventas mensuales')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad vendida')
    ax.grid(False)
   # Eliminar borde superior y derecho del gráfico para que se vea más limpio
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.savefig(ruta_grafico, facecolor='white')
    plt.close()

    return render_template('estadisticas_mensuales.html', grafico=nombre_archivo)
