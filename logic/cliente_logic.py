from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, FlushError
from werkzeug.exceptions import NotFound

from data.data_cliente import DataCliente
from entity_models.cliente_model import Cliente

#Variable creada para lanzar un mensaje al usuario de cómo resultó la operación que intenta
#realizar
mensaje = ''

class ClienteLogic():
    @classmethod
    def get_all_clientes(cls):
        clientes = DataCliente.get_all_clientes()
        return clientes

    @classmethod
    def get_one_cliente(cls, id):
        try:
            cliente = DataCliente.get_one_cliente(id)
            return cliente
        except NotFound as e:
            raise e

    @classmethod
    def add_cliente(cls, cliente):
        DataCliente.add_cliente(cliente)


    #En desarrollo
    @classmethod
    def get_cliente_by_user(cls, username):
        cliente = DataCliente.get_cliente_by_user(username)
        return cliente

    @classmethod
    def valida_credenciales(cls, username, password):
        cliente = ClienteLogic.get_cliente_by_user(username)
        if cliente and Cliente.valida_contraseña(cliente, password):
            print(f'Id de cliente: {cliente.id_cliente}')
            return cliente
        return None

    @classmethod
    def delete_cliente(cls, id):
        global mensaje
        try:
            cliente = DataCliente.delete_cliente(id)
            mensaje = f'Cliente {cliente.nombre} {cliente.apellido} eliminado exitosamente'
            return mensaje
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
            cliente = DataCliente.update_cliente(cliente)
            mensaje = f'Cliente {cliente.nombre} {cliente.apellido} actualizado exitosamente'
            return mensaje
        except IntegrityError as e:
            raise e
        except StaleDataError as e:
            raise e
        except FlushError as e:
            raise e
        except DBAPIError as e:
            raise e