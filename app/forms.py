from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from app.models import Proveedor  

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    stock_maximo = IntegerField('Stock Máximo', validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Producto')

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email')
    telefono = StringField('Teléfono')
    submit = SubmitField('Registrar Proveedor')

class RegistroForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class VentaForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Confirmar Venta')
