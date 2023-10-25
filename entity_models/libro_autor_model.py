from data.database import Database

db = Database.db


class LibroAutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id_libro'))
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))
