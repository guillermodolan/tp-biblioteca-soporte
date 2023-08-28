from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nombre_usuario = StringField('Nombre de usuario', validators=[DataRequired()])
    contrasenia = StringField('Contraseña', validators=[DataRequired()])
    ingresar = SubmitField('Ingresar')