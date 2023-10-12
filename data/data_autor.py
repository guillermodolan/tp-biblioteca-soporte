from entity_models.autor_model import Autor
from data.database import Database


class DataAutor:
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
    def get_author_by_name(cls, nombre):
        autor = Autor.query.filter_by(nombre=nombre).first()
        return autor


    @classmethod
    def delete_autor(cls, id):
        autor = DataAutor.get_one_autor(id)
        Database.db.session.delete(autor)
        Database.db.session.commit()
