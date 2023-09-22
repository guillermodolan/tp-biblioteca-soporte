import sqlalchemy.exc
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, FlushError
from werkzeug.exceptions import NotFound

from data.data_cliente import DataCliente
from entity_models.cliente_model import Cliente
from flask import Flask

app = Flask(__name__)

# Variable creada para lanzar un mensaje al usuario de cómo resultó la operación que intenta
# realizar
mensaje = ''


class ClienteLogic:
    @classmethod
    def get_all_clientes(cls):
        try:
            clientes = DataCliente.get_all_clientes()
            return clientes
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_cliente(cls, id):
        try:
            cliente = DataCliente.get_one_cliente(id)
            return cliente
        except NotFound as e:
            app.logger.debug(f'Cliente no encontrado: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def add_cliente(cls, cliente):
        global mensaje
        try:
            DataCliente.add_cliente(cliente)
            mensaje = f'Cliente {cliente.nombre} {cliente.apellido} insertado exitosamente'
            # return mensaje
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_cliente_by_user(cls, username):
        try:
            cliente = DataCliente.get_cliente_by_user(username)
            return cliente
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f"Error de base de datos: {e}")
            raise e
        except Exception as e:
            app.logger.debug(f"Error inesperado: {e}")
            raise e

    @classmethod
    def valida_credenciales(cls, username, contraseña):
        try:
            cliente = ClienteLogic.get_cliente_by_user(username)
            if cliente:
                clienteValidado = Cliente.valida_contraseña(cliente, contraseña)
                if clienteValidado is not None:
                    return cliente
                else:
                    return None
            return None
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f"Error de base de datos: {e}")
            raise e
        except Exception as e:
            app.logger.debug(f"Error inesperado: {e}")
            raise e

    @classmethod
    def delete_cliente(cls, id):
        global mensaje
        try:
            DataCliente.delete_cliente(id)
            # mensaje = f'Cliente {cliente.nombre} {cliente.apellido} eliminado exitosamente'
            # return mensaje
        except IntegrityError as e:
            raise e
        except ObjectDeletedError as e:
            raise e
        except StaleDataError as e:
            raise e

    @classmethod
    def update_cliente(cls, cliente):
        global mensaje
        try:
            DataCliente.update_cliente(cliente)
            mensaje = f'Cliente {cliente.nombre} {cliente.apellido} actualizado exitosamente'
            app.logger.debug(mensaje)
            return mensaje
        except IntegrityError as e:
            raise e
        except StaleDataError as e:
            raise e
        except FlushError as e:
            raise e
        except DBAPIError as e:
            raise e
