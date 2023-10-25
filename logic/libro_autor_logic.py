from data.data_libro_autor import DataLibroAutor


class LibroAutorLogic:

    @classmethod
    def add_libro_autor(cls, libro_autor):
        DataLibroAutor.add_libro_autor(libro_autor)

    @classmethod
    def get_libro_autor(cls, id):
        libro_autor = DataLibroAutor.get_libro_autor(id)
        return libro_autor
