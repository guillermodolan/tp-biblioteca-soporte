import base64
import io

import matplotlib.pyplot as plt
import numpy as np
from flask import render_template

from logic.autor_logic import AutorLogic


class AutorMasLeidoEnUnMesGrafico:

    @classmethod
    def crea_grafico(cls, mes, año):
        resultados = AutorLogic.autor_mas_leido_en_un_mes(mes, año)

        print(f'Año: {año}')
        print(f'Mes: {mes}')
        print(resultados)

        autores, libros_leidos = zip(*resultados)

        plt.bar(autores, libros_leidos)
        plt.xlabel('Autores')
        plt.ylabel('Libros Leídos')
        plt.title('Autores Más Leídos')
        plt.xticks(rotation=0)
        plt.tight_layout()

        # Guarda el gráfico en un objeto BytesIO
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convierte el gráfico en una imagen base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return render_template('autores_mas_leidos_en_un_mes.html',
                               image_base64=image_base64)
    # @classmethod
    # def crea_grafico(cls, mes, año):
    #     resultados = AutorLogic.autor_mas_leido_en_un_mes(mes, año)
    #     autores, libros_leidos = zip(*resultados)
    #
    #     plt.bar(autores, libros_leidos)
    #     plt.xlabel('Autores')
    #     plt.ylabel('Libros Leídos')
    #     plt.title(f'Autores Más Leídos en {mes}/{año}')
    #     plt.xticks(rotation=0)  # Rota los nombres de los autores para facilitar la lectura
    #     plt.tight_layout()
    #
    #     # Guarda o muestra el gráfico
    #     # plt.savefig('autores_mas_leidos.png')
    #     plt.show()
