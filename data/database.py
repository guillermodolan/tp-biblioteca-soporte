from flask_sqlalchemy import SQLAlchemy

class Database:
    # Inicialización del objeto db de sqlalchemy. Esto es la conexión hacia la base de datos
    # utilizando SQLAlchemy.
    db = SQLAlchemy()

    @classmethod
    def configura_conexion(cls) -> str:
        # Configuro la conexión a la base de datos
        USER_DB = 'postgres'
        PASS_DB = 'mg123'
        HOST_DB = 'localhost'
        PORT_DB = '5432'
        NAME_DB = 'konigari'

        # Creo la cadena de conexión completa a la base de datos(PostgreSQL en nuestro caso)
        FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}'
        return FULL_URL_DB