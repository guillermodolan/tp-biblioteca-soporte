from entity_models.autor_model import Autor
from data.database import Database


# get_all
# get_one
# add
# delete


class DataAutor():
    @classmethod
    def get_all_autores(cls):
        autores = Autor.query.order_by('id_autor')
        return autores

    @classmethod
    def get_one_autor(cls, id):
        autor = Autor.query.get_or_404(id)
        return autor

    @classmethod
    def add_autor(cls, autor):
        Database.db.session.add(autor)
        Database.db.session.commit()

    @classmethod
    def delete_autor(cls, id):
        autor = DataAutor.get_one_autor(id)

        # Elimino al autor
        Database.db.session.delete(autor)

        # Guardo los cambios en la base de datos
        Database.db.session.commit()
