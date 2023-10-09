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
    def update_existencia(cls):
        DataLibro.update_existencia()
        return 'Existencia actualizada'

    @classmethod
    def delete_libro(cls, id):
        DataLibro.delete_libro(id)


    # Método que servirá para buscar un libro por título. Esto nos servirá para cuando se confirman
    # libros a un pedido, que no se creen 2 veces en la base de datos.
    @classmethod
    def get_libros_by_titulo(cls, titulo):
        libro = DataLibro.get_libro_by_titulo(titulo)
        return libro


    # Por regla de negocio 3 en el documento 'Narrativa TPI', validamos que el libro que
    # se quiere alquilar no esté ya alquilado.
    @classmethod
    def valida_existencia_libro(cls, titulo):
        libro = LibroLogic.get_libros_by_titulo(titulo)
        if libro.existencia:
            return libro
        else:
            return None