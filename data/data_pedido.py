from sqlite3 import IntegrityError

from flask import Flask
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.orm.exc import StaleDataError, FlushError

from entity_models.pedido_model import Pedido
from data.database import Database

app = Flask(__name__)

class DataPedido():
    @classmethod
    def get_all_pedidos(cls):
        try:
            pedidos = Pedido.query.order_by('numero_pedido')
            return pedidos
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al obtener todos los pedidos: {e}')
            raise e

    @classmethod
    def get_one_pedido(cls, id):
        try:
            pedido = Pedido.query.get_or_404(id)
            return pedido
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al obtener un pedido por ID: {e}')
            raise e

    @classmethod
    def get_pedidos_by_persona(cls, persona):
        try:
            pedidos_total = DataPedido.get_all_pedidos()
            pedidos = [pedido for pedido in pedidos_total if pedido.id_persona == persona.id]
            return pedidos
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al obtener pedidos por persona: {e}')
            raise e

    @classmethod
    def add_pedido(cls, pedido):
        try:
            Database.db.session.add(pedido)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al agregar un pedido: {e}')
            Database.db.session.rollback()
            raise e

    @classmethod
    def delete_pedido(cls, id):
        try:
            pedido = DataPedido.get_one_pedido(id)
            Database.db.session.delete(pedido)
            Database.db.session.commit()
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al eliminar un pedido: {e}')
            Database.db.session.rollback()
            raise e

    @classmethod
    def get_pedidos_2_dias_de_devolucion(cls, fecha):
        try:
            pedidos = Pedido.query.filter_by(fecha_devolucion=fecha).all()
            return pedidos
        except SQLAlchemyError as e:
            app.logger.debug(f'Error al obtener pedidos con 2 días de devolución: {e}')
            raise e

    @classmethod
    def update_pedido(cls):
        try:
            Database.db.session.commit()
        except IntegrityError as e:
            raise e
        except StaleDataError as e:
            raise e
        except FlushError as e:
            raise e
        except DBAPIError as e:
            raise e
