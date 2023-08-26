from data.database import Database

db = Database.db

#Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
#vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Pedido(db.Model):
    numero_pedido = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.String(15))
    estado = db.Column(db.String(50))
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    cliente = db.relationship("Cliente", backref=db.backref("cliente", uselist=False))