from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LibroForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired()])
    existencia = StringField('Existencia', validators=[DataRequired()])
    # categoria_fkey
    id_categoria = StringField('ID Categoría', validators=[DataRequired()])
    guardar = SubmitField('Guardar')
