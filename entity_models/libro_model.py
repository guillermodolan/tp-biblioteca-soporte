from data.database import Database
from entity_models.autor_model import Autor
from entity_models.categoria_model import Categoria

db = Database.db


class Libro(db.Model):
    id_libro = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30))
    titulo = db.Column(db.String(100))
    existencia = db.Column(db.Boolean)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    categoria = db.relationship("Categoria", backref=db.backref("categoria", uselist=False))

    # Agrega la relación con la tabla intermedia LibroAutor
    autores = db.relationship('Autor', secondary='libro_autor', back_populates='libros')

    def to_dict(self):
        return {
            'id_libro': self.id_libro,
            'isbn': self.isbn,
            'titulo': self.titulo,
            'existencia': self.existencia,
            'id_categoria': self.id_categoria,
            'categoria': self.categoria.to_dict() if self.categoria else None,
            'autores': [autor.to_dict() for autor in self.autores] if self.autores else []
        }

    @classmethod
    def from_dict(cls, data):
        libro = cls()
        libro.id_libro = data['id_libro']
        libro.isbn = data['isbn']
        libro.titulo = data['titulo']
        libro.existencia = data['existencia']
        libro.id_categoria = data['id_categoria']
        # Puedes manejar la relación con la categoría según tus necesidades
        # En este caso, asumimos que el valor en 'categoria' es un diccionario
        libro.categoria = Categoria.from_dict(data['categoria']) if data['categoria'] else None
        # También debes manejar la relación con los autores
        libro.autores = [Autor.from_dict(autor) for autor in data['autores']] if data['autores'] else []
        return libro
