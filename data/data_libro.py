from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from entity_models.libro_model import Libro
from data.database import Database
app = Flask(__name__)


class DataLibro:
    @classmethod
    def get_all_libros(cls):
        try:
            libros = Libro.query.order_by('id_libro')
            return libros
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_libro(cls, id):
        try:
            libro = Libro.query.get_or_404(id)
            return libro
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Libro no encontrado')
            raise NotFound(description='Libro no encontrado')

    @classmethod
    def add_libro(cls, libro):
        try:
            Database.db.session.add(libro)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al agregar el libro: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def update_existencia(cls):
        try:
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al actualizar la existencia: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def delete_libro(cls, id):
        try:
            libro = DataLibro.get_one_libro(id)
            Database.db.session.delete(libro)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al eliminar el libro: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Libro no encontrado')
            raise NotFound(description='Libro no encontrado')
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_libro_by_titulo(cls, titulo):
        try:
            libro = Libro.query.filter(Libro.titulo.ilike(f'%{titulo}%')).first()
            return libro
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e
