from flask import Flask
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from entity_models.autor_model import Autor
from data.database import Database
from entity_models.libro_autor_model import LibroAutor
from entity_models.libro_model import Libro
from entity_models.pedido_model import Pedido

app = Flask(__name__)


class DataAutor:
    @classmethod
    def get_all_autores(cls):
        try:
            autores = Autor.query.order_by('id_autor')
            return autores
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_autor(cls, id):
        try:
            autor = Autor.query.get_or_404(id)
            return autor
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Autor no encontrado')
            raise NotFound(description='Autor no encontrado')

    @classmethod
    def add_autor(cls, autor):
        try:
            Database.db.session.add(autor)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al agregar el autor: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_author_by_name(cls, nombre):
        try:
            autor = Autor.query.filter_by(nombre=nombre).first()
            return autor
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def delete_autor(cls, id):
        try:
            autor = DataAutor.get_one_autor(id)
            Database.db.session.delete(autor)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al eliminar el autor: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Autor no encontrado')
            raise NotFound(description='Autor no encontrado')
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def autor_mas_leido_en_un_mes(cls, mes, año):
        try:
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
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e
