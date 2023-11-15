from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from entity_models.categoria_model import Categoria
from data.database import Database
app = Flask(__name__)


class DataCategoria:
    @classmethod
    def get_all_categorias(cls):
        try:
            categorias = Categoria.query.order_by('id_categoria')
            return categorias
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_categoria(cls, id):
        try:
            categoria = Categoria.query.get_or_404(id)
            return categoria
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Categoría no encontrada')
            raise NotFound(description='Categoría no encontrada')

    @classmethod
    def get_categoria_by_desc(cls, descripcion):
        try:
            categoria = Categoria.query.filter_by(descripcion=descripcion).first()
            return categoria
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def add_categoria(cls, categoria):
        try:
            Database.db.session.add(categoria)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al agregar la categoría: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def delete_categoria(cls, id):
        try:
            categoria = DataCategoria.get_one_categoria(id)
            Database.db.session.delete(categoria)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al eliminar la categoría: {e}')
            raise e
        except NotFound:
            app.logger.debug(f'Categoría no encontrada')
            raise NotFound(description='Categoría no encontrada')
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e
