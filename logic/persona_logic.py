from sqlite3 import IntegrityError

import sqlalchemy
from flask import Flask
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, FlushError
from werkzeug.exceptions import NotFound

from data.data_persona import DataPersona
from entity_models.persona_model import Persona

app = Flask(__name__)

class PersonaLogic:
    @classmethod
    def get_all_personas(cls):
        try:
            personas = DataPersona.get_all_personas()
            return personas
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_all_clientes(cls):
        try:
            clientes = DataPersona.get_all_clientes()
            return clientes
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_one_persona(cls, id):
        try:
            persona = DataPersona.get_one_persona(id)
            return persona
        except NotFound as e:
            app.logger.debug(f'Persona no encontrada: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def add_persona(cls, persona):
        global mensaje
        try:
            DataPersona.add_persona(persona)
            mensaje = f'Persona {persona.nombre} {persona.apellido} insertada exitosamente'
            # return mensaje
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f'Error en la base de datos: {e}')
            raise e
        except Exception as e:
            app.logger.debug(f'Error inesperado: {e}')
            raise e

    @classmethod
    def get_persona_by_user(cls, username):
        try:
            persona = DataPersona.get_persona_by_user(username)
            return persona
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f"Error de base de datos: {e}")
            raise e
        except Exception as e:
            app.logger.debug(f"Error inesperado: {e}")
            raise e

    @classmethod
    def valida_credenciales(cls, username, contraseña):
        try:
            persona = PersonaLogic.get_persona_by_user(username)
            if persona:
                persona_validada = Persona.valida_contraseña(persona, contraseña)
                if persona_validada is not None:
                    return persona
                else:
                    return None
            return None
        except sqlalchemy.exc.SQLAlchemyError as e:
            app.logger.debug(f"Error de base de datos: {e}")
            raise e
        except Exception as e:
            app.logger.debug(f"Error inesperado: {e}")
            raise e

    @classmethod
    def delete_persona(cls, id):
        global mensaje
        try:
            DataPersona.delete_persona(id)
        except IntegrityError as e:
            raise e
        except ObjectDeletedError as e:
            raise e
        except StaleDataError as e:
            raise e

    @classmethod
    def update_persona(cls, persona):
        global mensaje
        try:
            DataPersona.update_persona(persona)
            mensaje = f'Cliente {persona.nombre} {persona.apellido} actualizada exitosamente'
            app.logger.debug(mensaje)
            return mensaje
        except IntegrityError as e:
            raise e
        except StaleDataError as e:
            raise e
        except FlushError as e:
            raise e
        except DBAPIError as e:
            raise e