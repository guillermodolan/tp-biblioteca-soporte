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
        autores, libros_leidos = zip(*resultados)
        return render_template("autores_mas_leidos_en_un_mes.html",
                               resultados=resultados,
                               autores=autores,
                               libros_leidos=libros_leidos)
