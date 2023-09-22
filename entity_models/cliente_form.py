from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    nombre_usuario = StringField('Nombre de usuario', validators=[DataRequired()])
    contraseña = StringField('Contraseña', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    usuario_telegram = StringField('Usuario de Telegram', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
