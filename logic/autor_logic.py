from data.data_autor import DataAutor


class AutorLogic:
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

    @classmethod
    def get_author_by_name(cls, nombre):
        autor = DataAutor.get_author_by_name(nombre)
        return autor

    @classmethod
    def autor_mas_leido_en_un_mes(cls, mes, año):
        resultados = DataAutor.autor_mas_leido_en_un_mes(mes, año)
        return resultados
