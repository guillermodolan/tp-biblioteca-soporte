from data.database import Database


class DataLibroAutor:
    @classmethod
    def add_libro_autor(cls, libro_autor):
        Database.db.session.add(libro_autor)
        Database.db.session.commit()