from data.data_cliente import DataCliente

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
    def delete_cliente(cls, id):
        cliente = DataCliente.delete_cliente(id)