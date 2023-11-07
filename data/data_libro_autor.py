from entity_models.libro_autor_model import LibroAutor
from data.database import Database


class DataLibroAutor:
    @classmethod
    def add_libro_autor(cls, libro_autor):
        Database.db.session.add(libro_autor)
        Database.db.session.commit()

    @classmethod
    def get_libro_autor(cls, id):
        todos = LibroAutor.query.order_by('id_libro')
        libro_autor = []
        for lib_aut in todos:
            if lib_aut.id_libro == id:
                libro_autor.append(lib_aut)
        return libro_autor
