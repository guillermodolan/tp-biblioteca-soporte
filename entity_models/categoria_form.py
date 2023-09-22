from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CategoriaForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
