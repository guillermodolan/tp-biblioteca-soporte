from entity_models.pedido_model import Pedido
from data.database import Database

class DataPedido():
    @classmethod
    def get_all_pedidos(cls):
        pedidos = Pedido.query.order_by('numero_pedido')
        return pedidos

    @classmethod
    def get_one_pedido(cls, id):
        pedido = Pedido.query.get_or_404(id)
        return pedido

    @classmethod
    def get_pedidos_by_persona(cls, persona):
        pedidos_total = DataPedido.get_all_pedidos()
        pedidos = []
        for pedido in pedidos_total:
            if pedido.id_persona == persona.id:
                pedidos.append(pedido)
        return pedidos

    @classmethod
    def add_pedido(cls, pedido):
        Database.db.session.add(pedido)
        Database.db.session.commit()

    @classmethod
    def delete_pedido(cls, id):
        pedido = DataPedido.get_one_pedido(id)
        Database.db.session.delete(pedido)
        Database.db.session.commit()

    @classmethod
    def get_pedidos_2_dias_de_devolucion(cls, fecha):
        pedidos = Pedido.query.filter_by(fecha_devolucion=fecha).all()
        return pedidos
