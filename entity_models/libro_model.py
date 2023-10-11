from data.database import Database

db = Database.db


# Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
# vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Libro(db.Model):
    id_libro = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13))
    titulo = db.Column(db.String(100))
    existencia = db.Column(db.Boolean)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    categoria = db.relationship("Categoria", backref=db.backref("categoria", uselist=False))
