from entity_models.libro_model import Libro
from data.database import Database

#get_all
#get_one
#add
#delete


class DataLibro():
    @classmethod
    def get_all_libros(cls):
        libros = Libro.query.order_by('id_libro')
        return libros

    @classmethod
    def get_one_libro(cls, id):
        libro = Libro.query.get_or_404(id)
        return libro

    @classmethod
    def add_libro(cls, libro):
        Database.db.session.add(libro)
        Database.db.session.commit()

    @classmethod
    def delete_libro(cls, id):
        libro = DataLibro.get_one_libro(id)

        #Elimino al libro
        Database.db.session.delete(libro)

        #Guardo los cambios en la base de datos
        Database.db.session.commit()