from data.data_libro import DataLibro

class LibroLogic():
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


    # Método que servirá para buscar un libro por ISBN. Esto nos servirá para cuando se confirman
    # libros a un pedido, que no se creen 2 veces en la base de datos.
    @classmethod
    def get_libro_by_isbn(cls, isbn):
        libro = DataLibro.get_libro_by_isbn(isbn)
        return libro

    @classmethod
    def get_libros_by_titulo(cls, titulo):
        libro = DataLibro.get_libro_by_titulo(titulo)
        return libro