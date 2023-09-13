from data.data_autor import DataAutor

class AutorLogic():
    @classmethod
    def get_all_autores(cls):
        autores = DataAutor.get_all_autores()
        return autores

    @classmethod
    def get_one_autor(cls, id):
        autor = DataAutor.get_one_autor(id)
        return autor

    @classmethod
    def add_autor(cls, autor):
        DataAutor.add_autor(autor)

    @classmethod
    def delete_autor(cls, id):
        DataAutor.delete_autor(id)