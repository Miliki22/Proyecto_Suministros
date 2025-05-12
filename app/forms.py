from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import Proveedor  

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    costo_proveedor = FloatField('Costo al proveedor', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    stock_maximo = IntegerField('Stock Máximo', validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Producto')

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email')
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    cif = StringField('CIF')
    porcentaje_descuento = FloatField('Descuento (%)')
    iva = FloatField('IVA (%)')
    submit = SubmitField('Registrar')

class RegistroForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class VentaForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Confirmar Venta')
