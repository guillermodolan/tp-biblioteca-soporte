import matplotlib.pyplot as plt

from logic.autor_logic import AutorLogic


class AutorMasLeidoEnUnMesGrafico:

    @classmethod
    def crea_grafico(cls, mes, año):
        print(año)
        resultados = AutorLogic.autor_mas_leido_en_un_mes(mes, año)
        autores, libros_leidos = zip(*resultados)

        plt.bar(autores, libros_leidos)
        plt.xlabel('Autores')
        plt.ylabel('Libros Leídos')
        plt.title(f'Autores Más Leídos en {mes}/{año}')
        plt.xticks(rotation=0)  # Rota los nombres de los autores para facilitar la lectura
        plt.tight_layout()

        # Guarda o muestra el gráfico
        # plt.savefig('autores_mas_leidos.png')
        plt.show()
