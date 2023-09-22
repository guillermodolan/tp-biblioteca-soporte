from entity_models.categoria_model import Categoria
from data.database import Database


# get_all
# get_one
# add
# delete


class DataCategoria():
    @classmethod
    def get_all_categorias(cls):
        categoria = Categoria.query.order_by('id_categoria')
        return categoria

    @classmethod
    def get_one_categoria(cls, id):
        categoria = Categoria.query.get_or_404(id)
        return categoria

    @classmethod
    def add_categoria(cls, categoria):
        Database.db.session.add(categoria)
        Database.db.session.commit()

    @classmethod
    def delete_categoria(cls, id):
        categoria = DataCategoria.get_one_categoria(id)

        # Elimino a la categoría
        Database.db.session.delete(categoria)

        # Guardo los cambios en la base de datos
        Database.db.session.commit()
