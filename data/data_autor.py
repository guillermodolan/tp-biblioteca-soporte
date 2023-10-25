from sqlalchemy import func

from entity_models.autor_model import Autor
from data.database import Database
from entity_models.libro_autor_model import LibroAutor
from entity_models.libro_model import Libro
from entity_models.pedido_model import Pedido


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

    @classmethod
    def autor_mas_leido_en_un_mes(cls, mes, año):
        resultados = (
            Database.db.session.query(Autor.nombre, func.count(Libro.id_libro))
            .join(Libro.autores)
            .join(LibroAutor, Libro.id_libro == LibroAutor.id_libro)
            .join(Pedido, Pedido.id_libro == LibroAutor.id_libro)
            .filter(func.extract('month', func.to_date(Pedido.fecha_pedido, 'YYYY-MM-DD')) == mes,
                    func.extract('year', func.to_date(Pedido.fecha_pedido, 'YYYY-MM-DD')) == año)
            .group_by(Autor.nombre)
            .all()
        )
        return resultados
