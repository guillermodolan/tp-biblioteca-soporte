from data.data_categoria import DataCategoria


class CategoriaLogic:
    @classmethod
    def get_all_categorias(cls):
        categorias = DataCategoria.get_all_categorias()
        return categorias

    @classmethod
    def get_one_categoria(cls, id):
        categoria = DataCategoria.get_one_categoria(id)
        return categoria

    @classmethod
    def add_categoria(cls, categoria):
        DataCategoria.add_categoria(categoria)

    @classmethod
    def delete_categoria(cls, id):
        DataCategoria.delete_categoria(id)
