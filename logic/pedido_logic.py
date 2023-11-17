from data.data_pedido import DataPedido


class PedidoLogic:
    @classmethod
    def get_all_pedidos(cls):
        pedidos = DataPedido.get_all_pedidos()
        return pedidos

    @classmethod
    def get_pedidos_activos(cls):
        pedidos_activos = DataPedido.get_pedidos_activos()
        return pedidos_activos

    @classmethod
    def get_one_pedido(cls, id):
        pedido = DataPedido.get_one_pedido(id)
        return pedido

    @classmethod
    def get_pedidos_by_persona(cls, persona):
        pedidos = DataPedido.get_pedidos_by_persona(persona)
        return pedidos

    @classmethod
    def get_pedidos_by_persona_pendientes(cls, persona):
        pedidos_pendientes = []
        pedidos = DataPedido.get_pedidos_by_persona(persona)
        for ped in pedidos:
            if ped.estado == True:
                pedidos_pendientes.append(ped)
        return pedidos_pendientes


    @classmethod
    def add_pedido(cls, pedido):
        DataPedido.add_pedido(pedido)

    @classmethod
    def delete_pedido(cls, id):
        DataPedido.delete_pedido(id)

    @classmethod
    def get_pedidos_2_dias_de_devolucion(cls, fecha):
        pedidos = DataPedido.get_pedidos_2_dias_de_devolucion(fecha)
        return pedidos

    @classmethod
    def update_pedido(cls):
        DataPedido.update_pedido()
