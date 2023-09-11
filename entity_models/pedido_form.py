from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PedidoForm(FlaskForm):
    fecha = StringField('Fecha del pedido', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    #cliente_fkey
    id_cliente = StringField('ID Cliente', validators=[DataRequired()])
    guardar = SubmitField('Guardar')