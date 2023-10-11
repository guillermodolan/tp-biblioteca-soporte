from data.data_libro import DataLibro


class LibroLogic:
    @classmethod
    def get_all_libros(cls):
        libros = DataLibro.get_all_libros()
        return libros

    @classmethod
    def get_one_libro(cls, id):
        libro = DataLibro.get_one_libro(id)
        return libro

    @classmethod
    def add_libro(cls, libro):
        DataLibro.add_libro(libro)

    @classmethod
    def delete_libro(cls, id):
        DataLibro.delete_libro(id)
