from flask_wtf import FlaskForm   # Importa la clase base FlaskForm, que permite crear formularios usando Flask-WTF
# Importa distintos tipos de campos que pueden usarse en un formulario
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo   # Importa validadores predefinidos
from app.models import Proveedor   # Importa el modelo Proveedor por si se necesita cargar dinámicamente sus datos (como en una lista desplegable)

# Formulario para registrar o editar productos
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    costo_proveedor = FloatField('Costo al proveedor', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    stock_maximo = IntegerField('Stock Máximo', validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Producto')


# Formulario para registrar o editar proveedores
class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email')
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    cif = StringField('CIF')
    porcentaje_descuento = FloatField('Descuento (%)')
    iva = FloatField('IVA (%)')
    submit = SubmitField('Registrar')        # Boton de envio

# Formulario para registrar nuevos usuarios
class RegistroForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])  # Verifica formato de email
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])  # Debe coincidir con 'password'
    submit = SubmitField('Registrarse')


# Formulario para realizar una venta
class VentaForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])  # Selección de producto
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Confirmar Venta')
