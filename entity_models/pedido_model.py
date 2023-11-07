from data.database import Database

db = Database.db


class Pedido(db.Model):
    numero_pedido = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.String(30))
    fecha_devolucion = db.Column(db.String(30))
    estado = db.Column(db.Boolean())
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    persona = db.relationship("Persona", backref=db.backref("pedidos", uselist=True))
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id_libro'))
    libro = db.relationship("Libro", backref=db.backref("libro", uselist=False))
