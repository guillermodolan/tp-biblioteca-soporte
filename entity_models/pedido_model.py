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

    def to_dict(self):
        return {
            'numero_pedido': self.numero_pedido,
            'fecha_pedido': self.fecha_pedido,
            'fecha_devolucion': self.fecha_devolucion,
            'estado': self.estado,
            'id_persona': self.id_persona,
            'id_libro': self.id_libro
        }


    @classmethod
    def from_dict(cls, data):
        pedido = cls()
        pedido.numero_pedido = data['numero_pedido']
        pedido.fecha_pedido = data['fecha_pedido']
        pedido.fecha_devolucion = data['fecha_devolucion']
        pedido.estado = data['estado']
        pedido.id_persona = data['id_persona']
        pedido.id_libro = data['id_libro']
        return pedido