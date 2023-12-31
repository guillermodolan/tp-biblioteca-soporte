import requests


class DataLibroAPI:
    @classmethod
    def get_libros_by_author(cls, autor):
        url = f'https://openlibrary.org/search.json?author="{autor}"'
        response = requests.get(url)
        return response

    @classmethod
    def get_libros_by_genre(cls, genero):
        url = f'https://openlibrary.org/subjects/{genero}.json'
        response = requests.get(url)
        return response
