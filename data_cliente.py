from cliente_model import Cliente
from database import Database

class DataCliente():
    @classmethod
    def get_all_clientes(cls):
        clientes = Cliente.query.order_by('id_cliente')
        return clientes