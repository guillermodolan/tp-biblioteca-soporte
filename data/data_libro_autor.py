from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from entity_models.libro_autor_model import LibroAutor
from data.database import Database

app = Flask(__name__)


class DataLibroAutor:
    @classmethod
    def add_libro_autor(cls, libro_autor):
        try:
            Database.db.session.add(libro_autor)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al agregar libro_autor: {e}')
            Database.db.session.rollback()
            raise e

    @classmethod
    def get_libro_autor(cls, id):
        try:
            todos = LibroAutor.query.order_by('id_libro')
            libro_autor = [lib_aut for lib_aut in todos if lib_aut.id_libro == id]
            if not libro_autor:
                raise NotFound(f'LibroAutor con ID {id} no encontrado')
            return libro_autor
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al obtener libro_autor: {e}')
            raise e
