from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AutorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
