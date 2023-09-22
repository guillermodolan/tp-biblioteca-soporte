import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DBAPIError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, FlushError
from werkzeug.exceptions import NotFound

from entity_models.cliente_model import Cliente
from data.database import Database
from flask import Flask

app = Flask(__name__)


class DataCliente:
    @classmethod
    def get_all_clientes(cls):
        try:
            clientes = Cliente.query.order_by('id_cliente')
            return clientes
        except SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_cliente(cls, id):
        try:
            cliente = Cliente.query.get_or_404(id)
            return cliente
        except NotFound as e:
            app.logger.debug(f'Cliente no encontrado: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def add_cliente(cls, cliente):
        try:
            Database.db.session.add(cliente)
            Database.db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def delete_cliente(cls, id):
        try:
            cliente = DataCliente.get_one_cliente(id)
            Database.db.session.delete(cliente)
            Database.db.session.commit()
        except IntegrityError as e:
            raise e
        except ObjectDeletedError as e:
            raise e
        except StaleDataError as e:
            raise e

    @classmethod
    def get_cliente_by_user(cls, username):
        try:
            cliente = Cliente.query.filter_by(nombre_usuario=username).first()
            return cliente
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f"Error de base de datos: {e}")
            raise e
        except Exception as e:
            app.logger.debug(f"Error inesperado: {e}")
            raise e

    @classmethod
    def update_cliente(cls, cliente):
        try:
            Database.db.session.commit()
        except IntegrityError as e:
            raise e
        except StaleDataError as e:
            raise e
        except FlushError as e:
            raise e
        except DBAPIError as e:
            raise e
