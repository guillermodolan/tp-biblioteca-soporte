from data.data_pedido import DataPedido


class PedidoLogic():
    @classmethod
    def get_all_pedidos(cls):
        pedidos = DataPedido.get_all_pedidos()
        return pedidos

    @classmethod
    def get_one_pedido(cls, id):
        pedido = DataPedido.get_one_pedido(id)
        return pedido

    @classmethod
    def get_pedidos_by_cliente(cls, cliente):
        pedidos = DataPedido.get_pedidos_by_cliente(cliente)
        return pedidos

    @classmethod
    def add_pedido(cls, pedido):
        DataPedido.add_pedido(pedido)

    @classmethod
    def delete_pedido(cls, id):
        DataPedido.delete_pedido(id)
