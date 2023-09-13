from entity_models.pedido_model import Pedido
from data.database import Database

#get_all
#get_one
#add
#delete


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
    def add_pedido(cls, pedido):
        Database.db.session.add(pedido)
        Database.db.session.commit()

    @classmethod
    def delete_pedido(cls, id):
        pedido = DataPedido.get_one_pedido(id)

        #Elimino al pedido
        Database.db.session.delete(pedido)

        #Guardo los cambios en la base de datos
        Database.db.session.commit()