from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired


class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    nombre_usuario = StringField('Nombre de usuario', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    tipo_persona = SelectField('Tipo de Usuario', choices=[('cliente', 'Cliente'), ('administrador', 'Administrador')], validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
