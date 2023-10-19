from data.database import Database

db = Database.db


# Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
# vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Autor(db.Model):
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    # Agrega la relación con la tabla intermedia LibroAutor
    libros = db.relationship('Libro', secondary='libro_autor', back_populates='autores')
