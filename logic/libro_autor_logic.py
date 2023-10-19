from data.data_libro_autor import DataLibroAutor


class LibroAutorLogic:

    @classmethod
    def add_libro_autor(cls, libro_autor):
        DataLibroAutor.add_libro_autor(libro_autor)