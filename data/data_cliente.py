from entity_models.cliente_model import Cliente
from data.database import Database

#get_all_clientes
#get_one
#update_cliente
#delete_cliente


class DataCliente():
    @classmethod
    def get_all_clientes(cls):
        clientes = Cliente.query.order_by('id_cliente')
        return clientes

    @classmethod
    def get_one_cliente(cls, id):
        cliente =Cliente.query.get_or_404(id)
        return cliente

    @classmethod
    def delete_cliente(cls, id):
        cliente = DataCliente.get_one_cliente(id)

        #Elimino al cliente
        Database.db.session.delete(cliente)

        #Guardo los cambios en la base de datos
        Database.db.session.commit()