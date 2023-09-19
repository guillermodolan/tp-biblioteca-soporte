from data.data_cliente import DataCliente
from entity_models.cliente_model import Cliente


class ClienteLogic():
    @classmethod
    def get_all_clientes(cls):
        clientes = DataCliente.get_all_clientes()
        return clientes

    @classmethod
    def get_one_cliente(cls, id):
        cliente = DataCliente.get_one_cliente(id)
        return cliente

    @classmethod
    def add_cliente(cls, cliente):
        DataCliente.add_cliente(cliente)

    @classmethod
    def delete_cliente(cls, id):
        DataCliente.delete_cliente(id)

    @classmethod
    def valida_credenciales(cls, username, password):
        cliente = ClienteLogic.get_cliente_by_user(username)
        if cliente and Cliente.valida_contraseña(cliente, password):
            print(f'Id de cliente: {cliente.id_cliente}')
            return cliente
        return None

    @classmethod
    def get_cliente_by_user(cls, username):
        cliente = DataCliente.get_cliente_by_user(username)
        return cliente
