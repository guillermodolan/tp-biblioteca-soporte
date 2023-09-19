import requests.exceptions

from data.libros_API import DataLibroAPI
from flask import Flask

app = Flask(__name__)

class LibroAPILogic:
    @classmethod
    def get_libros_by_author(cls, autor):
        try:
            response = DataLibroAPI.get_libros_by_author(autor)
            if response.status_code == 200:
                data = response.json()
                if "docs" in data:
                    libros = []
                    for libro in data["docs"]:
                        titulo = libro.get("title", "Título no disponible")
                        autores = libro.get("author_name", ["Autor no disponible"])
                        isbn = libro.get("isbn", ["ISBN no disponible"])
                        libros.append({"titulo": titulo, "autores": autores, "isbn": isbn})
                    return libros
            else:
                return None
        except requests.exceptions.RequestException as e:
            raise e
        except Exception as e:
            raise e