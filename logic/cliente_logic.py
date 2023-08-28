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

    @classmethod
    def add_cliente(cls, cliente):
        DataCliente.add_cliente(cliente)


    #En desarrollo
    @classmethod
    def get_cliente_by_user(cls, username, password):
        cliente = DataCliente.get_cliente_by_user(username, password)
        if cliente:
            return cliente
        else:
            #Aca va una excepción!
            print("Aca va una excepción")

    @classmethod
    def update_cliente(cls, cliente):
        cliente = DataCliente.update_cliente(cliente)