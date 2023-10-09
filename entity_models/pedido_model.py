from data.database import Database

db = Database.db


class Pedido(db.Model):
    numero_pedido = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.String(30))
    fecha_devolucion = db.Column(db.String(30))
    estado = db.Column(db.Boolean())
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    cliente = db.relationship("Cliente", backref=db.backref("cliente", uselist=False))
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id_libro'))
    libro = db.relationship("Libro", backref=db.backref("libro", uselist=False))
