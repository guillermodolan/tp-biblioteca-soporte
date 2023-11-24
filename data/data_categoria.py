from flask import Flask
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from entity_models.categoria_model import Categoria
from data.database import Database
from entity_models.libro_model import Libro
from entity_models.pedido_model import Pedido

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

    @classmethod
    def categorias_mas_leidas_en_un_mes(cls, mes, año):
        try:
            resultados = (
                Database.db.session.query(Categoria.descripcion, func.count(Libro.id_libro))
                .join(Libro, Libro.id_categoria == Categoria.id_categoria)
                .join(Pedido, Pedido.id_libro == Libro.id_libro)
                .filter(func.extract('month', func.to_date(Pedido.fecha_pedido, 'YYYY-MM-DD')) == mes,
                        func.extract('year', func.to_date(Pedido.fecha_pedido, 'YYYY-MM-DD')) == año)
                .group_by(Categoria.descripcion)
                .order_by(func.count(Libro.id_libro).desc())
                .all()
            )
            return resultados
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e
