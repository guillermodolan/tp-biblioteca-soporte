from data.libros_API import DataLibroAPI


class LibroAPILogic:
    @classmethod
    def get_libros_by_author(cls, autor):
        response = DataLibroAPI.get_libros_by_author(autor)
        if response.status_code == 200:
            data = response.json()
            if "docs" in data:
                libros = []
                for libro in data["docs"]:
                    titulo = libro.get("title", "Título no disponible")
                    autores = libro.get("author_name", ["Autor no disponible"])
                    libros.append({"titulo": titulo, "autores": autores})
                return libros
            else:
                return None
        else:
            return None